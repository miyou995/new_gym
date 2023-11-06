from celery import shared_task, group
from config.celery import app
# from celery.app.control import Inspect
from celery.utils.log import get_task_logger

from .device import AccessControl
from .face import FaceControl
from .models import Door
import time
from datetime import datetime
import logging
from django.conf import settings
logger = logging.getLogger(__name__)

def is_time_to_stop():
    stop_hour  = settings.STOP_HOUR
    stop_minute = settings.STOP_MINUTE
    current_time = datetime.now()
    return current_time.hour == stop_hour and current_time.minute == stop_minute



@shared_task(bind=True)
def start_linsten_test_device_1(self):
    # tennis 236
    device = AccessControl()
    print(' the instance start_linsten_test_device_1', device)
    device.get_login_info(ip='192.168.0.145', port=37777, username='admin', password='123456')
    # device.get_login_info(ip='192.168.1.230', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)
   

@shared_task(bind=True)
def start_linsten_test_device_2(self):
    # tennis 237
    print('The task ID is:', self.request.id)
    device = AccessControl()
    print(' the instance start_linsten_test_device_2', device)
    device.get_login_info(ip='192.168.0.146', port=37777, username='admin', password='123456')

    # device.get_login_info(ip='192.168.1.231', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    device.deactivate_alarm()
    while True:
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
        device.reboot_device()
    app.control.revoke(self.request.id, terminate=True)


@shared_task(bind=True)
def start_linsten_2(self):
    device = AccessControl()
    print(' the instance start_linsten_3', device)
    device.get_login_info(ip='192.168.1.230', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)
        
@shared_task(bind=True)
def start_linsten_3(self):

    device = AccessControl()
    print(' the instance start_linsten_3', device)
    
    device.get_login_info(ip='192.168.1.232', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        
        
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_4(self):
    device = AccessControl()
    print(' the instance start_linsten_4', device)
    
    device.get_login_info(ip='192.168.1.233', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        
        
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_5(self):
    device = AccessControl()
    print(' the instance start_linsten_5', device)
    
    device.get_login_info(ip='192.168.1.234', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        
        
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_6(self):
    device = AccessControl()
    
    device.get_login_info(ip='192.168.1.235', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        
        
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_7(self):
    device = AccessControl()
    
    device.get_login_info(ip='192.168.1.236', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        
        
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_8(self):
    device = AccessControl()
    device.get_login_info(ip='192.168.1.237', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        
        
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_9(self):
    device = AccessControl()
    device.get_login_info(ip='192.168.1.238', port=37777, username='admin', password='123456')
    device.login()
    print('device.loginid===========================', device.loginID)
    device.alarm_listen()
    while True:
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                print('LOGOOUUUUUTO SUCCEEEED device.loginID------------------|')
            else:
                print('THERE IS NO device.loginID------------------|')
            break
        
        time.sleep(15)
    app.control.revoke(self.request.id, terminate=True)


@shared_task(bind=True)
def start_face_door_right(self):
    device = FaceControl()
    device.get_login_info(ip='192.168.1.220', port=37777, username='admin', password='mc091924')
    device.login()
    device.intelligent_operate()
    # if result:
    #     device.intelligent_operate()
 
@shared_task(bind=True)
def start_face_door_left(self):
    device = FaceControl()
    device.get_login_info(ip='192.168.1.221', port=37777, username='admin', password='mc091924')
    device.login()
    device.intelligent_operate()
    # if result:
    #     device.intelligent_operate()
    


# @shared_task(bind=True)
# def stop_listening_1(self):
#     # res = app.control.revoke(task_id, terminate=True) #i think it can go on a view directly not celery task because it means it will stop other and starts this one
#     device = AccessControl()
#     print(' the instance start_linsten_1', device)
#     device.get_login_info(ip='192.168.0.145', port=37777, username='admin', password='123456')
#     device.login()
#     result = device.logout()
# logger = get_task_logger(__name__)

# @shared_task(bind=True)
# def stop_and_restart_tasks(self):
#     logger.info('Stopping and restarting tasks...')
#     i = app.control.inspect()
#     active_tasks = i.active()
#     reser = i.reserved()
#     print('reser-------------->', reser)
#     print('active_tasks-------------->', active_tasks)
#     if not active_tasks:
#         logger.warning('No active tasks were found.')
#         return 'No active tasks were found.'
    
#     logger.info(f'Active tasks: {active_tasks}')
    
#     for worker, tasks in active_tasks.items():
#         for task in tasks:
#             logger.info(f'Revoking task {task["id"]}...')
#             app.control.revoke(task['id'], terminate=True)
    
#     app.control.purge()
#     logger.info('All active tasks have been revoked and the queue has been purged.')
    
#     # Rest of your task logic follows...

#     if settings.DEBUG == True:
#         task_group = group(
#             start_linsten_test_device_1.s(),
#             start_linsten_test_device_2.s(),
#         )
#     else:
#         task_group = group(
#             start_linsten_2.s(),
#             #start_linsten_3.s(),
#             # start_linsten_4.s(),
#             # start_linsten_5.s(),
#             #  start_linsten_6.s(),
#             #  start_linsten_7.s(),
#             #  start_linsten_8.s(),
#             #  start_linsten_9.s(),

#             start_face_door_right.s(),
#             start_face_door_left.s()
#         )
#     logger.warning('All tasks have been stopped, memory cleared, and tasks restarted.')
#     task_group.apply_async()
#     message = 'All tasks have been stopped, memory cleared, and tasks restarted. New way'
#     app.logger.warning(message)
#     return message
