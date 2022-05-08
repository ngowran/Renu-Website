from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
import pyrebase

config={
  "apiKey": "AIzaSyCRLXur7Aruh_EADjxKRsWtA-HY0P-G_ao",
  "authDomain": "renu-22cf0.firebaseapp.com",
  "databaseURL": "https://renu-22cf0-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "renu-22cf0",
  "storageBucket": "renu-22cf0.appspot.com",
  "messagingSenderId": "478924071511",
  "appId": "1:478924071511:web:d5cd8a215a9cd724bb7912",
  "measurementId": "G-F0J0XM9SJQ"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()


def index(request):
    print(request.user)
    test1 = database.child('Renu').child('Key1').get().val()
    return render(request, "index.html", {"test":test1})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")

def profile(request):
  sensor_data = database.child('Renu').child('Key1').get().val()
  return render(request, "accounts/profile.html", {"data":sensor_data})

def login(request):
    return render(request, "accounts/login.html")

def postlogin(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid login! Please check your input."
        return render(request,"accounts/login.html",{"message":message})
    request.session["email"] = email
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return redirect('index')

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "accounts/login.html")

def register(request):
    return render(request, "accounts/register.html")

def postregister(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        user = authe.create_user_with_email_and_password(email,passs)
        data = {
                "name": name, 
                "email": email,
                "status": 1
            }
        results = database.child("users").push(data, user['idToken'])
        return redirect('login')
    except:
        message ='Signup failed. Make sure email is unique and password is minimum 6 characters long.'
        return render(request, "accounts/register.html", {'message':message})

#class ProfileView(LoginRequiredMixin, TemplateView):
 #   template_name = "accounts/profile.html"
