from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from home.models import Contact
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Ask2,Comment
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm,UserChangeForm,PasswordResetForm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.views import generic
from .forms import EditProfileForm, CommentForm
from home.forms import EditProfileForm
from django.conf import settings 
from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.urls import reverse
from django.contrib.auth import authenticate
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
import json
from django.core import serializers
import bleach
import markdown2
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
class UserEditView(generic.UpdateView):
    form_class=EditProfileForm
    template_name = 'registration/editprofile.html'
    success_url = reverse_lazy('edit_success')
    # fields = ['first_name','username']
    def get_object(self):
        return self.request.user
def edit_success(request):

    messages.success(request, "Profile Updated")
    return redirect("home")
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
# class PasswordResetCompleteView(PasswordResetCompleteView):
#     success_url = reverse_lazy('password_success2')

def askquestion(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            question = request.POST.get('question')
            posted_by = request.POST.get('posted_by')
            q = Ask2(question_title=title, question_text=question, posted_by=posted_by)
            q.save()
            return redirect(viewquestion, q.qid, q.slug)
        except Exception as e:
            return render(request, 'question/askquestion.html', { 'error': 'Something is wrong with the form!' })
    else:
        return render(request, 'question/askquestion.html', {})
def viewquestion(request, qid, qslug):
    context = {}
    template_name = 'question/questionpost1.html'
    post = Ask2.objects.get(qid=qid, slug=qslug)
    comments = post.comments.filter(active=False)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    question = Ask2.objects.get(qid=qid, slug=qslug)
    # assuming obj is a model instance
    question_json = json.loads(serializers.serialize('json', [ question ]))[0]['fields']
    question_json['date_posted'] = question.date_posted
    question_json['qid'] = question.qid
    question_json['question_text'] = bleach.clean(markdown2.markdown(question_json['question_text']), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
    context['question'] = question_json
    context['answers'] = []
    answers = Comment.objects.filter(qid=qid)
    for answer in answers:
        answer.answer_text = bleach.clean(markdown2.markdown(answer.answer_text), tags=['p', 'pre','code', 'sup', 'strong', 'hr', 'sub', 'a'])
        context['answers'].append(answer)
    return render(request, template_name, {'post': post,
                                            'question':question,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})        
    return render(request, 'question/questionpost.html', context)


def password_success2(request):
    # return render (request,'registration/password_success.html')
    messages.success(request, "Password has been succesfully changed.")
    return redirect("home")
def password_success(request):
    # return render (request,'registration/password_success.html')
    messages.success(request, "Password has been succesfully changed.")
    return redirect("home")
def home(request): 
    postss=Ask2.objects.all()
    context = {'postss':postss}
    return render(request, "home/home2.html",context)   
def view_profile(request): 
    return render(request, "registration/viewprofile.html")
# def home2(request):
#     return render(request, "home/home.html")
def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            subject = 'New message...'
            message =  f'''You have got a new message from {contact.name}.
            
            Name: {contact.name}
            
            Email: {contact.email}
            
            Phone: {contact.phone}
            
            Message: {contact.content}'''
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = ['jha36binayak@gmail.com', ] 
            send_mail( subject, message, email_from, recipient_list ) 
            messages.success(request, "Your message has been successfully sent")

    return render(request, "home/contact.html")

def search(request):
    query=request.GET['query']
    categ = request.GET["title2"]
    # title1 = request.GET['title2']
    if len(query)>78:
        allPosts=Ask2.objects.none()
    else:
        if categ == "all":
            allPostsTitle= Ask2.objects.filter(question_title__icontains=query)
            # allPostsCategory = Ask2.objects.filter(question_title__icontains=category)
            allPostsAuthor= Ask2.objects.filter(question_text__icontains=query)
            # allPostsContent =Post.objects.filter(content__icontains=query)
            allPosts=  allPostsTitle.union(allPostsAuthor)
        else:
            allPostsTitle= Ask2.objects.filter(question_title__icontains=query, question_title=categ)
            # allPostsCategory = Ask2.objects.filter(question_title__icontains=category)
            allPostsAuthor= Ask2.objects.filter(question_text__icontains=query, question_title=categ)
            # allPostsContent =Post.objects.filter(content__icontains=query)
            allPosts=  allPostsTitle.union(allPostsAuthor)

    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        # lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #check if user/email already exsist or not

        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
            messages.error(request, "Email and username already exsist.")
            return redirect('home')  

        if User.objects.filter(email=email).exists():
            messages.error(request, " Email already exsist.")
            return redirect('home')

        if User.objects.filter(username=username).exists():
            messages.error(request, " Username already exsist.")
            return redirect('home')
          

        # check for errorneous input

        if len(username)<3:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        emails=authenticate(email=email)
        if emails is not None:
            messages.error(request, "Email you entered already exists. Please login or use different email")
            return redirect("home")
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.save()     
        subject = 'Thankyou For Joining Us..'
        message = f'Hi {myuser.username}, thank you for registering in our website.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [myuser.email, ] 
        send_mail( subject, message, email_from, recipient_list ) 

        messages.success(request, " Your account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")
   

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')


def about(request): 
    return render(request, "home/about.html")

def detect(request):
    return render(request, 'home/detect.html')

def detected(request):
    return render(request, 'home/detected.html')


def category(request, category):
    post = Ask2.objects.filter(question_title=category)
    return render(request, 'home/category.html', {"post" : post})