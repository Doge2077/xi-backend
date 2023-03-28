import random
from app02 import WyNews
from bson import ObjectId
from bson.json_util import dumps
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
import json
import os
import pymongo
from rest_framework.response import Response
from rest_framework.views import APIView


class head_info(APIView):
    def get(self, request):
        dirs = os.listdir('apps/app02/static')
        num = (len(dirs) - 1) // 2
        with open('apps/app02/static/titles.txt', 'r', encoding='utf8') as f:
            titles = f.read().split('\n')
        data_list = []
        for item in range(1, num + 1):
            pram = {
                'title': titles[item - 1],
                'rank': item,
                'img_src': f'http://127.0.0.1:8000/static/{item}.jpg'
            }
            data_list.append(pram)

        return Response(data_list)


class get_news_info(APIView):
    def get(self, request):
        num = request.GET.get('rank')
        J = open(f'apps/app02/static/{num}.json', 'r', encoding='utf8')
        jsonData = json.loads(J.read())
        J.close()
        return Response(jsonData)




class daily_sentences(APIView):
    def get(self, request):
        MyClient = pymongo.MongoClient(host='localhost', port=27017)
        db = MyClient['Sentence']
        collection = db.DaySentence
        _id = 1
        sentences = []
        queries = random.sample(range(1, 200), 50)
        sentences_list = []
        for query in queries:
            document = collection.find_one({'sid': query}, {'content': 1, 'title': 1})
            pram = {
                'id': _id,
                'title': document['title'],
                'content': document['content']
            }
            _id += 1
            sentences_list.append(pram)
        _id = 1
        return Response(sentences_list)
