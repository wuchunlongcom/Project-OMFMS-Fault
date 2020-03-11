#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.conf import settings
from django.core import validators
import uuid
from django.utils import timezone
from django.contrib.auth.models import UserManager


class Project(models.Model):
    """ 影响项目表（故障影响的项目）"""
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256,blank=True,null=True)

    def __str__(self): 
        return self.name
     
    class Meta:
        permissions = (
            ("get_project", ("获取项目列表")),
            ("add_project", ("添加项目")),
            ("edit_project", ("编辑项目")),
            ("del_project", ("删除项目")),
        )
        default_permissions = ()
        
        verbose_name = u"项目表"
        verbose_name_plural = verbose_name

   
class Contact(models.Model):
    """ 联系人表 """
    name = models.CharField(max_length=64,unique=True)
    email = models.CharField(max_length=256,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("get_contact", ("获取邮件组列表")),
            ("add_contact", ("添加邮件组")),
            ("edit_contact", ("编辑邮件组")),
            ("del_contact", ("删除邮件组")),
        )
        default_permissions = ()
        
        verbose_name = u"联系人表"
        verbose_name_plural = verbose_name
        

class MyUserManager(BaseUserManager):
    def create_user(self, email, fullname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            is_active = True,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            fullname=fullname
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    groups = models.ForeignKey(Group, verbose_name=u'组',null=True, on_delete=models.PROTECT)
    email = models.EmailField(max_length=255, unique=True, verbose_name=u'邮箱')
    mobile = models.CharField((u'手机'), max_length=30, blank=False,validators=[validators.RegexValidator(r'^[0-9+()-]+$',('Enter a valid mobile number.'),'invalid')])
    fullname = models.CharField(max_length=64, null=True, verbose_name=u'中文姓名')
    is_active = models.BooleanField(default=True, verbose_name=u'状态')
    is_superuser = models.BooleanField(default=False, verbose_name=u'超级管理员')
    last_login = models.DateTimeField(default=timezone.now, verbose_name='最近登录时间')
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(verbose_name=u'日期',null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']
    
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
        permissions = (
            ("get_user", ("查看用户")),
            ("add_user", ("添加用户")),
            ("edit_user", ("编辑用户")),
            ("del_user", ("删除用户")),
        )
        default_permissions = ()
    def __str__(self): 
        if self.fullname:
            field = self.fullname
        else:
            field = self.username
        return field
    def get_full_name(self):
		# The user is identified by their email address
        return self.email
    def get_short_name(self):
		# The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
	
    @property
    def is_staff(self):
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return True

	
	
"""        
class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_superuser,last_login,**extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                  
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

       
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=40, unique=True, verbose_name=u'用户名')
    email = models.EmailField(max_length=255, unique=True, verbose_name=u'邮箱')
    mobile = models.CharField((u'手机'), max_length=30, blank=False,
                              validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                    ('Enter a valid mobile number.'),
                                                                    'invalid')])
    fullname = models.CharField(max_length=64, null=True, verbose_name=u'中文姓名')
    is_active = models.BooleanField(default=False, verbose_name=u'状态')
    is_superuser = models.BooleanField(default=False, verbose_name=u'超级管理员')
    last_login = models.DateTimeField(default=timezone.now, verbose_name='最近登录时间')
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
        permissions = (
            ("get_user", ("查看用户")),
            ("add_user", ("添加用户")),
            ("edit_user", ("编辑用户")),
            ("del_user", ("删除用户")),
        )
        default_permissions = () 

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self): 

        if self.fullname:
            field = self.fullname
        else:
            field = self.username

        return field



    def get_short_name(self):
        "Returns the short name for the user."
        return self.username

    # def has_perm(self, perm, obj=None):
    #     if self.is_active and self.is_superuser:
    #         return True

"""