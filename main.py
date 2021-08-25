import sys

from core.wrapper import Wrapper

api = Wrapper(['gunicorn', "-k", "uvicorn.workers.UvicornWorker",
               "--log-config", "log.conf",
               '--bind', '0.0.0.0:8000',
               'api:api'], sys.stdout)
api.start()
