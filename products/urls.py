from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="home"),
    path("products", views.product_list_view, name="product_list"),
    path("products/detail/<slug:handle>", views.product_detail_view, name="product_detail"),
    path("products/create", views.product_create_view, name="product_create"),
    path("products/download/<int:pk>", views.product_attachment_download_view, name="product_download")
]
