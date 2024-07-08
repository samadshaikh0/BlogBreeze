from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

# In Django, a model is a Python class that represents a database table. Each attribute of the model class usually corresponds to a field in the table. Django models are defined in models.py files within Django apps.



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    tags = models.CharField(max_length=255)

    def set_tags(self, tags_list):
        self.tags = ','.join([tag for tag in tags_list])
        print(self.tags)
    
    def get_tags(self):
        return [f'#{tag}' for tag in self.tags.split(',')]
    
    def get_formatted_tags(self):
        return ' '.join(self.get_tags())

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
