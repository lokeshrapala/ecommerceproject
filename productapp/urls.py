from django.conf.urls import url
from . import views
app_name = 'productapp'
urlpatterns = [
    url(r'^search$', views.search, name='search'),
    ]
