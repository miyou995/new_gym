from celery.app import default_app
from client.models import Client
from datetime import datetime, timedelta, date


def output_all_clients():
    all_client = Client.objects.all()
    for client in all_client:
        client.init_output()
    return
    
        
        





def revoke_all_tasks():
    i = default_app.control.inspect()
    active_tasks = i.active()

    for worker, tasks in active_tasks.items():
        for task in tasks:
            task_id = task['id']
            default_app.control.revoke(task_id, terminate=True)
            print(f"Revoked task {task_id}")