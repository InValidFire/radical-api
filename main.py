import sys

from core.wrapper import Wrapper

api = Wrapper(['gunicorn', "-k", "uvicorn.workers.UvicornWorker", "--log-config", "log.conf", 'api:api'], sys.stdout)
api.start()
