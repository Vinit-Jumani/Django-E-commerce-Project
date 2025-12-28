from django.db import models
from django.utils.safestring import mark_safe

STATUS = [
    ("Inactive", "Inactive"),
    ("Active", "Active"),
]
PRODUCT_STATUS = [
    ("0","Out of stock"),
    ("1","Instock"),
]
# Create your models here.
class Login_Table(models.Model):
    First_name = models.CharField(max_length=30, null=True)
    Last_name = models.CharField(max_length=30, null=True)
    User_name = models.CharField(max_length=30, null=True)
    Email_id = models.EmailField()
    Phone_no = models.BigIntegerField()
    Password = models.CharField(max_length=30)
    ROLE = (
        ("Vendor", "Vendor"),
        ("User", "User"),
    )
    Role = models.CharField(max_length=30, default='')
    Status = models.CharField(max_length=30,choices=STATUS)

    def __str__(self):
        return self.User_name

    class Meta:
        verbose_name = 'Login Detail'
        verbose_name_plural = "Login Details"
class Detail_Table(models.Model):
    login_id = models.ForeignKey(Login_Table,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    DOB = models.DateField()
    gender = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to="photos")

    class Meta:
        verbose_name = 'Profile Detail'
        verbose_name_plural = "Profile Details"

    def user_dp(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.profile_picture.url))


class Category_Table(models.Model):
    Category_Name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Category Detail'
        verbose_name_plural = "Category Details"

    def __str__(self):
        return self.Category_Name

class Product_Table(models.Model):
    Category_id = models.ForeignKey(Category_Table,on_delete=models.CASCADE)
    Vendor = models.ForeignKey(Login_Table, on_delete=models.CASCADE, limit_choices_to={'Role': 'Vendor'}, default='')
    Product_Name = models.CharField(max_length=100)
    Product_Description = models.TextField()
    Product_Price = models.FloatField()
    Stock = models.IntegerField()
    Image = models.ImageField(upload_to="photos",null=True)
    Image1 = models.ImageField(upload_to="photos", null=True)
    Image2 = models.ImageField(upload_to="photos", null=True)
    Image3 = models.ImageField(upload_to="photos", null=True)
    Product_Status = models.CharField(max_length=20,choices=PRODUCT_STATUS)

    class Meta:
        verbose_name = 'Product Detail'
        verbose_name_plural = "Product Details"

    def product_image(self):
        return mark_safe('<img src="{}" width="25"/>'.format(self.Image.url))

    def product_image1(self):
        if self.Image1:
            return mark_safe('<img src="{}" width="25"/>'.format(self.Image1.url))
        else:
            return ""

    def product_image2(self):
        if self.Image2:
            return mark_safe('<img src="{}" width="25"/>'.format(self.Image2.url))
        else:
            return ""

    def product_image3(self):
        if self.Image3:
            return mark_safe('<img src="{}" width="25"/>'.format(self.Image3.url))
        else:
            return ""

    def __str__(self):
        return self.Product_Name

class Cart_Table(models.Model):
    Login_ID = models.ForeignKey(Login_Table,on_delete=models.CASCADE)
    Product_ID = models.ForeignKey(Product_Table,on_delete=models.CASCADE)
    Price = models.IntegerField(default=100)
    Total_Amount = models.IntegerField(default=200)
    Quantity = models.IntegerField()
    Order_id = models.IntegerField(default=0)
    Order_status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Cart Detail'
        verbose_name_plural = "Cart Details"

class product_order(models.Model):
    Login_ID = models.ForeignKey(Login_Table,on_delete=models.CASCADE,null=True)
    totalAmount = models.IntegerField(default=0)
    Address = models.TextField()
    order_status = models.CharField(max_length=50, choices=(('Pending', 'Pending'), ('Placed', 'Placed')))
    Payment_status = models.CharField(max_length=30)
    Date_time = models.DateTimeField(auto_now=True, editable=False)

    def total_orders(cls):
        return cls.objects.count()

    def __str__(self):
        return f"Order ID: {self.id} - User: {self.Login_ID.User_name} - Status: {self.order_status} - Total : {self.totalAmount}"


class Payment_Table(models.Model):
    Login_ID = models.ForeignKey(Login_Table, on_delete=models.CASCADE, null=True)
    order_id = models.ForeignKey(product_order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('online', 'Online'), ('offline', 'Offline'), ])
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=30, choices=[('failed', 'Failed'), ('pending', 'Pending'),
                                                              ('complete', 'Complete'), ], default='pending')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment - Order ID: {self.order_id}, User: {self.Login_ID.User_name}, Amount: {self.amount}, Status: {self.payment_status}"

    class Meta:
        verbose_name = 'Payment Detail'
        verbose_name_plural = "Payment Details"

class CardDetail(models.Model):
    name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50)
    card_cvv = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=50)
    card_balance = models.IntegerField(default=1000000)

    def __str__(self):
        return self.card_number

class Feedback_Table(models.Model):
    Login_ID = models.ForeignKey(Login_Table,on_delete=models.CASCADE,null=True)
    order_id = models.ForeignKey(product_order, on_delete=models.CASCADE, null=True, blank=True, default='')
    ratings = models.IntegerField()
    comment = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Feedback Detail'
        verbose_name_plural = "Feedback Details"



class Complain_Table(models.Model):
    Loging_id = models.ForeignKey(Login_Table,on_delete=models.CASCADE)
    complain = models.TextField()
    Complain_Datetime = models.DateTimeField(auto_now=True)
    Complain_Status = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Complain Detail'
        verbose_name_plural = "Complain Details"

class Contact_Us_Table(models.Model):
    First_name = models.CharField(max_length=30,null=True)
    Last_name = models.CharField(max_length=30,null=True)
    Email_ID = models.EmailField()
    Phone_No = models.BigIntegerField()
    Message = models.TextField()
    Timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Us Detail'
        verbose_name_plural = "Contact Us Details"