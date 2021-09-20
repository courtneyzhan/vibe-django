import random

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.contrib.auth.models import User
# from django.http import HttpResponse

# Routes
def home(request):
    # return HttpResponse('<h1>Diary Home</h1>')
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'post/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'post/home.html' # <app>/<model>_<viewtype>/html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(DeleteView):
    model = Post
    success_url = "/"


class PostCreateView(CreateView):
    # Redirect if not authenticated
    login_url = '/login/'

    model = Post
    fields = ['title', 'content']

    gratitude_question = "What are you grateful for today?"
    reflection_questions = [
        "What would you do if you knew you could not fail?",
        "What did you do today that you are most proud of?",
        "Are you letting things out of your control make you stressed?",
        "What did you achieve today?",
        "What inspires you?",
        "I can't imagine living without..."
    ]  # https://positivepsychology.com/introspection-self-reflection/

    def get_initial(self):
        """
        Pre-populates post title based on post type
        Post type sent through GET request (0 -> gratitude, 1 -> reflective, none -> personal entry)
        """
        initial = super(CreateView, self).get_initial()
        for k, v in self.request.GET.items():
            if v == '0':  # gratitude post
                initial.update({'title': self.gratitude_question})
            elif v == '1':  # reflective question
                initial.update({'title': random.choice(self.reflection_questions)})
            else:
                initial.update({'title': ""})
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = User.objects.get(id=1)
        return super().form_valid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def login(request):
    next = "posts/"
    return render(request, 'registration/login.html', {'title': 'User Login'})

def about(request):
    # return HttpResponse('<h1>Diary About</h1>')
    return render(request, 'post/about.html', {'title': 'About'})

