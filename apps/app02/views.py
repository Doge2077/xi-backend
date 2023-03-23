import random

from bson import ObjectId
from bson.json_util import dumps
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
import json
import pymongo
from rest_framework.response import Response
from rest_framework.views import APIView


class head_info(APIView):
    def get(self, request):
        info = {
            "message": [
                {
                    "image_src": "http://127.0.0.1:8000/static/app02/image01.png",
                    "open_type": "navigate",
                    "goods_id": 122,
                    # "navigator_url": "/pages/goods_detail/index?goods_id=129"
                },
                {
                    "image_src": "http://127.0.0.1:8000/static/app02/image02.png",
                    "open_type": "navigate",
                    "goods_id": 123,
                    # "navigator_url": "/pages/goods_detail/index?goods_id=129"
                }
            ],
            "meta": {
                "msg": "获取成功",
                "status": 200
            }
        }
        return Response(info)


class daily_sentences(APIView):
    def get(self, request):
        MyClient = pymongo.MongoClient(host='localhost', port=27017)
        db = MyClient['DaySentence']
        collection = db.DaySentence
        documents = collection.find()
        id, idx = 0, 0
        sentences = []

        # for item in range(100):
        #     sentences.append({
        #         'id': id,
        #         'info': documents[item]['text'],
        #         'title': documents[item]['title']
        #     })
        #     id += 1
        while id < 50:
            infolength, titlelength = len(documents[idx]['text']), len(documents[idx]['title'])
            if infolength < 50 and titlelength < 50:
                sentences.append({
                    'id': id,
                    'info': documents[idx]['text'],
                    'title': documents[idx]['title']
                })
                id += 1
            idx += 1
        return Response(sentences)
