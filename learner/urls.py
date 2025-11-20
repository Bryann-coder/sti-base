from django.urls import path
from .views import TutorInteractionView

urlpatterns = [
    path('interact/', TutorInteractionView.as_view(), name='tutor-interaction'),
]