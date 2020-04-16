import datetime
import json
import sys
import re

FRIEND_CODE_PATH = 'config/friend_codes.json'

''' set commands'''
def set_friend_code(user_id, friend_code):
    regex = 'SW-\d{4}-\d{4}-\d{4}'
    if re.findall(regex, friend_code):
        with open(FRIEND_CODE_PATH) as f:
            friend_codes = json.load(f)
            
        user_and_code = {
            user_id: friend_code
        }
    
        friend_codes.update(user_and_code)
        with open(FRIEND_CODE_PATH, 'r+') as wf:
            json.dump(friend_codes, wf)
            return 0
        
    else:
        return -1
           
    
''' get commands'''
def get_friend_code(user_id):
    with open(FRIEND_CODE_PATH) as f:
        friend_codes = json.load(f)
    
    if str(user_id) not in list(friend_codes.keys()):
        return -1
    
    return friend_codes[str(user_id)]
    
    