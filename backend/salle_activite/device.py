# coding=utf-8
import sys
import os
import time
from ctypes import *
from NetSDK.NetSDK import NetClient
from NetSDK.SDK_Callback import *
from NetSDK.SDK_Enum import *
from NetSDK.SDK_Struct import *
from client.models import Client

file = "c:/log.log"
@CB_FUNCTYPE(c_int, c_char_p, c_uint, C_LDWORD)
def SDKLogCallBack(szLogBuffer, nLogSize, dwUser):
    # try:
    #     with open(file, 'a') as f:
    #         f.write(szLogBuffer.decode())
    # except Exception as e:
    #     print(e)
    return 1

class AccessControl:
    def __init__(self):

        self.loginID = C_LLONG()
        self.playID = C_LLONG()
        self.freePort = c_int()
        self.m_DisConnectCallBack = fDisConnect(self.DisConnectCallBack)
        self.m_ReConnectCallBack = fHaveReConnect(self.ReConnectCallBack)
        self.m_MessCallBackEx1 = fMessCallBackEx1(self.messCallBackEx1)
        self.m_AnalyzerDataCallBack = fAnalyzerDataCallBack(self.AnalyzerDataCallBack)
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
       
    def get_login_info(self, ip, port, username, password):
        self.ip         = ip
        self.port       = port
        self.username   = username
        self.password   = password

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
                print('ip=>', self.ip)
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

    def get_authorization(self, card_n, door_ip):
        # dictio = {'card' : card_n, 'door' : door_ip}
        # print("dictioooo",dictio)
        # if card_n:
        card = card_n.decode("utf-8")
        print(' la carte est ', card)
        print(' la door_ip  ', door_ip)
        #0099F9AB
        # 10126599
        try:
            client=  Client.objects.get(hex_card=card)
            print(' le client est ', client)
            if client:
                print('le client la la permission dentree ')
                return client.get_access_permission(door_ip)
            else: 
                print('rani fel else')
                return False
        except Client.DoesNotExist:
            return False
        #     print('client doesnt exist or doesnt have permission to get in')
        # print(' la has_perm has_perm>>>>> ', has_perm)

    def messCallBackEx1(self, lCommand, lLoginID, pBuf, dwBufLen, pchDVRIP, nDVRPort, bAlarmAckFlag, nEventID, dwUser):
        # print('rani SELF lLoginID' , self.loginID)
        # print('rani lLoginID' , lLoginID)
        if (lLoginID != self.loginID):
            print('le code et la clé sont different')
            return
            # return
        if (lCommand == SDK_ALARM_TYPE.ALARM_ACCESS_CTL_EVENT):
            print("ALARM_ACCESS_CTL_EVENT")  # 门禁事件; Access control event
            alarm_info = cast(pBuf, POINTER(NET_A_ALARM_ACCESS_CTL_EVENT_INFO)).contents
            card_n = alarm_info.szCardNo
            if card_n != b'00000000':
                door = self.ip
                client = self.get_authorization(card_n,door)
                if client : 
                    self.open_door()
                    # client.init_presence()

                    # self.logout()
                    # self.login()
                    # self.alarm_listen()
                print('get_authorization => ', client)
        return 

    def alarm_listen(self):
        if self.alarmEvent == 0:
            # 设置报警回调函数 set alarm callback
            self.sdk.SetDVRMessCallBackEx1(self.m_MessCallBackEx1, 0)

            result = self.sdk.StartListenEx(self.loginID)
            if result:
                print("StartListenEx operate succeed.")
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
        print(' access_operate')
        result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_OPEN, stuInParam, c_char(), 5000)
        # result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_OPEN, stuInParam, c_char(), 5000)
        # if result:
        #     print("Open the door succeed.")
        #     stuInParam = NET_CTRL_ACCESS_CLOSE()
        #     stuInParam.dwSize = sizeof(NET_CTRL_ACCESS_CLOSE)
        #     stuInParam.nChannelID = 0
        #     result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_CLOSE, stuInParam, c_char(), 5000)
        #     # result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_CLOSE, stuInParam, c_char(), 5000)
        #     if result:
        #         print("Close the door succeed.")
        #     else:
        #         print("Close the door fail. " + self.sdk.GetLastErrorMessage())
        #         return False
        # else:
        #     print("Open the door fail. " + self.sdk.GetLastErrorMessage())
        #     return False
        return True

    def open_door(self):
        print(' open_door')
        stuInParam = NET_CTRL_ACCESS_OPEN()
        stuInParam.dwSize = sizeof(NET_CTRL_ACCESS_OPEN)
        stuInParam.nChannelID = 0 # channel
        stuInParam.emOpenDoorType = EM_OPEN_DOOR_TYPE.EM_OPEN_DOOR_TYPE_REMOTE
        stuInParam.emOpenDoorDirection = EM_OPEN_DOOR_DIRECTION.EM_OPEN_DOOR_DIRECTION_FROM_ENTER
        result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_OPEN, stuInParam, c_char(), 5000)

                # result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_OPEN, stuInParam, c_char(), 5000)
        # if result:
        #     print("Open the door succeed.")
        #     stuInParam = NET_CTRL_ACCESS_CLOSE()
        #     stuInParam.dwSize = sizeof(NET_CTRL_ACCESS_CLOSE)
        #     stuInParam.nChannelID = 0
        #     result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_CLOSE, stuInParam, c_char(), 5000)
        #     # result = self.sdk.ControlDeviceEx(self.loginID, CtrlType.ACCESS_CLOSE, stuInParam, c_char(), 5000)
        #     if result:
        #         print("Close the door succeed.")
        #     else:
        #         print("Close the door fail. " + self.sdk.GetLastErrorMessage())
        #         return False
        # else:
        #     print("Open the door fail. " + self.sdk.GetLastErrorMessage())
        return True
        