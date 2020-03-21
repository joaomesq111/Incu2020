import os


class Config(object):
    MONGO_URI = f'mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASS")}'\
              f'@{os.getenv("MONGO_HOST")}:27017/{os.getenv("MONGO_DB")}'




