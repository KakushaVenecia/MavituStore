from email.policy import default
from django.db import models 
import uuid
from django.contrib.auth.models import User
 
class Product(models.Model):
    name=models.CharField(max_length=90)
    brand=models.CharField(max_length=90, null=True, blank=True)
    image=models.ImageField(upload_to='media/',default='')
    description=models.CharField(max_length=300, null=True, blank=True)
    price=models.FloatField()
    product_id=models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=False) 

    def __str__(self):
        return self.name

    @classmethod
    def searchbar(cls, search_term):
        items = cls.objects.filter(name__icontains=search_term)
        return items

class Cart(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    product_id=models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True, editable=False) 
    completed=models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username

    @property
    def grandtotal(self):
        cartitems =self.cartitems_set.all()
        '''
        loop through cart items and calculate grandtotal

        '''
        total= sum([item.subtotal for item in cartitems])
        return total
    
    @property
    def cartquantity(self):
        cartitems =self.cartitems_set.all()
        '''
        loop through cart items and calculate grandtotal

        '''
        total= sum([item.quantity for item in cartitems])
        return total

class Cartitems(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return self.product.name

    @property
    def subtotal(self):
        total = self.quantity * self.product.price
        return total
