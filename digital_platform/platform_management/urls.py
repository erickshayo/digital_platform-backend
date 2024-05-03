from django.urls import path
from .views import *

app_name = 'platform_management'

urlpatterns = [
    path('address', AddressView.as_view()),
    path('address_user', AddressUserView.as_view()),
    path('announcement', AnnouncementView.as_view()),
    path('forum', ForumView.as_view()),
    path('comment', CommentView.as_view()),
    # path('lost_found', GetUserInformationByNida.as_view()),
]