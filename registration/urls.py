from django.conf.urls import url
from . import views
from django.urls import path
app_name = 'registration'
urlpatterns = [
    path('reg', views.reg,name='reg'),
    path('otpvalidation',views.otpvalidation),
    path('login/',views.login),
    path('my_logout/',views.my_logout),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^addcart/', views.addcart, name='addcart'),
    url(r'^insertcart/', views.insertcart, name='insertcart'),
    url(r'^viewcart', views.viewcart, name='viewcart'),
    url(r'^deletecart/', views.deletecart, name='deletecart'),
    url(r'^modifycart/', views.modifycart, name='modifycart'),
    url(r'^modifiedcart/', views.modifiedcart, name='modifiedcart'),
    url(r'^track/$', views.track, name='track'),
    url(r'^cancel/$',views.cancel, name='cancel'),
]