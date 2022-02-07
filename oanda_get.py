from requests import get
from requests.exceptions import ConnectionError
from time import sleep


def oanda_get(url, params=None, **kwargs):
    try:
        return get(url, params, **kwargs)
    except ConnectionError as e:
        print("Connection Error:")
        print(e)
        print("Trying again in 5 Seconds")
        sleep(5)
        return oanda_get(url, params, **kwargs)

