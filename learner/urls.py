from django.urls import path
from .views import TutorInteractionView, RegisterView, LoginView, LogoutView # <-- import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), # <-- Nouvelle route
    path('interact/', TutorInteractionView.as_view(), name='tutor-interaction'),
]