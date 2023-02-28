import logging

log_tmp = logging.getLogger()
log_tmp.setLevel(logging.WARNING)
screen_h = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s')
screen_h.setFormatter(formatter)
log_tmp.addHandler(screen_h)