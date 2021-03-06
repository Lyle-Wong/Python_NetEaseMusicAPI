import json
import logging
import random
from typing import List

from requests.models import Response

from .__init__ import BASE_URL, Http_Response, getCookie, request_query, send


def home(request):
    return Http_Response("", "这里是歌曲信息接口", "")

def task(request):
    """
    每天刷歌
        :param request: 
    """
    recommend_songs_resp = send({"total": "true"}).POST("weapi/v1/discovery/recommend/songs")
    
    if recommend_songs_resp.status_code != 200:
        logging.info('status_code of recommend songs: ' + str(recommend_songs_resp.status_code))
        logging.warn('get recommand songs fail')
    resp_data = json.loads(recommend_songs_resp.text)
    logging.debug(json.dumps(resp_data, indent=2))
    songs = resp_data['recommend']
    music_list: List = [(s['id']) for s in songs]
    cookie = getCookie()
    csrf = cookie["__csrf"] if "__csrf" in cookie else ""
    music_id: List = []

    query = request_query(request, ["limit", {"limit": 100}])
    query["total"] = True
    query["n"] = 1000
    personalized_playlist: Response = send(query).POST("weapi/personalized/playlist")

    personalized_playlist_json_data = json.loads(personalized_playlist.text)
    playlist_ids = [i.get('id') for i in personalized_playlist_json_data.get('result')]

    music_list.extend(playlist_ids)

    for m in music_list:
        resp = send({'id':m,
        'n':1000, 
        'csrf_token':csrf}).POST('weapi/v6/playlist/detail')
        ret = json.loads(resp.text)
        try:
            for i in ret['playlist']['trackIds']:
                music_id.append(i['id'])
        except:
            logging.error(json.dumps(ret, indent=2))
    logging.info('get music_ids:' + str(music_id))
    post_data = json.dumps({
        'csrf_token': csrf,
        'logs':
        json.dumps(
            list(
                map(
                    lambda x: {
                        'action': 'play',
                        'json': {
                            'download':0,
                            'end': 'playend',
                            'id':x,
                            'sourceId': '',
                            'time': 240,
                            'type': 'song',
                            'wifi': 0
                        }
                    },
                    random.sample(music_id, 420 if len(music_id)>420 else len(music_id))
                )
            )
        )
    })

    res = send(json.loads(post_data)).POST('weapi/feedback/weblog')
    ret = json.loads(res.text)

    return Http_Response(request, json.dumps(ret, indent=2))
