from celery import shared_task
from .device import AccessControl
from .face import FaceControl
from .models import Door
from celery.signals import celeryd_init
import time

@shared_task
def start_linsten_1():
    print('CALLED') 
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    device.alarm_listen()
    if result:
        device.alarm_listen()
    #     # card= device.card_infos
    #     # print(' card', card)
    #     # if message:
    #     #     print('one jaaat',message, ' ------')
    #     print('DONEEEEEE')
    # else:
    #     device_1_1 = AccessControl()
    #     print(' the instance start_linsten_1', device_1_1)
    #     device_1_1.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    #     result = device_1_1.login()
    #     device_1_1.alarm_listen()

    # device_2 = AccessControl()
    # print(' the instance start_linsten_2', device_2)
    # device_2.get_login_info(ip='192.168.1.3', port=37777, username='admin', password='123456')
    # result = device_2.login()
    # device_2.alarm_listen()
    # if result:
    #     result = device_2.alarm_listen()
    #     # card= device_2.card_infos
    #     # print(' card', card)
    #     # if message:
    #     #     print('one jaaat',message, ' ------')
    # else:
    #     device_2_2 = AccessControl()
    #     print(' the instance start_linsten_1', device_2_2)
    #     device_2_2.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    #     result = device_2_2.login()
    #     device_2_2.alarm_listen()


@shared_task
def start_linsten_2():
    print('CALLED') 
    device_2 = AccessControl()
    print(' the instance start_linsten_2', device_2)
    device_2.get_login_info(ip='192.168.1.3', port=37777, username='admin', password='123456')
    result = device_2.login()
    device_2.alarm_listen()
    if result:
        device_2.alarm_listen()
    #     # card= device_2.card_infos
    #     # print(' card', card)
    #     # if message:
    #     #     print('one jaaat',message, ' ------')
    # else:
    #     device_2.logout()
    #     device_2.login()
    #     print('DONEEEEEE')
# i want to run this shared_task automaticly 
# not from the frontend

@shared_task
def stop_listening_1():
    print('CALLED') 
    device = AccessControl()
    print(' the instance start_linsten_1', device)
    device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = device.login()
    result = device.logout()


@shared_task
def register_user(client):
    print('CALLED') 
    face1 = FaceControl()
    face2 = FaceControl()
    print(' the instance face1', face1)
    print(' the instance face2', face2)
    face1.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    face2.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = face1.login()
    result = face2.login()
    face1.register_new_user(client)
    face2.register_new_user(client)
    if result : 
        print('YEs,', result)
    # result = device.logout()

@shared_task
def start_face_door_1():
    print('start_face_door_1') 


# @shared_task
# def stop_listening_2():
#     print('CALLED') 
#     device_2 = AccessControl()
#     print(' the instance start_linsten_2', device_2)
#     device_2.get_login_info(ip='192.168.1.3', port=37777, username='admin', password='123456')
#     result = device_2.login()
#     result = device_2.logout()





# @shared_task
# def open_door2():
#     # premission ckeck
#     print('CALLED')
#     for i in range(2):
#         device = AccessControl()
#         device.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
#         result = device.login()
#         device.alarm_listen()
#         if result:
#             result = device.open_door()
#             # card= device.card_infos()
#             mess = messCallBackEx1()
#             print(' card', card)
#             # if message:
#             #     print('one jaaat',message, ' ------')
#         print('DONEEEEEE')