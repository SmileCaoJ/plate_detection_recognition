import logging
import threading
import argparse

import plate_detector
from common.config import server_config
from video_cron import local_detect_cron, cooperate_detect_cron
from http_svc.app import webserver

from common import config

logger = logging.getLogger(__name__)


class HttpSvcThread(threading.Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self) -> None:
        port = server_config.get_video_processor("port")
        webserver.run(port)


class LocalDetectSvcThread(threading.Thread):

    def __init__(self, name, arg_opt):
        super().__init__()
        self.name = name
        self.arg_opt = arg_opt

    def run(self) -> None:
        local_detect_cron.run(self.arg_opt)


class RemoteDetectSvcThread(threading.Thread):

    def __init__(self, name, arg_opt):
        super().__init__()
        self.name = name
        self.arg_opt = arg_opt

    def run(self) -> None:
        cooperate_detect_cron.run(self.arg_opt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--detect_model', nargs='+', type=str, default='weights/plate_detect.pt',
                        help='model.pt path(s)')  # 检测模型
    parser.add_argument('--rec_model', type=str, default='weights/plate_rec_color.pth',
                        help='model.pt path(s)')  # 车牌识别+颜色识别模型
    parser.add_argument('--is_color', type=bool, default=True, help='plate color')  # 是否识别颜色
    parser.add_argument('--image_path', type=str, default='imgs', help='source')  # 图片路径
    parser.add_argument('--img_size', type=int, default=640, help='inference size (pixels)')  # 网络输入图片大小
    parser.add_argument('--output', type=str, default='result', help='source')  # 图片结果保存的位置
    parser.add_argument('--video', type=str, default='', help='source')  # 视频的路径
    parser.add_argument('--detect_svc_mode', type=str, default='', help='source')  # 处理模式，local：本地做检测，remote: 调用检测服务

    opt = parser.parse_args()

    httpSvcThread = HttpSvcThread("HttpSvcThread")
    httpSvcThread.start()

    if opt.detect_svc_mode == "remote":
        detectSvcThread = RemoteDetectSvcThread("DetectSvcThread", opt)
        detectSvcThread.start()
    else:
        plate_detector.init_detector(opt)
        detectSvcThread = LocalDetectSvcThread("DetectSvcThread", opt)
        detectSvcThread.start()

    detectSvcThread.join()
    httpSvcThread.join()


