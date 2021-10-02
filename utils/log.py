import logging as log

log.basicConfig(
    format='%(asctime)s:%(msecs)d\t%(name)s:\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log.INFO
)