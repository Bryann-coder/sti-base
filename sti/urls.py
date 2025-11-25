from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Route pour l'API du module user
    path('api/user/', include('user.urls')),
    # Route pour l'API du module learner
    path('api/learner/', include('learner.urls')),
    # Route pour l'API du module tuteur
    path('api/tutor/', include('tutor.urls')),
    # Route pour obtenir un token d'authentification
    path('api-token-auth/', views.obtain_auth_token) 
]