#! /usr/bin/env python3

import base64
import requests
import json
import sys
import sched
import configparser, os
import time
import argparse

#read config from CLI config file (~/.nemxorc)
config = configparser.ConfigParser()
homedir = os.path.expanduser("~")
config.read(f'{homedir}/.nexmorc')

API_KEY = config['credentials']['api_key']
API_SECRET = config['credentials']['api_secret']

debug = False

def get_secrets():
  url = f"https://api.nexmo.com/accounts/{API_KEY}/secrets"
  keystring = bytes(f"{API_KEY}:{API_SECRET}", 'utf-8')
  auth =  base64.b64encode(keystring).decode('utf-8')
  headers = {'Authorization' : f'Basic {auth}'}
  resp = requests.get(url, headers=headers)
  data = resp.json()
  print(f"You have {len(data['_embedded']['secrets'])} secrets on your account")
  if debug:
    print(data)
  else:
    for secret in data['_embedded']['secrets']:
      created_date, created_time = secret['created_at'].split('T')
      print(f"Secret with Secret ID: {secret['id']} was created on: {created_date} at {created_time.strip('Z')} UTC")
 
def new_secret(secret):
  url = f"https://api.nexmo.com/accounts/{API_KEY}/secrets"
  keystring = bytes(f"{API_KEY}:{API_SECRET}", 'utf-8')
  auth =  base64.b64encode(keystring).decode('utf-8')
  headers = {'Authorization' : f'Basic {auth}'}
  payload = {'secret' : secret}
  resp = requests.post(url, headers=headers, json=payload)
  if resp.status_code == 201:
    data = resp.json()
    return data['id']
  else:
    print(f"Request errored out with the following response code: {resp.status_code}")
    if debug:
      print(resp)
      print(resp.text)
    else:
      resp_obj = json.loads(resp.text)
      print(f"Reason: {resp_obj['detail']}")

def revoke_secret(secret_id):
  url = f"https://api.nexmo.com/accounts/{API_KEY}/secrets/{secret_id}"
  keystring = bytes(f"{API_KEY}:{API_SECRET}", 'utf-8')
  auth =  base64.b64encode(keystring).decode('utf-8')
  headers = {'Authorization' : f'Basic {auth}'}
  resp = requests.delete(url, headers=headers)
  if resp.status_code == 204:
    print('Set time has elapsed and secret has been revoked')
    return True
  else:
    if debug:
      print(resp.text)
    else:
      resp_obj = json.loads(resp.text)
      print(resp_obj['detail'])
    return False

def main():
  global debug
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--password', default='Password123', action='store', help='The Temporary Password (default Password123)')
  parser.add_argument('-t', '--time', default=300, action='store', help='How long should the temporary password be active (default 300s)')
  parser.add_argument('-c', '--check', default=False, action='store_true', help='Check how many secrets are on the account')
  parser.add_argument('-d', '--debug', default=False, action='store_true', help='To enable debug features such as being able to view full request response data')
  args = parser.parse_args()
  if args.debug:
    debug = True
  if not args.check:
    secret = args.password
    ttl = int(args.time)
    s = sched.scheduler(time.time, time.sleep)
    secretid = new_secret(secret)
    if secretid is not None:
      print(f"Successfully sent request and recieved the following Secret ID:{secretid}")
    else:
      quit()
    print(f"Temporary password {secret} has been set for {ttl} seconds")
    s.enter(ttl, 1, revoke_secret, argument=(str(secretid),))
    s.run()
  else:
    get_secrets()
  
if __name__ == "__main__":
  main()
