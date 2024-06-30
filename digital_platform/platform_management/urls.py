from django.urls import path
from .views import *

app_name = 'platform_management'

urlpatterns = [
    path('address', AddressView.as_view()),
    path('address_user', AddressUserView.as_view()),
    path('announcement', AnnouncementView.as_view()),
    path('forum', ForumView.as_view()),
    path('forums/<uuid:pk>/', ForumView.as_view(), name='forum-detail'),
    path('forums/<uuid:pk>/deactivate/', ForumView.as_view(), name='forum-deactivate'),
    path('comment', CommentView.as_view()),
    path('lost_found', LostAndFoundListCreate.as_view()),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]