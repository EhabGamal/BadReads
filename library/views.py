from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.views import generic
from django.db.models import Q
from .models import Book, Author, Category, UserBooks

@login_required(redirect_field_name='returnURL', login_url='library:login')
def index(request):
    books = UserBooks.objects.filter(user=request.user)
    authors = Author.objects.filter(users=request.user)
    categories = Category.objects.filter(users=request.user)
    context = {
        'books': books,
        'authors': authors,
        'categories': categories
    }
    return render(request, 'home.html', context)


@login_required(redirect_field_name='returnURL', login_url='library:login')
def book(request, id):
    book = get_object_or_404(Book, id=id)

    context = {
        'book': book,
    }
    return render(request, 'book.html', context)


@login_required(redirect_field_name='returnURL', login_url='library:login')
def author(request, id):
    author = get_object_or_404(Author, id=id)
    context = {
        'author': author
    }
    return render(request, 'author.html', context)


@login_required(redirect_field_name='returnURL', login_url='library:login')
def category(request, id):
    category = get_object_or_404(Category, id=id)
    context = {
        'category': category
    }
    return render(request, 'category.html', context)


@login_required(redirect_field_name='returnURL', login_url='library:login')
def books(request):
    q = request.GET.get('q','')
    books = Book.objects.filter(
        Q(title__icontains=q) |
        Q(summary__icontains=q) |
        Q(category__name__icontains=q) |
        Q(author__name__icontains=q)
    )
    for book in books:
        book.rel = UserBooks.objects.filter(book_id=book.pk)
    context = {
        'books': books
    }
    return render(request, 'books.html', context)


@login_required(redirect_field_name='returnURL', login_url='library:login')
def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context)


@login_required(redirect_field_name='returnURL', login_url='library:login')
def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'categories.html', context)


def api(request):
    view = request.POST.get('view')
    action = request.POST.get('action')
    response = {'success':False}

    if view == 'book':
        book = Book.objects.get(pk=request.POST.get('book_id'))
        rel, created = UserBooks.objects.get_or_create(user__id=request.POST.get('user_id'), book=book)
        if action == 'rate':
            rel.rate = request.POST.get('rating')
        rel.save()
    elif view == 'author':
        author = Author.objects.get(pk=request.POST.get('author_id'))
        user = User.objects.get(pk=request.POST.get('user_id'))
        if action == 'follow':
            author.users.add(user)
            print('inside follow action')
        elif action == 'unfollow':
            author.users.remove(user)
            print('inside unfollow action')
        author.save()
    elif view == 'category':
        category = Category.objects.get(pk=request.POST.get('category_id'))
        user = User.objects.get(pk=request.POST.get('user_id'))
        if action == 'follow':
            category.users.add(user)
            print('inside follow action')
        elif action == 'unfollow':
            category.users.remove(user)
            print('inside unfollow action')
        category.save()

    return JsonResponse(response)


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
            authlogin(request, user)
            if request.GET.get('returnURL'):
                return redirect(request.GET.get('returnURL'))
            return redirect('library:home')
        else:
            errors.append('Invalid UserName or Password')
            return render(request, 'login.html',{'errors':errors})

    else:
        return render(request, 'login.html')


def logout(request):
    authlogout(request)
    return redirect('library:login')
