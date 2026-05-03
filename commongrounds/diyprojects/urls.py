from django.urls import path
from . import views

app_name = "diyprojects"

urlpatterns = [
    path('diyprojects/projects/', views.ProjectListView.as_view(), name='project_list'),
    path('diyprojects/project/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('diyprojects/project/add/', views.ProjectCreateView.as_view(), name='project_create'),
    path('diyprojects/project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('diyprojects/projects/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('diyprojects/projects/<int:pk>/review/', views.add_review, name='add_review'),
    path('diyprojects/projects/<int:pk>/rate/', views.rate_project, name='rate_project'),
]