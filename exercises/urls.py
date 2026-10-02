from django.urls import path

from . import views

app_name = 'exercises'

urlpatterns = [
    path('', views.home, name='home'),
    path('manual/', views.manual_exercise_create, name='manual_exercise_create'),
    path('ai/', views.ai_exercise_create, name='ai_exercise_create'),
    path('ai/correct/', views.ai_exercise_correct, name='ai_exercise_correct'),
    path("exercise/save/", views.save_corrected_exercise, name="save_corrected_exercise"),
    path("history/", views.exercise_history, name="exercise_history"),
    path("history/<int:exercise_id>/", views.exercise_history_detail, name="exercise_history_detail"),
    path("history/<int:exercise_id>/title/", views.edit_exercise_title, name="edit_exercise_title"),
    path("history/<int:exercise_id>/delete/", views.delete_exercise, name="delete_exercise")
]