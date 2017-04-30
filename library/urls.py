from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name='library'

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^home', views.index,name='home'),
    url(r'^book/(?P<id>[0-9]+)', views.book, name='book'),
    url(r'^books', views.books,name='books'),
    url(r'^author/(?P<id>[0-9]+)', views.author, name='author'),
    url(r'^authors', views.authors,name='authors'),
    url(r'^category/(?P<id>[0-9]+)', views.category, name='category'),
    url(r'^categories', views.categories,name='categories'),
    url(r'login', views.login, name='login'),
    url(r'logout', views.logout, name='logout'),
    url(r'register', views.register, name='register'),

    url(r'api', views.api, name='api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)