import uuid
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .numtoword import num_to_word

GST_CHOICES = (
    (5, 5),
    (12, 12),
    (18, 18),
    (28, 28),
)

HSN_CODE = (
    (8471, 8471),
    (8443, 8443),
    (8523, 8523),
    (8504, 8504),
    (8507, 8507),

)


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    buyer_gst = models.CharField(max_length=256)
    contact = models.IntegerField(null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("src:client-detail", kwargs={'pk': self.pk})


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product_name = models.CharField(max_length=256, null=True, blank=True)
    product_company = models.CharField(max_length=256, null=True, blank=True)
    product_model = models.CharField(max_length=256, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    hsn_code = models.IntegerField(choices=HSN_CODE)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("src:product-detail", kwargs={'pk': self.pk})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order_id = models.CharField(default=uuid.uuid4, max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0, )
    hsn_code = models.IntegerField(choices=HSN_CODE, default=8471)
    gst = models.IntegerField(choices=GST_CHOICES, default=18)
    ordered = models.BooleanField(default=False)

    def get_total_item_price(self):
        price = self.price * self.quantity
        return price


class Bill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        Client, null=True, blank=True, on_delete=models.SET_NULL)
    buyer_gst = models.CharField(max_length=256, null=True, blank=True)
    buyer_address = models.CharField(max_length=256, null=True, blank=True)
    date = models.DateField(auto_now=True, null=True, blank=True)
    items = models.ManyToManyField(OrderItem,  default=1)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("src:bill-detail", kwargs={'pk': self.pk})

    def get_c_gst_amount(self):
        x = []
        for item in self.items.all():
            price = item.price
            quantity = item.quantity
            gst = item.gst
            tax = ((item.price*(item.gst/100))/2)*item.quantity
            x.append(tax)
        c_gst_amount = sum(x)
        return c_gst_amount

    def final_price(self):
        x = []
        for item in self.items.all():
            price = item.price * item.quantity
            tax = (item.price*(item.gst/100))*item.quantity
            total_price = price + tax
            x.append(total_price)
        return sum(x)

    def gst_in_word(self):
        total_price = self.final_price()
        total_price_in_word = num_to_word(total_price)
        return total_price_in_word

    def get_sub_total(self):
        x = []
        for item in self.items.all():
            price = item.price * item.quantity
            x.append(price)
        return sum(x)

    def amount_in_word(self):
        x = []
        for item in self.items.all():
            price = item.price * item.quantity
            x.append(price)
        amount = sum(x)
        amountinword = num_to_word(amount)
        return amountinword

    class Meta:
        ordering = ('-date',)

    # @receiver(post_save,sender=OrderItem)
    # def order_created(sender,instance,created,**kwargs):
    #     if created:
    #         order = instance.order_id
    #         ordered_items = OrderItem.objects.filter(order_id=order)
    #         for x in ordered_items:
    #             print('Product :',x.product)
    #             print('Quantity :',x.quantity)
    #             print('Price :',x.price)
    #             print('HSN CODE :',x.hsn_code)
    #             print('Gst: ',x.gst)
