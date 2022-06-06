import os
import pandas as pd

def getCurrentUserId(sp):
    result = sp.current_user()
    userId = result['id']
    return userId


def getTrackIds(tracks):
    trackIds = []
    for i in range(len(tracks)):
        trackIds.append(tracks[i]['id'])
    return trackIds


def getCurrentPlaying(sp):
    result = sp.currently_playing()
    track = result['item']
    print("\nCurrent Playing =", track['artists'][0]['name'], "–", track['name'])


def getUserPlaylists(sp):
    userPlaylistsIds = []
    userPlaylistsNames = []
    user = getCurrentUserId(sp)
    results = sp.user_playlists(user=user)
    for idx, item in enumerate(results['items']):
        userPlaylistsIds.append(item['id'])
        userPlaylistsNames.append(item['name'])
    return userPlaylistsIds, userPlaylistsNames

def getAllPlaylistTracks(sp, playlistIds, playlistNames):
    allPlaylistsTracks = []
    for i in range(len(playlistIds)):
        results = sp.playlist_tracks(playlist_id=playlistIds[i])
        for _, item in enumerate(results['items']):
            allPlaylistsTracks.append(item["track"])
    return allPlaylistsTracks

def getTrackFeatures(sp, tracks):
    trackIds = getTrackIds(tracks)
    trackFeaturesArr = []
    print("Number of Total Tracks:", len(trackIds))
    if (len(trackIds) <= 100):
        trackFeatures = sp.audio_features(trackIds)
        trackFeaturesArr.append(trackFeatures)
    else:
        lowerLimit = 0
        upperLimit = 100
        howManyReruns = int(len(trackIds) / 100) + 1
        print(howManyReruns)
        for i in range(howManyReruns):
            trackFeatures = sp.audio_features(trackIds[lowerLimit:upperLimit])
            for k in range(len(trackFeatures)):
                trackFeaturesArr.append(trackFeatures[k])
            upperLimit += 100
            lowerLimit += 100
    return trackFeaturesArr


def convertTrackFeaturesToDataFrame(trackFeatures):
    if os.path.exists('data/trackFeatures.csv'):
        df = pd.read_csv('data/trackFeatures.csv')
        print("There is already a track feature data for your playlists")
        x = input("Do you want to update data with this database (Y or N):")
        if (x == 'Y') or (x == 'y'):
            df = pd.DataFrame(trackFeatures)
            df.to_csv(r'data/trackFeatures.csv')
        elif (x != 'Y') and (x != 'N') and (x != 'y') and (x != 'n'):
            print("Wrong Input")
    else:
        df = pd.DataFrame(trackFeatures)
        df.to_csv(r'data/trackFeatures.csv')
    return df
