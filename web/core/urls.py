from django.urls import path
from .views import HomeView
from .views import DetailView, LoginView, RegisterCustomer


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('detail/<int:product_id>/', DetailView.as_view(), name='detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterCustomer.as_view(), name='register'),
    path('success/', LoginView.as_view(), name='success'),
]