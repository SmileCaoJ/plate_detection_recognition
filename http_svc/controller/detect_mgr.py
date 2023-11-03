import base64
import json
import logging
import traceback

import cv2
import numpy as np
from flask import Blueprint, request, make_response

import plate_detector
from http_svc.controller.http_util import pathPrefix, response_options, add_common_headers, _return_error_response

from common import config

detect_mgr = Blueprint('detect_mgr', __name__)
logger = logging.getLogger(__name__)


@detect_mgr.route(pathPrefix + '/detect/detect-car', methods=['POST', 'OPTIONS'])
def detect_car():
    if request.method == "OPTIONS":
        return response_options(request)

    if request.method == "POST":
        try:
            return _detect_car(request)
        except:
            logging.error(str(traceback.format_exc()))
            return _return_error_response(500, "Internal Error")


def _detect_car(request):
    req_data_object = json.loads(request.data)
    png_as_str = req_data_object['img_data']

    png_as_bytes = png_as_str.encode('ascii')
    png_original = base64.b64decode(png_as_bytes)
    png_as_np = np.frombuffer(png_original, dtype=np.uint8)
    img = cv2.imdecode(png_as_np, flags=1)

    detector = plate_detector.detector
    ori_img, dict_list = detector.detect_video_img(img)
    png_image = cv2.imencode('.png', ori_img)[1]
    img_data = str(base64.b64encode(png_image))[2:-1]

    resp_object = {
            "code": 0,
            "message": "success",
            "data": {
                "img_data": img_data,
                "car_info": []
            }
    }

    for row in dict_list:
        resp_object['data']['car_info'].append({
            "plate_no": row["plate_no"],
            "plate_color": row["plate_color"]
        })

    resp = make_response(resp_object)
    resp.status = 200
    add_common_headers(resp)

    return resp

