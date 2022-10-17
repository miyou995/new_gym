from celery import shared_task
from .device import AccessControl
from .face import FaceControl
from .models import Door
from celery.signals import celeryd_init
import time
import logging
logger = logging.getLogger('celery_tasks')

@shared_task
def start_linsten_1():
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    logger.info("Task inited... dev=>", device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()
   
@shared_task
def start_linsten_2():
    device_2 = AccessControl()
    print(' the instance start_linsten_2', device_2)
    device_2.get_login_info(ip='192.168.1.3', port=37777, username='admin', password='123456')
    result = device_2.login()
    device_2.alarm_listen()
    if result:
        device_2.alarm_listen()
        
@shared_task
def start_linsten_3():
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    logger.info("Task inited... dev=>", device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_4():
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    logger.info("Task inited... dev=>", device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_5():
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    logger.info("Task inited... dev=>", device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_6():
    device = AccessControl()
    logger.info("Task inited... dev=>", device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()


@shared_task
def stop_listening_1():
    logger.info("Taskj inited...")

    device = AccessControl()
    print(' the instance start_linsten_1', device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    result = device.logout()




@shared_task
def start_face_door_1():
    device = FaceControl()
    logger.info("Task inited... dev=>", device)
    device.get_login_info(ip='192.168.1.220', port=37777, username='admin', password='mc091924')
    result = device.login()
    device.intelligent_operate()
    if result:
        device.intelligent_operate()
 
@shared_task
def start_face_door_2():
    device = FaceControl()
    logger.info("Task inited... dev=>", device)
    device.get_login_info(ip='192.168.1.221', port=37777, username='admin', password='mc091924')
    result = device.login()
    device.intelligent_operate()
    if result:
        device.intelligent_operate()
