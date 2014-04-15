from flask import Flask, request, render_template
from flask.ext import restful
from controllers import Reco, RecoCompare
from utils import Responder

app = Flask(__name__)
api = restful.Api(app, catch_all_404s=True)

@app.route('/test_reco/', methods=['GET', 'POST'])
def test_reco():
    def _get():
        return render_template('test_reco.html')

    def _post():
        pass

    funcs = {
        'GET': _get,
        'POST': _post
    }

    try:
        func = funcs[request.method]
    except KeyError:
        return Responder.forbidden(msg='No resource here')
    else:
        return func()


api.add_resource(Reco, '/reco/')
api.add_resource(RecoCompare, '/recompare/')