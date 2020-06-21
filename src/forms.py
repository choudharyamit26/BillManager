from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Bill, Product, Client, OrderItem


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class OrderItemForm(forms.ModelForm):
    class Meta:
        fields = ('products', 'quantity', 'price', 'hsn_code', 'gst')


class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['buyer'].queryset = Client.objects.filter(user=user)

    class Meta:
        model = Bill
        fields = ('buyer', 'buyer_address', 'buyer_gst')

BillFormSet = modelformset_factory(OrderItem, fields=(
    'product', 'quantity', 'gst', 'price', 'hsn_code'))


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'address', 'buyer_gst', 'contact', 'email')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'product_company',
                  'product_model', 'quantity', 'price', 'hsn_code')


class BillUpdateForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
