from rest_framework import serializers
from django.utils import timezone
from .models import CourierShops
from .models import Customer
from .models import Delivery

class CourierShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierShops
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer                
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            'id',
            'courier_shop',
            'customer_name',
            'delivery_address',
            'pincode',
            'mobile_number',
            'delivery_date',
            'status',
            'tracking_number'
        ]

    def validate_delivery_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Delivery date cannot be in the past.")
        return value


from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  





