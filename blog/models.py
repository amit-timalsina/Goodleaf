
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.timezone import now
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="media/static/images/")
    facebook_url= models.CharField(max_length=255, null= True, blank=True)
    Instagram_url= models.CharField(max_length=255, null= True, blank=True)
    Twitter_url= models.CharField(max_length=255, null= True, blank=True)

    
    def __str__(self):
        return str(self.user)

# class Ask(models.Model):
#     sno=models.AutoField(primary_key=True)
#     title=models.CharField(max_length=255)
#     author=models.CharField(max_length=14)
#     slug=models.CharField(max_length=130)
#     timeStamp=models.DateTimeField(blank=True)
#     content=models.TextField()

#     def __str__(self):
#         return self.title + " by " + self.author
class Ask2(models.Model):
    qid = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=100)
    question_text = models.TextField(max_length=50000)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.TextField(max_length=20)
    slug = models.SlugField(max_length=40)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question_title)
        super(Ask2, self).save(*args, **kwargs)
    def __str__(self):
        return self.question_text + " by " + self.posted_by

class Comment(models.Model):
    qid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Ask2,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    


