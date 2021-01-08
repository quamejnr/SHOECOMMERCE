from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
import json
from django.contrib import messages
from django.shortcuts import redirect
from shop.forms import ShippingAddressForm
import stripe
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY


class StoreListView(ListView):
    model = Product
    template_name = 'shop/store.html'

    def get_context_data(self, **kwargs):
        # Adding cart items to the context
        context = super().get_context_data(**kwargs)

        try:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cart_items = order.cart_items()
        except AttributeError:
            cart_items = 0
        context['cart_items'] = cart_items

        return context


class ProductView(DetailView):
    model = Product
    template_name = 'shop/product.html'


class CartView(ListView):
    model = OrderItem
    template_name = 'shop/cart.html'

    def get_queryset(self):
        try:
            # Returning items in cart of a registered customer
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cart_items = order.orderitem_set.all()
            return cart_items
        except AttributeError:
            # Assigning cart items to an empty list if customer is not logged in.
            cart_items = []
            return cart_items

    def get_context_data(self, **kwargs):
        # Adding order to the context
        try:
            context = super().get_context_data(**kwargs)
            customer = self.request.user.customer
            order = get_object_or_404(Order, customer=customer)
            context['order'] = order
            return context

        except AttributeError:
            # Data displayed when the user is not a registered customer.
            order = {
                'cart_items': 0,
                'cart_total': 0,
            }

            context['order'] = order
            return context


class CheckoutView(View, LoginRequiredMixin):

    def get(self, *args, **kwargs):
        form = ShippingAddressForm()

        # Checks if user is logged in
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            # Gets customer's order with items or creates one if none available
            order, created = Order.objects.get_or_create(customer=customer)
            items = order.orderitem_set.all()
            cart_items = order.cart_items()

        else:
            items = []

            order = {
                'cart_items': 0,
                'cart_total': 0,
            }
            cart_items = order['cart_items']

        context = {
            'items': items,
            'order': order,
            'cart_items': cart_items,
            'form': form,
        }

        return render(self.request, 'shop/checkout.html', context)

    def post(self, *args, **kwargs):
        # Checks if a request is a POST request
        if self.request.method == 'POST':
            # Creates an instance of form with POST request
            form = ShippingAddressForm(self.request.POST)
            print(self.request.POST)
            # Form is validated and saved
            try:
                order = Order.objects.get(customer=self.request.user.customer, complete=False)
                if form.is_valid():
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    city = form.cleaned_data.get('city')
                    country = form.cleaned_data.get('country')
                    # payment_option = form.cleaned_data('payment_option')
                    billing_address = BillingAddress(
                        customer=self.request.user.customer,
                        country=country,
                        street_address=street_address,
                        city=city,
                        apartment_address=apartment_address,
                    )
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()
                    print(form.cleaned_data)
                    # TODO: Add redirect to the selected payment option
                    messages.success(self.request, "Form submitted")
                    return redirect('checkout')
            except ValueError:
                messages.warning(self.request, 'You do not have an active order')
                return redirect('checkout')


class PaymentView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'shop/payment.html')


def update_item(request):
    # Loading and parsing the data received from UpdateItems Function in cart.js
    data = json.loads(request.body)
    product_id = data['productId']
    action = data["action"]

    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    # Gets customer's order with items or creates one if none available
    order, created = Order.objects.get_or_create(customer=customer)
    # Gets or creates an order item with order(if available) or create one
    item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        item.quantity += 1
        messages.info(request, 'Item added to cart')
    elif action == 'remove':
        item.quantity -= 1
        messages.info(request, 'Item removed from cart')

    elif action == 'clear':
        item.quantity = 0

    item.save()

    if item.quantity <= 0:
        item.delete()

    return JsonResponse("Updated cart", safe=False)



