import logging

def get_logger():
    # setup logging
    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s'
    )
    # create a file handler
    log_to_file = logging.FileHandler('power_service.log')
    log_to_file.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_to_file.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(log_to_file)
    return logger