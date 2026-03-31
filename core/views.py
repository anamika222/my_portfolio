

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ConsultationForm
from .models import FAQ, Consultation, Course, MultiCertificate, Post, Service
from .models import NewsletterSubscriber, Tag
from django.contrib import messages
from .models import ContactMessage
from django.contrib.auth.models import User


# ১. হোম পেইজ ভিউ (সব পোস্ট দেখানোর জন্য)
def home(request):
   # সর্বশেষ ৩টি ব্লগ নিয়ে আসা (নতুনগুলো আগে দেখাবে)
    recent_blogs = Post.objects.order_by('-published_date')[:5]
    
    # সব সার্ভিসগুলো নিয়ে আসা
    services = Service.objects.all().order_by('order')

    courses = Course.objects.all().order_by('-created_at')
    
    context = {
        'recent_blogs': recent_blogs,
        'services': services,
        'courses': courses,
    }
    return render(request, 'index.html', context)




# ৪. ডিজিটাল মার্কেটিং ক্যাটাগরি ভিউ
def digital_marketing_view(request):
    # মেইন ক্যাটাগরি ফিল্টার
    posts = Post.objects.filter(category__name__icontains='Digital Marketing')
    
    # URL থেকে 'tag' প্যারামিটার চেক করা (যেমন: ?tag=SEO)
    selected_tag = request.GET.get('tag')
    
    if selected_tag:
        # যদি ইউজার কোনো ট্যাগে ক্লিক করে, তবে আরও ফিল্টার হবে
        posts = posts.filter(content__icontains=selected_tag) # অথবা model-এ tag থাকলে সেটা দিয়ে
        
    posts = posts.order_by('-published_date')
    
    context = {
        'posts': posts,
        'selected_tag': selected_tag
    }
    return render(request, 'digital_marketing.html', context)

# ৫. ফ্রিল্যান্সিং ক্যাটাগরি ভিউ
def freelancing_view(request):
    posts = Post.objects.filter(category__name__icontains='Freelancing').order_by('-published_date')
    return render(request, 'freelancing.html', {'posts': posts})

# ৬. কর্পোরেট গ্রোথ ক্যাটাগরি ভিউ
def corporate_view(request):
    posts = Post.objects.filter(category__name__icontains='Corporate').order_by('-published_date')
    return render(request, 'corporate.html', {'posts': posts})

# ৭. ব্লগের ভেতরের ডিটেইল পেইজ ভিউ
def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog_detail.html', {'post': post})




def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            # ইমেইলটি আগে থেকেই আছে কি না চেক করে সেভ করা
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "ধন্যবাদ! আপনি সফলভাবে সাবস্ক্রাইব করেছেন।")
            else:
                messages.info(request, "আপনি ইতিমধ্যে সাবস্ক্রাইব করে আছেন।")
        
        # যে পেজ থেকে রিকোয়েস্ট এসেছে সেখানেই ফেরত পাঠানো
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    


def freelancing_view(request):
    posts = Post.objects.filter(category__name__icontains='Freelancing')
    tags = Tag.objects.all()
    
    # সার্চ লজিক
    query = request.GET.get('q')
    if query:
        posts = posts.filter(title__icontains=query)
        
    # ট্যাগ ফিল্টার
    selected_tag = request.GET.get('tag')
    if selected_tag:
        posts = posts.filter(tags__slug=selected_tag)
        
    return render(request, 'freelancing.html', {
        'posts': posts.order_by('-published_date'),
        'tags': tags
    })
def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # 👇 পোস্টটি ওপেন করলেই ভিউ ১ বাড়বে
    post.views_count += 1
    post.save()
    
    return render(request, 'blog_detail.html', {'post': post})


def corporate_view(request):
    # ক্যাটাগরির নাম 'Corporate Growth' এর সাথে মিল রেখে ফিল্টার
    posts = Post.objects.filter(category__name='Corporate Growth Strategy').order_by('-published_date')
    
    return render(request, 'corporate.html', {
        'posts': posts,
    })



def services_view(request):
    if request.method == 'POST':
        # কন্টাক্ট ফর্মের কোড যা আগে ছিল...
        # (এখানে মেসেজ সেভ করার লজিকটুকু রাখুন)
        return redirect('services')

    # শুধু সার্ভিস এবং এফএকিউ ডাটা পাঠাবেন
    services = Service.objects.all().order_by('order')
    faqs = FAQ.objects.all()
    
    context = {
        'services': services,
        'faqs': faqs,
    }
    return render(request, 'services.html', context)



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # ডাটাবেসে সেভ করা
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # সফলতার মেসেজ দেখানো
        messages.success(request, "আপনার মেসেজটি সফলভাবে পাঠানো হয়েছে! আমি শীঘ্রই যোগাযোগ করব।")
        return redirect('contact') # আপনার কন্টাক্ট ইউআরএল এর নাম দিন

    return render(request, 'contact.html')



def blog_list_view(request):
    # এখানে চাইলে আপনি আপনার Post মডেল থেকে সব ডেটা আনতে পারেন
    # posts = Post.objects.all()
    return render(request, 'blog_list.html')


from django.shortcuts import render

# সার্টিফিকেট পেজের জন্য ভিউ
def cert_page(request):
    return render(request, 'certificates.html')

# অভিজ্ঞতার সার্টিফিকেট পেজের জন্য ভিউ (এটি মিসিং ছিল)
def exp_page(request):
    return render(request, 'testimonials.html')



def course_detail(request, course_id):
    # স্লাগ (slug) অনুযায়ী নির্দিষ্ট কোর্সটি খুঁজে বের করবে
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_details.html', {'course': course})


# views.py

def courses_view(request):
    # ডাটাবেস থেকে সব কোর্স নিয়ে আসা হচ্ছে
    all_courses = Course.objects.all().order_by('-created_at') 
    
    context = {
        'courses': all_courses, # এই 'courses' ভেরিয়েবলটিই HTML-এ লুপে ব্যবহার হবে
    }
    return render(request, 'courses.html', context)


def free_consultation(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')

        # ডাটাবেজে সেভ
        Consultation.objects.create(
            name=name, 
            email=email, 
            phone=phone, 
            description=description
        )
        
        messages.success(request, "ধন্যবাদ! আপনার বুকিং সফল হয়েছে। আমি শীঘ্রই যোগাযোগ করব।")
        return redirect('free_consultation')

    return render(request, 'consultation.html')

# core/views.py

def exp_page(request):
    #cert_set = MultiCertificate.objects.last()
    # এখানে 'testimonials.html' কেটে 'experience_certificate.html' লিখুন
    return render(request, 'experience_certificate.html')




from django.contrib.auth.models import User
from django.http import HttpResponse

def force_password_reset(request):
    username = 'soptok'
    password = 'Soptok@#$234' # এটি আপনার একদম নতুন পাসওয়ার্ড
    
    # ১. পুরনো ইউজার থাকলে তা মুছে ফেলবে
    User.objects.filter(username=username).delete()
    
    # ২. নতুন করে সুপার ইউজার তৈরি করবে
    new_user = User.objects.create_superuser(
        username=username, 
        email='admin@example.com', 
        password=password
    )
    
    # ৩. অতিরিক্ত নিরাপত্তা হিসেবে ইউজারকে একটিভ করে দেবে
    new_user.is_active = True
    new_user.is_staff = True
    new_user.is_superuser = True
    new_user.save()
    
    return HttpResponse(f"Everything Cleaned! User '{username}' created. Login with: {password}")