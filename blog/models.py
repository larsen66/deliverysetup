from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"

class BlogTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(blank=True, help_text="A short summary of the post")
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    
    # Script field
    script = models.TextField(
        blank=True, 
        null=True,
        help_text="Custom JavaScript code for this blog post"
    )
    
    # Meta data
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=200, blank=True, help_text="SEO keywords (comma-separated)")
    
    # Relations
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')
    
    # Status and dates
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Reading time
    reading_time = models.PositiveIntegerField(default=0, help_text="Estimated reading time in minutes")
    
    def get_absolute_url(self):
        """
        Returns the absolute URL for the blog post, used by sitemap and templates
        """
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Calculate reading time
        if self.content:
            words_per_minute = 200  # Average reading speed
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / words_per_minute))
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
