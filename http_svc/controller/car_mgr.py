import logging
import traceback

from flask import Blueprint, request, make_response

import result_store
from http_svc.controller.http_util import pathPrefix, response_options, add_common_headers, _return_error_response

car_mgr = Blueprint('car_mgr', __name__)
logger = logging.getLogger(__name__)


@car_mgr.route(pathPrefix + '/car/car_info', methods=['GET', 'OPTIONS'])
def get_car_info():
    if request.method == "OPTIONS":
        return response_options(request)

    if request.method == "GET":
        try:
            return _get_car_info(request)
        except:
            logging.error(str(traceback.format_exc()))
            return _return_error_response(500, "Internal Error")


def _get_car_info(request):
    data = result_store.get_data()

    resp_object = {
            "code": 0,
            "message": "success",
            "data": {
                "img_data": data['img_data'],
                "cars": []
            }
    }

    for row in data['car_info']:
        resp_object['data']['cars'].append({
            "plate_no": row["plate_no"],
            "plate_color": row["plate_color"],
            "owner": "张三",
            "register_status": "已在社区注册"
        })

    resp = make_response(resp_object)
    resp.status = 200
    add_common_headers(resp)

    return resp

