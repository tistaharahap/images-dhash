class DbDevSettings(object):

    uri = 'mysql://root:@127.0.0.1/pyimagereco'


class DbStageSettings(DbDevSettings):

    uri = 'mysql://root:@127.0.0.1/pyimagereco'


class DbProductionSettings(DbStageSettings):

    uri = 'mysql://root:@127.0.0.1/pyimagereco'