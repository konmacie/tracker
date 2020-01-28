from django.urls import path
from services import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logs/', views.LogsView.as_view(), name='logs'),
    path('service/add/', views.ServiceCreateView.as_view(),
         name='service_add'),
    path('service/<int:pk>/', views.ServiceView.as_view(), name='service'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
