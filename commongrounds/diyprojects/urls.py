from django.urls import path
from . import views

app_name = "diyprojects"

urlpatterns = [
    path('diyprojects/projects/', views.ProjectListView.as_view(), name='project_list'),
    path('diyprojects/project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),

]