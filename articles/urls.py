from django.urls import path, include
from articles.views import *

urlpatterns = [
    path('article/', ArticlesView.as_view()),
    path('category/', CategoryView.as_view()),
    path('like/', LikeView.as_view()),
    path('image/', FileUploadView.as_view()),
    # path('send/', post_file),
    # path('test/', test.as_view())
]
