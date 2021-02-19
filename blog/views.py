from django.shortcuts import render, HttpResponse
from blog.models import Ask2,Comment
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def blogHome(request): 
    allPosts= Ask2.objects.all()
    context={'allPosts': allPosts}
    return render(request, "question/blogHome.html", context)

def blogPost(request, slug):
    post=Ask2.objects.filter(slug=slug).first()
    comments= Answer.objects.filter(post=post)
    context={'post':post, 'comments': comments, 'user': request.user}
    return render(request, "question/questionpost.html", context)
