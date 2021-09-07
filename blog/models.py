from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import  reverse

# Create your models here.

# create model manager for published status
class PublisherManager(models.Manager):
    def get_queryset(self):
        return super(PublisherManager, self).get_queryset()\
            .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    # the default manager
    objects = models.Manager() 
    #our custom manager
    published = PublisherManager() 

    # caninical url
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                    args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Meta:
    ordering = ('-publish',)
    # publish posts in descending order
    def __str__(self):
        return self.title 
