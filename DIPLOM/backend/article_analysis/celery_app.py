from celery import Celery

# Replace with your broker URL (Redis or RabbitMQ)
app = Celery('tasks',
             broker='redis://localhost:6379/0',
             include=['tasks'])

# Configure the scheduler (beat)
app.conf.beat_schedule = {
    # Task running every 15 minutes
    'task-news-analysis': {
        'task': 'tasks.news_analysis',
        'schedule': 15 * 60,  # seconds
    },
    # Task running every hour
    'task-fact-recommendations_update': {
        'task': 'tasks.refresh_recommendations',
        'schedule': 60 * 60,  # seconds
    },
    # Task running every 24 hours
    'task-fact-checkers-analysis': {
        'task': 'tasks.fact_checkers_analysis',
        'schedule': 24 * 60 * 60,  # seconds
    },
    # Task running every 7 days
    'task-weekly-digest': {
        'task': 'tasks.weekly_digest',
        'schedule': 7 * 24 * 60 * 60,  # seconds
    },
}

# Optional configurations
app.conf.timezone = 'UTC'