from django.urls import path
from .views import ChatView, ProgressionView, SessionView

app_name = 'tutor'

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('progression/', ProgressionView.as_view(), name='progression'),
    path('session/', SessionView.as_view(), name='session'),
    path('session/<str:session_id>/', SessionView.as_view(), name='session_detail'),
]