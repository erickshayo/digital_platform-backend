from django.db.models import QuerySet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRoleSerializer, UserSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .tokens import get_user_token
from .models import User
from rest_framework.generics import UpdateAPIView
from nida import load_user

# BASE_URL = "https://ors.brela.go.tz/um/load/load_nida/{}"

# header = {
#             "Content-Type": "application/json",
#             "Content-Length": "0",
#             "Connection": "keep-alive",
#             "Accept-Encoding": "gzip, deflate, br",
#         }


# def load_user_information(self, national_id: str):
#     try:
#         user_information = requests.post(
#             self.BASE_URL.format(national_id), headers=self.get_headers()
#         ).json()

#         if user_information["obj"].get("result"):
#             user_data = user_information["obj"].get("result")
#             return user_data
#         if user_information["obj"].get("error"):
#             return None
#     except (requests.ConnectionError, requests.ConnectTimeout):
#         raise ConnectionError(
#             "Can't load user information probably connection issues"
#         )


# def load_user(self, national_id: str, json: bool = False):
#     try:
#         user_data = self.load_user_information(national_id)
#         if not json:
#             user_data = self.preprocess_user_data(user_data)
#             return user_data
#         return user_data
#     except Exception as bug:
#         print(bug)
#         return None


class GetUserInformationByNida(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        nin_number = request.GET.get("nida")
        if nin_number:
            user_detail = load_user(national_id=nin_number)
            message = {'save': True, 'user_info':user_detail}
            return Response(message)  
        else:           
            message = {'save': True, message:'provide nida number'}
            return Response(message) 


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        print(request.data)
        serializer = UserSerializer(data=data)
        print(serializer.is_valid())
        if not serializer.is_valid():
            errors = serializer.errors
            return Response({'save': False, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            email = data['email']
            user = User.objects.filter(email=email)
            if user:
                message = {'status': False, 'message': 'username or email already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            userr = serializer.save()
            message = {'save': True}
            return Response(message)

        message = {'save': False, 'errors': serializer.errors}
        return Response(message)
    
    
class UserRoleUpdateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserRoleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {
# "email":"hassan@gm++++++++++++++.com",
# "password":"ha+++++++++++++++++++++3",
# "username":"hassaan",
# "phone_number":"078676726",
# "role":1,
# "gender":"L"
# }


class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        print('Data: ', phone_number, password)
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            user_id = User.objects.get(phone_number=phone_number)
            user_info = UserSerializer(instance=user_id, many=False).data
            response = {
                'token': get_user_token(user_id),
                'user': user_info,
                'success':True,
            }

            return Response(response)
        else:
            response = {
                'msg': 'Invalid phone_number or password',
            }

            return Response(response)

# {
#     "phone_number":"hdhdhdh",
#     "password":"2+++++++++++++++++++++++++++++++5"
# }


class UserInformation(APIView):

    @staticmethod
    def get(request):
        queryType = request.GET.get("queryType")
        role = request.GET.get("role") 
        print(queryType)
        if queryType == 'single':

            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'})
            return Response(UserSerializer(instance=user, many=False).data)

        elif queryType == 'all':
            if role:  # Check if role is provided
                queryset = User.objects.filter(role=role)
            else:
                queryset = User.objects.all()
            return Response(UserSerializer(instance=queryset, many=True).data)

        else:
            return Response({'message': 'Wrong Request!'})


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        username = request.data['username']
        email = request.data['email']
        pharmacyName = request.data['pharmacyName']
        profile = request.data['profile']
        location = request.data['location']
        phone_number = request.data['phone_number']
        if phone_number:
            try:
                query = User.objects.get(phone_number=phone_number)
                query.email = email
                query.pharmacyName = pharmacyName
                query.location = location
                query.username = username
                query.phone_number = phone_number
                query.profile = profile
                query.save()
                return Response({'save': True, "user": UserSerializer(instance=query, many=False).data})
            except User.DoesNotExist:
                return Response({'message': 'You can not change the email'})

        else:

            return Response({'message': 'Not Authorized to Update This User'})
        
