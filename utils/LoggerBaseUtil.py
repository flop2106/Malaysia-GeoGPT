import logging

class LoggerBaseUtil:
    @staticmethod
    def get_logger()-> logging.Logger:
        logger = logging.getLogger(__name__)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger