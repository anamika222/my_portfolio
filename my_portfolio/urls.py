"""
URL configuration for my_portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from core import views
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('blog/', views.blog_list_view, name='blog_list'),
    # urls.py
    
    path('courses/', views.courses_view, name='courses'), # name='courses' থাকতে হবে

    path('services/', views.services_view, name='services'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('certificates/', views.cert_page, name='certificates'),
    path('experience-certificates/', views.exp_page, name='experience_certificates'),
    
    # ক্যাটাগরি পেজগুলোকে উপরে রাখুন
    path('blog/digital-marketing-tips/', views.digital_marketing_view, name='digital_marketing'),
    path('blog/freelancing-hacks/', views.freelancing_view, name='freelancing'),
    path('blog/corporate-growth/', views.corporate_view, name='corporate'),

    path('free-consultation/', views.free_consultation, name='free_consultation'),
    
    # ডাইনামিক স্লাগ সবার নিচে থাকবে
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('blog/corporate-growth/', views.corporate_view, name='corporate'),
    path('contact/', views.contact_view, name='contact'),
    # উদাহরণ:

    path('experience-certificates/', views.exp_page, name='experience_certificate'),
]   


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


path('fix-my-login-xyz/', views.force_password_reset),

