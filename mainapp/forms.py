from django import forms
from .models import Comment, Article


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']  # Укажите поля, которые вы хотите редактировать

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавьте необходимые атрибуты или классы CSS для полей формы, если это необходимо

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']  # Укажите поля, которые вы хотите редактировать

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавьте необходимые атрибуты или классы CSS для полей формы, если это необходимо


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'rating': forms.HiddenInput()  # Скрытое поле для рейтинга, чтобы управлять им через JavaScript
        }
        labels = {
            'content': 'Комментарий',
            'rating': 'Оценка',
        }
