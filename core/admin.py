from django.contrib import admin
from django.shortcuts import render
from .models import FAQ, Course, Post, Tag, Category, Consultation, NewsletterSubscriber, Service, Consultation
from core import models 

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'published_date', 'views_count')
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')



@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')  # অ্যাডমিন লিস্টে টাইটেল এবং অর্ডার দেখাবে
    search_fields = ('title',)        # টাইটেল দিয়ে সার্চ করা যাবে


def services_view(request):
    services = Service.objects.all().order_by('order')
    faqs = FAQ.objects.all() # এটি ডাটাবেস থেকে সব FAQ নিয়ে আসবে
    return render(request, 'services.html', {
        'services': services, 
        'faqs': faqs
    })



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # অ্যাডমিন লিস্টে যা যা কলাম হিসেবে দেখাবে
    list_display = ('title', 'price', 'duration', 'total_lessons', 'created_at')
    
    # যে ফিল্ডগুলোতে ক্লিক করলে এডিট করা যাবে
    list_links = ('title',)
    
    # ডানপাশে ফিল্টার অপশন (সহজে কোর্স খোঁজার জন্য)
    list_filter = ('created_at',)
    
    # সার্চ বার (নাম বা বর্ণনা দিয়ে খোঁজার জন্য)
    search_fields = ('title', 'description')






@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    # এই কলামগুলো অ্যাডমিন লিস্টে দেখাবে
    list_display = ('name', 'email', 'phone', 'created_at')
    
    # ডানপাশে ফিল্টার থাকবে
    list_filter = ('created_at',)
    
    # সার্চ বার থাকবে
    search_fields = ('name', 'email', 'phone', 'business_website')