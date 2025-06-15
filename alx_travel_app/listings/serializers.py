from rest_framework import serializers
from .models import Property, Booking


class ListingSerializer(serializers.ModelSerializer):
    host_username = serializers.CharField(source='host.username', read_only=True)

    class Meta:
        model = Property
        fields = [
            'property_id',
            'name',
            'description',
            'location',
            'price_per_night',
            'created_at',
            'updated_at',
            'host',
            'host_username',
        ]
        read_only_fields = ['property_id', 'created_at', 'updated_at', 'host_username']


class BookingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    property_name = serializers.CharField(source='property.name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'property',
            'property_name',
            'user',
            'user_username',
            'start_date',
            'end_date',
            'total_price',
            'status',
            'created_at',
        ]
        read_only_fields = ['booking_id', 'created_at', 'user_username', 'property_name']
