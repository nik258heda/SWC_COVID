from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from auths.forms import SignUpForm, ProfileCollectionForm

    
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user.is_authenticated:     
                login(request, user)
            # return redirect('home:home')
            return redirect('auths:profileCollection')
    else:
        form = SignUpForm()
    return render(request, 'auths/signup.html', {'form': form})


def profileCollectionView(request):
    if request.user.is_authenticated:
        # if not Profile.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            form = ProfileCollectionForm(request.POST)
            if form.is_valid():
                form.save(request.user)

            return redirect('home:home')

        else :
            form = ProfileCollectionForm()
            return render(request, 'auths/profileCollection.html', {'form': form})

    return redirect('home:home')
