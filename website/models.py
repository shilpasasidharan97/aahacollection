from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import qrcode
from io import BytesIO
from django.core.files import File
import random

from PIL import Image, ImageDraw

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,phone,password=None,**extra_fields):

        if not phone:
            raise ValueError('User must have a phone')
        user = self.model(phone=phone,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if user:
            return user
    def create_superuser(self,phone,password=None,**extra_fields):

        if not phone:
            raise ValueError('User must have a phone')
        user = self.model(phone=phone,**extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff   = True
        user.save(using=self._db)
        return user


class Shop(models.Model):
    shop_name = models.CharField(max_length=350,null=True)
    email=models.EmailField(unique=True)
    phone = models.CharField(max_length=20,unique=True)
    place = models.CharField(max_length=200,null=True)
    district = models.CharField(max_length=150,null=True)
    state = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=300,null=True)
    password = models.CharField(max_length=200,null=True)
    logo = models.FileField(upload_to='resto_logo', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = ("Restaurant")

    def __str__(self):
        return str(self.shop_name)


class User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=20,unique=True)
    shop = models.ForeignKey(Shop , on_delete=models.CASCADE,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD='phone'


class ShopQrcode(models.Model):
    shop = models.OneToOneField(Shop,on_delete=models.CASCADE,null=True)
    resto_url = models.CharField(max_length=200,null=True)
    image = models.ImageField(upload_to='qrcode',blank=True)
    

    def save(self,*args,**kwargs):
      qrcode_img=qrcode.make(self.resto_url)
      canvas=Image.new("RGB", (380,380),"white")
    #   draw=ImageDraw.Draw(canvas)
      canvas.paste(qrcode_img)
      buffer=BytesIO()
      canvas.save(buffer,"PNG")
      self.image.save(f'image{random.randint(0,9999)}',File(buffer),save=False)
      canvas.close()
      super().save(*args,**kwargs)

    class Meta:
        verbose_name_plural = ("Restaurant Qrcode")

    def __str__(self):
        return str(self.shop)


class ShopSocialMediaLinks(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    facebook = models.CharField(max_length=20000, null=True, blank=True)
    whatsapp = models.CharField(max_length=20000, null=True, blank=True)
    instagram = models.CharField(max_length=20000, null=True, blank=True)
    location = models.CharField(max_length=20000, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name_plural = ("Shop Links")