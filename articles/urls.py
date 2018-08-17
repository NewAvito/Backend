from django.urls import path, include
from articles.views import *

urlpatterns = [
    path('api/', ArticlesView.as_view()),
    path('cat/', get_category)
]
