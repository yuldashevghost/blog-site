from django.contrib import messages, auth
from django.contrib.auth.models import User

from django.views.generic import TemplateView, ListView, DetailView, CreateView

from post.models import Post, Comment
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(TemplateView):
    template_name = "about.html"


class PostsListView(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get("page")


        posts = Post.objects.all()
        paginator = Paginator(posts, self.paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["page"] = page
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect("post-detail", pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    # fields = ['text']
    template_name = "add_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts")
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm(instance=post)
    return render(request, "create_post.html", {"form": form})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Bu Username allaqochon bor")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "bu Email allaqachon bor")
                return redirect("register")
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect("login")
        else:
            messages.error(request, "Parollar mos emas")
            return redirect("register")
    else:
        return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Siz kirdingiz!")
            return redirect("home")
        else:
            messages.error(request, "Nimadir xato!")
            return redirect("login")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    messages.success(request, "Siq chiqdingiz")
    return redirect("home")


#
# def login(request):
#     return render('login.html')
