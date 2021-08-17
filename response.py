import json


class ResponseEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Response:
    def __init__(self, status_code, obj):
        self.status_code = status_code
        self.response = obj

    def to_json(self):
        return json.dumps(self, indent=4, cls=ResponseEncoder)
