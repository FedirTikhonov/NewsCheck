from celery import Celery
import celery_montiroing


app = Celery('tasks',
             broker='redis://localhost:6379/0',
             include=['tasks'])

app.conf.beat_schedule = {
    'task-news-analysis': {
        'task': 'tasks.news_analysis',
        'schedule': 15 * 60,
    },
    'task-fact-recommendations_update': {
        'task': 'tasks.refresh_recommendations',
        'schedule': 60 * 60,
    },
    'task-fact-checkers-analysis': {
        'task': 'tasks.fact_checkers_analysis',
        'schedule': 24 * 60 * 60,
    },
    'task-weekly-digest': {
        'task': 'tasks.weekly_digest',
        'schedule': 7 * 24 * 60 * 60,
    },
}

app.conf.timezone = 'UTC'