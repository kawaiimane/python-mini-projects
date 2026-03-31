import requests
import time

base_url = 'https://api.jikan.moe/v4/'


def search(title):
    response = requests.get(f'{base_url}anime?q={title}&limit=1')
    time.sleep(1)

    try:
        return (response.json()['data'][0]['mal_id'])
    except IndexError:
        print('Error: data not found.')


def get_recommendations(mal_id):
    if mal_id is None:
        print('Anime doesn\'t exist.')
        return

    recommendations = requests.get(f'{base_url}anime/{mal_id}/recommendations')
    time.sleep(1)

    recs = []
    for item in recommendations.json()['data']:
        recs.append(item)
    return recs
