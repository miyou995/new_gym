# coding=utf-8
import sys
import os
import time
from ctypes import *

from NetSDK.NetSDK import NetClient
from NetSDK.SDK_Callback import *
from NetSDK.SDK_Enum import *
from NetSDK.SDK_Struct import *
from pathlib import Path

global my_demo

file = "c:/log.log"
@CB_FUNCTYPE(c_int, c_char_p, c_uint, C_LDWORD)
def SDKLogCallBack(szLogBuffer, nLogSize, dwUser):
    '''try:
        with open(file, 'a') as f:
            f.write(szLogBuffer.decode())
    except Exception as e:
        print(e)'''
    return 1

class FaceControl:
    def __init__(self):
        self.loginID = C_LLONG()
        self.playID = C_LLONG()
        self.freePort = c_int()
        self.m_DisConnectCallBack = fDisConnect(self.DisConnectCallBack)
        self.m_ReConnectCallBack = fHaveReConnect(self.ReConnectCallBack)
        self.m_AnalyzerDataCallBack = fAnalyzerDataCallBack(self.AnalyzerDataCallBack)
        self.m_MessCallBackEx1 = fMessCallBackEx1(self.MessCallBackEx1)

        self.sdk = NetClient()
        self.sdk.InitEx(self.m_DisConnectCallBack)
        self.sdk.SetAutoReconnect(self.m_ReConnectCallBack)

        self.ip = ''
        self.port = 0
        self.username = ''
        self.password = ''
        self.operatetype = 0
        self.findHandle = 0
        self.recordNo = 0
        self.alarmEvent = 0
        self.lAnalyzerHandle = C_LLONG()

    def get_login_info(self, ip='192.168.1.220', port=37777, username='admin', password='mc091924'):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def login(self):
        if not self.loginID:
            stuInParam = NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY()
            stuInParam.dwSize = sizeof(NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY)
            stuInParam.szIP = self.ip.encode()
            stuInParam.nPort = self.port
            stuInParam.szUserName = self.username.encode()
            stuInParam.szPassword = self.password.encode()
            stuInParam.emSpecCap = EM_LOGIN_SPAC_CAP_TYPE.TCP
            stuInParam.pCapParam = None

            stuOutParam = NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY()
            stuOutParam.dwSize = sizeof(NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY)

            self.loginID, device_info, error_msg = self.sdk.LoginWithHighLevelSecurity(stuInParam, stuOutParam)
            if self.loginID != 0:
                print("Login succeed. Channel num:" + str(device_info.nChanNum))
                return True
            else:
                print("Login failed. " + error_msg)
                return False

    def logout(self):
        if self.loginID:
            if self.playID:
                self.sdk.StopRealPlayEx(self.playID)
                self.playID = 0
            if self.alarmEvent:
                self.sdk.StopListen(self.loginID)
                self.alarmEvent = 0
            if self.lAnalyzerHandle:
                self.sdk.StopLoadPic(self.lAnalyzerHandle)
                self.lAnalyzerHandle = 0
            self.sdk.Logout(self.loginID)
            self.loginID = 0
        print("Logout succeed")

    def DisConnectCallBack(self, lLoginID, pchDVRIP, nDVRPort, dwUser):
        print("Device-OffLine")

    def ReConnectCallBack(self, lLoginID, pchDVRIP, nDVRPort, dwUser):
        print("Device-OnLine")



    def AnalyzerDataCallBack(self, lAnalyzerHandle, dwAlarmType, pAlarmInfo, pBuffer, dwBufSize, dwUser, nSequence, reserved):
        if self.lAnalyzerHandle == lAnalyzerHandle:
            print("AnalyzerDataCallBack!! lAnalyzerHandle:%s" % lAnalyzerHandle)
            if dwAlarmType == EM_EVENT_IVS_TYPE.ACCESS_CTL:
                print("ACCESS_CTL callback, dwBufSize:%d " % dwBufSize)
                # data handle
                pic_buf = cast(pBuffer, POINTER(c_ubyte * dwBufSize)).contents
                with open('./picture.jpg', 'wb+') as f:
                    f.write(pic_buf)
                p_buffer = cast(pAlarmInfo, POINTER(DEV_EVENT_ACCESS_CTL_INFO)).contents
                print("p_buffer szUserID:", p_buffer.szUserID)
                print("p_buffer szCardNo:", p_buffer.szCardNo)
                user_id = p_buffer.szUserID
                door = self.ip
                user_data = False
                if user_data : 
                    self.open_door()
                print('user_data => ', user_data)


    def MessCallBackEx1(self, lCommand, lLoginID, pBuf, dwBufLen, pchDVRIP, nDVRPort, bAlarmAckFlag, nEventID, dwUser):
        if (lLoginID != self.loginID):
            return
        if (lCommand == SDK_ALARM_TYPE.ALARM_ACCESS_CTL_EVENT):
            print("ALARM_ACCESS_CTL_EVENT")  # 门禁事件; Access control event
            alarm_info = cast(pBuf, POINTER(NET_A_ALARM_ACCESS_CTL_EVENT_INFO)).contents
            print("nDoor:%d" % alarm_info.nDoor)
            print("alarm_info:" , alarm_info)
            # print("dwUser:%d" % alarm_info.dwUser)
            print("szDoorName:%s" % alarm_info.szDoorName)
            print("stuTime:%d-%d-%d %d:%d:%d" % (alarm_info.stuTime.dwYear, alarm_info.stuTime.dwMonth, alarm_info.stuTime.dwDay,
                                  alarm_info.stuTime.dwHour, alarm_info.stuTime.dwMinute, alarm_info.stuTime.dwSecond))

    def quit_demo(self):
        if self.loginID:
            self.sdk.Logout(self.loginID)
        self.sdk.Cleanup()
        print("Demo finish")

    def log_open(self):
        log_info = LOG_SET_PRINT_INFO()
        log_info.dwSize = sizeof(LOG_SET_PRINT_INFO)
        log_info.bSetFilePath = 1
        log_info.szLogFilePath = os.path.join(os.getcwd(), 'sdk_log.log').encode('gbk')
        log_info.cbSDKLogCallBack = SDKLogCallBack
        result = self.sdk.LogOpen(log_info)

    def get_operate_info(self):
        print("")
        print("0:Finish Demo")
        print("1:User operation")
        print("2:Subscription card swiping")
        print("3:Open and close the door")
        self.operatetype = int(input('Please select operate type:'))

    def intelligent_operate(self):
        nChannelID = 0
        dwAlarmType = EM_EVENT_IVS_TYPE.ACCESS_CTL
        result = self.sdk.RealLoadPictureEx(self.loginID, nChannelID, dwAlarmType, True, self.m_AnalyzerDataCallBack, 0, 0)
        if result:
            print("RealLoadPictureEx operate success!%s" % result)
            self.lAnalyzerHandle = result
        else:
            print("RealLoadPictureEx operate fail. " + self.sdk.GetLastErrorMessage())
            return False
        return True
    def register_new_user(self):
        pass
    def start_operate(self):
        card_info = NET_RECORDSET_ACCESS_CTL_CARD()
        card_info.dwSize = sizeof(NET_RECORDSET_ACCESS_CTL_CARD)
        card_info.nDoorNum = 2
        card_info.sznDoors = (c_int * 32)()
        card_info.sznDoors[0] = 0
        card_info.sznDoors[1] = 1
        card_info.nTimeSectionNum = 2
        card_info.sznTimeSectionNo = (c_int * 32)()
        card_info.sznTimeSectionNo[0] = 255
        card_info.sznTimeSectionNo[1] = 255
        card_info.szCardNo = "112233".encode()
        card_info.szCardName = "445566".encode()
        card_info.szUserID = "AABBCC".encode()
        card_info.emStatus = EM_A_NET_ACCESSCTLCARD_STATE.NET_ACCESSCTLCARD_STATE_NORMAL
        card_info.emType = NET_ACCESSCTLCARD_TYPE.GENERAL
        card_info.szPsw = "123654".encode()
        card_info.nUserTime = 100
        card_info.bFirstEnter = 1
        card_info.bIsValid = 1
        card_info.stuValidStartTime.dwYear = 2022
        card_info.stuValidStartTime.dwMonth = 1
        card_info.stuValidStartTime.dwDay = 1
        card_info.stuValidStartTime.dwHour = 12
        card_info.stuValidStartTime.dwMinute = 0
        card_info.stuValidStartTime.dwSecond = 0
        card_info.stuValidEndTime.dwYear = 2022
        card_info.stuValidEndTime.dwMonth = 9
        card_info.stuValidEndTime.dwDay = 1
        card_info.stuValidEndTime.dwHour = 11
        card_info.stuValidEndTime.dwMinute = 59
        card_info.stuValidEndTime.dwSecond = 59

        stuInParam = NET_CTRL_RECORDSET_INSERT_PARAM()
        stuInParam.dwSize = sizeof(NET_CTRL_RECORDSET_INSERT_PARAM)
        stuInParam.stuCtrlRecordSetInfo.dwSize = sizeof(NET_CTRL_RECORDSET_INSERT_IN)
        stuInParam.stuCtrlRecordSetInfo.emType = EM_NET_RECORD_TYPE.ACCESSCTLCARD
        stuInParam.stuCtrlRecordSetInfo.pBuf = cast(pointer(card_info), c_void_p)
        stuInParam.stuCtrlRecordSetInfo.nBufLen = sizeof(NET_RECORDSET_ACCESS_CTL_CARD)
        stuInParam.stuCtrlRecordSetResult.dwSize = sizeof(NET_CTRL_RECORDSET_INSERT_OUT)
        
        result = self.sdk.ControlDevice(self.loginID, CtrlType.RECORDSET_INSERT, stuInParam, 5000)
        if result:
            print("Add card info success.nRecNo:%d" % stuInParam.stuCtrlRecordSetResult.nRecNo)
            self.recordNo = stuInParam.stuCtrlRecordSetResult.nRecNo
            
            result = self.search_card_info(card_num = "112233")
            if result:
                print("Search card info success")
            else:
                print("Search card info fail")
                return False

            stuInParam = NET_CTRL_RECORDSET_PARAM()
            stuInParam.dwSize = sizeof(NET_CTRL_RECORDSET_PARAM)
            stuInParam.emType = EM_NET_RECORD_TYPE.ACCESSCTLCARD

            card_info = NET_RECORDSET_ACCESS_CTL_CARD()
            card_info.nRecNo = self.recordNo
            card_info.dwSize = sizeof(NET_RECORDSET_ACCESS_CTL_CARD)
            card_info.nDoorNum = 2
            card_info.sznDoors = (c_int * 32)()
            card_info.sznDoors[0] = 0
            card_info.sznDoors[1] = 1
            card_info.nTimeSectionNum = 2
            card_info.sznTimeSectionNo = (c_int * 32)()
            card_info.sznTimeSectionNo[0] = 255
            card_info.sznTimeSectionNo[1] = 255
            card_info.szCardNo = "112233".encode()
            card_info.szCardName = "445566".encode()
            card_info.szUserID = "AABBCC".encode()
            card_info.emStatus = EM_A_NET_ACCESSCTLCARD_STATE.NET_ACCESSCTLCARD_STATE_NORMAL
            card_info.emType = NET_ACCESSCTLCARD_TYPE.GENERAL
            card_info.szPsw = "12345".encode()
            card_info.nUserTime = 100
            card_info.bFirstEnter = 1
            card_info.bIsValid = 1
            card_info.stuValidStartTime.dwYear = 2022
            card_info.stuValidStartTime.dwMonth = 1
            card_info.stuValidStartTime.dwDay = 1
            card_info.stuValidStartTime.dwHour = 12
            card_info.stuValidStartTime.dwMinute = 0
            card_info.stuValidStartTime.dwSecond = 0
            card_info.stuValidEndTime.dwYear = 2022
            card_info.stuValidEndTime.dwMonth = 10
            card_info.stuValidEndTime.dwDay = 1
            card_info.stuValidEndTime.dwHour = 11
            card_info.stuValidEndTime.dwMinute = 59
            card_info.stuValidEndTime.dwSecond = 59
            stuInParam.pBuf = cast(pointer(card_info), c_void_p)
            stuInParam.nBufLen = sizeof(NET_RECORDSET_ACCESS_CTL_CARD)
            result = self.sdk.ControlDevice(self.loginID, CtrlType.RECORDSET_UPDATE, stuInParam, 5000)
            if result:
                print("Modify card info succeed.")
                result = self.search_card_info(card_num="112233")
                if result:
                    print("Search card info success")
                else:
                    print("Search card info fail")
                    return False
            else:
                print("Modify card info fail. " + self.sdk.GetLastErrorMessage())
                return False

            stuInParam = NET_CTRL_RECORDSET_PARAM()
            stuInParam.dwSize = sizeof(NET_CTRL_RECORDSET_PARAM)
            stuInParam.emType = EM_NET_RECORD_TYPE.ACCESSCTLCARD

            card_info = NET_RECORDSET_ACCESS_CTL_CARD()
            card_info.dwSize = sizeof(NET_RECORDSET_ACCESS_CTL_CARD)
            card_info.nRecNo = self.recordNo

            stuInParam.pBuf = cast(pointer(card_info), c_void_p)
            stuInParam.nBufLen = sizeof(NET_RECORDSET_ACCESS_CTL_CARD)
            result = self.sdk.ControlDevice(self.loginID, CtrlType.RECORDSET_REMOVE, stuInParam, 5000)
            if result:
                print("Delete card info succeed.")
            else:
                print("Delete card info fail. " + self.sdk.GetLastErrorMessage())
                return False
        else:
            print("Add card info fail. " + self.sdk.GetLastErrorMessage())
            return False
        return True

    def alarm_listen(self):
        if self.alarmEvent == 0:
            # 设置报警回调函数 set alarm callback
            self.sdk.SetDVRMessCallBackEx1(self.m_MessCallBackEx1, 0)
            result = self.sdk.StartListenEx(self.loginID)
            if result:
                print("StartListenEx operate succeed.")
                #while True:
                self.alarmEvent = 1
            else:
                print("事件监听操作失败(StartListenEx operate fail). " + self.sdk.GetLastErrorMessage())
                return False
        else:
            print("StartListenEx operate already successful.")
        return True

    def access_operate(self):
        stuInParam = NET_CTRL_ACCESS_OPEN()
        stuInParam.dwSize = sizeof(NET_CTRL_ACCESS_OPEN)
        stuInParam.nChannelID = 0 # channel
        stuInParam.emOpenDoorType = EM_OPEN_DOOR_TYPE.EM_OPEN_DOOR_TYPE_REMOTE
        stuInParam.emOpenDoorDirection = EM_OPEN_DOOR_DIRECTION.EM_OPEN_DOOR_DIRECTION_FROM_ENTER
        result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_OPEN, stuInParam, c_char(), 5000)
        if result:
            print("Open the door succeed.")
            stuInParam = NET_CTRL_ACCESS_CLOSE()
            stuInParam.dwSize = sizeof(NET_CTRL_ACCESS_CLOSE)
            stuInParam.nChannelID = 0
            # result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_CLOSE, stuInParam, c_char(), 5000)
            # if result:
            #     print("Close the door succeed.")
            # else:
            #     print("Close the door fail. " + self.sdk.GetLastErrorMessage())
            #     return False
        else:
            print("Open the door fail. " + self.sdk.GetLastErrorMessage())
            return False
        return True
    def subscibe_user(self, user_name, user_id, picture_path):
        stuInParam = NET_IN_ACCESS_USER_SERVICE_INSERT()
        stuInParam.dwSize = sizeof(NET_IN_ACCESS_USER_SERVICE_INSERT)
        stuInParam.nInfoNum = 1
        record_info = NET_ACCESS_USER_INFO()
        record_info.szUserID = user_id.encode()
        record_info.szName = user_name.encode()
        record_info.emUserType = EM_A_NET_ENUM_USER_TYPE.NET_ENUM_USER_TYPE_NORMAL
        record_info.nUserStatus = 0
        record_info.szCitizenIDNo = b'123456789999'
        record_info.szPsw = b'admin'
        stuInParam.pUserInfo = cast(pointer(record_info), POINTER(NET_ACCESS_USER_INFO))
        stuOutParam = NET_OUT_ACCESS_USER_SERVICE_INSERT()
        stuOutParam.dwSize = sizeof(NET_OUT_ACCESS_USER_SERVICE_INSERT)
        stuOutParam.nMaxRetNum = 1
        print("tt")
        codes = []
        for i in range(stuOutParam.nMaxRetNum):
            code = 0
            codes.append(code)
        stuOutParam.pFailCode = cast((C_ENUM * stuOutParam.nMaxRetNum)(*codes), POINTER(C_ENUM))
        type = EM_A_NET_EM_ACCESS_CTL_USER_SERVICE.NET_EM_ACCESS_CTL_USER_SERVICE_INSERT
        result = self.sdk.OperateAccessUserService(self.loginID, type, stuInParam, stuOutParam, 5000)
        if result:
            print("OperateAccessUserService operate succeed.")
        else:
            print("OperateAccessUserService operate fail. " + self.sdk.GetLastErrorMessage())
            return False
        print("insert face image")
        stuInParam = NET_IN_ACCESS_FACE_SERVICE_INSERT()
        stuInParam.dwSize = sizeof(NET_IN_ACCESS_FACE_SERVICE_INSERT)
        stuInParam.nFaceInfoNum = 1
        record_info = NET_ACCESS_FACE_INFO()
        record_info.szUserID = user_id.encode()
        record_info.nFacePhoto = 1
        record_info.nInFacePhotoLen = (c_int * 5)()
        record_info.nOutFacePhotoLen = (c_int * 5)()
        record_info.pFacePhoto = (c_void_p * 5)()
        
        path = picture_path
        image_path = os.path.join(os.getcwd(), '/media',path)

        base_path =  Path(__file__).resolve().parent.parent
        media_path = base_path / 'media'
        image_path = base_path / f'media/photos/{picture_path}'
        print(' base_path--->',picture_path)
        print(' media_path--->',media_path)
        print(' image_path--->',image_path)

        # print(' picture_path--->',picture_path)
        # print(' os.getcwd()--->',os.getcwd())
        # print('complete image path--->',image_path)
      
        with open(image_path, 'rb') as face_pic:
            face_buf = face_pic.read()
            record_info.nInFacePhotoLen[0] = len(face_buf)
            record_info.nOutFacePhotoLen[0] = len(face_buf)
            record_info.pFacePhoto[0] = cast(c_char_p(face_buf), c_void_p)

        record_infos = []
        record_infos.append(record_info)
        stuInParam.pFaceInfo = cast(pointer(record_info), POINTER(NET_ACCESS_FACE_INFO))
        # stuInParam.pFaceInfo = cast((NET_ACCESS_FACE_INFO * 1)(*record_infos), POINTER(NET_ACCESS_FACE_INFO))

        stuOutParam = NET_OUT_ACCESS_FACE_SERVICE_INSERT()
        stuOutParam.dwSize = sizeof(NET_OUT_ACCESS_FACE_SERVICE_INSERT)
        stuOutParam.nMaxRetNum = 1
        codes = []
        for i in range(stuOutParam.nMaxRetNum):
            code = 0
            codes.append(code)
        stuOutParam.pFailCode = cast((C_ENUM * stuOutParam.nMaxRetNum)(*codes), POINTER(C_ENUM))

        type = EM_A_NET_EM_ACCESS_CTL_FACE_SERVICE.NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT
        result = self.sdk.OperateAccessFaceService(self.loginID, type, stuInParam, stuOutParam, 5000)
        if result:
            print("OperateAccessFaceService operate succeed.", result)
        else:
            print("OperateAccessFaceService operate fail. " + str(self.sdk.GetLastError()))
            return False
        # print("add card")

        # add card
        stuInParam = NET_IN_ACCESS_CARD_SERVICE_INSERT()
        stuInParam.dwSize = sizeof(NET_IN_ACCESS_CARD_SERVICE_INSERT)
        stuInParam.nInfoNum = 1

        record_info = NET_ACCESS_CARD_INFO()
        record_info.szCardNo = user_id.encode()
        record_info.szUserID = user_id.encode()
        record_info.emType = NET_ACCESSCTLCARD_TYPE.GENERAL

        stuInParam.pCardInfo = cast(pointer(record_info), POINTER(NET_ACCESS_CARD_INFO))

        stuOutParam = NET_OUT_ACCESS_CARD_SERVICE_INSERT()
        stuOutParam.dwSize = sizeof(NET_OUT_ACCESS_CARD_SERVICE_INSERT)
        stuOutParam.nMaxRetNum = 1
        codes = []
        for i in range(stuOutParam.nMaxRetNum):
            code = 0
            codes.append(code)
        stuOutParam.pFailCode = cast((C_ENUM * stuOutParam.nMaxRetNum)(*codes), POINTER(C_ENUM))

        type = EM_A_NET_EM_ACCESS_CTL_CARD_SERVICE.NET_EM_ACCESS_CTL_CARD_SERVICE_INSERT
        result = self.sdk.OperateAccessCardService(self.loginID, type, stuInParam, stuOutParam, 5000)
        if result:
            print("OperateAccessCardService operate succeed.", result)
        else:
            print("OperateAccessCardService operate fail. " + self.sdk.GetLastErrorMessage())
            return False

        return True

    def user_operate(self):
        stuInParam = NET_IN_ACCESS_USER_SERVICE_INSERT()
        stuInParam.dwSize = sizeof(NET_IN_ACCESS_USER_SERVICE_INSERT)
        stuInParam.nInfoNum = 1
        record_info = NET_ACCESS_USER_INFO()
        record_info.szUserID = b'C0003'
        record_info.szName = b'Taki'
        record_info.emUserType = EM_A_NET_ENUM_USER_TYPE.NET_ENUM_USER_TYPE_NORMAL
        record_info.nUserStatus = 0
        record_info.szCitizenIDNo = b'123456789999'
        record_info.szPsw = b'admin'
        stuInParam.pUserInfo = cast(pointer(record_info), POINTER(NET_ACCESS_USER_INFO))
        stuOutParam = NET_OUT_ACCESS_USER_SERVICE_INSERT()
        stuOutParam.dwSize = sizeof(NET_OUT_ACCESS_USER_SERVICE_INSERT)
        stuOutParam.nMaxRetNum = 1
        print("tt")
        codes = []
        for i in range(stuOutParam.nMaxRetNum):
            code = 0
            codes.append(code)
        stuOutParam.pFailCode = cast((C_ENUM * stuOutParam.nMaxRetNum)(*codes), POINTER(C_ENUM))
        type = EM_A_NET_EM_ACCESS_CTL_USER_SERVICE.NET_EM_ACCESS_CTL_USER_SERVICE_INSERT
        result = self.sdk.OperateAccessUserService(self.loginID, type, stuInParam, stuOutParam, 5000)
        if result:
            print("OperateAccessUserService operate succeed.")
        else:
            print("OperateAccessUserService operate fail. " + self.sdk.GetLastErrorMessage())
            return False
        print("insert face image")
        stuInParam = NET_IN_ACCESS_FACE_SERVICE_INSERT()
        stuInParam.dwSize = sizeof(NET_IN_ACCESS_FACE_SERVICE_INSERT)
        stuInParam.nFaceInfoNum = 1
        record_info = NET_ACCESS_FACE_INFO()
        record_info.szUserID = b'C0003'
        record_info.nFacePhoto = 1
        record_info.nInFacePhotoLen = (c_int * 5)()
        record_info.nOutFacePhotoLen = (c_int * 5)()
        record_info.pFacePhoto = (c_void_p * 5)()
        
        path = "picture.jpg"
        image_path = os.path.join(os.getcwd(), path)
        # path = str(input("please input face image path:"))
        with open(image_path, 'rb') as face_pic:
            face_buf = face_pic.read()
            record_info.nInFacePhotoLen[0] = len(face_buf)
            record_info.nOutFacePhotoLen[0] = len(face_buf)
            record_info.pFacePhoto[0] = cast(c_char_p(face_buf), c_void_p)

        record_infos = []
        record_infos.append(record_info)
        stuInParam.pFaceInfo = cast(pointer(record_info), POINTER(NET_ACCESS_FACE_INFO))
        # stuInParam.pFaceInfo = cast((NET_ACCESS_FACE_INFO * 1)(*record_infos), POINTER(NET_ACCESS_FACE_INFO))

        stuOutParam = NET_OUT_ACCESS_FACE_SERVICE_INSERT()
        stuOutParam.dwSize = sizeof(NET_OUT_ACCESS_FACE_SERVICE_INSERT)
        stuOutParam.nMaxRetNum = 1
        codes = []
        for i in range(stuOutParam.nMaxRetNum):
            code = 0
            codes.append(code)
        stuOutParam.pFailCode = cast((C_ENUM * stuOutParam.nMaxRetNum)(*codes), POINTER(C_ENUM))

        type = EM_A_NET_EM_ACCESS_CTL_FACE_SERVICE.NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT
        result = self.sdk.OperateAccessFaceService(self.loginID, type, stuInParam, stuOutParam, 5000)
        if result:
            print("OperateAccessFaceService operate succeed.")
        else:
            print("OperateAccessFaceService operate fail. " + str(self.sdk.GetLastError()))
            return False
        print("add card")

        # add card
        stuInParam = NET_IN_ACCESS_CARD_SERVICE_INSERT()
        stuInParam.dwSize = sizeof(NET_IN_ACCESS_CARD_SERVICE_INSERT)
        stuInParam.nInfoNum = 1

        record_info = NET_ACCESS_CARD_INFO()
        record_info.szCardNo = b'ABA'
        record_info.szUserID = b'777'
        record_info.emType = NET_ACCESSCTLCARD_TYPE.GB_CUSTOM1

        stuInParam.pCardInfo = cast(pointer(record_info), POINTER(NET_ACCESS_CARD_INFO))

        stuOutParam = NET_OUT_ACCESS_CARD_SERVICE_INSERT()
        stuOutParam.dwSize = sizeof(NET_OUT_ACCESS_CARD_SERVICE_INSERT)
        stuOutParam.nMaxRetNum = 1
        codes = []
        for i in range(stuOutParam.nMaxRetNum):
            code = 0
            codes.append(code)
        stuOutParam.pFailCode = cast((C_ENUM * stuOutParam.nMaxRetNum)(*codes), POINTER(C_ENUM))

        type = EM_A_NET_EM_ACCESS_CTL_CARD_SERVICE.NET_EM_ACCESS_CTL_CARD_SERVICE_INSERT
        result = self.sdk.OperateAccessCardService(self.loginID, type, stuInParam, stuOutParam, 5000)
        if result:
            print("OperateAccessCardService operate succeed.", result)
        else:
            print("OperateAccessCardService operate fail. " + self.sdk.GetLastErrorMessage())
            return False

        return True

