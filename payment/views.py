from django.shortcuts import render
# Create your views here.
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
import stripe 
from jobs.models import *
from django.http import HttpResponse, JsonResponse
from .models import Transaction

class HomePageView(TemplateView):
    template_name = 'payment/home.html'


# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
@csrf_exempt
def create_checkout_session(request, pk):
    """
    Note : We can receive the amount and currency in pk , that way we do not 
    need to hit db 
    """
    
    amount = int(request.GET.get('amount'))
    contract_detail = Contract.objects.get(id=pk)
    # amount = contract_detail.total 
    currency = contract_detail.currency.lower()
    job = contract_detail.proposal.job.title
    freelancer = contract_detail.proposal.user.username

    # inr unit is paisa in stripe , so amount * 100
    if currency == "rs":
        currency = 'inr'
        amount = amount * 100

    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                
                metadata = {
                            "contract_id":pk,
                            "amount":amount,
                            },
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'unit_amount': amount,
                        'product_data': {
                            'name': job,
                            'description': f'Payment to : {freelancer}',
                            
                        },
                        },
                        'quantity': 1,
                }]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        


class SuccessView(TemplateView):
    template_name = 'payment/success.html'


class CancelledView(TemplateView):
    template_name = 'payment/cancelled.html'

@csrf_exempt
def stripe_webhook(request):
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        meta_data = event.data.object.metadata
        contract_id = meta_data.contract_id
        con_obj = Contract.objects.get(id=contract_id)
        paid_amount = int(meta_data.amount)/100
        remaining = con_obj.remaining - paid_amount
        con_obj.remaining = remaining
        con_obj.save()
        Transaction.objects.create(contract=con_obj, amount = paid_amount )
    return HttpResponse(status=200)


class TransactionView(TemplateView):
    template_name = 'payment/transaction.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        contract_id = kwargs['pk']
        queryset= Transaction.objects
        transaction_obj = ''
        if queryset.filter(contract=contract_id).exists():
            transaction_obj = queryset.filter(contract=contract_id)
            context['trans_obj'] = transaction_obj
        return context