import base64
import copy
import threading
import cv2

data = {}

lock = threading.Lock()             # 实例化一个锁


def set_data(img_data, car_info):
    lock.acquire()  # 开锁，只允许当前线程访问共享的数据

    data['img_data'] = img_data
    data['car_info'] = []

    for result in car_info:
        data_item = {}
        data_item['plate_no'] = result['plate_no']
        data_item['plate_color'] = result['plate_color']
        data['car_info'].append(data_item)

    lock.release()  # 释放锁，允许其他线程访问共享数据


def get_data():
    lock.acquire()  # 开锁，只允许当前线程访问共享的数据
    data_copy = copy.deepcopy(data)
    lock.release()  # 释放锁，允许其他线程访问共享数据
    return data_copy
