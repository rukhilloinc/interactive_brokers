import logging


def log(info):
    FORMAT = '%(asctime)s|%(message)s'
    logging.basicConfig(filename='/Users/rustambekrukhilloev/PycharmProjects/IB/ib_logs.log', format=FORMAT)
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.INFO)
    logger.info(info)