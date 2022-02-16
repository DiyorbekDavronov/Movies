from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from django.contrib.auth.models import User

from .models import Film, Categories
from .forms import FilmForm, UserRegisterForm, UserLoginForm


# context - данные которые отрисовываются в шаблоне
# QuerySet - объект ответа нашего запроса
# objects - менеджер который управляет моделью
class BaseContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(BaseContextMixin, self).get_context_data(**kwargs)
        context["categories"] = Categories.objects.all()
        return context


class BaseView(ListView, BaseContextMixin):
    template_name = "films_app/index.html"
    context_object_name = "films"

    def get_queryset(self):
        return Film.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context | BaseContextMixin().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class FilmDetailView(DetailView, BaseContextMixin):
    template_name = "films_app/film_detail.html"
    context_object_name = "film"

    def get_queryset(self):
        return Film.objects.filter(pk=self.kwargs["pk"], is_published=True)

    def get_context_data(self, **kwargs):
        context = super(FilmDetailView, self).get_context_data(**kwargs)
        context | BaseContextMixin().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class CategoriesView(BaseView, BaseContextMixin):
    template_name = "films_app/index.html"
    context_object_name = "films"

    def get_queryset(self):
        return Film.objects.filter(category__slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super(CategoriesView, self).get_context_data(**kwargs)
        context | BaseContextMixin().get_context_data(**kwargs)
        context["title"] = Categories.objects.get(slug=self.kwargs["slug"])
        return context


class SearchView(BaseView, BaseContextMixin):
    template_name = "films_app/index.html"
    context_object_name = "films"

    def get_queryset(self):
        films_requests = self.request.GET["title"]
        return Film.objects.filter(title__icontains=films_requests)

    def get_context_data(self, **kwargs):
        films_requests = self.request.GET["title"]
        context = super(SearchView, self).get_context_data(**kwargs)
        context | BaseContextMixin().get_context_data(**kwargs)
        context["title"] = f"По запросу: '{films_requests}'. Найдено: {len(self.object_list)} фильмов"
        return context


class FilmCreateView(CreateView):
    template_name = "films_app/edit_film.html"
    form_class = FilmForm
    extra_context = {
        "title": "Создать фильм",
        "btn_color": "primary",
        "btn_text": "Создать"
    }

    def get_success_url(self):
        film = self.object
        film.author = self.request.user
        film.save()
        return film.get_absolute_url()


class FilmUpdateView(UpdateView):
    template_name = "films_app/edit_film.html"
    form_class = FilmForm
    extra_context = {
        "btn_color": "success",
        "btn_text": "Изменить"
    }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.pk == self.get_object().author.pk:
            return super(FilmUpdateView, self).dispatch(request, *args, **kwargs)
        messages.error(request, "Этот фильм вам не принадлежит !")
        return redirect("home")

    def get_queryset(self):
        return Film.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        film = self.object
        context = super(FilmUpdateView, self).get_context_data(**kwargs)
        context | BaseContextMixin().get_context_data(**kwargs)
        context["title"] = f"Изменить: {film.title}"
        return context

    def get_success_url(self):
        film = self.object
        return film.get_absolute_url()


class FilmDeleteView(DeleteView):
    model = Film

    def get_success_url(self):
        messages.success(self.request, f"Вы успешно удалили фильм {self.object.title}!")
        return reverse_lazy("home")

    def render_to_response(self, context, **response_kwargs):
        form = self.get_form()
        self.form_valid(form)
        return redirect("home")


class UserRegisterView(CreateView):
    # model =
    # fields =
    form_class = UserRegisterForm
    template_name = "films_app/user_auth.html"
    extra_context = {
        "title": "Регистрация",
        "btn_text": "Зарегистрироваться",
        "btn_color": "primary"
    }

    def get_success_url(self):
        user = self.object
        login(self.request, user)
        messages.success(self.request, "Вы успешно зарегистрировались !")
        return reverse_lazy("home")


class UserLoginView(LoginView):
    template_name = "films_app/user_auth.html"
    form_class = UserLoginForm
    extra_context = {
        "title": "Вход",
        "btn_text": "Войти",
        "btn_color": "success"
    }

    def get_success_url(self):
        messages.success(self.request, "Вы успешно авторизовались !")
        return reverse_lazy("home")


# user - пользователь который ходит по сайту
# profile - профиль пользователя который мы запросили

class ProfileView(DetailView):
    model = User
    template_name = "films_app/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        user = self.object
        context = super(ProfileView, self).get_context_data(**kwargs)
        context | BaseContextMixin().get_context_data(**kwargs)
        context["title"] = f"Профиль: {user.username}"
        context["films"] = Film.objects.filter(author_id=self.kwargs["pk"])
        return context


class EditProfileView(UpdateView):
    template_name = "films_app/edit_profile.html"
    model = User
    fields = ("username", "first_name", "last_name", "email")
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"]:
            messages.error(request, "У вас нет прав изменить этот профиль !")
            return redirect("home")
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.object
        context = super(EditProfileView, self).get_context_data(**kwargs)
        context | BaseContextMixin().get_context_data(**kwargs)
        context["title"] = f"Изменить профиль: {user.username}"
        return context


def user_logout(request):
    messages.success(request, "Вы успешно вышли из системы !")
    logout(request)
    return redirect("home")
