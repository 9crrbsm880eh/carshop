from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Модель для категорий статей
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Модель для статей блога
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='static/images', blank=True, null=True, default='/static/images/default_cover.png')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', args=[str(self.id)])


# Модель для комментариев к статьям
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by  on {self.article.title}'
