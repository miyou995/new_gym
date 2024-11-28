# coding=utf-8
import sys
import os
import time
from ctypes import *

from NetSDK.NetSDK import NetClient
from NetSDK.SDK_Callback import fDisConnect, fHaveReConnect, fAnalyzerDataCallBack
from NetSDK.SDK_Enum import *
from NetSDK.SDK_Struct import *

global my_demo

file = "d:/log.log"
@CB_FUNCTYPE(c_int, c_char_p, c_uint, C_LDWORD)
def SDKLogCallBack(szLogBuffer, nLogSize, dwUser):
    try:
        with open(file, 'a') as f:
            f.write(szLogBuffer.decode())
    except Exception as e:
        print(e)
    return 1

class ConsoleDemo:
    def __init__(self):

        self.loginID = C_LLONG()
        self.playID = C_LLONG()
        self.freePort = c_int()
        self.m_DisConnectCallBack = fDisConnect(self.DisConnectCallBack)
        self.m_ReConnectCallBack = fHaveReConnect(self.ReConnectCallBack)
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

    def get_login_info(self):
        print("Please input login info")
        print("")
        # self.ip = input('IP address:')
        # self.port = int(input('port:'))
        # self.username = input('username:')
        # self.password = input('password:')
        self.ip = '192.168.0.145'
        self.port = 37777
        self.username = 'admin'
        self.password = '123456'

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

            self.sdk.Logout(self.loginID)
            self.loginID = 0
        print("Logout succeed")

    def DisConnectCallBack(self, lLoginID, pchDVRIP, nDVRPort, dwUser):
        print("Device-OffLine")

    def ReConnectCallBack(self, lLoginID, pchDVRIP, nDVRPort, dwUser):
        print("Device-OnLine")

    def AnalyzerDataCallBack(self, lAnalyzerHandle, dwAlarmType, pAlarmInfo, pBuffer, dwBufSize, dwUser, nSequence, reserved):
        print("AnalyzerDataCallBack")

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
        print("1:Intelligent access control event")
        print("2:Access record operation")
        print("3:Open door face")
        self.operatetype = int(input('Please select operate type:'))

    def intelligent_operate(self):
        nChannelID = 0
        dwAlarmType = EM_EVENT_IVS_TYPE.ACCESS_CTL
        result = self.sdk.RealLoadPictureEx(self.loginID, nChannelID, dwAlarmType, True, self.m_AnalyzerDataCallBack, 0, 0)
        if result:
            print("RealLoadPictureEx operate success!")
            result = self.sdk.StopLoadPic(result)
            if result:
                print("StopLoadPic operate success!")
                return True
            else:
                print("StopLoadPic operate fail. " + self.sdk.GetLastErrorMessage())
        else:
            print("RealLoadPictureEx operate fail. " + self.sdk.GetLastErrorMessage())
        return False

    def access_record_operate(self):
        inParam = NET_IN_FIND_RECORD_PARAM()
        inParam.dwSize = sizeof(NET_IN_FIND_RECORD_PARAM)
        inParam.emType = EM_NET_RECORD_TYPE.ACCESSCTLCARDREC_EX
        in_condition = NET_FIND_RECORD_ACCESSCTLCARDREC_CONDITION_EX()
        in_condition.dwSize = sizeof(NET_FIND_RECORD_ACCESSCTLCARDREC_CONDITION_EX)
        in_condition.stStartTime = NET_TIME()
        in_condition.stStartTime.dwYear = 2022
        in_condition.stStartTime.dwMonth = 1
        in_condition.stStartTime.dwDay = 1
        in_condition.stStartTime.dwHour = 0
        in_condition.stStartTime.dwMinute = 0
        in_condition.stStartTime.dwSecond = 0
        in_condition.stEndTime = NET_TIME()
        in_condition.stEndTime.dwYear = 2022
        in_condition.stEndTime.dwMonth = 5
        in_condition.stEndTime.dwDay = 1
        in_condition.stEndTime.dwHour = 0
        in_condition.stEndTime.dwMinute = 0
        in_condition.stEndTime.dwSecond = 0
        inParam.pQueryCondition = cast(pointer(in_condition), c_void_p)
        outParam = NET_OUT_FIND_RECORD_PARAM()
        outParam.dwSize = sizeof(NET_OUT_FIND_RECORD_PARAM)
        # 按查询条件查询记录; by search filter search record
        result = self.sdk.FindRecord(self.loginID, inParam, outParam, 5000)
        if result:
            self.findHandle = outParam.lFindeHandle
            print("FindRecord operate success! lFindeHandle:%s" % self.findHandle)
            inFindParam = NET_IN_FIND_NEXT_RECORD_PARAM()
            inFindParam.dwSize = sizeof(NET_IN_FIND_NEXT_RECORD_PARAM)
            inFindParam.lFindeHandle = self.findHandle
            inFindParam.nFileCount = 10
            outFindParam = NET_OUT_FIND_NEXT_RECORD_PARAM()
            outFindParam.dwSize = sizeof(NET_OUT_FIND_NEXT_RECORD_PARAM)
            out_record = NET_RECORDSET_ACCESS_CTL_CARDREC()
            out_record.dwSize = sizeof(NET_RECORDSET_ACCESS_CTL_CARDREC)
            outFindParam.pRecordList = cast(pointer(out_record), c_void_p)
            # 查找记录; search record
            result = self.sdk.FindNextRecord(inFindParam, outFindParam, 5000)
            if result:
                out_record = cast(outFindParam.pRecordList, POINTER(NET_RECORDSET_ACCESS_CTL_CARDREC)).contents
                print("FindNextRecord operate success!")
                inControl = NET_CTRL_RECORDSET_PARAM()
                inControl.dwSize = sizeof(NET_CTRL_RECORDSET_PARAM)
                inControl.emType = EM_NET_RECORD_TYPE.ACCESSCTLCARDREC_EX
                inControl.pBuf = cast(pointer(out_record), c_void_p)
                # 清除记录; clear record
                result = self.sdk.ControlDevice(self.loginID, CtrlType.RECORDSET_CLEAR, inControl, 5000)
                if result:
                    print("ControlDevice operate success!result: %s" % result)
                    self.sdk.FindRecordClose(self.findHandle)
                    return True
                else:
                    print("ControlDevice operate fail. " + self.sdk.GetLastErrorMessage())
                    self.sdk.FindRecordClose(self.findHandle)
            else:
                print("FindNextRecord operate fail. " + self.sdk.GetLastErrorMessage())
                self.sdk.FindRecordClose(self.findHandle)
        else:
            print("FindRecord operate fail. " + self.sdk.GetLastErrorMessage())
        return False

    def open_door(self):
        inParam = NET_IN_FACE_OPEN_DOOR()
        inParam.dwSize = sizeof(NET_IN_FACE_OPEN_DOOR)
        inParam.emCompareResult = EM_COMPARE_RESULT.EM_COMPARE_RESULT_SUCCESS

        outParam = NET_OUT_FACE_OPEN_DOOR()
        outParam.dwSize = sizeof(NET_OUT_FACE_OPEN_DOOR)

        result = self.sdk.OpenDoor(self.loginID, inParam, outParam, 5000)
        if result:
            print("open door success! ")
        else:
            print("open door success. " + self.sdk.GetLastErrorMessage())
        return False
    

if __name__ == '__main__':
    my_demo = ConsoleDemo()
    my_demo.get_login_info()
    result = my_demo.login()
    if not result:
        my_demo.quit_demo()
    else:
        my_demo.log_open()
        while True:
            my_demo.get_operate_info()
            if my_demo.operatetype == 0:
                my_demo.logout()
                my_demo.quit_demo()
                break
            elif my_demo.operatetype == 1:
                result = my_demo.intelligent_operate()
                if not result:
                    my_demo.logout()
                    my_demo.quit_demo()
                    break
            elif my_demo.operatetype == 2:
                result = my_demo.access_record_operate()
                if not result:
                    my_demo.logout()
                    my_demo.quit_demo()
                    break
            elif my_demo.operatetype == 3:
                result = my_demo.open_door()
                if not result:
                    my_demo.logout()
                    my_demo.quit_demo()
                    break