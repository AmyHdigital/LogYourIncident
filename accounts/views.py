import logging
import re
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        # GET FORM VALUES
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks good
                    try:
                        validate_password(password=password, user=username);
                    except ValidationError as error:
                        message = "";
                        for item in error:
                            message = message + "* " + item + "<br/>"

                        messages.error(request, message)

                        return redirect('register')
                    else:
                        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                        last_name=last_name, email=email)
                        user.save()
                        messages.success(request, 'You are now registered, please log in')
                        return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        logger.debug("Accounts/login method has been called.")
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = auth.authenticate(request, username=username, password=password)
        except ValidationError as error:
            logger.warning(error.message)
            messages.error(request, error.message)
            return redirect('login')

        else:
            if user is not None:
                auth.login(request, user)
                logger.info(username + " has successfully logged in.")
                messages.success(request, 'You are now logged in')
                return redirect('dashboard')
            else:
                logger.warning("*** Login attempted with invalid credentials.")
                messages.error(request, 'Invalid credentials')
                return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('incidents')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
