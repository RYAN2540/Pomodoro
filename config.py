import os

class Config:
    '''
    General configuration
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///timer.db'
    SECRET_KEY = 'gakuyajefferson'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    '''
    Production configuration child class

    Args:
        Config: The parent configuration class with general configuration settings
    '''

class DevConfig(Config):
    '''
    Development configuration child class

    Args:
        Config: The parent configuration class with General configuaration settings
    '''

    pass

class TestConfig(Config):
    '''
    Testing Configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}