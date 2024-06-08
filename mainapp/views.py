from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from mainapp.forms import CommentForm, EditArticleForm, ArticleForm
from mainapp.models import Article, Comment, Category
from productapp.models import Product


class ArticleListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-created_at')
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = True
        context['article_categories'] = Category.objects.all()
        context['popular_product'] = Product.objects.first()
        return context


class EditArticleView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        form = EditArticleForm(instance=article)
        return render(request, 'mainapp/edit_article.html', {'article': article, 'form': form})

    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect(article.get_absolute_url())


class CreateArticleView(View):
    def get(self, request):
        form = ArticleForm()
        return render(request, 'mainapp/create_article.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
        return render(request, 'mainapp/create_article.html', {'form': form})


class DeleteArticleView(View):
    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article.delete()
        return redirect('home')


class ContactView(View):

    def get(self, request):
        return render(request, 'mainapp/contact.html')


class AboutView(View):

    def get(self, request):
        return render(request, 'mainapp/about.html')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'mainapp/article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['sidebar'] = True
        context['comments'] = Comment.objects.filter(article=self.get_object()).order_by('-created_at')
        context['sidebar'] = False

        return context


class AddCommentView(View):
    def post(self, request, article_id, *args, **kwargs):
        article = Article.objects.get(id=article_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article', pk=article_id)
        return HttpResponseForbidden()





class CommentDeleteView(View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if request.user == comment.author or request.user.is_superuser:
            comment.delete()
            return redirect('article', pk=comment.article.pk)
        return HttpResponseForbidden()


class NotFoundView(TemplateView):
    template_name = '404_template.html'
