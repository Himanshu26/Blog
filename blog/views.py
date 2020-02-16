from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import employees
from .serializer import employeesSerializer
from .models import Post

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
posts = [
    {
        'author': 'himanshu',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'August 17,2019'
    },
    {
        'author': 'Adyasha',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'August 16,2019'
    }
]
class employeeList(APIView):
    def get(self,request):
        employee1 = employees.objects.all()
        serializer = employeesSerializer(employee1,many =True)
        return Response(serializer.data)

    def post(self):
        pass
# Create your views here.
def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html', context)
    '''return HttpResponse('<h1>Blog Home</h1>')'''

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render (request, 'blog/about.html',{'title':'About'})