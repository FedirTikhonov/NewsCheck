import time
import json
from datetime import datetime
from celery.signals import task_prerun, task_postrun
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=1)  # Using db=1 to separate from Celery


@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Record when task starts"""
    redis_client.set(f"task_start_{task_id}", time.time(), ex=3600)  # Expire after 1 hour


@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None,
                         retval=None, state=None, **kwds):
    """Record task completion and calculate execution time"""
    start_time_key = f"task_start_{task_id}"
    start_time = redis_client.get(start_time_key)

    if start_time:
        execution_time = time.time() - float(start_time)

        # Store execution data
        execution_data = {
            'task_name': task.name if task else 'unknown',
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat(),
            'state': state,
            'task_id': task_id
        }

        # Store in a list for each task type (keep last 100 executions)
        task_name = task.name if task else 'unknown'
        redis_client.lpush(f"task_executions_{task_name}", json.dumps(execution_data))
        redis_client.ltrim(f"task_executions_{task_name}", 0, 99)  # Keep only last 100

        # Also store in a general list for all tasks
        redis_client.lpush("all_task_executions", json.dumps(execution_data))
        redis_client.ltrim("all_task_executions", 0, 499)  # Keep last 500 overall

        # Clean up
        redis_client.delete(start_time_key)

        print(f"Task {task_name} completed in {execution_time:.2f} seconds")


def get_task_execution_times(task_name=None, limit=50):
    """
    Get execution time data for charting

    Args:
        task_name: Specific task name (e.g., 'tasks.news_analysis') or None for all tasks
        limit: Number of recent executions to retrieve

    Returns:
        Dictionary with arrays for timestamps, execution_times, and task_names
    """
    if task_name:
        key = f"task_executions_{task_name}"
    else:
        key = "all_task_executions"

    # Get recent executions
    raw_data = redis_client.lrange(key, 0, limit - 1)

    timestamps = []
    execution_times = []
    task_names = []
    states = []

    for data in raw_data:
        try:
            execution_data = json.loads(data.decode())
            timestamps.append(execution_data['timestamp'])
            execution_times.append(execution_data['execution_time'])
            task_names.append(execution_data['task_name'])
            states.append(execution_data.get('state', 'UNKNOWN'))
        except (json.JSONDecodeError, KeyError):
            continue

    return {
        'timestamps': timestamps,
        'execution_times': execution_times,
        'task_names': task_names,
        'states': states,
        'count': len(timestamps)
    }


def get_task_stats(task_name=None):
    """Get basic statistics for task execution times"""
    data = get_task_execution_times(task_name, limit=100)

    if not data['execution_times']:
        return None

    execution_times = data['execution_times']

    return {
        'task_name': task_name or 'all_tasks',
        'count': len(execution_times),
        'avg_time': sum(execution_times) / len(execution_times),
        'min_time': min(execution_times),
        'max_time': max(execution_times),
        'recent_executions': data['execution_times'][:10]  # Last 10 executions
    }


def print_task_stats():
    """Convenient function to print stats for all your tasks"""
    task_names = [
        'tasks.news_analysis',
        'tasks.fact_checkers_analysis',
        'tasks.weekly_digest',
        'tasks.refresh_recommendations'
    ]

    print("=" * 60)
    print("CELERY TASK EXECUTION STATISTICS")
    print("=" * 60)

    for task_name in task_names:
        stats = get_task_stats(task_name)
        if stats:
            print(f"\n{task_name}:")
            print(f"  Total executions: {stats['count']}")
            print(f"  Average time: {stats['avg_time']:.2f}s")
            print(f"  Min time: {stats['min_time']:.2f}s")
            print(f"  Max time: {stats['max_time']:.2f}s")
        else:
            print(f"\n{task_name}: No execution data")


# Example usage for creating a simple chart
def create_simple_chart(task_name=None):
    """Create a simple text-based chart (you can replace with matplotlib/plotly)"""
    data = get_task_execution_times(task_name, limit=20)

    if not data['execution_times']:
        print("No data available for charting")
        return

    print(f"\nExecution Times Chart for {task_name or 'All Tasks'}")
    print("-" * 50)

    # Simple text chart
    max_time = max(data['execution_times'])
    for i, (time_val, task_name_val) in enumerate(zip(data['execution_times'], data['task_names'])):
        bar_length = int((time_val / max_time) * 30)
        bar = "█" * bar_length
        print(f"{i + 1:2d}: {bar:<30} {time_val:.2f}s ({task_name_val.split('.')[-1]})")


if __name__ == "__main__":
    print_task_stats()
