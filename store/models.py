from django.conf import settings
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField('نام دسته‌بندی', max_length=80)
    slug = models.SlugField(unique=True, allow_unicode=True)
    active = models.BooleanField('فعال', default=True)
    class Meta: verbose_name='دسته‌بندی'; verbose_name_plural='دسته‌بندی‌ها'
    def __str__(self): return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [('simple','ساده'),('formal','مجلسی'),('daily','روزمره')]
    name = models.CharField('نام محصول', max_length=180)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField('توضیحات', blank=True)
    fabric = models.CharField('جنس پارچه', max_length=120, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='دسته‌بندی')
    base_price = models.PositiveIntegerField('قیمت پایه (تومان)')
    discount_percent = models.PositiveSmallIntegerField('تخفیف درصدی', default=0)
    image = models.ImageField('تصویر', upload_to='products/', blank=True, null=True)
    featured = models.BooleanField('نمایش در نیو کالکشن', default=False)
    active = models.BooleanField('فعال', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']; verbose_name='محصول'; verbose_name_plural='محصولات'
    def __str__(self): return self.name
    @property
    def final_price(self): return int(self.base_price * (100-self.discount_percent)/100)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='محصول')
    color_name = models.CharField('نام رنگ', max_length=60)
    color_hex = models.CharField('کد رنگ', max_length=7, default='#111111')
    price = models.PositiveIntegerField('قیمت این رنگ (تومان)')
    stock = models.PositiveIntegerField('موجودی', default=0)
    active = models.BooleanField('فعال', default=True)
    class Meta: verbose_name='تنوع محصول'; verbose_name_plural='تنوع‌های محصول'
    def __str__(self): return f'{self.product.name} - {self.color_name}'

class Order(models.Model):
    STATUS = [('pending','در انتظار پرداخت'),('paid','پرداخت شده'),('processing','در حال آماده‌سازی'),('shipped','ارسال شده'),('completed','تکمیل شده'),('cancelled','لغو شده')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    customer_name = models.CharField('نام مشتری', max_length=120)
    phone = models.CharField('شماره تماس', max_length=30)
    address = models.TextField('آدرس')
    status = models.CharField('وضعیت', max_length=20, choices=STATUS, default='pending')
    total = models.PositiveIntegerField('مبلغ کل', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']; verbose_name='سفارش'; verbose_name_plural='سفارش‌ها'
    def __str__(self): return f'سفارش #{self.pk} - {self.customer_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='محصول')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='رنگ')
    quantity = models.PositiveIntegerField('تعداد', default=1)
    unit_price = models.PositiveIntegerField('قیمت واحد')
    def __str__(self): return f'{self.product} × {self.quantity}'

class ContactMessage(models.Model):
    name = models.CharField('نام', max_length=120)
    contact = models.CharField('ایمیل یا شماره تماس', max_length=120)
    message = models.TextField('پیام')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField('خوانده شده', default=False)
    class Meta: ordering=['-created_at']; verbose_name='پیام تماس'; verbose_name_plural='پیام‌های تماس'
    def __str__(self): return f'{self.name} - {self.contact}'
