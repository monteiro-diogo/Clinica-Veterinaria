from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # Donos
    path('donos/', views.DonoListView.as_view(), name='dono_list'),
    path('donos/add/', views.DonoCreateView.as_view(), name='dono_create'),
    path('donos/<int:pk>/', views.DonoDetailView.as_view(), name='dono_detail'),
    path('donos/<int:pk>/edit/', views.DonoUpdateView.as_view(), name='dono_edit'),
    path('donos/<int:pk>/delete/', views.DonoDeleteView.as_view(), name='dono_delete'),
    
    # Animais
    path('animais/', views.AnimalListView.as_view(), name='animal_list'),
    path('animais/add/', views.AnimalCreateView.as_view(), name='animal_create'),
    path('animais/<int:pk>/', views.AnimalDetailView.as_view(), name='animal_detail'),
    path('animais/<int:pk>/edit/', views.AnimalUpdateView.as_view(), name='animal_edit'),
    path('animais/<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal_delete'),

    # Consultas
    path('consultas/', views.ConsultaListView.as_view(), name='consulta_list'),
    path('consultas/add/', views.ConsultaCreateView.as_view(), name='consulta_create'),
    path('consultas/<int:pk>/', views.ConsultaDetailView.as_view(), name='consulta_detail'),

    # Login, Logout e Registo
    path('registo/', views.DonoCreateView.as_view(), name='registo'),
    path('login/', views.login_view, name='login'), # Ajustado para views.login_view
    path('logout/', views.logout_view, name='logout'),
    path('meu-perfil/', views.dono_view, name='perfil'),
]