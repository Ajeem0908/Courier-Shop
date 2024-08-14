
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status
from rest_framework import serializers
from .models import CourierShops
from .models import Customer
from .serializers import CourierShopsSerializer,UserListSerializer
from django.core.exceptions import ValidationError


  

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken,TokenError
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer, CharField
from rest_framework.permissions import IsAuthenticated,IsAdminUser



class ProtectedResourceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a protected resource'})


class UserRegistrationSerializer(Serializer):
    username = CharField(max_length=150)
    password = CharField(max_length=128)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("enter")
        username = request.data.get('username')
        password = request.data.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user, "********")
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshViewCustom(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TokenValidationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'detail': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            AccessToken(token)
            return Response({'detail': 'Token is valid.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
    
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
       
class UserListView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)





@api_view(['POST'])
def post_courier_shops(request):
    if not request.data:
        return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

    shopname = request.data.get('shop_name')
    phone_number = request.data.get('phone_number')
    mobile_number = request.data.get('mobile_number')

    if phone_number and mobile_number and phone_number == mobile_number:
        return Response({"error": "Phone number and mobile number cannot be the same."}, status=status.HTTP_400_BAD_REQUEST)

    if shopname and CourierShops.objects.filter(shop_name=shopname).exists():
        return Response({'error': "Shop name must be unique. This shop name already exists."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CourierShopsSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Unique constraint failed'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_courier_shops(request):
    couriers = CourierShops.objects.all()  
    serializer = CourierShopsSerializer(couriers, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_courier_shops_details(request, id):
    try:
        couriers = CourierShops.objects.get(pk=id)
        serializer = CourierShopsSerializer(couriers)
        print(f"Successfully get CourierShop with ID {id}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CourierShops.DoesNotExist:
        return Response({'error': 'CourierShop not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_courier_shops(request, pk):
    try:
        courier_shop = CourierShops.objects.get(pk=pk)
    except CourierShops.DoesNotExist:
        return Response({'error': 'CourierShop not found'}, status=status.HTTP_404_NOT_FOUND)

    phone_number = request.data.get('phone_number')
    mobile_number = request.data.get('mobile_number')
    new_email = request.data.get('email')

    if phone_number == mobile_number:
        return Response({"error": "Phone number and mobile number cannot be the same."}, status=status.HTTP_400_BAD_REQUEST)
    
    if phone_number and CourierShops.objects.filter(phone_number=phone_number).exclude(pk=pk).exists():
        return Response({"error": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    if mobile_number and CourierShops.objects.filter(mobile_number=mobile_number).exclude(pk=pk).exists():
        return Response({"error": "Mobile number already exists."}, status=status.HTTP_400_BAD_REQUEST)
    if new_email and new_email != courier_shop.Email and CourierShops.objects.exclude(pk=pk).filter(Email=new_email).exists():
        return Response({'error': 'This email has already been used for another CourierShop.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CourierShopsSerializer(courier_shop, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print(f"Successfully updated CourierShop with ID {pk}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
def delete_courier_shop(request, pk):
    try:
        courier_shop = CourierShops.objects.get(pk=pk)
    except CourierShops.DoesNotExist:
        return Response({'error': 'Courier shop not found'}, status=status.HTTP_404_NOT_FOUND)

    courier_shop.delete()
    print(f"Successfully deleted CourierShop with ID {pk}")
    return Response({'message': f'Courier shop with ID {pk} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from .models import Customer
from .serializers import CustomerSerializer
# from .filters import CustomerFilter




@api_view(['POST'])
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_customer(request):
    try:
        customers = Customer.objects.all()
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomerSerializer(customers, many=True) 
    return Response(serializer.data)

@api_view(['GET'])
def get_customer_details(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(customer, many=False)
        print(f"Successfully retrieved customer with ID {pk}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        print(f"No data found for customer with ID {pk}")
        return Response({'detail': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    customer.delete()
    print(f"Customer with ID {pk} successfully deleted.")
    return Response({'message': f'Courier shop with ID {pk} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class CustomerFilter(filters.FilterSet):
    Billing_address = filters.CharFilter(lookup_expr='icontains')  

    class Meta:
        model = Customer
        fields = [ 'Billing_address', 'customer_name']  

@api_view(['GET'])
def list_customers(request,customer_name=None):    
    queryset = Customer.objects.all()

    if customer_name:
        queryset = queryset.filter(customer_name__icontains=customer_name)
   
    filterset = CustomerFilter(request.GET, queryset=queryset)
    if filterset.is_valid():
        queryset = filterset.qs

    if not queryset.exists():
      if customer_name and not Customer.objects.filter(customer_name__icontains=customer_name).exists():
        return Response({"message": "No customers found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomerSerializer(queryset, many=True)
    return Response(serializer.data)


        
@api_view(['GET'])
def list_customers_by_billing_address(request, Billing_address=None):
    queryset = Customer.objects.all()
    if Billing_address:
        queryset = queryset.filter(Billing_address__icontains=Billing_address)
    
    filterset = CustomerFilter(request.GET, queryset=queryset)
    if filterset.is_valid():
        queryset = filterset.qs

    if not queryset.exists():
        if Billing_address and not Customer.objects.filter(Billing_address__icontains=Billing_address).exists():
            return Response({"message": "Billing address not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "No customers found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(queryset, many=True)
    return Response(serializer.data)
    
    

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Delivery
from .serializers import DeliverySerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

# class DeliveryViewSet(viewsets.ModelViewSet):
#     queryset = Delivery.objects.all()
#     serializer_class = DeliverySerializer
#     permission_classes = [IsAuthenticated]


@api_view(['GET'])
def get_deliveries(request):
    deliveries = Delivery.objects.all()
    serializer = DeliverySerializer(deliveries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_delivery(request, pk):
    try:
        delivery = Delivery.objects.get(pk=pk)
    except Delivery.DoesNotExist:
        return Response({'error': 'Delivery not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DeliverySerializer(delivery)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_delivery(request):
    serializer = DeliverySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_delivery(request, pk):
    try:
        delivery = Delivery.objects.get(pk=pk)
    except Delivery.DoesNotExist:
        return Response({'error': 'Delivery not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DeliverySerializer(delivery, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_delivery(request, pk):
    try:
        delivery = Delivery.objects.get(pk=pk)
    except Delivery.DoesNotExist:
        return Response({'error': 'Delivery not found'}, status=status.HTTP_404_NOT_FOUND)
    
    delivery.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class DeliveriesByStatusView(generics.ListAPIView):
    serializer_class = DeliverySerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status:
            return Delivery.objects.filter(status=status)
        return Delivery.objects.all()

















# from rest_framework.views import APIView
# from rest_framework.response import Response

# from .models import Delivery

# from .serializers import DeliverySerializer



# class DeliveryListView(APIView):
#     def get(self, request):

#         deliveries = Delivery.objects.all()
#         serializer = DeliverySerializer(deliveries, many=True)
#         return Response(serializer.data)

#     def post(self, request):
       
#         serializer = DeliverySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


# @api_view(['GET'])
# def customer_detail(request, pk):
#     try:
#         customer = Customer.objects.get(pk=pk)
#     except Customer.DoesNotExist:
#         return Response(status=404)
#     serializer = CustomerSerializer(customer)
#     return Response(serializer.data)









# class CourierShopsViewSet(viewsets.ModelViewSet):
#     queryset = CourierShops.objects.all()
#     serializer_class = CourierShopsSerializer

    # def post(self, request):

# def delivery_list(request):
#     deliveries = delivery.objects.all()
#     return render(request, 'delivery_list.html', {'deliveries': deliveries})
    