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


def manage_door(ip, port, username, password):
    device = AccessControl()
    print(' the instance start_linsten_test_device_1', device)
    device.get_login_info(ip=ip, port=port, username=username, password=password)
    result = device.login()
    if result:
        print('device.loginid===========================', device.loginID)
        logger.warning('Device started with Ip=======>{}'.format(ip))
    device.alarm_listen()
    while True:
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                logger.warning('Device Stopped with Ip--------->{}',format(device.ip))
            else:
                logger.warning('Could not stop device ERROR ON  Ip--------->{}',format(device.ip))
            break
        time.sleep(15)

@shared_task(bind=True)
def start_linsten_test_device_1(self):
    manage_door(ip='192.168.0.145', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)
   

@shared_task(bind=True)
def start_linsten_test_device_2(self):
    # tennis 237
    manage_door(ip='192.168.0.146', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)


@shared_task(bind=True)
def start_linsten_2(self):

    manage_door(ip='192.168.1.230', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)
        
@shared_task(bind=True)
def start_linsten_3(self):

    manage_door(ip='192.168.1.232', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_4(self):

    manage_door(ip='192.168.1.233', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_5(self):

    manage_door(ip='192.168.1.234', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_6(self):

    manage_door(ip='192.168.1.235', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_7(self):
    
    manage_door(ip='192.168.1.236', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_8(self):
    manage_door(ip='192.168.1.237', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)

@shared_task(bind=True)
def start_linsten_9(self):
    manage_door(ip='192.168.1.238', port=37777, username='admin', password='123456')
    app.control.revoke(self.request.id, terminate=True)


@shared_task(bind=True)
def start_face_door_right(self):
    device = FaceControl()
    device.get_login_info(ip='192.168.1.220', port=37777, username='admin', password='mc091924')
    result = device.login()
    if result:
        device.intelligent_operate()
        print('device.loginid===========================', device.loginID)
        logger.warning('Device started with Ip=======>{}'.format(device.ip))
    while True:
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                logger.warning('Device Stopped with Ip--------->{}',format(device.ip))
            else:
                logger.warning('Could not stop device ERROR ON  Ip--------->{}',format(device.ip))
            break
        time.sleep(15)


    # if result:
    #     device.intelligent_operate()
 
@shared_task(bind=True)
def start_face_door_left(self):
    device = FaceControl()
    device.get_login_info(ip='192.168.1.221', port=37777, username='admin', password='mc091924')
    result = device.login()
    if result:
        device.intelligent_operate()
        print('device.loginid===========================', device.loginID)
        logger.warning('Device started with Ip=======>{}'.format(device.ip))
    while True:
        if is_time_to_stop():
            if device.loginID:
                device.logout()
                device.sdk.Logout(device.loginID)
                device.sdk.Cleanup()
                logger.warning('Device Stopped with Ip--------->{}',format(device.ip))
            else:
                logger.warning('Could not stop device ERROR ON  Ip--------->{}',format(device.ip))
            break
        time.sleep(15)
