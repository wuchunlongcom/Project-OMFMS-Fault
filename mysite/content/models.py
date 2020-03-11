#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.conf import settings
from accounts.models import MyUser, Project
from .storage import images_storage
import uuid

class Type(models.Model):
    """ 故障类型 """
    fms_type = (
        ('0','运营商故障'),
        ('1','机房故障'),
        ('2','程序故障')
    )
    name = models.CharField(choices=fms_type , max_length=255, verbose_name=u"故障类型", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("update_type", ("更新故障类型")),
            ("del_type", ("删除故障类型")),
        )
        default_permissions = ()


class Content(models.Model):
    """ 故障表 """
    
    fms_level = (
        (0, u"非常严重"),
        (1, u"严重"),
        (2, u"中等"),
        (3, u"一般"),
        (4, u"无影响"),
    )
    fms_status = (
        (0, u"处理中"),
        (1, u"已恢复"),
        (2, u"改进中"),
        (3, u"已完结"),
    )
    fms_improve = (
        (0, u"开发"),
        (1, u"运维"),
        (2, u"机房"),
        (3, u"网络运营商"),
        (4, u"第三方"),

    )
    id = models.UUIDField(blank=True, primary_key=True, auto_created=True, default=uuid.uuid4)
    title = models.CharField(max_length=255, verbose_name=u'故障标题', unique=True)
    effect = models.TextField(verbose_name=u'故障现象', null=True, blank=True)
    content = models.TextField(verbose_name=u'故障分析', null=True, blank=True)
    reasons = models.TextField(verbose_name=u'故障原因', null=True, blank=True)
    solution = models.TextField(verbose_name=u'解决方案', null=True, blank=True)
     
           
    author = models.ForeignKey(MyUser, verbose_name=u'创建者', on_delete=models.PROTECT, null=True, blank=True)
    type = models.ForeignKey(Type, verbose_name=u'故障类型',  on_delete=models.PROTECT, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name=u'影响项目', on_delete=models.PROTECT, null=True, blank=True)
     
    level = models.IntegerField(choices=fms_level, verbose_name=u'故障级别', default=0)
    status = models.IntegerField(choices=fms_status, verbose_name=u'故障状态', default=0)
    improve = models.IntegerField(choices=fms_improve, verbose_name=u'主导改进', default=0)
        
    start_time = models.DateTimeField(verbose_name=u'开始时间', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name=u'结束时间', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ("get_content", ("查看故障列表")),
            ("detail_content", ("故障详情")),
            ("add_content", ("添加故障")),
            ("edit_content", ("编辑故障")),
            ("del_content", ("删除故障")),
        )
        default_permissions = ()
        
        verbose_name = u"故障表"
        verbose_name_plural = verbose_name



class ZbxContent(models.Model):

    fms_status = (
        (0, u"处理中"),
        (1, u"已恢复"),
        (2, u"改进中"),
        (3, u"已完结"),
    )

    id = models.UUIDField(blank=True, primary_key=True, auto_created=True, default=uuid.uuid4)
    eventid = models.IntegerField(unique=True, verbose_name=u'事件ID')
    title = models.CharField(max_length=255, verbose_name=u'故障简述')
    host = models.CharField(max_length=120, verbose_name='故障服务器Top10', null=True)
    author = models.CharField(max_length=10, default='ZABBIX', verbose_name=u'ZBX用户')
    level = models.CharField(max_length=60, verbose_name=u'故障级别')
    type = models.CharField(max_length=120, verbose_name=u'zbx应用集', blank=True, null=True)
    project = models.CharField(max_length=255, verbose_name=u'ZBX主机组')
    effect = models.TextField(blank=True, verbose_name=u'故障影响', null=True)
    reasons = models.TextField(blank=True, verbose_name=u'故障原因', null=True)
    solution = models.TextField(blank=True, verbose_name=u'解决方案', null=True)
    status = models.CharField(max_length=60, verbose_name=u'处理状态', default=u'未恢复')
    improve = models.CharField(max_length=10, default=u'运维', verbose_name=u'主导改进')
    content = models.TextField(blank=True, verbose_name=u'故障分析')
    start_time = models.DateTimeField(verbose_name=u'开始时间')
    end_time = models.DateTimeField(verbose_name=u'结束时间', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"故障表"
        verbose_name_plural = verbose_name


class Images(models.Model):

    url = models.ImageField(upload_to='img/%Y/%m/%d', blank=True, null=True, storage=images_storage())
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

