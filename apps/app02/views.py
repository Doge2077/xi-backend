from django.shortcuts import render

# Create your views here.
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
