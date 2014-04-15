class FlaskDevSettings(object):

    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 5000
        self.debug = True
        self.secret_key = '4V3rYs3CRe7Key'

        self.allowed_file_exts = set(['png', 'jpg', 'jpeg', 'gif'])


class FlaskStageSettings(FlaskDevSettings):

    def __init__(self):
        super(FlaskStageSettings, self).__init__()

        self.host = '127.0.0.1'
        self.debug = False
        self.secret_key = 'a6r9i2yZaS&*NRZBRB6.38~!2D_9EV(3t3$b7|^R%Ee>8D>bw%+/5C:())5si+W'


class FlaskProductionSettings(FlaskStageSettings):

    def __init__(self):
        super(FlaskProductionSettings, self).__init__()

        self.secret_key = 'T/#1/BS-ml|o&Lg:Kjw.=3*jC:`#3@[eZ0ObVl;yeW"]?Nt08Df`q|/y@iJ``)*'