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
            # 调用微信 code2Session 接口，换取用户唯一标识 OpenID 和 会话密钥 session_key
            data = wx_login.login(param.get('code'))
            if data:
                # 将openid 和 session_key拼接
                val = data['openid'] + "&" + data["session_key"]
                key = data['openid'] + str(int(time.time()))
                # 利用 md5 加密方式 对 key 加密
                md5 = hashlib.md5()
                md5.update(key.encode("utf-8"))
                key = md5.hexdigest()
                # 保存到 redis 内存库，以便快速校验登录信息
                cache.set(key, val)
                # 从 MySQL 数据库中查找 openid 以便确认用户是否存在
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
