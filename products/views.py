from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product



def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def product_list_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "products/list.html", {"products": products})


def product_detail_view(request: HttpRequest, handle: str) -> HttpResponse:
    product = get_object_or_404(Product, handle=handle)
    form = False
    if product.user == request.user:
        form = ProductForm(instance=product)
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product.name = form.cleaned_data["name"]
                product.handle = form.cleaned_data["handle"]
                product.price = form.cleaned_data["price"]
                product.image = form.cleaned_data["image"]

                product.save()

    return render(request ,"products/detail.html", {"product": product, "form": form})

@login_required
def product_create_view(request: HttpRequest) -> HttpResponse:
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        print(list(request.FILES.items()))
        if form.is_valid():
            Product.objects.create(
                name=form.cleaned_data["name"],
                handle=form.cleaned_data["handle"],
                price=form.cleaned_data["price"],
                image=form.cleaned_data["image"],
                user=request.user
            )
            return redirect("home")
        
    return render(request, "products/create.html", {"form": form}) 