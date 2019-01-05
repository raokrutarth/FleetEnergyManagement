# Author: Krutarth Rao
# Email: raok@purdue.edu

import logging


logfile = '~/power_service/data/power_service.log'

def get_logger():
    # setup logging
    logger = logging.getLogger()
    fmt = '%(levelname)-8s %(filename)s:%(lineno)s - %(funcName)s() - %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        format=fmt
    )
    # create a file handler
    log_to_file = logging.FileHandler(logfile)
    log_to_file.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter(fmt)
    log_to_file.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(log_to_file)
    return logger