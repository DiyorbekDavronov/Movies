from django.urls import path

from . import views

# localhost:8000/category/action
urlpatterns = [
    path("", views.BaseView.as_view(), name="home"),
    path("film/<int:pk>/", views.FilmDetailView.as_view(), name="film_detail"),
    path("category/<str:slug>/", views.CategoriesView.as_view(), name="category_detail"),

    path("add_film/", views.FilmCreateView.as_view(), name="add_film"),
    path("edit_film/<int:pk>/", views.FilmUpdateView.as_view(), name="edit_film"),
    path("delete_film/<int:pk>/", views.FilmDeleteView.as_view(), name="delete_film"),

    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("edit_profile/<int:pk>/", views.EditProfileView.as_view(), name="edit_profile"),
    path("exit/", views.user_logout, name="exit_profile"),

    path("search/", views.SearchView.as_view(), name="search"),
]
