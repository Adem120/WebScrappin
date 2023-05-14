
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
 path('phone', views.Listesm, name='phone'),
  path('', views.Listesm, name='phone'),

path('phone/<str:nom>', views.consultersm, name='phone'),

]