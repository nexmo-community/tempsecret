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
config.read(homedir+'/.nexmorc')

API_KEY = config['credentials']['api_key']
API_SECRET = config['credentials']['api_secret']


def get_secrets():
  url = "https://api.nexmo.com/accounts/{}/secrets".format(API_KEY)
  keystring = bytes("{}:{}".format(API_KEY, API_SECRET), 'utf-8')
  auth =  base64.b64encode(keystring).decode('utf-8')
  headers = {'Authorization' : 'Basic '+auth}
  resp = requests.get(url, headers=headers)
  data = resp.json()
  print("You have {} secrets on your account".format(str(len(data['_embedded']['secrets']))))
  for x in data['_embedded']['secrets']:
    print("{} was created at: {}".format(x['id'], x['created_at']))
 
 
def new_secret(secret):
  url = "https://api.nexmo.com/accounts/{}/secrets".format(API_KEY)
  keystring = bytes("{}:{}".format(API_KEY, API_SECRET), 'utf-8')
  auth =  base64.b64encode(keystring).decode('utf-8')
  headers = {'Authorization' : 'Basic '+auth}
  payload = {'secret' : secret}
  resp = requests.post(url, headers=headers, json=payload)
  if resp.status_code == 201:
    data = resp.json()
    return data['id']
  else:
    print(resp)
    print(resp.text)

def revoke_secret(secret_id):
   url = "https://api.nexmo.com/accounts/{}/secrets/{}".format(API_KEY, secret_id)
   keystring = bytes("{}:{}".format(API_KEY, API_SECRET), 'utf-8')
   auth =  base64.b64encode(keystring).decode('utf-8')
   headers = {'Authorization' : 'Basic '+auth}
   resp = requests.delete(url, headers=headers)
   if resp.status_code == 204:
     print('Secret Revoked')
     return True
   else:
     print(resp.text)
     return False
     
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--password', default='Password123', action='store', help='The Temporary Password (default Password123)')
  parser.add_argument('-t', '--time', default=300, action='store', help='How long should the temporary password be active (default 300s)')
  parser.add_argument('-c', '--check', default=False, action='store_true', help='Check how many secrets are on the account')
  args = parser.parse_args()
  if args.check == False:
    secret = args.password
    ttl = int(args.time)
    s = sched.scheduler(time.time, time.sleep)
    secretid = new_secret(secret)
    print(secretid)
    print("Temporary password {} set for {} seconds".format(secret, str(ttl)))
    s.enter(ttl, 1, revoke_secret, argument=(str(secretid),))
    s.run()
  else:
    get_secrets()
  
if __name__ == "__main__":
  main()
