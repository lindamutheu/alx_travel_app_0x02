#!/usr/bin/env python3
"""Views for the listings app"""

# week 6
import requests
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import (
    send_payment_confirmation_email,  # ✅ Existing Celery task
    send_booking_confirmation_email   # ✅ New Celery task
)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        """
        Override perform_create to trigger email notification asynchronously
        """
        booking = serializer.save(user=self.request.user)
        # ✅ Send booking confirmation email via Celery
        send_booking_confirmation_email.delay(
            user_email=self.request.user.email,
            booking_id=booking.id
        )


@api_view(['POST'])
def initiate_payment(request):
    """
    Initialize payment with Chapa API and create Payment record
    """
    data = request.data
    tx_ref = f"ref_{data['booking_id']}"
    payload = {
        "amount": data['amount'],
        "currency": "KES",
        "email": data['email'],
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "tx_ref": tx_ref,
        "callback_url": "https://yourdomain.com/api/verify-payment/",
        "return_url": "https://yourfrontend.com/payment-success",
        "customization": {
            "title": "Room Booking",
            "description": "Payment for room booking"
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.post('https://api.chapa.co/v1/transaction/initialize', json=payload, headers=headers)
    res_data = response.json()

    if response.status_code == 200 and res_data.get('status') == 'success':
        booking = Booking.objects.get(booking_id=data['booking_id'])
        Payment.objects.create(
            booking=booking,
            amount=data['amount'],
            chapa_tx_ref=tx_ref,
            status='pending'
        )
        return Response({"checkout_url": res_data['data']['checkout_url']})
    else:
        return Response({"error": "Failed to initiate payment"}, status=400)


@api_view(['GET'])
def verify_payment(request):
    """
    Verify payment status with Chapa API and update Payment record
    """
    tx_ref = request.query_params.get('tx_ref')
    url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data.get('status') == 'success':
        try:
            payment = Payment.objects.get(chapa_tx_ref=tx_ref)
            payment.status = 'completed' if res_data['data']['status'] == 'success' else 'failed'
            payment.chapa_transaction_id = res_data['data']['id']
            payment.save()

            # ✅ Send confirmation email if payment succeeded
            if payment.status == 'completed':
                send_payment_confirmation_email.delay(
                    email=payment.booking.user.email,
                    booking_reference=str(payment.booking.booking_id)
                )

            return Response({"message": "Payment verified successfully", "status": payment.status})
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=404)

    return Response({"error": "Verification failed"}, status=400)


def home(request):
    """
    Simple home endpoint
    """
    return JsonResponse({"message": "Welcome to ALX Travel App API"})
