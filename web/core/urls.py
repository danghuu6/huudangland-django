from django.urls import path
from .views import HomeView
from .views import DetailView, LoginView, RegisterCustomer, predictProduct, logoutUser, delFeedback, managePage, createData, delProduct, updateData


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('detail/<int:product_id>/', DetailView.as_view(), name='detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterCustomer.as_view(), name='register'),
    path('logout/', logoutUser, name='logout'),
    path('del/', delFeedback, name='delcmt'),
    path('product-predict/', predictProduct.as_view(), name='predict-product'),
    path('manage-page/', managePage.as_view(), name='manage-page'),
    path('create/', createData.as_view(), name='create-data'),
    path('update/<int:product_id>/', updateData.as_view(), name='update-data'),
    path('del-product/', delProduct, name='delproduct'),
]

