from django.urls import path
from . import views

urlpatterns = [
    path('', views.communications_dashboard, name='communications-dashboard'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement-create'),
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message-create'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('sent/', views.SentView.as_view(), name='sent'),
    path('notifications/', views.notification_list, name='notification-list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='notification-read'),
    path('api/notifications/', views.get_notifications, name='api-notifications'),
]