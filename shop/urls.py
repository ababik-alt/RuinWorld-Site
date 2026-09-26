from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("buy/<slug:slug>/", views.checkout, name="checkout"),
    path("ruinpay/<int:order_id>/", views.ruinpay, name="ruinpay"),
    path("ruinpay/<int:order_id>/processing/<str:method>/", views.ruinpay_processing, name="ruinpay_processing"),
    path("ruinpay/<int:order_id>/finish/", views.ruinpay_finish, name="ruinpay_finish"),
    path("success/<int:order_id>/", views.success, name="success"),
    path("order/<int:order_id>/", views.order_detail, name="order"),
]
