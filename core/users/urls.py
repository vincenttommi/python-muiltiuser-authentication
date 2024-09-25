from django.urls import path
from .views import (
    ClientOnlyView, 
    CustomAuthToken, 
    FreelancerOnlyView, 
    FreelancerSignUpView, 
    ClientSignUpView, 
    LogoutView
)

urlpatterns = [
    path('freelancer/signup/', FreelancerSignUpView.as_view(), name='freelancer_signup'),
    path('client/signup/', ClientSignUpView.as_view(), name='client_signup'),
    path('login/', CustomAuthToken.as_view(), name='auth_token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('freelancer-view/', FreelancerOnlyView.as_view(), name='freelancer_only_view'),
    path('clients-view/', ClientOnlyView.as_view(), name='client_only_view'),
]
