import json
# from FriendCodeHelper import *

PLAYER_PROFILE_PATH = 'config/player_profile.json'
FRIEND_CODE_PATH = 'config/friend_codes.json'

player_name = 'player_name'
island_fruit = 'island_fruit'
island_flowers = 'island_flowers'
    
def instantiate_user_in_database(friend_code, author):
    with open(PLAYER_PROFILE_PATH, 'r+') as f:
        player_profiles = json.load(f)
        profile = {player_name: str(author)}
        player_profiles[friend_code] = profile
        
    with open(PLAYER_PROFILE_PATH, 'r+') as f:
        json.dump(player_profiles, f)


def get_friend_code(user_id):
    with open(FRIEND_CODE_PATH) as f:
        friend_codes = json.load(f)
    
    if str(user_id) not in list(friend_codes.keys()):
        return -1
    
    return friend_codes[str(user_id)]


def query_profile(friend_code):
    profile = None
    with open(PLAYER_PROFILE_PATH) as f:
        player_profiles = json.load(f)
        try:
            profile = player_profiles[friend_code]
            
        except KeyError:
            return -1
        
    return profile


def add_to_profile(args, author):
    if len(args) < 3:
            # await ctx.send('No target specified. Possible tags are `fruit` or `flower`')
            return -1
            
    else:
        friend_code = get_friend_code(author.id)
            
        if friend_code == -1:
            # await ctx.send('Player not found. You must add your friend code to the bot to use this feature. For help using this feature, type `!help add`')
            return -2
                
                
        with open(PLAYER_PROFILE_PATH, 'r+') as f:
            '''
            "SW-XXXX-XXXX-XXXX" : {
                "player_name": "Test name", 
                "island_fruit": "Fruit name", 
                "island_flowers": "Island flowers"
            }
            '''
            player_profiles = json.load(f)
            try:
                profile = player_profiles[friend_code]
                    
            except KeyError:
                profile = {player_name: str(author)}
            
            if args[1] == 'fruit':
                new_item = {island_fruit: args[2]}
                
            elif args[1] == 'flower':
                new_item = {island_flowers: args[2]}
                
            profile.update(new_item)
            player_profiles[friend_code] = profile
            f.seek(0) # reset cursor
            json.dump(player_profiles, f)
            
            