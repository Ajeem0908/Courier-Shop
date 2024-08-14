  
# urlpatterns = [
#      path('', views.home, name='home'),
#      path('couriers/',views.courier_list, name = 'my_app'),
#      path('deliveries/', 'views.delivery_list', name='delivery_list')
#  ]

from django.urls import path
from .views import (
    post_courier_shops, get_courier_shops, update_courier_shops,
    get_courier_shops_details, delete_courier_shop, create_customer,
    get_customer, get_customer_details, update_customer, delete_customer,
    list_customers, list_customers_by_billing_address, get_deliveries,
    get_delivery, update_delivery, create_delivery, delete_delivery,
    DeliveriesByStatusView, CustomTokenObtainPairView,TokenRefreshViewCustom,UserRegistrationView,ProtectedResourceView, UserProfileView,TokenValidationView,UserListView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView






urlpatterns = [
    path('api/create/', post_courier_shops, name='create_courier_shop'),
    path('api/get/', get_courier_shops, name='get_courier_shops'),
    path('api/get_details/<int:id>/', get_courier_shops_details, name='get_courier_shops_details'),
    path('api/update/<int:pk>/', update_courier_shops, name='update_courier_shop'),
    path('api/delete/<int:pk>/', delete_courier_shop, name='delete_courier_shop'),
    path('api/create_customer/', create_customer, name='create_customer'),
    path('api/get_customer/', get_customer, name='get_customer'),
    path('api/get_customer/details/<int:pk>/', get_customer_details, name='get_customer_details'),
    path('api/update_customer/<int:pk>/', update_customer, name='update_customer'),
    path('api/delete_customer/<int:pk>/', delete_customer, name='delete_customer'),
    path('api/list_customers_by_customer_name/<str:customer_name>/', list_customers, name='list_customers_by_customer_name'),
    path('api/list_customers_by_billing_address/<str:Billing_address>/', list_customers_by_billing_address, name='list_customers_by_billing_address'),
    path('deliveries/', get_deliveries, name='get_deliveries'),
    path('deliveries/<int:pk>/', get_delivery, name='get_delivery'),
    path('deliveries/create/', create_delivery, name='create_delivery'),
    path('deliveries/update/<int:pk>/', update_delivery, name='update_delivery'),
    path('deliveries/delete/<int:pk>/', delete_delivery, name='delete_delivery'),
    path('deliveries/status/', DeliveriesByStatusView.as_view(), name='deliveries_by_status'),
    # path('login/', login, name='login'),
    # path('refresh-token/', refresh_token, name='refresh-token'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/protected/', ProtectedResourceView.as_view(), name='protected_resource'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/token/validate/', TokenValidationView.as_view(), name='token_validate'),
    path('users/', UserListView.as_view(), name='user-list')

   

    

]










         







       

       













# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CourierShopsViewSet

# router = DefaultRouter()
# router.register(r'couriershops', CourierShopsViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
