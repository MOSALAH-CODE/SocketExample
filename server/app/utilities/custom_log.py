import logging
import sys


class FastAPIPathFilter(logging.Filter):
    def filter(self, record):
        record.apiName = getattr(record, 'apiName', 'N/A')
        record.token = getattr(record, 'token', None)
        record.user = 'N/U'
        if (record.token):
            from utilities.config_variables import SECRET_KEY, ALGORITHM
            import jwt
            record.user = jwt.decode(
                record.token, SECRET_KEY, algorithms=[ALGORITHM])
        return True


logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.addFilter(FastAPIPathFilter())
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(apiName)s - %(user)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
