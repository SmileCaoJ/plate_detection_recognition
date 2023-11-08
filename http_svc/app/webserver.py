from flask import Flask
from flask import make_response
from gevent import pywsgi

import common
from common.config import server_config
from http_svc.controller.car_mgr import car_mgr
from http_svc.controller.detect_mgr import detect_mgr

flask_app = Flask(__name__, static_url_path='/', static_folder=common.config.web_dir)
flask_app.register_blueprint(car_mgr)
flask_app.register_blueprint(detect_mgr)


@flask_app.before_request
def proxy():
    return None


@flask_app.route('/', methods=['GET', 'OPTIONS'])
def index():
    data_object = {"name": "edwin", "grade": 100}
    resp = make_response(data_object)
    resp.status = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Access-Control-Allow-Methods"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Access-Token"
    resp.headers["Access-Control-Expose-Headers"] = "*"

    return resp


def run(port):
    server = pywsgi.WSGIServer(('0.0.0.0', int(port)), flask_app)
    server.serve_forever()
