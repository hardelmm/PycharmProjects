import logging

log_format = "%(asctime)s - %(levelname)s - %(message)s"
#logging.basicConfig(filename='run.log',level=logging.DEBUG,format=log_format)
logging.basicConfig(level=logging.DEBUG,format=log_format)
log = logging.getLogger()