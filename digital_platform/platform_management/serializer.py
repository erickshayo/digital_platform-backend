from rest_framework import serializers
from .models import *


class AddressGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        depth = 1


class AddressPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "name",
            "postalCode",
            "admin"
        ]

class AddressUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUser
        fields = "__all__"
        depth = 2


class AddressUserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUser
        fields = [
            "userId",
            "address",
        ]

class AnnouncementGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"
        depth = 2


class AnnouncementPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            "name",
            "postalCode",
            "address",
            "time",
            "date",
            "announcement"
        ]



class ForumGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = "__all__"
        depth = 2


class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = [
            "name",
            "userId",
            "address",
            "problem",
        ]  

class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "userId",
            "forum",
            "comment",
        ]

class LostAndFoundGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        fields = "__all__"
        depth = 2


class LostAndFoundPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        depth = 2
        fields = [
            "name",
            "userId",
            "address",
            "type",
            "picture",
            "desc"
        ] 