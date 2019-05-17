from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .Module.UseMongoDB import RecSysLogsToMongo
import json
import glob
from django.db import connection
from django.contrib.auth.decorators import login_required


db = RecSysLogsToMongo()

def index(request):
    static_list = glob.glob('web/static/music/*.mp3')
    name_of_musics = [f.split('/')[-1].split('.')[0] for f in  static_list]
    return render(request,'index.html',{
        'mp3_list':name_of_musics,
    })

@csrf_exempt
def music_record_logs(request):
    if request.method == 'POST':
        # db.insert_log_to_mongodb(request.body)
        return HttpResponse(request.body)

@csrf_exempt
def add_to_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']
        track_info = data['track'].split(':')
        ablum_id = track_info[0]
        track_id = track_info[1]
        print(user, track_id, ablum_id)
        return HttpResponse(request.body)


@login_required
def browser_artist(request):
    # Every time user refresh page will get 30 different artists.
    sql = 'select * from tracks_artist order by rand() limit 30'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        dict_row = dictfetchall(cursor)

    return render(request,'browserArtist.html',{
        'artist_list':dict_row,
    })

@login_required
def browser_artist_from_letter(request, letter):
    sql = "SELECT * from  tracks.tracks_artist where Name LIKE '" + letter +"%'"
    print(sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        dict_row = dictfetchall(cursor)
    return render(request,'selected_artist.html',{
        'artist_list':dict_row,
    })

@login_required
def artist_info(request, artist_id):
    sql = "select * from tracks_album where artist_id ='" + artist_id +"'ORDER BY release_date DESC;"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        dict_row = dictfetchall(cursor)
    return render(request,'artistInfo.html',{
        'artist_album':dict_row,
    })

@login_required
def ablum_info(request, album_id):
#     print(album_id)
    with connection.cursor() as cursor:
        sql = "select  M.artist, M.artist_id, M.album_name, M.album_id,  M.img, features.id, features.name, features.preview_url from tracks_features as features INNER JOIN  ( \
                SELECT artist.name as artist, artist.id as artist_id, album.name as album_name, \
                album.img_url as img, album.id as album_id \
                FROM tracks_artist as artist \
                INNER JOIN tracks_album as album \
                where album.artist_id = artist.id) M \
                where M.album_id = features.album_id and M.album_id = '"+album_id +"';"
        cursor.execute(sql)
        dict_row = dictfetchall(cursor)
    return render(request,'album.html',{
        'album':dict_row,
    })


def sql_join_table_example(request):
    with connection.cursor() as cursor:
        sql = "select * from tracks_features as features INNER JOIN  ( \
                SELECT artist.name as artist, artist.id as artist_id, album.name as album_name, \
                album.img_url as img, album.id as album_id \
                FROM tracks_artist as artist \
                INNER JOIN tracks_album as album where album.artist_id = artist.id) M where M.album_id = features.album_id;" 
        cursor.execute(sql)
        dict_row = dictfetchall(cursor)
    return HttpResponse(
                json.dumps(dict_row, sort_keys=False, indent=2), 
                content_type="application/json")  

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row))
        for row in cursor.fetchall()]
