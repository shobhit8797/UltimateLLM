import logging
import time

logger = logging.getLogger(__name__)


def log_time(task_name, start_time):
    elapsed_time = time.time() - start_time
    logger.info(f"{task_name} completed in {elapsed_time:.2f} seconds")
