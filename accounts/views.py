from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


# Create your views here.
def loginUser(request):
    template_name = 'accounts/pages/login.html'
    if request.method == 'GET':
        return render(request, template_name)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, template_name)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
    return redirect('accounts:loginUser')
