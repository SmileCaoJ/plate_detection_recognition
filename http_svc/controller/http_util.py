from flask import make_response, request, session

pathPrefix = '/api/v1'


def response_options(request):
    if request.method == "OPTIONS":
        data_object = {}
        resp = make_response(data_object)
        resp.status = 200
        add_common_headers(resp)
        return resp


def add_common_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Access-Control-Allow-Methods"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    resp.headers["Access-Control-Expose-Headers"] = "*"


def _return_error_response(code, msg):
    data_object = {
        "code": 50000,
        "message": msg
    }

    resp = make_response(data_object)
    resp.status = code
    add_common_headers(resp)

    return resp
