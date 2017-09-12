from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.summary),
    url(r'^summary/', views.summary),
    url(r'^detail/', views.detail),
    url(r'^date_summary/',views.date_summary),
]
