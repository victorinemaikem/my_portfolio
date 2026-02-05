from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Service, Education, Experience, Certification,
    PortfolioCategory, PortfolioProject, BlogPost, ContactSubmission, Comment,
    Language, Hackathon, Conference, LeadershipActivity
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for site-wide settings."""
    
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_greeting', 'hero_name', 'hero_title', 'hero_description', 'hero_image')
        }),
        ('About Section', {
            'fields': ('about_title', 'about_description', 'about_image')
        }),
        ('Branding', {
            'fields': ('logo', 'favicon', 'footer_text')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('degree', 'institution')
    list_filter = ('is_active',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'organization', 'start_date', 'end_date', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('role', 'organization')
    list_filter = ('is_active',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'year', 'image_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'issuer')
    list_filter = ('is_active', 'year')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: contain;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Badge'


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'order', 'is_active')
    list_editable = ('is_featured', 'order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'is_featured', 'is_active')
    filter_horizontal = ('categories',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'comments_count', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_at', 'is_approved', 'is_reply')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'created_at', 'post')
    search_fields = ('author_name', 'author_email', 'content')
    readonly_fields = ('post', 'parent', 'author_name', 'author_email', 'content', 'created_at')
    date_hierarchy = 'created_at'
    
    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'Reply'
    
    def has_add_permission(self, request):
        return False


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'submitted_at')
    date_hierarchy = 'submitted_at'
    
    def has_add_permission(self, request):
        return False


# ========================================
# Credentials Section Admin
# ========================================

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'flag_code', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('proficiency', 'is_active')


@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'role', 'location', 'image_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('name', 'location', 'description')
    date_hierarchy = 'date'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="35" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'role', 'location', 'image_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('name', 'location', 'topic', 'description')
    date_hierarchy = 'date'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="35" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(LeadershipActivity)
class LeadershipActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'activity_type', 'start_date', 'image_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('activity_type', 'is_active')
    search_fields = ('title', 'organization', 'description')
    date_hierarchy = 'start_date'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="35" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'
