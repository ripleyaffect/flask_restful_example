"""

    Create a logger to standard out

"""

import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

root_handler = logging.StreamHandler(sys.stdout)
root_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
root_handler.setFormatter(formatter)

logger.addHandler(root_handler)