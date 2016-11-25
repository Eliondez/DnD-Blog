from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Character
from .forms import PostForm

def story_list(request):
    queryset = Post.objects.all().order_by('-timestamp')
    leftchars = Character.objects.all()[:3]
    rightchars = Character.objects.all()[3:]

    paginator = Paginator(queryset, 3)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'leftchars': leftchars,
        'rightchars': rightchars,
        'queryset': queryset,
        'title': 'List'
    }
    return render(request, 'bolders/index.html', context)


def story_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Успешно создано')
            return redirect(instance.get_absolute_url())
        else:
            messages.error(request, 'Что-то пошло не так')
    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'bolders/story_form.html', context)

def story_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    leftchars = Character.objects.all()[:3]
    rightchars = Character.objects.all()[3:]
    context = {
        'leftchars': leftchars,
        'rightchars': rightchars,
        'title': 'Detail',
        'story': instance
    }
    return render(request, 'bolders/detail.html', context)

def story_update(request):
    return HttpResponse('Hello')

def story_delete(request):
    return HttpResponse('Hello')


# Create your views here.
