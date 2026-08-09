from django.urls import path
from .views import GetUserProfile, CreateCheckoutSession, PaymentSuccess, PaymentCancel, YourSignupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/signup/', YourSignupView.as_view(), name='signup'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('user_profile/get_user_profile/', GetUserProfile.as_view()),
    path('payment/create_checkout/', CreateCheckoutSession.as_view()),
    path('payment/success/', PaymentSuccess.as_view()),
    path('payment/cancel/', PaymentCancel.as_view()),
]
