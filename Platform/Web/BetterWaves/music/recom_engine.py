from music import models
import pandas as pd
from music import Recommenders
from sklearn.model_selection import train_test_split


class RecommendationEngine:
    def __init__(self):
        self.pm = Recommenders.popularity_recommender_py()
        self.retrain()

    def retrain(self):
        print("=====Training=====")
        user_songs = models.UserSong.objects.all()
        user_songs_dict = {
            'user_id': [],
            'song_id': [],
            'listen_count': []
        }
        for user_song in user_songs:
            user_id = user_song.user_of_song_id
            song_id = user_song.song_id
            listen_count = user_song.listen_count
            user_songs_dict['user_id'].append(user_id)
            user_songs_dict['song_id'].append(song_id)
            user_songs_dict['listen_count'].append(listen_count)
        print("=====Data Framed!=====")
        data = pd.DataFrame(user_songs_dict)
        train_data, test_data = train_test_split(data, test_size=0.20, random_state=0)
        self.pm.create(train_data, 'user_id', 'song_id')

    def recommend(self, user_id):
        result = dict(self.pm.recommend(user_id))
        del(result['user_id'])
        del(result['score'])
        song_ids = list(result['song_id'])
        ranks = list(result['Rank'])
        result = []
        for i in range(len(song_ids)):
            result.append({
                'song_id': song_ids[i],
                'rank': ranks[i]
            })
        return result