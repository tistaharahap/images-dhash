from flask import request
from flask.ext import restful
from werkzeug.utils import secure_filename
from models import HashModel
from utils import Responder
from PIL import Image
from dhash import Dhash
from errors import ItemExistsError
from settings import get_flask_settings
import os
import time
import hashlib


class Reco(restful.Resource):

    model = HashModel()
    settings = get_flask_settings('dev')

    def get(self):
        return Responder.forbidden()

    def post(self):
        f = request.files.get('reco_image')
        if not f:
            return Responder.bad_request(msg='Reco Image is required')

        filename = secure_filename('%s-%s' % (Reco.md5(s=str(Reco.get_unix_time())), f.filename))
        fullpath = os.path.join(self.settings.upload_path, filename)

        f.save(fullpath)

        img = Image.open(fullpath, 'r')
        dhash = Dhash.get_dhash(img,
                                hash_size=8)

        try:
            self.model.create_hash(filename=filename,
                                   hash=dhash)
        except ItemExistsError:
            return Responder.forbidden(msg='Image already exists')

        return Responder.create_response(code=200,
                                         msg='ok',
                                         payload={
                                             'dhash': dhash
                                         })

    @classmethod
    def md5(cls, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    @classmethod
    def get_unix_time(cls):
        return int(time.time())


class RecoCompare(restful.Resource):

    model = HashModel()

    def get(self):
        hash = request.args.get('hash')
        if not hash:
            return Responder.bad_request(msg='Hash is needed as query string')

        images = self.model.compare_hash(hash=hash)
        if not images:
            return Responder.not_found(msg='No similarities found')

        return Responder.create_response(code=200,
                                         msg='ok',
                                         payload=images)


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