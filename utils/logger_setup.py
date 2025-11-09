
import logging, os
from datetime import datetime

def setup_logger(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"maze_{ts}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger()
    logger.info("Logger initialized")
    return logger, log_file
