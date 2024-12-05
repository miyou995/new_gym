from celery.app import default_app
from client.models import Client
from datetime import datetime, timedelta, date
import logging 
logger = logging.getLogger(__name__)

def output_all_clients():
    all_client = Client.objects.all()
    for client in all_client:
        client.init_output()
    return
    
        
        
def get_celery_worker_status():
    i = default_app.control.inspect()
    availability = i.ping()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    result = {
        'availability': availability,
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks
    }
    return result




def revoke_all_tasks():
    i = default_app.control.inspect()
    active_tasks = i.active()
    if active_tasks:
        for worker, tasks in active_tasks.items():
            for task in tasks:
                task_id = task['id']
                default_app.control.revoke(task_id, terminate=True)
                print(f"Revoked task {task_id}")
    else:
        logger.info("No active tasks to revoke")