if __name__ == '__main__':
    my_demo = FaceControl()
    my_demo.get_login_info()
    result = my_demo.login()
    if not result:
        my_demo.quit_demo()
    else:
        my_demo.log_open()
        print("1:ASI1201E-D")
        print("2:ASI7223Y-A-V3")
        device_type = int(input('Please select device type:'))
        if device_type == 1:
            while True:
                my_demo.get_operate_info()
                if my_demo.operatetype == 0:
                    my_demo.logout()
                    my_demo.quit_demo()
                    break
                elif my_demo.operatetype == 1:
                    result = my_demo.start_operate()
                    if not result:
                        my_demo.logout()
                        my_demo.quit_demo()
                        break
                elif my_demo.operatetype == 2:
                    result = my_demo.alarm_listen()
                    if not result:
                        my_demo.logout()
                        my_demo.quit_demo()
                        break
                elif my_demo.operatetype == 3:
                    result = my_demo.access_operate()
                    if not result:
                        my_demo.logout()
                        my_demo.quit_demo()
                        break
        elif device_type == 2:
            while True:
                my_demo.get_operate_info()
                if my_demo.operatetype == 0:
                    my_demo.logout()
                    my_demo.quit_demo()
                    break
                elif my_demo.operatetype == 1:
                    result = my_demo.user_operate()
                    if not result:
                        my_demo.logout()
                        my_demo.quit_demo()
                        break
                elif my_demo.operatetype == 2:
                    result = my_demo.intelligent_operate()
                    if not result:
                        my_demo.logout()
                        my_demo.quit_demo()
                        break
                elif my_demo.operatetype == 3:
                    result = my_demo.access_operate()
                    if not result:
                        my_demo.logout()
                        my_demo.quit_demo()
                        break
        else:
            print("Wrong device type")
            my_demo.logout()
            my_demo.quit_demo()