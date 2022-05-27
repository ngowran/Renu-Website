from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
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

def sensor_data(request):
  sensor_data = database.child('sensor-2').child('Data').get().val()
  return JsonResponse({"data":sensor_data})

def contact(request):
    return render(request, "contact.html")

def reset(request):
  return render(request, "accounts/reset.html")

def postreset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message  = "An email to reset your password has been successfully sent."
        return render(request, 'accounts/login.html', {"message":message})
    except:
        message  = "Something went wrong, please check the email you provided is correct."
        return render(request, "accounts/reset.html", {"messsage":message})

def profile(request):
  if request.session['uid']:
    sensor_data = database.child('sensor-2').child('Data').get().val()
    info = database.child('users').child(request.session['localId']).child('username').get().val()
    return render(request, "accounts/profile.html", {"data":sensor_data, "info":info})
  else:
    message = "Sorry, you're not signed in"
    return render(request, 'login', {"message":message})


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
    request.session['localId'] = user['localId']
    request.session["email"] = email
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    message = 'Signed in.'
    return render(request, 'index.html', {"message":message})

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    message = 'Logged out.'
    return render(request, "index.html", {"message":message})

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
                "username": name, 
                "email": email,
                "status": 1
            }
        message = "Thank you for signing up!"
        results = database.child("users").child(user['localId']).set(data)
        send_mail(
            subject="ReNu Ireland - Register Confirmation",
            message=f"Dear {name},\nThank you for registering your account with ReNu Ireland.\n\nRegards,\nReNu Ireland Team.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return render(request, 'accounts/login.html', {'message':message})
    except:
        message = 'Signup failed. Make sure email is unique and password is minimum 6 characters long.'
        return render(request, "accounts/register.html", {'message':message})

#class ProfileView(LoginRequiredMixin, TemplateView):
#   template_name = "accounts/profile.html"

def postbeta(request):
  email = request.POST.get('email')
  try:
    database.child("testers").push(email)
    message = "Thank you for signing up."
    send_mail(
            subject="ReNu Ireland - Beta Confirmation",
            message=f"Thank you for signing up to beta test ReNu Ireland.\nWe may contact you in the future about potential testing!\n\nRegards,\nReNu Ireland Team.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email, "nsgowran@gmail.com"]
        )
    return render(request, "index.html", {"message":message})
  except:
    message = "Sorry, something went wrong!"
    return render(request, "index.html", {"message":message})

def postcontact(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    try:
      contact_data = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
      }
      contact = database.child("contact").child(name).set(contact_data)
      send_mail(
            subject="ReNu Support Team " + subject,
            message=f"From: {name} {email}\n\n\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER, "nsgowran@gmail.com", "kevinjamestomescu@gmail.com"]
        )
      send_mail(
            subject="ReNu Ireland Support - Contact Confirmation",
            message=f"Dear {name},\nThank you for contacting ReNu Ireland.\nOur team will be back to you shortly!\n\nRegards,\nReNu Ireland Support Team.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
    except:  
      message = "Sorry, that email is incorrect. Please try again."
      return render(request, "contact.html", {'message':message})
    message = "Thank you for contacting Renu."
    return render(request, 'index.html', {"message":message})