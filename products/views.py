from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, FileResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from products.forms import ProductForm
from products.models import Product, ProductAttachment
import mimetypes



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
                form.save()

    return render(request ,"products/detail.html", {"product": product, "form": form})

@login_required
def product_create_view(request: HttpRequest) -> HttpResponse:
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect("home")
        
    return render(request, "products/create.html", {"form": form})


def product_attachment_download_view(request: HttpRequest, pk: int) -> FileResponse:
    attachment = get_object_or_404(ProductAttachment, pk=pk)
    
    can_download = attachment.is_free

    if request.user.is_authenticated:
        can_download = True

    if not can_download:
        return HttpResponseBadRequest()

    # this way will change we use object storage like S3
    file = attachment.file.open(mode="rb")

    filename = attachment.file.name

    response = FileResponse(file)

    content_type, encoding = mimetypes.guess_type(filename)

    response["Content-Type"] = content_type or "application/octet-stream"

    # here we force download after accessing this view
    response["Content-Disposition"] = f"attachment;filename={filename}"

    return response