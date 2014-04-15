from flask import request, Response
import json


class Responder(object):

    @classmethod
    def create_response(cls, code, msg, payload={}):
        data = {
            'status': code,
            'message': msg,
            'payload': payload
        }
        headers = {
            'WWW-Authenticate': 'OAuth realm="%s"' % request.host_url,
            'Server': 'Image Hasher'
        }
        return Response(response=json.dumps(data),
                        mimetype='application/json',
                        headers=headers,
                        status=int(code))

    @classmethod
    def bad_request(cls, msg='Bad Request'):
        return Responder.create_response(400, msg)

    @classmethod
    def unauthorized(cls, msg='Unauthorized to access this resource'):
        return Responder.create_response(401, msg)

    @classmethod
    def forbidden(cls, msg='Forbidden to consume this resource'):
        return Responder.create_response(403, msg)

    @classmethod
    def not_found(cls, msg='Cannot find the resource you are looking for'):
        return Responder.create_response(404, msg)

    @classmethod
    def server_error(cls, msg='Server Error'):
        return Responder.create_response(500, msg)