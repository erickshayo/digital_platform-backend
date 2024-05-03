from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Address, AddressUser, Announcement, Forum, Comment, LostAndFound])