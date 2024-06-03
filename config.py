class Config:
    """Base config."""
    SECRET_KEY = 'your_secret_key_here'
    DEBUG = False
    TESTING = False

config = Config()
class ProductionConfig(Config):
    """Production specific config."""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development environment specific config."""
    DEBUG = True
    TESTING = True
