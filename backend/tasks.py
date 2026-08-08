import csv
import io
import os
from datetime import datetime, timedelta

from celery_app import FlaskTask, celery_app
from flask import render_template
from mail import send_email
from db.models import db, User, Trek, Booking


# task test
# @celery_app.task(base=FlaskTask)
# def test_notification():
#     from datetime import datetime
#     print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Test notification fired")
#     return {"status": "completed"}


@celery_app.task(base=FlaskTask)
def monthly_activity_report():
    current_month = datetime.now().month
    current_year = datetime.now().year

    # TEST MODE / FLIP THE LINES FOR ACTUAL PRODUCTION
    prev_month = current_month
    # prev_month = current_month - 1 if current_month > 1 else 12

    year = current_year if current_month > 1 else current_year - 1
    month_start = datetime(year, prev_month, 1)
    month_end = datetime(year + 1, 1, 1) if prev_month == 12 else datetime(year, prev_month + 1, 1)

    month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                  7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}[prev_month]

    # bookings made inside the target month
    monthly_bookings = Booking.query.filter(
        Booking.booking_date >= month_start,
        Booking.booking_date < month_end,
    ).all()

    # group bookings per trek to find the popular ones
    trek_counts = {}
    for b in monthly_bookings:
        trek_counts[b.trek_id] = trek_counts.get(b.trek_id, 0) + 1

    popular = []
    for trek_id, count in sorted(trek_counts.items(), key=lambda x: x[1], reverse=True):
        trek = db.session.get(Trek, trek_id)
        if trek:
            popular.append({
                'name': trek.name,
                'location': trek.location,
                'difficulty': trek.difficulty,
                'bookings': count,
            })

    # count of treks happened in that month
    conducted = Trek.query.filter(
        Trek.start_date >= month_start.date(),
        Trek.start_date < month_end.date(),
    ).count()
    participant_ids = {b.user_id for b in monthly_bookings}

    summary = {
        'treks': conducted,
        'users': len(participant_ids),
        'bookings': len(monthly_bookings),
    }

    rendered_html = render_template(
        'monthly_report.html',
        summary=summary,
        popular=popular,
        month=month_name,
        year=year,
    )

    admin_email = os.getenv('ADMIN_EMAIL', 'admin@trekbase.com')
    success = send_email(admin_email, f"Monthly Trekking Activity Report - {month_name} {year}", rendered_html)

    print(f"Monthly report sent to {admin_email}" if success else f"Failed to send monthly report to {admin_email}")
    return {
        "status": "completed" if success else "failed",
        "month": f"{month_name} {year}",
        "summary": summary,
        "popular_treks": popular,
    }


@celery_app.task(base=FlaskTask)
def daily_trek_reminders():
    today = datetime.now().date()
    horizon = today + timedelta(days=7)

    # treks that start within the next 7 days
    upcoming = Trek.query.filter(
        Trek.start_date >= today,
        Trek.start_date <= horizon,
    ).all()

    # group each user's upcoming bookings -> one email per user
    user_bookings = {}
    for trek in upcoming:
        for b in Booking.query.filter_by(trek_id=trek.id, status='booked').all():
            b.trek = trek
            user_bookings.setdefault(b.user_id, []).append(b)

    users_notified = 0
    for user_id, bookings in user_bookings.items():
        user = db.session.get(User, user_id)
        if not user:
            continue
        rendered_html = render_template('trek_reminder.html', user=user, bookings=bookings)
        success = send_email(user.email, "Upcoming Trek Reminder - TrekBase", rendered_html)
        if success:
            users_notified += 1
            print(f"Reminder sent to {user.name} ({user.email})")
        else:
            print(f"Failed to send reminder to {user.name} ({user.email})")

    return {
        "status": "completed",
        "upcoming_treks": len(upcoming),
        "users_notified": users_notified,
    }


@celery_app.task(base=FlaskTask)
def export_booking_history_csv(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "User not found"}

    bookings = Booking.query.filter_by(user_id=user_id).all()
    if not bookings:
        return {"error": "No bookings found"}

    # build the CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["User ID", "User Name", "Trek Name", "Location", "Booking Status", "Start Date", "End Date", "Booked On"])

    for b in bookings:
        trek = db.session.get(Trek, b.trek_id)
        writer.writerow([
            user.id,
            user.name,
            trek.name if trek else '-',
            trek.location if trek else '-',
            b.status,
            trek.start_date if trek else '-',
            trek.end_date if trek else '-',
            b.booking_date,
        ])

    csv_content = output.getvalue()
    output.close()

    return {
        "status": "success",
        "user_name": user.name,
        "csv_content": csv_content,
        "record_count": len(bookings),
    }