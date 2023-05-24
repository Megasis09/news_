from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters import FilterSet, DateTimeFilter, CharFilter, ChoiceFilter
from django.forms import DateTimeInput

from .models import Article, News

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:20] + '...'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'articles/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'articles/article_form.html'

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    template_name = 'articles/article_confirm_delete.html'

class NewsCreateView(CreateView):
    model = News
    fields = ['title', 'content']
    template_name = 'news/news_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NewsUpdateView(UpdateView):
    model = News
    fields = ['title', 'content']
    template_name = 'news/news_form.html'

class NewsDeleteView(DeleteView):
    model = News
    success_url = reverse_lazy('home')
    template_name = 'news/news_confirm_delete.html'

class NewsFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    category = ChoiceFilter(field_name='category', choices=News.CATEGORIES)
    published_after = DateTimeFilter(
    field_name='published_at',
    lookup_expr='gt',
    widget=DateTimeInput(
    format='%Y-%m-%dT%H:%M',
    attrs={'type': 'datetime-local'},
    ),
    )

    class Meta:
        model = News
        fields = ['title', 'category']
