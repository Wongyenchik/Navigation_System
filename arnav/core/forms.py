from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User,Product
ACCOUNT_TYPE = {
    ("orderpicker", "Order Picker"),
    ("stockpurchaser", "Stock Purchaser"),
    ("admin", "Admin"),
}

CATEGORY_TYPE = {
    ("clampcylinder", "Clamp Cylinder"),
    ("coupler", "Coupler"),
    ("nylontubing", "Nylon Tubing"),
    ("silencer", "Silencer"),
}
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)

    class Meta:
        model = User
        fields = ['username','email']


class ProductForm(forms.ModelForm):
    product_id = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Product ID"}))
    product_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Product Name"}))
    product_category = forms.ChoiceField(choices=CATEGORY_TYPE)
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"Stock Count"}))

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_category', 'stock']

class UpdateStock(forms.ModelForm):
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"Stock Count"}))

    class Meta:
        model = Product
        fields = ['stock']