from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.html import mark_safe

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
DEPART_TYPE = {
    ("location1", "Location 1"),
    ("location2", "Location 2"),

}
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length= 100)
    account_type = models.CharField(choices=ACCOUNT_TYPE, max_length=30, null=False, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Product(models.Model):
    product_id = models.CharField(max_length= 100, unique=True)
    product_name = models.CharField(max_length= 100, unique=True)
    product_category = models.CharField(choices=CATEGORY_TYPE, max_length=30, null=False, blank=False)
    image = models.ImageField(upload_to="product")
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    location = models.CharField(max_length= 100)

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.product_name

class Map(models.Model):
    depart = models.CharField(choices=DEPART_TYPE, max_length=30)  # Use the same choices as in Product model
    destination = models.CharField(choices=DEPART_TYPE, max_length=30)  # Use the same choices as in Product model
    map = models.ImageField(upload_to="map")

    def map_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return f"{self.depart} to {self.destination}"

class ProductList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length= 100)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class ProductListItem(models.Model):
    order = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    product_id = models.CharField(max_length= 100)
    product_name = models.CharField(max_length= 100)
    product_category = models.CharField(choices=CATEGORY_TYPE, max_length=30, null=False, blank=False)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    location = models.CharField(max_length= 100)
    image = models.ImageField(upload_to="product")
