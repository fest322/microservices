import logging


class Logger:
    formatter = logging.Formatter('%(asctime)s - LEVEL:%(levelname)s - %(message)s',  datefmt='%d-%b-%y %H:%M:%S')

    def __init__(self, name, level=logging.INFO, rewrite=False):
        self.logger = None
        self.setup_logger(name, level, rewrite)

    def setup_logger(self, name, level=logging.INFO, rewrite=False):
        name = str(name)
        log_file = './' + name + '.txt'
        if rewrite:
            with open(log_file, 'w'):
                pass
        handler = logging.FileHandler(log_file)
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
        self.logger = logger

    def logging(self, *logs):
        text = ''
        for log in logs:
            text += str(log)
        self.logger.info(text)
