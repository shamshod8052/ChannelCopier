from environs import Env

env = Env()
env.read_env()


PHONE_NUMBER = env.str("PHONE_NUMBER")
INTERVAL_SECONDS = env.int("INTERVAL_SECONDS")
COPY_START_TIME = env.int("COPY_START_TIME")
API_ID = env.int("API_ID")
API_HASH = env.str("API_HASH")