import logging

logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s %(name)s %(levelname)-8s %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
)

def setup(name: str = __name__) -> logging:
    return logging.getLogger(name)