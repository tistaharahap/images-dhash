from flask import request
from flask.ext import restful
from werkzeug.utils import secure_filename
from utils import Responder
from PIL import Image
from dhash import Dhash
import os


class Reco(restful.Resource):

    def get(self):
        return Responder.forbidden()

    def post(self):
        f = request.files.get('reco_image')
        if not f:
            return Responder.bad_request(msg='Reco Image is required')

        filename = secure_filename(f.filename)
        fullpath = os.path.join('/tmp', filename)

        f.save(fullpath)

        img = Image.open(fullpath, 'r')
        dhash = Dhash.get_dhash(img,
                                hash_size=8)

        return Responder.create_response(code=200,
                                         msg='ok',
                                         payload={
                                             'dhash': dhash
                                         })


class RecoCompare(restful.Resource):

    def post(self):
        f1 = request.files.get('reco_image1')
        if not f1:
            return Responder.bad_request(msg='Reco Image 1 is required')

        f2 = request.files.get('reco_image2')
        if not f2:
            return Responder.bad_request(msg='Reco Image 2 is required')

        filename = [secure_filename(f1.filename), secure_filename(f2.filename)]
        fullpath = [os.path.join('/tmp', filename[0]), os.path.join('/tmp', filename[1])]

        print fullpath

        f1.save(fullpath[0])
        f2.save(fullpath[1])

        img1 = Image.open(fullpath[0])
        img2 = Image.open(fullpath[1])

        dhashes = {
            'reco_image1': Dhash.get_dhash(img1,
                                           hash_size=8),
            'reco_image2': Dhash.get_dhash(img2,
                                           hash_size=8)
        }

        prediction = Dhash.compute_hashes(hash1=dhashes['reco_image1'],
                                          hash2=dhashes['reco_image2'])

        return Responder.create_response(code=200,
                                         msg='ok',
                                         payload={
                                             'dhashes': dhashes,
                                             'prediction': prediction
                                         })