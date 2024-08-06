from django.urls import path
from .views import *

app_name = 'platform_management'

urlpatterns = [
    path('address', AddressView.as_view()),
    path('address/<uuid:pk>/', AddressView.as_view(), name='address-detail'),
    path('address_user', AddressUserView.as_view()),
    path('announcement', AnnouncementView.as_view()),
    path('announcement/<uuid:pk>/', AnnouncementView.as_view(), name='announcement-detail'),
    path('forum', ForumView.as_view()),
    path('forum/<uuid:pk>/', ForumView.as_view(), name='forum-detail'),
    path('forum/<uuid:pk>/deactivate/', ForumView.as_view(), name='forum-deactivate'),
    path('comment', CommentView.as_view()),
    path('comment/<uuid:pk>/', CommentView.as_view(), name='comment-detail'),
    path('lost_found', LostAndFoundListCreate.as_view()),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]