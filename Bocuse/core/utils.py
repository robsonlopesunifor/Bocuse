import json


def returnMessageError(error):
    error_message = json.loads(error.decode("utf-8").replace("'", '"'))
    return error_message["error"]["message"]
