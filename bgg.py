import xml.etree.ElementTree as ET
import requests
from time import sleep


def find_games(bgg_user):
    user_name = bgg_user
    print("BGG User = {}".format(user_name))
    params = {'wanttoplay': '1', 'wanttobuy': '0', 'wantintrade': '0', 'wishlist': '0'}
    user = requests.get(url='https://www.boardgamegeek.com/xmlapi/collection/%s' % user_name, params=params)
    while user.status_code != 200:
        sleep(1)
        print(user.status_code)
        user = requests.get(url='https://www.boardgamegeek.com/xmlapi/collection/%s' % user_name, params=params)

    print(user.text)
    user_root = ET.fromstring(user.text.encode('utf-8'))
    want_to_play = []
    for game in user_root:
        want_to_play.append(game.find('name').text)

    vpc = requests.get('https://www.boardgamegeek.com/xmlapi/collection/victorypointcafe?own=1&subtype=boardgame')
    while vpc.status_code != 200:
        sleep(1)
        print(vpc.status_code)
        vpc = requests.get('https://www.boardgamegeek.com/xmlapi/collection/victorypointcafe?own=1&subtype=boardgame')

    vpc_root = ET.fromstring(vpc.text.encode('utf-8'))
    vpc_owned = []
    for game in vpc_root:
        vpc_owned.append(game.find('name').text)

    results = []

    for game in want_to_play:
        if game in vpc_owned:
            results.append(game)

    # for i in range(len(results)):
    #     results[i] = results[i].encode('utf-8')

    return results


# results = find_games('dlutsch')
# print(results)