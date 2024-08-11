from django.db import models

# Create your models here.

# user = User.objects.all()

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.TextField(max_length=500)
    phone_number = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name 
    

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    sub_category = models.CharField(max_length=100, default="")
    price = models.IntegerField()
    decs = models.CharField(max_length=550)

    image = models.ImageField(upload_to='image/image')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    def __str__(self) -> str:
        return self.product_name
    


