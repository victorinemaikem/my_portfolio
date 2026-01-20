from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.html import escape
from django.views.decorators.cache import cache_page

from .models import (
    SiteSettings, Service, Education, Experience, Certification,
    PortfolioCategory, PortfolioProject, BlogPost, Comment
)
from .forms import ContactForm, CommentForm


def index(request):
    """Main portfolio page view."""
    
    context = {
        'settings': SiteSettings.get_settings(),
        'services': Service.objects.filter(is_active=True),
        'education': Education.objects.filter(is_active=True),
        'experience': Experience.objects.filter(is_active=True),
        'certifications': Certification.objects.filter(is_active=True),
        'portfolio_categories': PortfolioCategory.objects.all(),
        'portfolio_projects': PortfolioProject.objects.filter(is_active=True),
        'blog_posts': BlogPost.objects.filter(is_published=True)[:6],
        'contact_form': ContactForm(),
    }
    
    return render(request, 'index.html', context)


def blog_detail(request, slug):
    """Individual blog post detail view with comments."""
    
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Get approved top-level comments (not replies)
    comments = Comment.objects.filter(
        post=post, 
        is_approved=True, 
        parent=None
    ).prefetch_related('replies')
    
    # Initialize comment form
    comment_form = CommentForm()
    
    # Get related posts (same category or recent)
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'settings': SiteSettings.get_settings(),
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog_detail.html', context)


@require_POST
@csrf_protect
def comment_submit(request, slug):
    """Handle comment submission with security measures."""
    
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    form = CommentForm(request.POST)
    
    if form.is_valid():
        # Check honeypot
        if form.cleaned_data.get('website'):
            # Silently reject spam
            return JsonResponse({'success': False, 'message': 'Invalid submission.'}, status=400)
        
        comment = form.save(commit=False)
        comment.post = post
        
        # Handle reply
        parent_id = form.cleaned_data.get('parent_id')
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id, post=post, is_approved=True)
                comment.parent = parent_comment
            except Comment.DoesNotExist:
                pass
        
        # Escape content to prevent XSS
        comment.content = escape(comment.content)
        comment.author_name = escape(comment.author_name)
        
        comment.save()
        
        # Update comment count on post
        post.comments_count = Comment.objects.filter(post=post, is_approved=True).count() + 1
        post.save(update_fields=['comments_count'])
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your comment has been submitted and is awaiting moderation.'
        })
    else:
        errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
        return JsonResponse({
            'success': False,
            'message': 'Please correct the errors below.',
            'errors': errors
        }, status=400)


@require_POST
@csrf_protect
def contact_submit(request):
    """Handle contact form submission via AJAX."""
    
    form = ContactForm(request.POST)
    
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message! I will get back to you soon.'
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def sitemap_xml(request):
    """Generate dynamic XML sitemap for SEO."""
    
    domain = 'https://victorinemaikem.com'
    
    urls = []
    
    # Homepage
    urls.append({
        'loc': f'{domain}/',
        'lastmod': '2026-01-20',
        'changefreq': 'weekly',
        'priority': '1.0'
    })
    
    # Blog posts
    blog_posts = BlogPost.objects.filter(is_published=True)
    for post in blog_posts:
        urls.append({
            'loc': f'{domain}/blog/{post.slug}/',
            'lastmod': post.published_date.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8'
        })
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    return HttpResponse(xml_content, content_type='application/xml')


def robots_txt(request):
    """Serve robots.txt for search engine crawlers."""
    
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin",
        "Disallow: /admin/",
        "",
        "# Sitemap",
        "Sitemap: https://victorinemaikem.com/sitemap.xml"
    ]
    
    return HttpResponse("\n".join(lines), content_type="text/plain")
