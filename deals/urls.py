from django.contrib import admin
from django.urls import path, include
from deals.views import *

app_name = 'deals'
urlpatterns = [
    path('upload/', DealsUploadView.as_view()),
    path('result/', ResultResponseView.as_view()),
]
