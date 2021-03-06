from django.urls import path, include
from shop.views import StoreListView, ProductView, CheckoutView, CartView, update_item, PaymentView, AddCouponView, RefundView


urlpatterns = [
    path('', StoreListView.as_view(), name='store'),
    path('product/<slug>', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('update_item/', update_item, name='update-item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
    path('coupon/', AddCouponView.as_view(), name='add_coupon'),
    path('refund_request/', RefundView.as_view(), name='refund-request'),

]
