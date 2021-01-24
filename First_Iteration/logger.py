import logging


def log(info, path):
    FORMAT = '%(asctime)s|%(message)s'
    logging.basicConfig(filename=path, format=FORMAT)
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.INFO)
    logger.info(info)