import requests
import hmac
import time
import urllib
import hashlib

class ApiException(Exception):
    pass

class Api():

  def __init__(self, key, secret):
    self.key = key
    self.secret = secret

  def private(self, method, **params):
    endpoint = "https://www.bitmarket.pl/api2/"
    times = int(time.time())
    params.update({
      "method": method,
      "tonce": times,
      "currency": "BTC"
    })

    post = urllib.urlencode(params)
    sign = hmac.HMAC(str(self.secret), post, digestmod=hashlib.sha512).hexdigest()
    headers = {"API-Key": str(self.key), "API-Hash": sign}
    raw = requests.post(endpoint, data=post, headers=headers)

    if 'error' in raw.json():
      raise ApiException(raw.json())
    return raw.json()


  def public(self, method, **params):
    endpoint = "https://www.bitmarket.pl/json/"
    raw = requests.get(endpoint + method)

    if 'error' in raw.json():
      raise BitapiException(raw.json())
    return raw.json()


  def btc_swaps(self):
    return self.public("swapBTC/swap.json")

  def list_btc_swaps(self):
    return self.private("swapList", currency = "BTC")

  def info(self):
    return self.private("info")

  def close_swap(self, swap_id):
    return self.private("swapClose", id = swap_id, currency = "BTC")

  def open_swap(self, amount, rate):
    return self.private("swapOpen", currency = "BTC", amount = amount, rate = rate)
