from django.utils.dateparse import parse_date
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,get_object_or_404
from .models import Post,User
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
# dummy posts ideally from database
# posts = [
#     {
#         'author' : 'Mike Millions',
#         'title' : 'My first Job Experience',
#         'content' : 'First Post Content',
#         'date_posted' : '27th August 2003'
#     }
# ,    
#     {
#         'author' : 'John Smilga',
#         'title' : 'My first Youtube Video Got Viral!',
#         'content' : 'Second Post Content',
#         'date_posted' : '11th september 2011'
#     }
# ] 


# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context=context)


def search(request):
  if 'q' in request.GET:
    q = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=q)  # Or use other search criteria
  else:
    posts = Post.objects.all()
  context = {'posts': posts}
  return render(request, 'blog/search_results.html', context=context)

# it is a class based view
class PostListView(ListView):
    model = Post
    # naming convention for class based views
    # <app>/<model>_<viewtype>.html
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    
            

    def get_queryset(self):
        query = self.request.GET.get('q')
        selected_tags = self.request.GET.get('selected_tags')
        selected_date = self.request.GET.get('selected_date')
        
        posts = Post.objects.all()
        
        if query:
            posts = Post.objects.filter(title__icontains=query)
            posts = posts.union(Post.objects.filter(content__icontains=query))
            posts = posts.union(Post.objects.filter(tags__icontains=query))
            
            if not posts.exists():
                messages.error(self.request, f'No results found for "{query}".')
        else:
            if selected_tags and selected_tags != 'All':
                posts = posts.filter(tags__icontains=selected_tags)
            if selected_tags == 'All':
                post = posts.union(Post.objects.filter(tags__icontains=selected_tags))
            if not posts.exists():
                messages.error(self.request, f'No results found for Tag "{selected_tags}".')
            
        if selected_date:
            try:
                selected_date = parse_date(selected_date)
                posts = posts.filter(date_posted__date=selected_date)
            except ValueError:
                messages.error(self.request, 'Invalid date format.')
                
        return posts
        
        


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content', 'tags']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


def about(req): 
    return render(req,'blog/about.html', {'title' : "My title"})
