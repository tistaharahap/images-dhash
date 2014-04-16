from bootstrap import app
from settings import get_flask_settings


app.ENV = 'dev'

if __name__ == '__main__':
    flask_settings = get_flask_settings(app.ENV)

    app.config['allowed_file_exts'] = flask_settings.allowed_file_exts

    app.secret_key = flask_settings.secret_key
    app.run(host=flask_settings.host,
            port=flask_settings.port,
            debug=flask_settings.debug)