from celery import shared_task
from .device import AccessControl
from .face import FaceControl
from .models import Door
from celery.signals import celeryd_init
import time
import logging

@shared_task
def start_linsten_1():
    # tennis 236
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    
    device.get_login_info(ip='192.168.0.145', port=37777, username='admin', password='123456')
    # device.get_login_info(ip='192.168.1.230', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()
   
@shared_task
def start_linsten_2():
    # tennis 237
    device = AccessControl()
    print(' the instance start_linsten_2', device)
    device.get_login_info(ip='192.168.0.146', port=37777, username='admin', password='123456')

    # device.get_login_info(ip='192.168.1.231', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()
        
@shared_task
def start_linsten_3():

    device = AccessControl()
    print(' the instance start_linsten_1', device)
    
    device.get_login_info(ip='192.168.1.232', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_4():
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    
    device.get_login_info(ip='192.168.1.233', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_5():
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    
    device.get_login_info(ip='192.168.1.234', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    
    
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_6():
    device = AccessControl()
    
    device.get_login_info(ip='192.168.1.235', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_7():
    device = AccessControl()
    
    device.get_login_info(ip='192.168.1.236', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_8():
    device = AccessControl()
    
    device.get_login_info(ip='192.168.1.237', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

@shared_task
def start_linsten_9():
    device = AccessControl()
    
    device.get_login_info(ip='192.168.1.238', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()

# @shared_task
# def start_linsten_10():
#     device = AccessControl()
#     
#     device.get_login_info(ip='192.168.1.239', port=37777, username='admin', password='123456')
#     result = device.login()
#     device.alarm_listen()
#     if result:
#         device.alarm_listen()

# @shared_task
# def start_linsten_11():
#     device = AccessControl()
#     
#     device.get_login_info(ip='192.168.1.240', port=37777, username='admin', password='123456')
#     result = device.login()
#     device.alarm_listen()
#     if result:
#         device.alarm_listen()





@shared_task
def start_face_door_1():
    device = FaceControl()
    
    device.get_login_info(ip='192.168.1.220', port=37777, username='admin', password='123456')
    result = device.login()
    device.intelligent_operate()
    if result:
        device.intelligent_operate()
 
@shared_task
def start_face_door_2():
    device = FaceControl()
    
    device.get_login_info(ip='192.168.1.221', port=37777, username='admin', password='123456')
    result = device.login()
    device.intelligent_operate()
    if result:
        device.intelligent_operate()
    


@shared_task
def stop_listening_1():

    device = AccessControl()
    print(' the instance start_linsten_1', device)
    device.get_login_info(ip='192.168.0.145', port=37777, username='admin', password='123456')
    result = device.login()
    result = device.logout()
