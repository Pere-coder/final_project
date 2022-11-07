from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from mnemonic import Mnemonic
from .models import hellman_encrypt,saved_keys, profile
import random
from django. http import HttpResponse

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        if len(password) < 3:
            messages.error(request, 'password must be at least three characters')
            return redirect('register')
        
        get_all_users_by_email = User.objects.filter(email=email)
        if get_all_users_by_email:
            messages.error(request, 'email already exist')
            return redirect('register')
        
        new_user = User.objects.create_user(username=username, email=email,  password=password)
        new_user.save
        
        messages.success(request, 'user sucesfully created, login now')
        return redirect('login')
    return render(request, 'register.html')


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('a_input')
        else:
           messages.error(request, 'user does not exist')
           return redirect('login') 
        
    return render(request,'login.html')


def LogoutView(request):
    logout(request)
    return redirect('login')

@login_required
def a_input(request):
    if request.method == 'POST':
        alice = request.POST.get('alice')
        p = request.POST.get('p')
        q = request.POST.get('q')
        b = random.randint(0, 20)
        new_a =hellman_encrypt.objects.create(user=request.user ,p=p, alice=alice, q=q,  b=b)
        new_a.save()
        
        enc = hellman_encrypt.objects.all()
        for values in enc:
            p = values.p
            q = values.q
            b = values.b
            alice= values.alice
        bob = p** b % q
        Bob = alice** b % q
        keys=  Bob
        saved_key = saved_keys.objects.create(user=request.user, Bob=Bob)
        saved_key.save()
        return redirect('profile')
    
    return render(request, 'a.html')


@login_required
def profile_view(request):
    if request.method =='POST':
        key_password= request.POST.get('key_password')
        saved_key_password = profile.objects.create(username=request.user, key_password=key_password)
        saved_key_password.save()
       
        
        return redirect('ceaser')
        
    return render(request, 'profile.html')

@login_required
def profile_view2(request):
    information= profile.objects.all()
    if information.exists():
        for info in information: 
            info = info.key_password
            print(info)
    
        def encrypt(info,s):
            result = ""

        # traverse text
            for i in range(len(info)):
                char = info[i]

            # Encrypt uppercase characters
                if (char.isupper()):
                    result += chr((ord(char) + s-65) % 26 + 65)

            # Encrypt lowercase characters
                else:
                    result += chr((ord(char) + s - 97) % 26 + 97)

            return result
        keys = saved_keys.objects.all()
        for s in keys:
            s = s.Bob
    
        new_mnemo = encrypt(info,s)
    else:
        return redirect('no_ceaser')
    
    data = hellman_encrypt.objects.all()
    context= { 'new_mnemo': new_mnemo, 'data':data}
    return render(request, 'profile2.html', context)
@login_required
def no_ceaser(request):
    pass
    return render(request, 'no_ceaser.html')

