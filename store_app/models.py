from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Slider(models.Model):
    image=models.ImageField(upload_to='images/slider_image',verbose_name='slider_image')
    is_active=models.BooleanField(default=True,verbose_name='Available')

class Category(models.Model):
    cat_name=models.CharField(max_length=250)
    cat_image=models.ImageField(upload_to='images/category_image',verbose_name='cat_image')
    no_of_products=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True,verbose_name='Available')

    def __str__(self):
        return self.cat_name

class Product(models.Model):
    pname=models.CharField(max_length=200)
    cat_id=models.ForeignKey(Category,on_delete=models.CASCADE,db_column='catid',default=0)   
    sku=models.CharField(max_length=200)
    quantity=models.IntegerField(default=0)
    is_bestseller=models.BooleanField(default=True,verbose_name='BestSeller')
    is_active=models.BooleanField(default=True,verbose_name='Active')
    description=models.TextField()
    price=models.FloatField(default=0)
    actual_price=models.FloatField(default=0)
    is_customer_choice=models.BooleanField(default=True,verbose_name='CustomerChoice')
    image1=models.ImageField(upload_to='images/products',verbose_name='product_image')
    image2=models.ImageField(upload_to='images/products',verbose_name='product_image')
    image3=models.ImageField(upload_to='images/products',verbose_name='product_image')
    image4=models.ImageField(upload_to='images/products',verbose_name='product_image')


class Cart(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid= models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)   

class Wishlist(models.Model):
    uid= models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid= models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    # qty=models.IntegerField(default=1)   

class Address(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
    name=models.CharField(max_length=200)
    address=models.TextField()
    email_address=models.EmailField()
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    postal_code=models.BigIntegerField()
    country=models.CharField(max_length=200)
    phone_number=models.BigIntegerField(0)
    is_default=models.BooleanField(default=0,verbose_name='Default')
    is_active=models.BooleanField(default=True,verbose_name='Active')
 
 
class Order(models.Model):
    orderid=models.CharField(max_length=50)
    uid= models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid= models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1) 
    aid= models.ForeignKey(Address,on_delete=models.CASCADE,db_column='aid',blank=True,null=True)
    order_status=models.CharField(max_length=50,default='pending')
 
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    mobile=models.BigIntegerField(blank=True,null=True)
    message=models.CharField(max_length=255) 
    status=models.CharField(max_length=255,default=True)
