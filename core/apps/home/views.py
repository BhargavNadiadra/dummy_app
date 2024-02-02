from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_desc = data.get('recipe_desc')
        recipe_image = request.FILES.get('recipe_image')

        recipe = Recipe.objects.create()
        recipe.recipe_name = recipe_name
        recipe.recipe_desc = recipe_desc
        recipe.recipe_image = recipe_image
        recipe.save()

        return redirect('/')

    queryset = Recipe.objects.all()

    # for filter search
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))

    context = {'recipes': queryset}

    return render(request, 'index.html', context)


@login_required(login_url='/login/')
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')


@login_required(login_url='/login/')
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_desc = data.get('recipe_desc')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_desc = recipe_desc

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect('/')

    context = {'recipe': queryset}

    return render(request, 'update_recipe.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/')

    context = {'page': 'login'}
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username is already taken')
            return redirect('/register/')

        user = User.objects.create(username=username, password=password)
        user.set_password(password)
        user.save()

        messages.info(request, 'Account created successfully')
        return redirect('/register/')

    context = {'page': 'register'}
    return render(request, 'register.html', context)
