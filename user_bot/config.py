from environs import Env

env = Env()
env.read_env()

NUMBER = env.str('NUMBER')

API_ID = env.int('API_ID')
API_HASH = env.str('API_HASH')

SLEEP_TIME_MEDIA_GROUP = env.str('SLEEP_TIME_MEDIA_GROUP')
SLEEP_TIME_EDIT = env.str('SLEEP_TIME_EDIT')
