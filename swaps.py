import sys
from decimal import *

from schema import Balance, Base, Swap
from db import Session
from bitapi import Api, ApiException
from config import api_key, api_secret
import json

cutoff_rate = Decimal('0.95')

def profitable(last, current, cutoff):
  earnings_delta = current.earnings - last.earnings
  rate_delta = current.rate - (cutoff_rate * cutoff)
  print "Earnings delta: {0}".format(earnings_delta)
  print "Swap rate: {0}, cutoff: {1}".format(current.rate, cutoff)
  print "Rate delta: {0}".format(rate_delta)
  return earnings_delta > 0 and rate_delta > Decimal('-0.1')

class Client():
  def __init__(self):
    self.api = Api(api_key, api_secret)


  def create_swap(self):
    session = Session()
    cutoff = self.current_cutoff()
    print "Current cutoff: {0}".format(cutoff)
    rate = (cutoff_rate * cutoff).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    print "Rate for new swaps: {0}".format(rate)
    balance = self.get_balance()
    print "Available balance: {0}".format(balance)

    if balance > 0:
      print "Creating new swap..."
      res = self.api.open_swap(amount = balance, rate = rate)
      swap = Swap(amount = balance, rate = rate, timestamp = res['time'], swap_id = res['data']['id'], op = 'open')
      print "Created swap: {0}".format(swap)
      session.add(swap)

    session.commit()


  def update_swaps(self):
      res = self.api.list_btc_swaps()
      timestamp = res['time']
      data = res['data']
      for s in data:
        s['timestamp'] = timestamp
        swap = Swap.fromjson(s)
        self.update_swap(swap)

  def update_swap(self, swap):
    swap_id = swap.swap_id
    session = Session()
    print "Updating swap: {0}".format(swap)
    last_swap_state = session.query(Swap).filter_by(swap_id = swap_id).order_by(Swap.id.desc()).first()

    if last_swap_state == None or last_swap_state.op == 'open':
      print "No existing swap earnings record found"
      swap.op = 'update'
      session.add(swap)
    elif last_swap_state.op == "close":
      print "Swap already closed in the db"
    else:
      print "Existing swap record found: {0}".format(last_swap_state)
      cutoff = self.current_cutoff()
      if profitable(last_swap_state, swap, cutoff):
        print "Swap still profitable"
        swap.op = 'update'
        session.add(swap)
      else:
        print "Swap not profitable, closing..."
        self.api.close_swap(swap_id)
        swap.op = 'close'
        session.add(swap)

    session.commit()


  def current_cutoff(self):
    res = self.api.btc_swaps()
    return Decimal(str(res['cutoff']))

  def get_balance(self):
    return Decimal(str(self.api.info()['data']['balances']['available']['BTC']))


def main():
  try:
    client = Client()
    client.update_swaps()
    client.create_swap()
  except ApiException as err:
    print("API error: {0}".format(err))
    raise


if __name__ == "__main__": main()