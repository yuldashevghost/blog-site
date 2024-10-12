from django.urls import path

from post import views
from post.views import HomeView, PostsListView, PostDetailView, AddComment, AboutView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("posts/", PostsListView.as_view(), name="posts"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<int:pk>/edit/", views.post_update, name="post_update"),
    path("posts/<int:pk>/comment/", AddComment.as_view(), name="add_comment"),
]
