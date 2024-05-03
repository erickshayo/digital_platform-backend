from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


from .serializer import *
from rest_framework.views import APIView


class AddressView(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def post(request):
        data = request.data
        serialized = AddressPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        queryType = request.GET.get("queryType")
        if queryType == "all":
            queryset = Address.objects.all()
            print(queryset)
            serialized = AddressGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "single":
            addressId = request.GET.get("addressId")
            queryset = Address.objects.filter(id=addressId)
            serialized = AddressGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "addressUsers":
            addressId = request.GET.get("addressId")
            queryset = AddressUser.objects.filter(address=addressId)
            serialized = AddressUserGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class AddressUserView(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        data = request.data
        serialized = AddressUserPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        queryType = request.GET.get("queryType")
        if queryType == "all":
            queryset = AddressUser.objects.all()
            serialized = AddressUserGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "single":
            addressId = request.GET.get("addressId")
            queryset = AddressUser.objects.filter(id=addressId)
            serialized = AddressUserGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "userAddress":
            userId = request.GET.get("userId")
            queryset = AddressUser.objects.filter(userId=userId)
            serialized = AddressUserGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})
        

class AnnouncementView(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        data = request.data
        serialized = AnnouncementPostSerializer(data=data)
        if serialized.is_valid():
            try:
                queryset = AddressUser.objects.filter(address=data['adress'])
                print(queryset)
                ##todo post push message to users
                serialized.save()
                return Response({"save": True})
            except AddressUser.DoesNotExist:
                 return Response({"save": False, "error": "Theres no users on this address"})

        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        queryType = request.GET.get("queryType")
        if queryType == "all":
            queryset = Announcement.objects.all()
            serialized = AnnouncementGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "single":
            announcementId = request.GET.get("announcementId")
            queryset = Announcement.objects.filter(id=announcementId)
            serialized = AnnouncementGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "addressAnnouncement":
            addressId = request.GET.get("addressId")
            queryset = Announcement.objects.filter(address=addressId)
            serialized = AnnouncementGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})
        
class ForumView(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def post(request):
        data = request.data
        serialized = ForumPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):

        queryType = request.GET.get("queryType")
        if queryType == "all":
            queryset = Forum.objects.all()
            serialized = ForumGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "single":
            forumId = request.GET.get("forumId")
            queryset = Forum.objects.filter(id=forumId)
            serialized = ForumGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "UserForums":
            userId = request.GET.get("userId")
            queryset = Forum.objects.filter(userId=userId)
            serialized = ForumGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})
        

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    @staticmethod
    def post(request):
        data = request.data
        serialized = CommentPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        queryType = request.GET.get("queryType")
        if queryType == "all":
            queryset = Comment.objects.all()
            serialized = CommentGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "single":
            commentId = request.GET.get("commentId")
            queryset = Comment.objects.filter(id=commentId)
            serialized = CommentGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "forumComment":
            forumId = request.GET.get("forumId")
            queryset = Comment.objects.filter(forum=forumId)
            serialized = CommentGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})