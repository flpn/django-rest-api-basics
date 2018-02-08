from django.urls import path

from . import views


app_name = 'postings'

urlpatterns = [
    path('', views.BlogPostAPIView.as_view(), name='post-list-create'),
    path('<int:pk>/', views.BlogPostRudAPIView.as_view(), name='post-rud'),
]