import uuid
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):
    try:
        lid = request.session['user_id']
        query = Login_Table.objects.get(id=lid)
        fetchquery = Product_Table.objects.all()
        vendor = False
        if query.Role == "vendor":
            vendor = True

        context = {
            "productdata": fetchquery,
            "vendor": vendor
        }
        return render(request, "index.html", context)
    except:
        fetchquery = Product_Table.objects.all()[:12]
        context = {
            "productdata": fetchquery,
        }
    return render(request,"index.html",context)

def about(request):
    return render(request,'about.html')

def aboutus(request):
    return render(request,'aboutus.html')
def add_to_wishlist(request):
    return render(request,'add-to-wishlist.html')

def cart(request):
    lid = request.session['user_id']
    fetchqueryy = Cart_Table.objects.filter(Login_ID=lid, Order_status=0)
    fetchquery = Cart_Table.objects.filter(Login_ID=lid, Order_status=0).aggregate(Sum("Total_Amount"))
    total=fetchquery['Total_Amount__sum']
    context = {
        "cartdata": fetchqueryy,
        "total": total,

        "amount": fetchquery,
    }
    return render(request,'cart.html',context)
    # return render(request,'cart.html',{"amount":fetchquery})
    # return render(request,'cart.html',{"amount":fetchquery})


def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')

def men(request):
    fetchquery = Product_Table.objects.filter(Category_id=2)
    return render(request,'men.html',{"productdetail":fetchquery})
def allproduct(request):
    fetchquery = Product_Table.objects.all()
    return render(request,'allproduct.html',{"productdetail":fetchquery})

def order_complete(request):
    return render(request,'order-complete.html')

def product_detail(request,pid):
    data = Product_Table.objects.get(id=pid);
    feedbackdata = Feedback_Table.objects.all();
    context = {
        "productdata": data,
        "feedback": feedbackdata
    }
    return render(request,'product-detail.html',context)

def women(request):
    fetchquery = Product_Table.objects.filter(Category_id=3)
    return render(request,'women.html',{"productdetail":fetchquery})

def signup(request):
    return render(request,'signup.html')

def login(request):
    return render(request,'login.html')

def insertdata(request):
    if request.method == 'POST':
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        user_email = request.POST.get("uemail")
        user_phone_no = request.POST.get("uphone")
        user_name = request.POST.get("uname")
        user_password = request.POST.get("upassword")
        user_role = request.POST.get("urole")
        insertquery = Login_Table(First_name=first_name,Last_name=last_name,Email_id=user_email,Phone_no=user_phone_no,User_name=user_name ,Password=user_password,Role=user_role,Status='Active')
        insertquery.save()
        messages.success(request, "REGISTERATION SUCCESSFULL")
        return render(request,'login.html')
    else:
        messages.error(request,"UNABLE TO REGISTER!!")
        return render(request,'signup.html')

def checklogin(request):
    useremail = request.POST.get("uemail")
    userpassword = request.POST.get("upassword")
    try:
        query = Login_Table.objects.get(Email_id=useremail, Password=userpassword)
        request.session['user_email'] = query.Email_id
        request.session['user_role'] = query.Role
        request.session['user_id'] = query.id
        request.session.save()
    except Login_Table.DoesNotExist:
        query = None

    if query is not None:
        messages.info(request,"Login Successfully")
        return redirect(index)
        # return render(request,'index.html')
    else:
        messages.info(request,"Account does not exist!! Please Sign in ")
        return redirect('login')
    return render(request,'signup.html')


def insertprofiledetail(request):
    if request.method == 'POST':
        lid = request.session['user_id']
        user_name = request.POST.get("name")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        profile_picture = request.FILES["pimage"]
        insertquery = Detail_Table(login_id=Login_Table(id=lid),name=user_name ,DOB=dob,gender=gender,profile_picture=profile_picture)
        insertquery.save()
        messages.success(request, "Profile Details update successfully")
        return render(request,'index.html')
    else:
        messages.error(request,"Error!!")
        return render(request,'profile.html')#profile details

def show_product(request):
    fetchquery = Product_Table.objects.all()
    return render(request,"index.html",{"productdata":fetchquery})

