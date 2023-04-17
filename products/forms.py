from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from products.models import Product, ProductAttachment


className = "form-control"

class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #? adding class "form-control" to all fields in the form
        for field in self.fields:
            if field == "image":
                self.fields[field].widget.attrs["class"] = "block w-full text-sm text-gray-00 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
            else:
                self.fields[field].widget.attrs["class"] = className
    

    class Meta:
        model = Product
        fields = ["name", "handle", "price", "image"]


class ProductAttachmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field in ["is_free", "is_active"]:
                self.fields[field].widget.attrs["class"] = "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
            elif field == "file":
                self.fields[field].widget.attrs["class"] = "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
            else:
                self.fields[field].widget.attrs["class"] = className

    class Meta:
        model = ProductAttachment
        fields = ["file", "name", "is_free", "is_active"]
        



#? =============================================================== Formset ====================================================================================================================
#? formset is in general a collection of forms, for example if we have a parent has some relation to multiple children like the relation between Product (parent) and ProductAttachment (child)
#? ============================================================================================================================================================================================



ProductAttachmentModelFormSet = modelformset_factory(
    model=ProductAttachment,
    form=ProductAttachmentForm,
    fields=["file", "name", "is_free", "is_active"],
    extra=0,
    can_delete=True,
)


ProductAttachmentInlineFormSet = inlineformset_factory(
    parent_model=Product,
    model=ProductAttachment,
    form=ProductAttachmentForm,
    formset=ProductAttachmentModelFormSet,
    fields=["file", "name", "is_free", "is_active"],
    extra=0,  #? when we put extra equal to 0 then we keep the number of forms as the number of children
    # extra=1,  #? and when we make extra equal to 1 then we add an extra child form for adding a new child if we want
    can_delete=True,
)