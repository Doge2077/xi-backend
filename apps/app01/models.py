from django.db import models


class Wxuser(models.Model):
    openid = models.CharField(max_length=100, unique=True, null=False, verbose_name='唯一标识')
    nickname = models.CharField(max_length=50, null=True, verbose_name='昵称')
    gender = models.IntegerField(default=0, null=True, verbose_name='性别')
    city = models.CharField(max_length=50, null=True, verbose_name='城市')
    province = models.CharField(max_length=50, null=True, verbose_name='省份')
    country = models.CharField(max_length=50, null=True, verbose_name='国家')
    avatar_url = models.URLField(max_length=200, null=True, verbose_name='头像')

    class Meta:
        app_label = 'app01'
        db_table = 'wx'  # 指定数据库中的表名
        ordering = ['-id']  # 排序方式按照 id 倒序
        verbose_name = '微信用户'  # 设置该模型在 Django 管理界面中的可读名称为 '微信用户'
        verbose_name_plural = '微信用户'  # 设置该模型在 Django 管理界面中的复数可读名称为 '微信用户'
        unique_together = ('openid',)  # 设置 openid 字段的值必须唯一
        indexes = [  # 设置 openid 和 nickname 两个字段在数据库中创建索引
            models.Index(fields=['openid']),
            models.Index(fields=['nickname']),
        ]

    def __str__(self):
        return self.nickname
