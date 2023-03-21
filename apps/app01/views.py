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

from app01 import models, wx_login, confirm, serializer


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
                key = data['openid'] + str(int(time.time()))
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
                    "data": {
                        "openid": data['openid'],
                        "login_key": key
                    }
                })
            else:
                return Response({"code": 401, "msg": "code无效"})
        else:
            return Response({"code": 401, "msg": "缺少参数"})


class Confirm(APIView):
    def post(self, request):
        param = request.data
        # 需要小程序端将 encryptedData iv login_key 的值传到后端
        # encryptedData iv session_key 用于解密获取用户信息
        # login_key 用于校验用户登录状态
        if param['encryptedData'] and param['iv'] and param['login_key']:
            # 从redis中拿到login_key并切分拿到 openid 和 session_key
            openid, session_key = cache.get(param['login_key']).split("&")
            # 利用微信官方提供算法拿到用户的开放数据
            data = confirm.WXBizDataCrypt.getInfo(param['encryptedData'], param['iv'], session_key)
            save_data = {
                "nickname": data['nickName'],
                "avatar_url": data['avatarUrl'],
                "gender": data['gender'],
                "province": data['province'],
                "city": data['city'],
                "country": data['country'],
            }
            # 将拿到的用户信息更新到用户表中
            models.Wxuser.objects.filter(openid=openid).update(**save_data)
            # 反序列化用户对象,并返回到小程序端
            data = models.Wxuser.objects.filter(openid=openid).first()
            data = serializer.User_ser(instance=data, many=False).data
            return Response({"data": data})
        else:
            return Response({"code": 200, "msg": "缺少参数"})