"""
main.py
--------
نقطه ورود اصلی برنامه.
این فایل رو اجرا می‌کنی: python main.py

کاری که می‌کنه:
1. دیتابیس محلی رو آماده می‌کنه
2. هر N دقیقه (پیش‌فرض ۱۵) خودکار ایمیل‌های جدید رو چک می‌کنه
3. هر ایمیل جدید رو با AI تحلیل می‌کنه
4. اگه مهم بود، نوتیف ویندوزی نشون میده
5. نتیجه رو ذخیره می‌کنه تا دوباره پردازش نشه
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from database import init_db, is_already_processed, save_processed_email
from gmail_service import get_new_emails
from ai_analyzer import analyze_email
from notifier import notify_user

load_dotenv()

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_MINUTES", "15"))


def check_emails_job():
    """این تابع هر بار که scheduler بیدار میشه، اجرا میشه."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] در حال بررسی ایمیل‌های جدید...")

    try:
        emails = get_new_emails(max_results=10)
    except Exception as e:
        print(f"خطا در دریافت ایمیل‌ها: {e}")
        return

    new_count = 0

    for email in emails:
        if is_already_processed(email["id"]):
            continue  # قبلاً بررسی شده، رد شو

        new_count += 1
        decision = analyze_email(email["subject"], email["sender"], email["snippet"])

        print(f"  - '{email['subject'][:50]}' → {decision}")

        if decision == "IMPORTANT_ACTION":
            notify_user("⚡ نیاز به اقدام", email["subject"])
        elif decision == "IMPORTANT_INFO":
            notify_user("ℹ️ ایمیل مهم", email["subject"])
        # IGNORE → هیچ نوتیفی فرستاده نمیشه

        save_processed_email(email["id"], email["subject"], email["sender"], decision)

    if new_count == 0:
        print("  ایمیل جدیدی نبود.")
    else:
        print(f"  {new_count} ایمیل جدید پردازش شد.")


def main():
    print("=" * 50)
    print("Email Agent - در حال راه‌اندازی...")
    print("=" * 50)

    init_db()

    # اولین بار رو بلافاصله اجرا کن، منتظر ۱۵ دقیقه اول نمون
    check_emails_job()

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_emails_job, "interval", minutes=CHECK_INTERVAL)
    scheduler.start()

    print(f"\nسیستم فعاله. هر {CHECK_INTERVAL} دقیقه خودکار چک می‌کنه.")
    print("برای توقف: Ctrl+C را بزن.\n")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\nمتوقف شد.")


if __name__ == "__main__":
    main()
