from flask_settings import FlaskDevSettings, FlaskProductionSettings, FlaskStageSettings
from db_settings import DbDevSettings, DbStageSettings, DbProductionSettings


def get_flask_settings(env='dev'):
    settings = {
        'dev': FlaskDevSettings,
        'prod': FlaskProductionSettings,
        'stage': FlaskStageSettings
    }

    try:
        func = settings[env]
    except KeyError:
        raise KeyError('No such environment is available')

    return func()


def get_db_settings(env='dev'):
    settings = {
        'dev': DbDevSettings,
        'prod': DbProductionSettings,
        'stage': DbStageSettings
    }

    try:
        func = settings[env]
    except KeyError:
        raise KeyError('No such environment is available')

    return func()