def logout(request):
    try:
        del request.session['user_email']
        del request.session['user_id']
        del request.session['user_role']

    except:
        pass
    return render(request,'login.html')


def addtocart(request):
    lid = request.session['user_id']
    prodid = request.POST.get("pid")
    prodprice = float(request.POST.get("pprice"))
    qty = float(request.POST.get("quantity"))
    print(type(qty))
    print(type(prodprice))
    # qty = float(qty)
    # prodprice = float(prodprice)
    totalprice = qty*prodprice
    try:
       data = Cart_Table.objects.filter(Login_ID=Login_Table(id=lid), Product_ID=prodid, Order_status=0).first()
       data.Quantity = (data.quantity)+qty
       data.Total_Amount = (data.totalprice)+totalprice
       messages.success(request, 'Cart Updated Successfully')
    except:
        storedata = Cart_Table(Login_ID=Login_Table(id=lid),Product_ID=Product_Table(id=prodid),Quantity=qty,Price=prodprice,Total_Amount=totalprice,Order_id=0,Order_status=0)
        storedata.save()
        messages.success(request,'Product added to cart successfully')
    return redirect(cart)

def addproduct(request):
    return render(request,'addproduct.html')
def addproduct2(request):
    return render(request,'addproduct2.html')

def feedback(request):
    return render(request,'feedback.html')

def insertproduct(request):
    lid = request.session['user_id']
    product_name = request.POST.get("prodname")
    product_price = request.POST.get("prodprice")
    product_category = request.POST.get("prodcategory")
    product_stock = request.POST.get("prodstock")
    product_description = request.POST.get("proddesc")
    product_image = request.FILES["prodimage"]
    product_image1 = request.FILES["prodimage1"]
    product_image2 = request.FILES["prodimage2"]
    product_image3 = request.FILES["prodimage3"]
    insertquery = Product_Table(Vendor=Login_Table(id=lid),Product_Name=product_name,Product_Price=product_price,Category_id=Category_Table(id=product_category),Stock=product_stock,
                                Product_Description=product_description,Image=product_image,Image1=product_image1,Image2=product_image2,Image3=product_image3,Product_Status='1')
    insertquery.save()
    messages.success(request, "Product added successfully!")
    return render(request,"index.html")

def manageproduct(request):
    lid = request.session['user_id']
    fetchquery = Product_Table.objects.filter(Vendor=lid)
    # fetchquery = Product_Table.objects.all()
    return render(request,"manageproduct.html",{"productdata":fetchquery})

def increaseitem(request , id):
    getdata = Cart_Table.objects.get(id=id)
    getdata.Quantity += 1
    getdata.Total_Amount += getdata.Product_ID.Product_Price
    getdata.save()
    return redirect("/cart")

def decreaseitem(request , id):
    getdata = Cart_Table.objects.get(id=id)
    getdata.Quantity -= 1
    getdata.Total_Amount -= getdata.Product_ID.Product_Price
    getdata.save()
    return redirect("/cart")


def removeproduct(request,rid):
    data = Cart_Table.objects.get(id=rid)
    data.delete()
    messages.success(request, "Product successfully removed from cart.")
    return redirect(cart)

def deleteproduct(request,did):
    data = Product_Table.objects.get(id=did)
    data.delete()
    messages.success(request, "Product successfully deleted.")
    return redirect(manageproduct)

def basic(request,id):
    try:
        lid = request.session['user_id']
        query = Login_Table.objects.get(id=lid)
        fetchquery = Product_Table.objects.all()
        vendor = False
        if query.Role == "vendor":
            vendor = True

        context = {
            "productdata": fetchquery,
            "vendor": vendor,
        }
        return render(request, "basics.html", context)
    except:
        fetchquery = Product_Table.objects.get(id=id)
        context = {
            "productdata": fetchquery,
        }
    return render(request,"basics.html",context)

def profile(request):
    return render(request,'profile.html',context)
def editproduct(request,eid):
    query = Product_Table.objects.get(id=eid)
    return render(request,"editproduct.html",{"productdata":query})

