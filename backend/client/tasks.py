from celery import shared_task
from .face_sub import FaceControl
from celery.signals import celeryd_init
import time




@shared_task
def register_user(user_name, user_id, picture_path):
    print('CALLED') 
    face1 = FaceControl()
    face2 = FaceControl()
    print(' the instance face1', face1)
    print(' the instance face2', face2)
    face1.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    face2.get_login_info(ip='192.168.1.2', port=37777, username='admin', password='123456')
    result = face1.login()
    result2 = face2.login()
    face1.subscibe_user(user_name=user_name, user_id=user_id, picture_path=picture_path)
    face2.subscibe_user(user_name=user_name, user_id=user_id, picture_path=picture_path)
    face1 = face1.logout()
    face2 = face2.logout()
    return result
    # result = device.logout()



