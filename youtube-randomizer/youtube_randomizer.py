from googleapiclient.discovery import build
from dotenv import load_dotenv
import random
import os

load_dotenv()
api_key = os.getenv('API_KEY')
service = build('youtube', 'v3', developerKey=api_key)


def get_channel_id(username):

    channel_call = service.channels().list(
        part='snippet,contentDetails', forHandle=username)

    response = channel_call.execute()
    return (response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])


def get_videos(playlist_id):

    all_videos = []
    next_page_token = None

    while True:

        videos = service.playlistItems().list(
            playlistId=playlist_id, part='snippet', pageToken=next_page_token, maxResults=50)

        response = videos.execute()
        all_videos.extend(response['items'])

        if 'nextPageToken' in response:

            next_page_token = response['nextPageToken']

        else:
            break

    return all_videos


def get_random_video(videos):

    rand_video = random.choice(videos)

    return f'https://www.youtube.com/watch?v={rand_video["snippet"]["resourceId"]["videoId"]}'


username = input('Enter a YouTube username: @')
playlist_id = get_channel_id(username)
videos = get_videos(playlist_id)
print(get_random_video(videos))
