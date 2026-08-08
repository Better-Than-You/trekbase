import os

from celery import Celery, Task
from celery.schedules import crontab
import celery.app.trace
from flask import Flask

from cache import REDIS_URL
from mail import init_mail

celery_app = Celery(
    'trekbase_tasks',
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# "if it works, dont touch it" code:
celery.app.trace.setup_worker_optimizations = lambda *args, **kwargs: None

celery_app.conf.update(
    imports=('tasks',),
    timezone='Asia/Kolkata',
    beat_schedule={
        # 'test-notification-every-10s': {
        #     'task': 'tasks.test_notification',
        #     'schedule': 10.0,
        # testign
        # },
        'daily-trek-reminders': {
            'task': 'tasks.daily_trek_reminders',
            'schedule': crontab(hour=7, minute=0),  # every 7am
        },
        'monthly-activity-report': {
            'task': 'tasks.monthly_activity_report',
            'schedule': crontab(hour=8, minute=0, day_of_month=1),  # 1st of every month, 8am
        },
    }
)


def get_flask_app() -> Flask:
    """Create a minimal Flask app so Celery tasks can use db + mail."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///trekbase.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')
    init_mail(app)

    from db.models import db
    db.init_app(app)

    return app


class FlaskTask(Task):
    """Celery task that runs inside a Flask app context."""
    _flask_app = None

    @property
    def flask_app(self):
        if self._flask_app is None:
            self._flask_app = get_flask_app()
        return self._flask_app

    def __call__(self, *args, **kwargs):
        with self.flask_app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = FlaskTask