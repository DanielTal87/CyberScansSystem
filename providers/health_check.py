import random


def random_health_check():
    """
    This function is only for testing
    :return: randomly raise an exception
    """
    rand = bool(random.getrandbits(1))  # faster than True/False
    if not rand:
        raise Exception(f'Health check failed because a random error. random value = {rand}')
    return rand
