from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


from .serializer import *
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from BeemAfrica import Authorize, SMS
from rest_framework import status

# def pushMessage(otp, phone):
#     Authorize('478040a68e5f755d',
#               'ZTVkMzUwYWI5NjMwYjM2Zjc0ZTY1ZGQ5ZmQzZWNjNTMwYzRkOTEyYWRlODdhNWIxYmExYmQxOGZkMGNiODdiYg==')
#     request = SMS.send_sms(
#         'OTP for grocery app ' + otp,
#         phone,
#         sender_id='MC-Official'
#     )
#     return request

class AddressView(APIView):
    permission_classes = [AllowAny]
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
            addressId = request.GET.get("userId")
            queryset = Address.objects.get(admin=addressId)
            print(queryset)
            serialized = AddressGetSerializer(instance=queryset, many=False)
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
            queryset = AddressUser.objects.filter(address=addressId)
            print(queryset)
            serialized = AddressUserGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "userAddress":
            userId = request.GET.get("userId")
            queryset = AddressUser.objects.filter(userId=userId)
            serialized = AddressUserGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


def pushMessage(message, phone):
    Authorize('4ae92810061ef88a',
                'YjIzMmQ5ZmYwMGU0NjNmYmQ3Y2FiMmE1YzM0ZGYxZTNmNzkyNTMyNTE2ZDYwYWI2ODJkMmRjNmE1MjE0YzYzZg==')
    request = SMS.send_sms(
        message,
        phone,
        sender_id='JamiiConect'
    )
    return request

class AnnouncementView(APIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        data = request.data
        serialized = AnnouncementPostSerializer(data=data)
        if serialized.is_valid():
            print(data)
            try:
                queryset = AddressUser.objects.filter(address=data['address'])
                print('-----------------------------------------')
                print(queryset)
                
                for user in queryset:
                    print(user.userId.phone_number)
                    message = f"JamiiConnect {user.address.name} Announcement \n {data['name']} \n {data['announcement']} \n {data['date']} {data['time']}"

                    pushMessage(message, user.userId.phone_number)

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
    permission_classes = [AllowAny]
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
        elif queryType == "single_address":
            forumId = request.GET.get("addressId")
            queryset = Forum.objects.filter(address=forumId)
            serialized = ForumGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif queryType == "UserForums":
            userId = request.GET.get("userId")
            queryset = Forum.objects.filter(userId=userId)
            serialized = ForumGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})
        
    def delete(self, request, pk):
        try:
            forum = Forum.objects.get(id=pk)
            forum.delete()
            return Response({"message": "Forum deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Forum.DoesNotExist:
            return Response({"message": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            forum = Forum.objects.get(id=pk)
            forum.isActive = False  # Deactivate forum
            forum.save()
            return Response({"message": "Forum deactivated successfully"})
        except Forum.DoesNotExist:
            return Response({"message": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)

        

class CommentView(APIView):
    permission_classes = [AllowAny]
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
        

class LostAndFoundListCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        print(data)
        
        try:
            # Retrieve the related User and Address instances
            user = User.objects.get(id=data.get('userId'))
            address = Address.objects.get(id=data.get('address'))

            # Create the LostAndFound instance
            lost_and_found = LostAndFound(
                name=data.get('name'),
                type=data.get('type'),
                desc=data.get('desc'),
                userId=user,
                address=address,
                picture=data.get('picture') if data.get('picture') != 'null' else None,
                isActive=True
            )
            lost_and_found.save()

            return Response({"save": True})
        except Exception as e:
            print(e)
            return Response({"save": False, "error": str(e)})

    def get(self, request):
        queryset = LostAndFound.objects.all()
        serialized = LostAndFoundPostSerializer(queryset, many=True)
        return Response(serialized.data)


class StatisticsView(APIView):
    def get(self, request):
        # Calculate totals
        address_count = Address.objects.count()
        address_user_count = AddressUser.objects.count()
        announcement_count = Announcement.objects.count()
        forum_count = Forum.objects.count()
        comment_count = Comment.objects.count()
        lost_and_found_count = LostAndFound.objects.count()

        # Create response data
        data = {
            'total_addresses': address_count,
            'total_address_users': address_user_count,
            'total_announcements': announcement_count,
            'total_forums': forum_count,
            'total_comments': comment_count,
            'total_lost_and_found': lost_and_found_count,
        }

        return Response(data)