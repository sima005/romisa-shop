# رمـیصا | Rumisa Shop

فروشگاه اینترنتی چادر با Django و طراحی RTL بر اساس فایل Figma پروژه Rumisa Shop.

## امکانات
- صفحه خانه مطابق طراحی Figma
- فروشگاه با جستجو و دسته‌بندی
- صفحه جزئیات محصول
- تنوع رنگ با قیمت و موجودی مستقل
- سبد خرید session-based
- ثبت سفارش و پیگیری وضعیت در پنل
- فرم تماس و مدیریت پیام‌ها
- پنل کامل Django Admin برای محصولات، دسته‌ها، تنوع‌ها، سفارش‌ها و پیام‌ها
- آپلود تصویر محصول از پنل
- طراحی responsive برای موبایل و دسکتاپ

## اجرا

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

سایت: `http://127.0.0.1:8000/`
پنل مدیریت: `http://127.0.0.1:8000/admin/`

برای تولید واقعی، `SECRET_KEY` و `DEBUG` را در environment تنظیم کنید و یک دیتابیس production و سرویس پرداخت واقعی اضافه کنید.
