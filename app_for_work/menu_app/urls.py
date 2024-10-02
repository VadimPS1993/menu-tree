from django.urls import path
from .views import index_view, about_view, services_view, consulting_view

urlpatterns = [
    path('', index_view, name='index'),
    path('about/', about_view, name='about'),
    path('services/', services_view, name='services'),
    path('services/consulting/', consulting_view, name='consulting'),
]
