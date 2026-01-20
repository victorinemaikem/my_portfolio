from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/comment/', views.comment_submit, name='comment_submit'),
    # SEO
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots'),
]
