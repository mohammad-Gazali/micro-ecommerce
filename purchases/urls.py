from django.urls import path
from purchases import views



urlpatterns = [
    path("start", views.purchase_start_view, name='purchase_start'),
    path("success", views.purchase_success_view, name='purchase_success'),
    path("stopped", views.purchase_stopped_view, name='purchase_stopped'),
]
