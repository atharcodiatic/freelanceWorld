from django.urls import path
from . import views


from django.urls import path

from . import views
name = 'payment'
urlpatterns = [
    path('payment/', views.HomePageView.as_view(), name='home'),
    path('config/', views.stripe_config),  # new
    path('create-checkout-session/<int:pk>', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()), # new
    path('cancelled/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
]

