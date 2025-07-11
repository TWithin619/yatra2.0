
from .models import Destination, Detailed_desc, pessanger_detail,  Transactions, Contact
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import Library
from datetime import datetime
from .utils import recommend_tours
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from .forms import ContactForm


import random

#  __lte=      is eqivelent to lessthan or euivelent
#    table.all().filter().exclude().filer()   for two filters and one excluding condition
# Create your views here.

def index(request):
    dests = Destination.objects.all()
    dest1 = []
    j = 0
    for i in range(6):
        j += 2
        try:
            temp = Detailed_desc.objects.get(dest_id=j)
            dest1.append(temp)
        except Detailed_desc.DoesNotExist:
            # Handle the case where the Detailed_desc does not exist
            pass

    context = {
        'dests': dests,
        'dest1': dest1
    }

    return render(request, 'index.html', context)

    # dests = Destination.objects.all()
    # dest1 = []
    # j=0
    # for i in range(6):
    #     j=j+2
    #     temp =Detailed_desc.objects.get(dest_id=j)
    #     dest1.append(temp)

    # return render(request, 'index.html',{'dests': dests, 'dest1' : dest1})

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, last_name=last_name,
                                                first_name=first_name)
                user.save()
                print('user Created')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching ')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Sucessfully Logged in')
            email = request.user.email
            print(email)
            content = 'Hello ' + request.user.first_name + ' ' + request.user.last_name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
            # send_mail('Alert for Login', content
            #           , 'travellotours89@gmail.com', [email], fail_silently=True)
            dests = Destination.objects.all()
            return render(request, 'index.html',{'dests':dests})
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def about(request):
     #auth.about(request)
     return render(request, 'about.html')

@login_required(login_url='login')
def destination_list(request,city_name):
    dests = Detailed_desc.objects.all().filter(place=city_name)
    return render(request,'travel_destination.html',{'dests': dests})


def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'destination_details.html',{'dest':dest})

class KeyValueForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()
def pessanger_detail_def(request, city_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            try:
                obj = pessanger_detail.objects.get(Trip_id=1)
            except pessanger_detail.DoesNotExist:
                return redirect('index')
            pipo_id = obj.Trip_same_id
            request.session['Trip_same_id'] = pipo_id
            price = request.session['price']
            city = request.session.get('city', 'Kathmandu')
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            user = request.user  # This is the User instance
            request.session['n'] = formset.total_form_count()
            for i in range(formset.total_form_count()):
                form = formset.forms[i]

                t = pessanger_detail(
                    Trip_same_id=pipo_id,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    age=form.cleaned_data['age'],
                    Trip_date=temp_date,
                    payment=price,
                    username=user,  # Assign the User instance
                    city=city
                )
                t.save()

            obj.Trip_same_id = pipo_id + 1
            obj.save()
            no_of_person = formset.total_form_count()
            price1 = no_of_person * price
            GST = price1 * 0.13
            GST = float("{:.2f}".format(GST))
            final_total = GST + price1
            request.session['pay_amount'] = final_total
            return render(request, 'payment.html', {
                'no_of_person': no_of_person,
                'price1': price1,
                'GST': GST,
                'final_total': final_total,
                'city': city
            })
    else:
        formset = KeyValueFormSet()
        return render(request, 'sample.html', {'formset': formset, 'city_name': city_name})
    
def contact(request):
    if request.method == 'POST':
        name = request.POST('name')
        phone = request.POST('phone')
        email = request.POST('email')
        message = request.POST('message')

        # Save contact details to the database
        contact_entry = Contact(name=name, phone=phone, email=email, message=message)
        contact_entry.save()

        # Send email
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}',
            email,  # From address
            [settings.DEFAULT_FROM_EMAIL],  # To address
            fail_silently=False,
        )

        return render(request, 'index.html', {'name': name})
    return render(request, 'contact.html')

def upcoming_trips(request):
    username = request.user.get_username()
    date1=datetime.now().date()
    person = pessanger_detail.objects.all().filter(username=username).filter(pay_done=1)
    person = person.filter(Trip_date__gte=date1)
    print(date1)
    return render(request,'upcoming trip1.html',{'person':person})

@login_required(login_url='login')

def get_recommendations(request):
    if request.method == 'POST':
        preference = request.POST.get('preference')
        recommendations = recommend_tours(preference)
        return render(request, 'recommendations.html', {'recommendations': recommendations.to_dict(orient='records')})
    return render(request, 'index.html')

def initiate_payment(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = request.POST.get('amount')

    print("return_url", return_url)
    print("purchase_order_id", purchase_order_id)
    print("amount", amount)

    
    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": "Order01",
        "purchase_order_name": "test",
        "customer_info": {
        "name": "Pragya Khadka",
        "city": "Kathmandu",
        "username": "9869055270"
        }
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect (new_res['payment_url'])

@csrf_exempt
def verify_payment(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key b885cd9d8dc04eebb59e6f12190ae017',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            # user = request.user
            # user.has_verified_dairy = True
            # user.save()
            # perform your db interaction logic
            pass
        
        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        return redirect('home')


@login_required(login_url='login')
def otp_verification(request):
    otp1 = int(request.POST['otp'])
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Debit card'
    if otp1 == int(request.session['OTP']):
        del request.session["OTP"]
        total_balance = int(request.session['total_balance'])
        rem_balance = int(total_balance-int(request.session["pay_amount"]))
        c = Cards.objects.get(Card_number=request.session['dcard'])
        c.Balance = rem_balance
        c.save(update_fields=['Balance'])
        c.save()
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
        t.save()
        z = pessanger_detail.objects.all().filter(Trip_same_id=Trip_same_id1)
        for obj in z:
            obj.pay_done = 1
            obj.save(update_fields=['pay_done'])
            obj.save()
            print(obj.pay_done)
        return render(request, 'confirmetion_page.html')
    else:
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
        t.save()
        return render(request, 'wrong_OTP.html')

@login_required(login_url='login')
def data_fetch(request):
    username = request.user.get_username()
    person = pessanger_detail.objects.all().filter(username=username)
