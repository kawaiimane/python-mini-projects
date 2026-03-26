from googleapiclient.discovery import build
from dotenv import load_dotenv
import tkinter as tk
from PIL import ImageTk, Image
import requests
import random
import os
from io import BytesIO
import webbrowser
import json
from datetime import datetime, timedelta

load_dotenv()
api_key = os.getenv('API_KEY')
service = build('youtube', 'v3', developerKey=api_key)


def get_channel_id(username):
    channel_call = service.channels().list(
        part='snippet,contentDetails', forHandle=username)

    response = channel_call.execute()
    return (response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])


def get_videos(playlist_id, username):
    cache = load_cache(username)

    if cache is not None:
        return cache

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

    save_cache(username, all_videos)
    return all_videos


def get_random_video(videos):
    urls = []
    thumbnails = []
    titles = []

    for _ in range(20):
        rand_video = random.choice(videos)
        urls.append(
            f'https://www.youtube.com/watch?v={rand_video["snippet"]["resourceId"]["videoId"]}')
        thumbnails.append(rand_video['snippet']
                          ['thumbnails']['medium']['url'])
        titles.append(rand_video['snippet']['title'])

    return urls, thumbnails, titles


def window_gui():
    root = tk.Tk()
    root.geometry('1230x739+665+350')
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.config(bg='#121212')

    user_input = tk.Entry(root)
    user_input.grid(row=0, column=0, sticky='w')

    quit_gui = tk.Button(root, text='Quit', command=root.destroy)
    quit_gui.grid(row=0, column=4, sticky='e')

    frame = tk.Frame(root, bg='#121212')
    frame.grid(row=1, column=0, columnspan=5)

    def search_channel():
        username = user_input.get()
        playlist_id = get_channel_id(f'@{username}')
        videos = get_videos(playlist_id, username)
        new_urls, new_thumbnails, new_titles = get_random_video(videos)

        load_thumbnails(new_urls, new_thumbnails, new_titles)

    def load_thumbnails(urls, thumbnails, titles):
        nonlocal frame
        frame.destroy()
        frame = tk.Frame(root, bg='#121212')
        frame.grid(row=1, column=0, columnspan=5)

        for i, thumbnail in enumerate(thumbnails):
            get_image = requests.get(thumbnail).content
            convert_pil = Image.open(BytesIO(get_image))
            resize_image = convert_pil.resize((240, 135), Image.LANCZOS)
            convert_tk = ImageTk.PhotoImage(resize_image)

            title_label = tk.Label(
                frame, text=titles[i], wraplength=240, width=40, justify='center', fg='#C4C4C4', bg='#121212', font=('Arial', 8))
            title_label.grid(row=(i // 5) * 2 + 2, column=i % 5)
            thumbnail_label = tk.Label(frame, image=convert_tk, bg='#121212')
            thumbnail_label.grid(row=(i // 5) * 2 + 1, column=i % 5)
            thumbnail_label.image = convert_tk
            thumbnail_label.bind('<Button-1>', lambda event,
                                 u=urls[i]: webbrowser.open_new_tab(u))

    search = tk.Button(root, text='Search', command=search_channel)
    search.grid(row=0, column=0)

    root.mainloop()


def save_cache(username, videos):
    channel_name = f'{username}.json'
    video_amount = videos

    data = {
        'videos': video_amount,
        'timestamp': datetime.now().isoformat()
    }

    with open(channel_name, mode='w', encoding='utf-8') as file:
        json.dump(data, file)


def load_cache(username):
    channel_name = f'{username}.json'

    try:
        with open(channel_name, mode='r', encoding='utf-8') as file:
            open_json = json.load(file)

            check_cache = datetime.now() - \
                datetime.fromisoformat(open_json['timestamp'])

            if check_cache < timedelta(hours=24):
                return open_json['videos']
            else:
                return None

    except FileNotFoundError:
        return None


window_gui()