def updateproduct(request,uid):
    prod_name = request.POST.get("prodname")
    prod_price = request.POST.get("prodprice")
    prod_stock = request.POST.get("prodstock")
    prod_desc = request.POST.get("proddesc")
    query = Product_Table.objects.get(id=uid)
    query.Product_Name = prod_name
    query.Product_Price = prod_price
    query.Stock = prod_stock
    query.Product_Description = prod_desc
    if "prodimage" in request.FILES:
        prod_image = request.FILES["prodimage"]
        query.Image = prod_image
    if "prodimage1" in request.FILES:
        prod_image1 = request.FILES["prodimage1"]
        query.Image1 = prod_image1
    if "prodimage2" in request.FILES:
        prod_image2 = request.FILES["prodimage2"]
        query.Image2 = prod_image2
    if "prodimage3" in request.FILES:
        prod_image3 = request.FILES["prodimage3"]
        query.Image3 = prod_image3
    query.save()
    messages.success(request, "Product Data Updated Successfully!")
    return redirect(manageproduct)

def placeorder(request):
    lid=request.session["user_id"]
    finalamount = Cart_Table.objects.filter(Login_ID=lid, Order_status=0).aggregate(Total_Amount=Sum("Total_Amount"))
    amounts = finalamount['Total_Amount']


    if request.method == "POST":
        pay_method = request.POST.get("paymentmethod")
        address = request.POST.get('address')

        if pay_method == "offline":
            insertorderdata = product_order(Login_ID=Login_Table(id=lid),totalAmount=amounts, Address=address,order_status='Placed' ,Payment_status='pending')
            insertorderdata.save()
            order_id=insertorderdata.id
            insertpaymentdata = Payment_Table(Login_ID=Login_Table(id=lid), order_id=product_order(id=order_id), payment_method=pay_method, payment_status="pending", amount=amounts, transaction_id=None)
            insertpaymentdata.save()
            cart_items = Cart_Table.objects.filter(Login_ID=Login_Table(id=lid), Order_status=0)

            for items in cart_items:
                items.Order_id=order_id
                items.Order_status = 1
                items.save()

            messages.success(request,'Order Placed Succefully!!')
            return redirect('index')

        if  pay_method == "online":
            numbers = request.POST.get("cardno")
            cvv = request.POST.get("cvv")
            expiry = request.POST.get("expiry")
            carddata = CardDetail.objects.first()
            cnumber = carddata.card_number
            ccvv = carddata.card_cvv
            cexpiry = carddata.exp_date
            balance = carddata.card_balance

            if numbers == cnumber and cvv == ccvv and expiry == cexpiry and amounts < balance:
                insertorderdata = product_order(Login_ID=Login_Table(id=lid), totalAmount=amounts, Address=address,
                                                order_status='Placed', Payment_status='complete')
                insertorderdata.save()

                order_id = insertorderdata.id
                transaction_id = str(uuid.uuid4())
                insertpaymentdata = Payment_Table(Login_ID=Login_Table(id=lid), order_id=product_order(id=order_id),
                                                  payment_method=pay_method, payment_status="complete", amount=amounts,
                                                  transaction_id=transaction_id)
                insertpaymentdata.save()

                # Update the card balance
                carddata.card_balance -= amounts
                carddata.save()

                cart_items = Cart_Table.objects.filter(Login_ID=Login_Table(id=lid), Order_status=0)
                for items in cart_items:
                    items.Order_id = order_id
                    items.Order_status = 1
                    items.save()
                messages.success(request, "Order Placed Successfully!!")
                return redirect('index')
            else:
                messages.success(request, "Transaction Failed!!")
                return redirect('cart')

def myorder(request):
    uid = request.session["user_id"]
    orderdata = product_order.objects.filter(Login_ID=uid)
    context = ({'orderdetails': orderdata})
    return render(request, 'myorder.html', context)

def vieworder(request,id):
    user = request.session['user_id']
    order = product_order.objects.get(id=id, Login_ID=user)
    orderid = order.id
    products = Cart_Table.objects.filter(Login_ID=user, Order_id=orderid, Order_status=1)
    context = ({'orderitems': products})
    return render(request, 'vieworder.html', context)

