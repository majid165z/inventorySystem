from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignUpForm,UserUpdateForm
from django.contrib.auth import get_user_model

# Create your views here.

@login_required
def home(request:HttpRequest):
    return render(request,'core/home.html')

def logoutuser(request):
    logout(request)
    return redirect('home')

@login_required
def user_list(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "you don't have the required permissions."
        messages.error(request,msg)
        return redirect('home')
    users = get_user_model().objects.all()
    context = {'users':users}
    return render(request,'registration/user_list.html',context)



@login_required
def create_user(request:HttpRequest):
    user = request.user
    if not user.is_superuser:
        msg = "you don't have the required permissions."
        messages.error(request,msg)
        return redirect('home')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            warehouse_keeper = request.POST.get('warehouse_keeper',None)
            if warehouse_keeper == 'on':
                obj.warehouse_keeper = True
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            obj.first_name = name
            obj.last_name = last_name
            obj.save()
            msg = "The user was successfully created."
            messages.success(request,msg)
            return redirect('user_list')
        else:
            msg = "Please try again. something went wrong."
            messages.error(request,msg)
    context = {'form':form}
    return render(request,'registration/create_user.html',context)


@login_required
def edit_user(request:HttpRequest,username):
    user = request.user
    if not user.is_superuser:
        msg = 'شما دسترسی لازم برای اصلاح کاربر را ندارید'
        messages.error(request,msg)
        return redirect('home')
    instance = get_user_model().objects.get(username=username)
    form = UserUpdateForm(request.POST or None,instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            msg = 'کاربر با موفقیت اصلاح شد.'
            messages.success(request,msg)
            return redirect('user_list')
        else:
            msg = 'لطفا مجددا تلاش کنید'
            messages.error(request,msg)
    context = {'form':form}
    return render(request,'registration/update_user.html',context)

