import logging

log_tmp = logging.getLogger()
log_tmp.setLevel(logging.WARNING)
screen_h = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s')
screen_h.setFormatter(formatter)
log_tmp.addHandler(screen_h)

def rate_time(begin, now):
    seconds = now - begin
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    cost_time = "%02d:%02d:%02d" % (h, m, s)
    return cost_time
