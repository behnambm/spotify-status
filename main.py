import spotipy
from spotipy import SpotifyOAuth
from i3ipc import Connection
import os
import time
from update_twitter import UpdateTwitterBio
import subprocess
import sys


music_emoji = chr(127925)
speaker_head_emoji = chr(128483)


def prettify_bio_text(prefix: str, artists_list: str, playing_track_name: str):
    return prefix + '\n' + speaker_head_emoji + ' ' + artists_list + ' ' + music_emoji + ' ' + playing_track_name


def notify(message):
    if sys.platform == 'linux':
        subprocess.Popen(['notify-send', message])


def get_track_name_from_i3():
    """
    get title of Spotify window in i3WM
    """
    i3 = Connection()
    trees = i3.get_tree()  # retrieves all open windows in i3
    playing_track_name = None
    for tree in trees:
        if tree.name == '3:Music':  # static value in my own computer
            """ 
            Above condition is static because I open my Spotify
            in workspace 3 which has a label `:Music`
            """
            playing_track_name = tree.nodes[0].window_title

    playing_track_name = playing_track_name.split('-')
    if len(playing_track_name) > 1:
        playing_track_name = playing_track_name[1].strip()
        return playing_track_name
    else:
        return playing_track_name[0].strip()


def get_track_and_artists_name_from_api():
    """
    you should set three environment variables:
     SPOTIPY_CLIENT_ID
     SPOTIPY_CLIENT_SECRET
     SPOTIPY_REDIRECT_URI
        you need to set this value in your development dashboard
        this can be set this to http://127.0.0.1
        and in the first time execute you have to authenticate

     you can get these from Spotify development dashboard
    """
    auth_manager = SpotifyOAuth(scope='user-read-currently-playing')
    token = auth_manager.get_access_token(as_dict=False)

    sp = spotipy.Spotify(auth=token)

    current_track = sp.current_user_playing_track()

    if current_track:
        artists = []
        for i in current_track['item']['artists']:
            artists.append(i['name'])  # append name of artist to artists list

        playing_track_name = current_track['item']['name']
        artists = ','.join(artists)
        return artists, playing_track_name
    return False, False


if __name__ == '__main__':
    # set your current bio
    bio_prefix = ''

    path_to_home = os.environ['HOME']
    path_to_db = 'snap/opera/90/.config/opera'  # this is relative from one to another
    full_path = os.path.join(path_to_home, path_to_db, 'Cookies')

    twitter = UpdateTwitterBio(full_path)

    current_track_name = None

    # to reduce using resources
    timeout_to_check_from_api = 3

    while True:
        time.sleep(5)

        if not get_track_name_from_i3() or get_track_name_from_i3() == 'Spotify Premium':
            # in this case either spotify is closed or paused
            if timeout_to_check_from_api > 0:
                timeout_to_check_from_api -= 1
            else:  # after 15 seconds
                artists, track_name = get_track_and_artists_name_from_api()
                if track_name:  # if your playing music in other device
                    if current_track_name == track_name:
                        timeout_to_check_from_api = 3

                    else:  # in this case you are listening to another song (in other device)
                        current_track_name = track_name
                        # append new bio to the old one including track name, artist(s) name and emoji
                        bio_text = prettify_bio_text(artists, track_name)
                        twitter.set_bio_text(bio_text)
                        # the main method to update Twitter bio
                        twitter.update_bio()
                        # trigger system notification
                        notify('Your Twitter bio has been updated.')
                        current_track_name = track_name
                        timeout_to_check_from_api = 1
                else:  # spotify is not playing (at all)
                    # let's sleep for 2 min
                    timeout_to_check_from_api = 24

        else:  # spotify is playing
            if current_track_name != get_track_name_from_i3():

                artists, track_name = get_track_and_artists_name_from_api()

                if track_name != current_track_name:
                    # append new bio to the old one including track name, artist(s) name and emoji
                    bio_text = prettify_bio_text(artists, track_name)
                    twitter.set_bio_text(bio_text)
                    # the main method to update Twitter bio
                    twitter.update_bio()
                    # trigger system notification
                    notify('Your Twitter bio has been updated.')

                    current_track_name = track_name