def vendorvieworder(request):
    uid = request.session['user_id']
    sellers_products = Product_Table.objects.filter(Vendor=Login_Table(id=uid))
    getdetails =  Cart_Table.objects.filter(Product_ID__in = sellers_products , Order_status=1)
    context = {
        "sellerorderdetails":getdetails,
    }
    return render(request, 'vendorvieworder.html', context)


def productfeedback(request, order_id):
    context = {"order_id" : order_id}
    return render(request, 'feedback.html', context)

def storefeedback(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        ratings = request.POST.get('ratings')
        feedback_message = request.POST.get('feedback_message')
        order_id = request.POST.get('order_id')

        if Feedback_Table.objects.filter(order_id=order_id).exists():
            messages.error(request, 'you have already filled feedback.')
            return redirect('/myorder')
        else:
        # Assuming 'product' is a ForeignKey in the Feedback model pointing to Product
            feedback = Feedback_Table.objects.create(
                Login_ID=Login_Table(id=user_id),
                order_id=product_order(id=order_id),
                ratings=ratings,
                comment=feedback_message,
            )
        messages.success(request, "Thank you for your feedback! Your input has been successfully submitted.")
        return redirect(myorder)
    return render(request, 'index.html')

def showorders(request):
    uid = request.session["user_id"]
    getdata = product_order.objects.filter(Login_ID=uid)

    return render(request,'showorders.html',{"orderdata":getdata})


def yoursingleorder(request,id):
    getitemdata = Cart_Table.objects.filter(order_id=id)
    return render(request,'yoursingleorder.html',{"singleorderdetail":getitemdata})

# def placeorder(request):
#     lid = request.session["user_id"]
#     phone = request.POST.get("phone")
#     address = request.POST.get("address")
#     finaltotal = request.POST.get("finalamount")
#     payment = request.POST.get("payment")
#     # insertorderdata = Order_Table(Login_ID=Login_Table(id=lid), Total_Amount=amounts, Order_Status="placed")
#     # storedata = Order_Table(Login_ID=Login_Table(id=lid),phoneno=phone,address=address,finaltotal=finaltotal,
#     #                   paymode=payment,orderstatus="placed")
#     storedata = Order_Table(Login_ID=Login_Table(id=lid),Total_Amount=finaltotal,Order_Status="placed")
#     storedata.save()
#     order_id = storedata.id
#     insertpaymentdata = Payment_Table(Login_id=Login_Table(id=lid), Order_id=Order_Table(id=order_id),
#                                       Payment_Type=payment, Payment_Status="pending")
#     insertpaymentdata.save()
#
#     lastid = storedata.id # fetch last inserted id in order
#     getdata = Cart_Table.objects.filter(Login_ID=lid,Cart_Status=1)
#
#     for i in getdata:
#         i.Cart_Status = "CONFIRMED"
#         i.order_id = lastid
#         i.save()
#
#     messages.success(request,"order placed successfully")
#     return redirect(index)

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('uemail')
        try:
            user = Login_Table.objects.get(Email_id=username)

        except Login_Table.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'parthinfolabz19@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            # now update the password in model
            cuser = Login_Table.objects.get(Email_id=username)
            cuser.Password = password
            cuser.save(update_fields=['Password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
        return redirect(index)

def signupnew(request):
    return render(request,"signupnew.html")

def loginnew(request):
    return render(request,"loginnew.html")

def findproduct(request):
    itemname = request.POST.get("itemname")
    finddata = Product_Table.objects.filter(Product_Name__contains=itemname)
    context = {
        "productdata":finddata
    }
    return render(request,"index.html",context)

def profile2(request):
    return render(request,"profile2.html")
def editproduct2(request,eid):
    query = Product_Table.objects.get(id=eid)
    return render(request,"editproduct2.html",{"productdata":query})

def insertcontact(request):
    if request.method == 'POST':
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        user_email = request.POST.get("email")
        user_phone_no = request.POST.get("phone")
        user_message = request.POST.get("message")
        insertquery = Contact_Us_Table(First_name=first_name,Last_name=last_name,Email_ID=user_email,Phone_No=user_phone_no,Message=user_message)
        insertquery.save()
        messages.success(request, "Your message has been sent!")
        return render(request,'index.html')
    else:
        messages.error(request,"An error occurred. Please try again later.")
        return render(request,'contact.html')