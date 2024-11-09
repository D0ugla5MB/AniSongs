from django.urls import path
from . import views

app_name = "search_engine"
urlpatterns = [
    path("", views.search_song, name="main-view"),
    path('anisong/', views.anisong_searchBar, name='anisong'),
    path('feedback/', views.submit_feedback, name='songData_feedback')
]