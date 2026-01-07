from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    """Singleton model for site-wide settings and hero content."""
    
    hero_greeting = models.CharField(max_length=100, default="Hello, My name is")
    hero_name = models.CharField(max_length=100, default="Victorine Maikem")
    hero_title = models.CharField(max_length=200, default="Digital Health Systems Builder | AI in Healthcare | Health Informatics")
    hero_description = models.TextField()
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    
    about_title = models.CharField(max_length=200, default="Building digital health systems that solve real problems.")
    about_description = models.TextField()
    about_image = models.ImageField(upload_to='about/', blank=True, null=True)
    
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True)
    
    footer_text = models.CharField(max_length=200, default="Borox")
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    """Services/What I Do section."""
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Education(models.Model):
    """Education timeline entries."""
    
    degree = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=100, blank=True)  # e.g., "MHI", "First Class"
    institution = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', '-start_date']
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
    @property
    def date_range(self):
        if self.end_date:
            return f"{self.start_date.strftime('%B, %Y')} – {self.end_date.strftime('%B, %Y')}"
        return f"{self.start_date.strftime('%B, %Y')} – Present"


class Experience(models.Model):
    """Work experience timeline entries."""
    
    organization = models.CharField(max_length=200)
    role = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', '-start_date']
    
    def __str__(self):
        return f"{self.role} at {self.organization}"
    
    @property
    def date_range(self):
        if self.end_date:
            return f"{self.start_date.strftime('%b %Y')} – {self.end_date.strftime('%b %Y')}"
        return f"{self.start_date.strftime('%b %Y')} – Present"


class Certification(models.Model):
    """Professional certifications."""
    
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', '-year']
    
    def __str__(self):
        return self.title


class PortfolioCategory(models.Model):
    """Categories for portfolio filtering."""
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Portfolio Categories"
    
    def __str__(self):
        return self.name


class PortfolioProject(models.Model):
    """Portfolio projects."""
    
    title = models.CharField(max_length=150)
    categories = models.ManyToManyField(PortfolioCategory, related_name='projects')
    image = models.ImageField(upload_to='portfolio/')
    description = models.TextField()
    kicker = models.CharField(max_length=100, blank=True, help_text="Small text above title, e.g., 'AI in Healthcare • Academic Capstone'")
    role = models.CharField(max_length=100, blank=True, help_text="Your role in the project")
    link = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', '-id']
    
    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Blog/News posts."""
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100, default="Admin")
    image = models.ImageField(upload_to='blog/')
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    comments_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comments on blog posts with replies support."""
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Moderation
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"
    
    @property
    def is_reply(self):
        return self.parent is not None


class ContactSubmission(models.Model):
    """Contact form submissions."""
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
