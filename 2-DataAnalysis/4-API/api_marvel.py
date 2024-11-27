import requests
import json
import pandas as pd
import numpy as np
import hashlib
import datetime

def hash_params(timestamp,priv_key,pub_key):
    """ Marvel API requires server side API calls to include
    md5 hash of timestamp + public key + private key """

    hash_md5 = hashlib.md5()
    hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params

timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')

pub_key = '764083524c8a0ff7c0ca7c466b367db2'
priv_key = '3289aebd0cd55b12bc1ad5e5828daed7f5cb1a07'


params = {'ts': timestamp, 
        'apikey': pub_key, 
        'hash': hash_params(timestamp,priv_key,pub_key),
        'nameStartsWith':"R",
        # 'offset':,
        'limit': 10
        };

url = 'http://gateway.marvel.com/v1/public/characters'

res = requests.get(url,params=params,)

res=res.json()
print(json.dumps(res, indent=2, sort_keys=True))
marvel_list = [{"name": marvel["name"], "url": marvel['thumbnail'].get('path')+"."+marvel['thumbnail'].get('path')} for marvel in res['data']['results']]
df = pd.DataFrame(marvel_list)
print(df)


