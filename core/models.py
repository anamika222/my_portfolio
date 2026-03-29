from django.db import models
from django.utils import timezone


# ২. ক্যাটাগরি মডেল
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories" # অ্যাডমিন প্যানেলে বানান ঠিক দেখাবে

    def __str__(self):
        return self.name

# ৩. ট্যাগ মডেল
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# ৪. মেইন ব্লগ পোস্ট মডেল
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100, default="Soptok Chatterjee")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='blog_thumbnails/')
    published_date = models.DateTimeField(default=timezone.now)
    read_time = models.CharField(max_length=20, help_text="যেমন: 5 min read") 
    tags = models.ManyToManyField(Tag, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_date'] # নতুন পোস্ট সবসময় উপরে থাকবে

    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        # অটোমেটিক রিডিং টাইম ক্যালকুলেটর
        word_count = len(self.content.split())
        read_time = round(word_count / 200)
        return read_time if read_time > 0 else 1

# ৫. নিউজলেটার সাবস্ক্রাইবার মডেল
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Service(models.Model):
    icon = models.CharField(max_length=50, help_text="FontAwesome icon (e.g., fa-share-nodes)")
    title = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField(help_text="পয়েন্টগুলো কমা (,) দিয়ে লিখুন। যেমন: Facebook Ads, Content Plan", blank=True)
    order = models.IntegerField(default=0)

    def get_features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]

    def __str__(self):
        return self.title
    

class Course(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='courses/')
    description = models.TextField()
    price = models.IntegerField()
    duration = models.CharField(max_length=100) # যেমন: ৩ মাস
    total_lessons = models.IntegerField()
    enroll_link = models.URLField(blank=True, null=True) # যদি পেমেন্ট গেটওয়ে বা অন্য লিংক থাকে
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    


class Consultation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True) # ফোন নম্বর ঐচ্ছিক করা হলো
    # verbose_name দিলে অ্যাডমিন প্যানেলে এই বাংলা লেখাটি দেখাবে
    description = models.TextField(blank=True, null=True, verbose_name="বিস্তারিত")
    goal = models.TextField(blank=True, null=True) # যদি ভবিষ্যতে লাগে তাই রাখা হলো
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"



class MultiCertificate(models.Model):
    title = models.CharField(max_length=255, default="Professional Experience Certificates")
    # ৩টি ছবির জন্য আলাদা ফিল্ড
    akr_cert = models.ImageField(upload_to='certificates/', verbose_name="AKR Technology")
    infinity_cert = models.ImageField(upload_to='certificates/', verbose_name="Infinity Technology")
    elearning_cert = models.ImageField(upload_to='certificates/', verbose_name="e-Learning & Earning")

    def __str__(self):
        return self.title