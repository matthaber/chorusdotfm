import os
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTOPY_CLIENT_SECRET')
user = 'matt.haber'

token = util.prompt_for_user_token(user, scope='playlist-modify-private,playlist-modify-public', client_id=client_id, client_secret=client_secret, redirect_uri='https://localhost:8080')

spotify = spotipy.Spotify(auth=token)

band_dict = {'cllctyrslf': 'so poetic (Sundressed cover)', 'GRMLN': 'Non Classical', 'Dirt Buyer': 'Dirt Buyer', 'Sore Eyelids': 'avoiding life', 'Short Fictions': 'Fates Worse Than Death', 'Out of Service': 'Burden', 'Rat Tally': 'When You Wake Up'}

song_ids = []

for k, v in band_dict.items():
    spot_search = spotify.search(q=f'album:{v} artist:{k}',type="album")
    if(spot_search['albums']['items']):
        for i in spot_search['albums']['items']:
            songs = spotify.album_tracks(i['id'])
            for s in songs['items']:
                print(s['id'])
                song_ids += [s['id']]

print(song_ids)


spotify.user_playlist_add_tracks('matt.haber','1GAYCX9r6kkcVVk08eYd6D',song_ids)