from rest_framework import serializers

from apps.users.serializers import ReadUserSerializer
from .models import Seller

class ReadSellerSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer(read_only=True)
    class Meta:
        model = Seller
        fields = [
            'id',
            'user',
            'store_name',
            'description',
            'profile_image',
            'cover_image',
            'address'
        ]