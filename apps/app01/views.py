# import json
# import requests
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from app01.settings import *
# from app01 import models
#
#
# class Login(APIView):
#     def post(self, request):
#         """
#         提供 post 请求
#         """
#         # 从请求中获得code
#         try:
#             code = json.loads(request.body).get('code')
#         except json.decoder.JSONDecodeError:
#             return Response({'code': 'no code'})
#         # 填写你的测试号密钥
#         appid = AppId
#         appsecret = AppSecret
#         # 微信服务接口地址
#         base_url = 'https://api.weixin.qq.com/sns/jscode2session'
#         # 实际请求
#         url = base_url + "?appid=" + appid + "&secret=" + appsecret + "&js_code=" + code + "&grant_type=authorization_code"
#         try:
#             response = requests.get(url)
#         except AttributeError:
#             return Response({'code': 'wrong code'})
#         # 处理获取的 openid
#         try:
#             openid = response.json()['openid']
#             session_key = response.json()['session_key']
#         except KeyError:
#             return Response({'code': 'fail'})
#         else:
#             # 打印到后端命令行
#             print(openid, session_key)
#
#             try:
#                 user = models.Wxuser.objects.get(openid=openid)
#             except models.Wxuser.DoesNotExist:
#                 user = None
#
#             if user:
#                 user = models.Wxuser.objects.get(username=openid)
#             else:
#                 user = models.Wxuser.objects.create(openid=openid)
#
#             return Response({
#                     'openid': openid,
#                     'login_key': session_key
#                 })


import hashlib
import time

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from app01 import models, wx_login


class Login(APIView):
    def post(self, request):
        param = request.data
        # 拿到小程序端提交的code
        if param.get('code'):
            # 调用微信code2Session接口,换取用户唯一标识 OpenID 和 会话密钥 session_key
            data = wx_login.login(param.get('code'))
            if data:
                # 将openid 和 session_key拼接
                val = data['openid'] + "&" + data["session_key"]
                key = data["openid"] + str(int(time.time()))
                # 将 key 加密
                md5 = hashlib.md5()
                md5.update(key.encode("utf-8"))
                key = md5.hexdigest()
                # 保存到redis内存库,因为小程序端后续需要认证的操作会需要频繁校验
                cache.set(key, val)
                has_user = models.Wxuser.objects.filter(openid=data['openid']).first()
                # 用户不存在则创建用户
                if not has_user:
                    models.Wxuser.objects.create(openid=data['openid'])
                return Response({
                    "code": 200,
                    "msg": "ok",
                    "data": {"login_key": key}
                })
            else:
                return Response({"code": 401, "msg": "code无效"})
        else:
            return Response({"code": 401, "msg": "缺少参数"})
