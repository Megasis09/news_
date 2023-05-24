from django.shortcuts import render
from .models import News

def news_list_view(request):
    news_list = News.objects.order_by('-published_date')
    context = {
        'news_list': news_list,
    }
    return render(request, 'news_list.html', context)

def news_detail_view(request, pk):
    news = News.objects.get(pk=pk)
    context = {
        'news': news,
    }
    return render(request, 'news_detail.html', context)


