# If Loguru fails to retrieve the proper "name" value, assign it manually
from loguru import logger

logger = logger.patch(lambda record: record.update(name="my_module"))
