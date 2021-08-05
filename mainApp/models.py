from django.db import models

class MainCategory(models.Model):
    mcid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Brand(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Seller(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15,default=None,blank=True,null=True)
    postcode = models.IntegerField(default=None,blank=True,null=True)
    city = models.CharField(max_length=20,default=None,blank=True,null=True)
    state = models.CharField(max_length=20,default=None,blank=True,null=True)
    addressline1 = models.CharField(max_length=50,default=None,blank=True,null=True)
    addressline2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    addressline3 = models.CharField(max_length=50, default=None, blank=True, null=True)
    pic = models.FileField(upload_to='images',default=None,blank=True,null=True)
    otp = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.sid)+" "+self.username
class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    maincat = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    subcat = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    finalPrice = models.IntegerField(default=0)
    instock = models.BooleanField(default=True)
    size = models.CharField(max_length=5,default='xs',null=True,blank=True)
    color = models.CharField(max_length=20,default='red',null=True,blank=True)
    img1 = models.FileField(upload_to='images')
    img2 = models.FileField(upload_to='images',default=None,blank=True,null=True)
    img3 = models.FileField(upload_to='images',default=None,blank=True,null=True)
    img4 = models.FileField(upload_to='images',default=None,blank=True,null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pid)+" "+self.name

class Buyer(models.Model):
    byid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15,default=None,blank=True,null=True)
    postcode = models.IntegerField(default=None,blank=True,null=True)
    city = models.CharField(max_length=20,default=None,blank=True,null=True)
    state = models.CharField(max_length=20,default=None,blank=True,null=True)
    addressline1 = models.CharField(max_length=50,default=None,blank=True,null=True)
    addressline2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    addressline3 = models.CharField(max_length=50, default=None, blank=True, null=True)
    pic = models.FileField(upload_to='images',default=None,blank=True,null=True)
    otp = models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return str(self.byid)+" "+self.username

class Wishlist(models.Model):
    wid = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.wid)+" "+self.buyer.username

class Checkout(models.Model):
    cid = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,default=None)
    total = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    final = models.IntegerField(default=0)
    q=models.CharField(max_length=100,default="",null=True,blank=True)
    mode = models.CharField(max_length=20,default='cod')

    def __str__(self):
        return self.buyer.username

class Newsletter(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField()

    def __str__(self):
        return self.email
