from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, FileResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.forms import ProductForm, ProductAttachmentInlineFormSet
from products.models import Product, ProductAttachment
from core.storages.utils import generate_presigned_url



def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def product_list_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "products/list.html", {"products": products})


def product_manage_detail_view(request: HttpRequest, handle: str) -> HttpResponse:
    product = get_object_or_404(Product.objects.select_related("user").prefetch_related("productattachment_set"), handle=handle)
    product_attachments = product.productattachment_set.all()
    is_manager = product.user == request.user

    if not is_manager:
        return HttpResponseBadRequest()

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    formset = ProductAttachmentInlineFormSet(request.POST or None, request.FILES or None, queryset=product_attachments)

    if form.is_valid() and formset.is_valid():

        instance = form.save(commit=False)
        instance.save()
        
        formset.save(commit=False)

        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")

            try:
                attachment_obj = _form.save(commit=False)
            except:
                attachment_obj = None

            if is_delete and attachment_obj.pk and attachment_obj is not None:
                attachment_obj.delete()

            elif attachment_obj is not None:
                attachment_obj.product = instance
                attachment_obj.save()

            product_attachments = ProductAttachment.objects.filter(product=product)
            formset = ProductAttachmentInlineFormSet(queryset=product_attachments)
                
    return render(request ,"products/manager.html", {"product": product, "form": form, "formset": formset})



def product_detail_view(request: HttpRequest, handle: str) -> HttpResponse:
    
    product = get_object_or_404(Product.objects.prefetch_related("productattachment_set"), handle=handle)
    
    is_owner = False

    if request.user.is_authenticated:
        is_owner = request.user.purchase_set.filter(product=product, completed=True).exists()  # -> verify ownership

    return render(request ,"products/detail.html", {"product": product, "is_owner": is_owner})


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


def product_attachment_download_view(request: HttpRequest, pk: int):
    attachment = get_object_or_404(ProductAttachment, pk=pk)
    
    can_download = attachment.is_free

    if request.user.is_authenticated:
        can_download = request.user.purchase_set.filter(product=attachment.product, completed=True).exists()  # -> verify ownership

    if not can_download and not attachment.is_free:
        return HttpResponseBadRequest()

    file_name = attachment.file.name

    file_url = generate_presigned_url(file_name)

    return HttpResponseRedirect(file_url)