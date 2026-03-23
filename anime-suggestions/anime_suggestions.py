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

    for i, item in enumerate(recommendations.json()['data'], 1):
        print(i, item['entry']['title'])
        print(item['entry']['url'], '\n')


while True:
    title = input('What is the name of the anime? ')
    mal_id = search(title)
    get_recommendations(mal_id)

    repeat = input('Would you like to search for another anime? y/n: ')
    if repeat != 'y':
        break
