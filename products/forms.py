from django import forms
from .models import Product


className = "form-control"

class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #? adding class "form-control" to all fields in the form
        for field in self.fields:
            if self.fields[field].label == "Image":
                self.fields[field].widget.attrs["class"] = "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"

            else:
                self.fields[field].widget.attrs["class"] = className
    

    class Meta:
        model = Product
        fields = ["name", "handle", "price", "image"]