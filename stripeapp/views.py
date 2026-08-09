from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import stripe
from .models import UserProfile
from .serializers import UserProfileSerializer,SignupSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny

stripe.api_key = "sk_test_51QcILGA..."

class YourSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # creates the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class CreateCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        YOUR_DOMAIN = "http://localhost:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1RFBUmApvPzNPgSPYHv02KU9',
                'quantity': 1,
            }],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/api/payment/success/',
            cancel_url=YOUR_DOMAIN + '/api/payment/cancel/',
        )
        return Response({'checkout_url': checkout_session.url})

class PaymentSuccess(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        profile.is_subscribed = True
        profile.save()
        return Response({'message': 'Payment Success & User Subscribed!'})

class PaymentCancel(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Payment Cancelled.'})
