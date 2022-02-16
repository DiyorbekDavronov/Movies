from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User


# DJANGO ORM
# Модель - представление таблицы в БД
class Categories(models.Model):
    name = models.CharField("Категория", max_length=50)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Film(models.Model):
    title = models.CharField(verbose_name="Наименование", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="film-images/")
    time_create = models.DateTimeField("Дата создания", auto_now_add=True)
    time_update = models.DateTimeField("Дата обновления", auto_now=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Категория", default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default=1)

    def get_absolute_url(self):
        return reverse("film_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
