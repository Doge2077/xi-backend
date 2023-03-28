import json

from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
import pymongo


class category(APIView):
    def get(self, request):
        Client = pymongo.MongoClient(host='localhost', port=27017)
        table = Client.Sentence.Sentence
        data = table.find()
        data_list = []
        for i in list(data):
            pram = i
            # print(pram)
            data_list.append(
                {
                    'cat_a_id': pram['cat_a_id'],
                    'cat_a_title': pram['cat_a_title'],
                    'cat_b_title': [{'id': item['cat_b_id'], 'title': item['cat_b_title']} for item in
                                    pram['cat_a_info']]
                }
            )
        # return Response(data_list)
        # print(data[0]['cat_a_info'])
        return Response(data_list)
        # return Response(data[0]['cat_a_info'])


class get_article_info(APIView):
    def get(self, request):
        pram = request.GET
        cat_a_id, cat_b_id = int(pram.get('cat_a_id')), int(pram.get('cat_b_id'))
        Client = pymongo.MongoClient(host='localhost', port=27017)
        table = Client.Sentence.Sentence
        data = table.find_one({'cat_a_id': cat_a_id}, {'cat_a_info': 1})['cat_a_info'][cat_b_id - 1]['cat_b_info']
        return Response(data)
