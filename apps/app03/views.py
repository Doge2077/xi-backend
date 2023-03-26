import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import pymongo


class category(APIView):
    def get(self, request):
        Client = pymongo.MongoClient(host='localhost', port=27017)
        table = Client.Sentence.Sentence
        data = table.find()
        data_list = []
        for i in range(2):
            temp = data[i]
            data_list.append(
                {
                    'cat_a_title': temp['cat_a_title'],
                    'cat_a_id': temp['cat_a_id'],
                }
            )
        print(data_list)
        return Response(data_list)


class get_article_info(APIView):
    def get(self, request):
        pram = request.GET
        cat_a_id, cat_b_id = int(pram.get('cat_a_id')), int(pram.get('cat_b_id'))
        # print(cat_a_id, cat_b_id)
        Client = pymongo.MongoClient(host='localhost', port=27017)
        table = Client.Sentence.Sentence
        data = table.find_one({'cat_a_id': cat_a_id}, {'cat_a_info': 1})['cat_a_info'][cat_b_id - 1]['cat_b_info']
        print(data)
        return Response(data)