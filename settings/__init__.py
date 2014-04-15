from flask_settings import FlaskDevSettings, FlaskProductionSettings, FlaskStageSettings


def get_settings(env='dev'):
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