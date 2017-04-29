from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.views import generic
from django.db.models import Q
from .models import Book, Author

@login_required(redirect_field_name='returnURL', login_url='library:login')
def index(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'home.html', context)


def book(request, id):
    if not request.user.is_authenticated():
        return redirect('library:login')
    else:
        book = get_object_or_404(Book, id=id)

        context = {
            'book': book,
        }
        return render(request, 'book.html', context)


def author(request, id):
    if not request.user.is_authenticated():
        return redirect('library:login')
    else:
        author = get_object_or_404(Author, id=id)
        context = {
            'author': author
        }
        return render(request, 'author.html', context)


def books(request):
    q = request.GET.get('q','')
    if not request.user.is_authenticated():
        return redirect('library:login')
    # books = Book.objects.all()
    books = Book.objects.filter(
        Q(title__icontains=q) |
        Q(summary__icontains=q) |
        Q(category__name__icontains=q) |
        Q(author__name__icontains=q)
    )
    context = {
        'books': books
    }
    return render(request, 'books.html', context)


def authors(request):
    if not request.user.is_authenticated():
        return redirect('library:login')
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context)


def generate_user(name,email,password):
    user = User.objects.create_user(name,email,password)
    return True


def register(request):
    if request.method == 'POST':
        errors = []
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if (username is "" or email is "" or password is "" or repassword is ""):
            errors.append("Please Fill All The Fields")

        elif (password != repassword):
            errors.append("Password Mismatch")

        elif User.objects.filter(username=username).exists():
            errors.append('Username Already Exists With The Same Name')

        elif User.objects.filter(email=email).exists():
            errors.append('Email Already Exists')

        if (len(errors) > 0):
            return render(request, 'register.html', {'errors': errors})
        else:
            if generate_user(username, email, password):
                return redirect('library:home')
            else:
                return render(request, 'register.html')
    else:
        return render(request, 'register.html')


def login(request):
    errors=[]
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)

        if user is not None:
            print(user)
            authlogin(request, user)
            return redirect('library:home')
        else:
            errors.append('Invalid UserName or Password')
            return render(request, 'login.html',{'errors':errors})

    else:
        return render(request, 'login.html')


def logout(request):
    authlogout(request)
    return redirect('library:login')
