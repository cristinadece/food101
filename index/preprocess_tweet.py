"""

"""
# food101 : preprocess_tweet.py
# Created by muntean on 5/15/17

def get_media_url(tweet):
    if "media" in tweet["entities"]:
        foundMedia = tweet["entities"]["media"]
        return foundMedia[0]["media_url"]
    else:
        return None

def get_food_category(img_url):
    categ_list = ["Pizza", "Pasta", "Sushi", None]
    return random.choice(categ_list)