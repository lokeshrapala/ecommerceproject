from django.shortcuts import render, redirect
from .forms import MyUserForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import random
import http.client
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from productapp.models import Stock,Cart,Product
import json
# Create your views here.
def reg(request):
        if request.method == 'POST':
           regform = MyUserForm(request.POST)
           if regform.is_valid():
               x=otp_send(request)
               if x:
                   return render(request,'otp_input.html')
               else:
                   return render(request,'reg.html',{'regform': regform})
           else:
               return render(request, 'reg.html',{'regform': regform})
        else:
          regform = MyUserForm()
          return render(request,'reg.html',{'regform': regform})
def otpvalidation(request):
    newopt=request.POST["otp"]
    oldotp=request.session["otp"]
    if newopt==oldotp:
        form=MyUserForm(request.session["details"])
        new_user=User.objects.create_user(username = request.session["un"], password =request.session["pw"])
        new_user.save()
        form.save()
        login(request, new_user)
        return HttpResponse("registration success")
    else:
        return render(request,'otp_input.html')

def otp_send(request):
    ot = str(random.randint(100000, 999999))
    # request.session["pwd"]=request.POST["t1"]
    mobno = request.POST["mobno"]
    temail=request.POST["email"]
    request.session["un"]=request.POST["userName"]
    request.session["pw"]=request.POST["password"]
    subject="registration otp"
    From_mail = settings.EMAIL_HOST_USER
    to_list = [temail]

    send_mail(subject, ot, From_mail, to_list, fail_silently=False)
    print("otp sent to email")
    request.session["details"] = request.POST
    request.session["otp"] = ot
    conn = http.client.HTTPConnection("api.msg91.com")
    payload = "{ \"sender\":\"LKSHIT\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\":\"" + ot + "\",\"to\": [ \"" + mobno + "\" ] } ] }"
    headers = {
        'authkey': "274628A6aDjOb5jhN5cc8680d",  # PLEASE ENTER THE AUTHKEY BEFORE EXECUTING THE PROGRAM
        'content-type': "application/json"
    }

    conn.request("POST",
                 "/api/v2/sendsms?country=91&sender=&route=&mobiles=&authkey=&encrypt=&message=&flash=&unicode=&schtime=&afterminutes=&response=&campaign=",
                 payload, headers)

    data = conn.getresponse()
    res = json.loads(data.read().decode("utf-8"))
    print(res)
    if res["type"] == "success":
        return True
    else:
        return False
@login_required
def login(request):
        return render(request,"auth_home.html")


def my_logout(request):
    logout(request)
    return render(request, 'home.html')
@login_required
def cart(request):
    return render(request,'cart.html',display(request))
@login_required
def track(request):
    return render(request,'track.html')
@login_required
def cancel(request):
    return render(request,'cancel.html')

@login_required
def addcart(request):
    x=request.GET["pid"]
    qt=Stock.objects.filter(prodid=x)
    qtt=0
    for p in qt:
        #global qtt
        qtt=p
    qt=[q for q in range(1,qtt.tot_qty+1)]
    return render(request,'addcart.html',{"pid":x,"qtt":qt})


def insertcart(request):
    x = request.GET["pid"]
    qt = request.GET["qt"]
    user = User.objects.get(id=request.session.get("_auth_user_id"))
    un = str(user.username)
    pr = Product.objects.get(pid=x)
    a = int(str(x))
    b = int(str(qt))
    c = un
    d = float(pr.pcost)
    e = int(str(qt)) * float(pr.pcost)
    ct = Cart(username=c, pid=a, units=b, unitprice=d, tuprice=e)
    ct.save()
    return render(request, 'insertcart.html')


def viewcart(request):
    return render(request, 'cart.html', display(request))


def deletecart(request):
    cs = Cart.objects.filter(id=int(request.GET["id"]))
    cs.delete()
    return render(request, 'cart.html', display(request))


def modifycart(request):
    x = int(request.GET['pid'])
    qt = Stock.objects.filter(prodid=x)
    qtt = 0
    for p in qt:
        # global qtt
        qtt = p
    qt = [q for q in range(1, qtt.tot_qty + 1)]
    oldqt = request.GET["oqt"]
    cid = request.GET["id"]
    return render(request, 'modifyqty.html', {"cartid": cid, "pid": x, "qtt": qt, "oq": oldqt})


def modifiedcart(request):
    cid = int(request.GET["cid"])
    nqt = int(request.GET["nqt"])
    obj = Cart.objects.get(id=cid)
    obj.units = nqt
    obj.save()
    up = obj.unitprice
    obj.tuprice = up * nqt
    obj.save()
    return render(request, 'cart.html', display(request))


def display(request):
    user = User.objects.get(id=request.session.get("_auth_user_id"))
    un = str(user.username)
    ct = Cart.objects.filter(username=un)
    tp = 0.0
    for p in ct:
        tp = tp + float(p.tuprice)
    dic = {"k": ct, "tp": tp}
    return dic
