# -*- coding:utf-8 -*-
from django.db import models
from hashlib import md5


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    enable = models.IntegerField()
    info = models.TextField()
    groupid = models.IntegerField()
    permission = models.IntegerField()

    class Meta:
        db_table = 'user'

    def set_password(self, password):
        """加密用户密码"""
        self.password = md5(password).hexdigest()

    def check_password(self, password):
        if md5(password).hexdigest() == self.password:
            return True
        else:
            return False


class Group(models.Model):
    name = models.CharField(max_length=128)
    enable = models.CharField(max_length=128)
    info = models.TextField()
    tenantid = models.CharField(max_length=128)
    createdate = models.DateTimeField(auto_now=False, auto_now_add=True)

    @property
    def get_enable(self):
        if self.enable == "1":
            return "活跃"
        else:
            return "已禁用"

    @property
    def get_createdate(self):
        return self.createdate.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        db_table = 'group'


class Permission(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'permission'
