#!/usr/bin/env python3
"""URL configuration for the listings app"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ListingViewSet,
    BookingViewSet,
    initiate_payment,
    verify_payment,
    property_list,  # ✅ Import property_list view
    home  # Optional: keep home route
)

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', home, name='home'),  # Optional root route
    path('', include(router.urls)),
    path('properties/', property_list, name='property_list'),  # ✅ Added properties endpoint
    path('initiate-payment/', initiate_payment, name='initiate_payment'),
    path('verify-payment/', verify_payment, name='verify_payment'),
]
