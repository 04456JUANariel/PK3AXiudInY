# 代码生成时间: 2025-09-13 15:52:19
#!/usr/bin/env python

"""
Task Scheduler using Falcon framework and APScheduler.
This script creates a HTTP server that acts as a task scheduler, allowing
users to add, remove, and list tasks.
"""

import falcon
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Tasks storage
tasks = {}

# Falcon API resource class for tasks
class TaskResource:
    def on_get(self, req, resp):
        """
        Handle GET requests to retrieve a list of tasks.
        """"
        resp.media = {'tasks': tasks}
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        Handle POST requests to add a new task.
        """"
        try:
            data = json.loads(req.stream.read())
            task_id = data.get('id')
            task_func = data.get('function')
            task_args = data.get('args', ())
            task_kwargs = data.get('kwargs', {})
            schedule_time = data.get('schedule_time')

            if not (task_id and task_func and schedule_time):
                raise ValueError('Missing required fields')

            # Add task to scheduler
            scheduler.add_job(task_func, 'date', run_date=schedule_time, args=task_args, kwargs=task_kwargs)
            tasks[task_id] = {'function': task_func, 'args': task_args, 'kwargs': task_kwargs, 'schedule_time': schedule_time}

            resp.media = {'status': 'Task added successfully'}
            resp.status = falcon.HTTP_201
        except (ValueError, json.JSONDecodeError) as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_400

    def on_delete(self, req, resp, task_id):
        """
        Handle DELETE requests to remove a task.
        """"
        try:
            if task_id in tasks:
                # Remove task from scheduler
                scheduler.remove_job(task_id)
                del tasks[task_id]
                resp.media = {'status': 'Task removed successfully'}
                resp.status = falcon.HTTP_200
            else:
                resp.media = {'error': 'Task not found'}
                resp.status = falcon.HTTP_404
        except Exception as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_500

# Falcon API app
app = falcon.API()

# Add routes
app.add_route('/tasks', TaskResource())
app.add_route('/tasks/{task_id}', TaskResource())

# Define a simple task function for demonstration
def demo_task():
    print(f"Demo task executed at {datetime.now()}")

# Add demo task
scheduler.add_job(demo_task, 'interval', seconds=10)
tasks['demo_task'] = {'function': demo_task.__name__, 'args': (), 'kwargs': {}, 'schedule_time': 'interval'}

# Main function to run the app
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Task Scheduler using Falcon and APScheduler')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind the server to')
    args = parser.parse_args()

    # Run the Falcon app
    app.run(host=args.host, port=args.port, debug=True)

if __name__ == '__main__':
    main()