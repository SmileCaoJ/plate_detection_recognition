import base64
import http
import json
import logging
import time
import argparse
import time
from pathlib import Path
import os
import cv2
import requests
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import copy
import numpy as np

import common
import result_store
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression_face, apply_classifier, scale_coords, xyxy2xywh, \
    strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized
from utils.cv_puttext import cv2ImgAddText
from plate_recognition.plate_rec import get_plate_result,allFilePath,init_model,cv_imread
# from plate_recognition.plate_cls import cv_imread
from plate_recognition.double_plate_split_merge import get_split_merge

from common import config

logger = logging.getLogger(__name__)


def run(opt):
    logger.info("detect_svc running...")

    print(opt)

    while True:
        video_name = opt.video
        capture = cv2.VideoCapture(video_name)

        frame_count = 0
        fps_all = 0
        if capture.isOpened():
            while True:
                t1 = cv2.getTickCount()
                frame_count += 1
                print(f"第{frame_count} 帧", end=" ")
                ret, img = capture.read()
                if not ret:
                    break

                # 抽
                if frame_count % 10 != 0:
                    continue

                # 发送请求

                retval, buffer = cv2.imencode('.png', img)
                png_as_bytes = base64.b64encode(buffer)
                png_as_str = png_as_bytes.decode('ascii')

                req_data = {
                    "img_data": png_as_str
                }
                req_url = common.config.server_config.get_video_processor("detect_server_url") + "/api/v1/detect/detect-car"
                try:
                    resp = requests.post(req_url, json=req_data)
                except:
                    print("call detect-car failed!")
                    continue
                else:
                    if resp.status_code != 200:
                        print("call detect-car failed, status_code: " + str(resp.status_code))
                        continue

                    resp_object = json.loads(resp.text)
                    result_store.set_data(resp_object['data']['img_data'], resp_object['data']['car_info'])

        capture.release()
        cv2.destroyAllWindows()
        print(f"all frame is {frame_count},average fps is {fps_all/frame_count} fps")