# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.

def main(request):
    if 'user_id' in request.session:
        request.session['user_id'] = None
    return render(request, 'dashboard/main.html')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect(reverse("get_main"))
    item_list = Item.objects.all()
    return render(request, 'dashboard/dashboard.html')

def wish_items(request):
    user_id = request.session['user_id']
    print user_id
    return render(request, 'wish_items/create.html')

def create(request):
    user_id = request.session['user_id']
    print user_id
    return render(request, 'dashboard/create.html')

def login(request):
    verify = User.objects.validate_login(request.POST)
    if type(verify) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    if request.method == "POST":    
        email = request.POST['email']
        password = request.POST['password']
        user_arr = User.objects.all().filter(email=email)
        if user_arr[0].password == password:
            request.session['user_id'] = user_arr[0].id
            request.session['name'] = user_arr[0].name
            print user_id
            return redirect('/dashboard')
    return redirect('/dashboard')

def register(request):
    if request.method == "POST":
        
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        date_hired = request.POST['date_hired']
        user = User.objects.create(name=name, username=username, email=email, password=password, date_hired=date_hired)
        request.session['user_id'] = user.id
        request.session['name'] = user.name
        print request.session['user_id']
        return redirect('/dashboard')

def add_item(request):
    if request.method == "POST":
        item_name = request.POST['item_product']
        print item_name
        if item_name == None:
            return redirect('/dashboard')
        else:
            Item.objects.create(name=item_name,item_creator=User.objects.get(id = request.session['user_id']))
        return redirect('/dashboard')    

def remove_item(request):
    # removal = Item.objects.get(id=)
    pass