from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .forms import UserCommentForm
from django.views.generic.detail import SingleObjectMixin
from django.views import View
# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDisplayView(DetailView): # this is passing the context to the template
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #dont need to pass all the comments
        #pk refers to the post primary key
        context['form'] = UserCommentForm()
        obj = context['object']
        RelComments = Comment.objects.filter(Poster = obj)
        if RelComments:
            context['comments'] = RelComments
        return context

class CommentForm(SingleObjectMixin, FormView):
    template_name = "blog/post_detail.html"
    form_class = UserCommentForm
    model = Comment

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        ThePost = Post.objects.get(pk=self.kwargs['pk'])
        Yes = {'author': request.user,'Poster': ThePost}
        form = UserCommentForm(initial = Yes)
        form.save()
        self.object = self.get_object()
        return super().post(request,*args,**kwargs)
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})
    # perform a query on the pk of the Post

class PostDetail(View):
    def get(self,request,*args, **kwargs):
        view = PostDisplayView.as_view()
        return view(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        view = CommentForm.as_view()
        return view(request,*args,**kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = Post
    success_url = ''
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def test_func(self):
        post =  self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request,'blog/about.html', {'title': 'About'})
