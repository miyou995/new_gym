from ctypes import *
import platform
import re
import os

def system_get_platform_info():
    sys_platform = platform.system().lower().strip()
    python_bit = platform.architecture()[0]
    python_bit_num = re.findall('(\d+)\w*', python_bit)[0]
    return sys_platform, python_bit_num

sys_platform, python_bit_num = system_get_platform_info()
system_type = sys_platform + python_bit_num

netsdkdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'dhnetsdk.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'dhnetsdk.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libdhnetsdk.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libdhnetsdk.so'}
configdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'dhconfigsdk.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'dhconfigsdk.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libdhconfigsdk.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libdhconfigsdk.so'}
playsdkdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'dhplay.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'dhplay.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libdhplay.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libdhplay.so'}

C_LLONG_DICT = {'windows64': c_longlong, 'windows32': c_long, 'linux32': c_long, 'linux64': c_long}
C_LONG_DICT = {'windows64': c_long, 'windows32': c_long, 'linux32': c_int, 'linux64': c_int}
C_LDWORD_DICT = {'windows64': c_longlong, 'windows32': c_ulong, 'linux32': c_long, 'linux64': c_long}
C_DWORD_DICT = {'windows64': c_ulong, 'windows32': c_ulong, 'linux32': c_uint, 'linux64': c_uint}

C_LLONG = C_LLONG_DICT[system_type]
C_LONG = C_LONG_DICT[system_type]
C_LDWORD = C_LDWORD_DICT[system_type]
C_DWORD = C_DWORD_DICT[system_type]
C_TP_U64 = c_ulonglong
C_BOOL = c_int
C_UINT = c_uint
C_BYTE = c_ubyte
C_ENUM = c_int

if sys_platform == 'linux':
    load_library = cdll.LoadLibrary
    CB_FUNCTYPE = CFUNCTYPE
elif sys_platform == 'windows':
    load_library = windll.LoadLibrary
    CB_FUNCTYPE = WINFUNCTYPE
else:
    print("************不支持的平台**************")
    exit(0)

netsdkdllpath = netsdkdllpath_dict[system_type]
configdllpath = configdllpath_dict[system_type]
playsdkdllpath = playsdkdllpath_dict[system_type]


class NETSDK_INIT_PARAM(Structure):
    """
    初始化参数;Initialization parameter
    """
    _fields_ = [
        ("nThreadNum", c_int),                 # 指定NetSDK常规网络处理线程数, 当值为0时, 使用内部默认值; specify netsdk's normal network process thread number, zero means using default value
        ("bReserved", c_ubyte * 1024),         # 保留字节; reserved
    ]


class NET_PARAM(Structure):
    """
    设置登入时的相关参数;The corresponding parameter when setting log in
    """
    _fields_ = [
        ("nWaittime", c_int),                 # 等待超时时间(毫秒为单位),为0默认5000ms;Waiting time(unit is ms), 0:default 5000ms.
        ("nConnectTime", c_int),              # 连接超时时间(毫秒为单位),为0默认1500ms;Connection timeout value(Unit is ms), 0:default 1500ms.
        ("nConnectTryNum", c_int),            # 连接尝试次数,为0默认1次;Connection trial times, 0:default 1.
        ("nSubConnectSpaceTime", c_int),      # 子连接之间的等待时间(毫秒为单位),为0默认10ms;Sub-connection waiting time(Unit is ms), 0:default 10ms.
        ("nGetDevInfoTime", c_int),           # 获取设备信息超时时间,为0默认1000ms;Access to device information timeout, 0:default 1000ms.
        ("nConnectBufSize", c_int),           # 每个连接接收数据缓冲大小(字节为单位),为0默认250*1024;Each connected to receive data buffer size(Bytes), 0:default 250*1024
        ("nGetConnInfoTime", c_int),          # 获取子连接信息超时时间(毫秒为单位),为0默认1000ms;Access to sub-connect information timeout(Unit is ms), 0:default 1000ms.
        ("nSearchRecordTime", c_int),         # 按时间查询录像文件的超时时间(毫秒为单位),为0默认为3000ms;Timeout value of search video (unit ms), default 3000ms
        ("nsubDisconnetTime", c_int),         # 检测子链接断线等待时间(毫秒为单位),为0默认为60000ms;dislink disconnect time,0:default 60000ms
        ("byNetType", c_ubyte),               # 网络类型, 0-LAN, 1-WAN;net type, 0-LAN, 1-WAN
        ("byPlaybackBufSize", c_ubyte),       # 回放数据接收缓冲大小（M为单位）,为0默认为4M;playback data from the receive buffer size(m),when value = 0,default 4M
        ("bDetectDisconnTime", c_ubyte),      # 心跳检测断线时间(单位为秒),为0默认为60s,最小时间为2s;Pulse detect offline time(second) .When it is 0, the default setup is 60s, and the min time is 2s
        ("bKeepLifeInterval", c_ubyte),       # 心跳包发送间隔(单位为秒),为0默认为10s,最小间隔为2s;Pulse send out interval(second). When it is 0, the default setup is 10s, the min internal is 2s.
        ("nPicBufSize", c_int),               # 实时图片接收缓冲大小（字节为单位）,为0默认为2*1024*1024;actual pictures of the receive buffer size(byte)when value = 0,default 2*1024*1024
        ("bReserved", c_ubyte*4)              # 保留字段字段;reserved
    ]


class NET_DEVICEINFO(Structure):
    """
    设备信息;Device info
    """
    _fields_ = [
        ('sSerialNumber', c_char * 48),     # 序列号;serial number
        ('byAlarmInPortNum', c_ubyte),      # DVR报警输入个数;DVR alarm input amount
        ('byAlarmOutPortNum', c_ubyte),     # DVR报警输出个数;DVR alarm output amount
        ('byDiskNum', c_ubyte),             # DVR硬盘个数;DVR HDD amount
        ('byDVRType', c_ubyte),             # DVR类型,见枚举 NET_DEVICE_TYPE DVR type.Please refer to NET_DEVICE_TYPE
        ('byChanNum', c_ubyte),             # DVR通道个数,登陆成功时有效,当登陆失败原因为密码错误时,通过此参数通知用户,剩余登陆次数,为0时表示此参数无效; DVR channel amount,When login failed due to password error, notice user via this parameter, remaining login times, is 0 means this parameter is invalid
    ]


class LOG_SET_PRINT_INFO(Structure):
    """
    SDK全局日志打印信息;SDK global log print
    """
    _fields_ = [
        ('dwSize', C_DWORD),                # 结构体大小;Structure size
        ('bSetFilePath', c_int),            # 是否重设日志路径;reset log path
        ('szLogFilePath', c_char * 260),    # 日志路径(默认"./sdk_log/sdk_log.log");log path(default"./sdk_log/sdk_log.log")
        ('bSetFileSize', c_int),            # 是否重设日志文件大小;reset log size
        ('nFileSize', c_uint),              # 每个日志文件的大小(默认大小10240), 单位:KB;each log file size(default size 10240), unit:KB
        ('bSetFileNum', c_int),             # 是否重设日志文件个数;reset log file number
        ('nFileNum', c_uint),               # 绕接日志文件个数(默认大小10);log file quantity(default size 10)
        ('bSetPrintStrategy', c_int),       # 是否重设日志打印输出策略;reset log print strategy
        ('nPrintStrategy', c_uint),         # 日志输出策略, 0:输出到文件(默认); 1:输出到窗口;log out strategy, 0: output to file(defualt); 1:output to window
        ('byReserved', c_ubyte * 4),        # 字节对齐;Byte alignment
        ('cbSDKLogCallBack', CB_FUNCTYPE(c_int, c_char_p, c_uint, C_LDWORD)),   # 日志回调，需要将sdk日志回调出来时设置，默认为None,对应SDK_Callback的fSDKLogCallBack;log callback, (default None),corresponding to SDK_Callback's fSDKLogCallBack
        ('dwUser', C_LDWORD)                # 用户数据;UserData
    ]


class DEVICE_NET_INFO_EX(Structure):
    """
    设备信息;Device info
    """
    _fields_ = [
        ('iIPVersion', c_int),          # 4代表IPV4,6代表IPV6;4 for IPV4, 6 for IPV6
        ('szIP', c_char*64),            # IP IPV4形如"192.168.0.1" IPV6形如"2008::1/64",;IP IPV4 likes "192.168.0.1" ,IPV6 likes "2008::1/64"
        ('nPort', c_int),               # tcp端口;Port
        ('szSubmask', c_char*64),       # 子网掩码 IPV6无子网掩码;Subnet mask
        ('szGateway', c_char*64),       # 网关;Gate way
        ('szMac', c_char*40),           # MAC地址;Mac
        ('szDeviceType', c_char*32),    # 设备类型;Device type
        ('byManuFactory', c_ubyte),     # 目标设备的生产厂商,具体参考sdk_enum.py的EM_IPC_TYPE;Manu factory,refer to EM_IPC_TYPE in sdk_enum.py
        ('byDefinition', c_ubyte),      # 1-标清 2-高清;1-Standard definition 2-High definition
        ('bDhcpEn', c_bool),            # Dhcp使能状态, true-开, false-关;Dhcp, true-open, false-close
        ('byReserved1', c_ubyte),       # 字节对齐;reserved
        ('verifyData', c_char * 88),    # 校验数据 通过异步搜索回调获取(在修改设备IP时会用此信息进行校验);ECC data
        ('szSerialNo', c_char * 48),    # 序列号;serial no
        ('szDevSoftVersion', c_char * 128),  # 设备软件版本号;soft version
        ('szDetailType', c_char * 32),  # 设备型号;device detail type
        ('szVendor', c_char * 128),     # OEM客户类型; OEM type
        ('szDevName', c_char * 64),     # 设备名称;device name
        ('szUserName', c_char * 16),    # 登陆设备用户名（在修改设备IP时需要填写）;user name for log in device(it need be filled when modify device ip)
        ('szPassWord', c_char * 16),    # 登陆设备密码（在修改设备IP时需要填写）;pass word for log in device(it need be filled when modify device ip)
        ('nHttpPort', c_ushort),        # HTTP服务端口号;HTTP server port
        ('wVideoInputCh', c_ushort),    # 视频输入通道数;count of video input channel
        ('wRemoteVideoInputCh', c_ushort),  # 远程视频输入通道数;count of remote video input
        ('wVideoOutputCh', c_ushort),   # 视频输出通道数;count of video output channel
        ('wAlarmInputCh', c_ushort),    # 报警输入通道数;count of alarm input
        ('wAlarmOutputCh', c_ushort),   # 报警输出通道数;count of alarm output
        ('bNewWordLen', c_int),         # TRUE使用新密码字段szNewPassWord;TRUE:szNewPassWord Enable
        ('szNewPassWord', c_char*64),   # 登陆设备密码（在修改设备IP时需要填写）;pass word for log in device(it need be filled when modify device ip)
        ('byInitStatus', c_ubyte),      # 设备初始化状态，按位确定初始化状态;init status
			                            # bit0~1：0-老设备，没有初始化功能 1-未初始化账号 2-已初始化账户;bit0~1：0-old device, can not be init; 1-not init; 2-already init
                                        # bit2~3：0-老设备，保留 1-公网接入未使能 2-公网接入已使能;bit2~3：0-old device,reserved; 1-connect to public network disable; 2-connect to public network enable
                                        # bit4~5：0-老设备，保留 1-手机直连未使能 2-手机直连使能;bit4~5：0-old device,reserved; 1-connect to cellphone disable; 2-connect to cellphone enable
                                        # bit6~7: 0- 未知 1-不支持密码重置 2-支持密码重置;bit6~7: 0- unknown 1-unsupported reset password 2-support password
        ('byPwdResetWay', c_ubyte),     # 支持密码重置方式：按位确定密码重置方式，只在设备有初始化账号时有意义;the way supported for reset password:make sense when the device is init
                                        # bit0-支持预置手机号 bit1-支持预置邮箱 ,bit2-支持文件导出;bit0-support reset password by cellphone; bit1-support reset password by mail; bit2-support reset password by XML file;
                                        # bit3-支持密保问题 bit4-支持更换手机号;bit3-support reset password by security question; bit4-support reset password by change cellphone
        ('bySpecialAbility', c_ubyte),  # 设备初始化能力，按位确定初始化能力,高八位 bit0-2D Code修改IP: 0 不支持 1 支持, bit1-PN制:0 不支持 1支持
                                        # ENGLISH_LANG:special ability of device ,high eight bit, bit0-2D Code:0 support  1 no support, bit1-PN:0 support  1 no support
        ('szNewDetailType', c_char*64),     # 设备型号;device detail type
        ('bNewUserName', c_int),        # true(szNewUserName)字段;TRUE:szNewUserName enable
        ('szNewUserName', c_char * 64), # 登陆设备用户名（在修改设备IP时需要填写）;new user name for login device(it need be filled when modify device ip)
        ('byPwdFindVersion', c_ubyte),  # 密码找回的版本号,设备支持密码重置时有效;;password find version, effective when device supports reset password
                                        # 0-设备使用的是老方案的密码重置版本;1-支持预留联系方式进行密码重置操作;2-支持更换联系方式进行密码重置操作;
                                        # ENGLISH_LANG:0-device of old scheme reset password version;1-support reset password by reserved contact;2-support reset password by change contact;
        ('szDeviceID', c_char * 24),    # 定制字段, 不作为通用协议，不对接通用客户端;Custom item, do not use for general client
        ('dwUnLoginFuncMask', C_DWORD), # Bit0 Wifi列表扫描及WLan设置,Bit1 支持会话外修改过期密码;function mask before login, Bit0 means wifi config
        ('szMachineGroup', c_char * 64),  # 设备分组;machine group
        ('cReserved', c_char * 12),     # 扩展字段;reserved
    ]


class DEVICE_NET_INFO_EX2(Structure):
    """
    对应StartSearchDevicesEx接口;Corresponding to StartSearchDevicesEx
    """
    _fields_ = [
        ('stuDevInfo', DEVICE_NET_INFO_EX), # 设备信息结构体;device net info
        ('szLocalIP', c_char*64),           # 搜索到设备的本地IP地址;local ip
        ('cReserved', c_char*2048)          # 保留字段;reserved
    ]


class NET_DEVICEINFO_Ex(Structure):
    """
    设备信息扩展;Device extension info
    """
    _fields_ = [
        ('sSerialNumber', c_char * 48),     # 序列号;serial number
        ('nAlarmInPortNum', c_int),         # DVR报警输入个数;count of DVR alarm input
        ('nAlarmOutPortNum', c_int),        # DVR报警输出个数;count of DVR alarm output
        ('nDiskNum', c_int),                # DVR硬盘个数;number of DVR disk
        ('nDVRType', c_int),                # DVR类型;DVR type, refer to NET_DEVICE_TYPE
        ('nChanNum', c_int),                # DVR通道个数;number of DVR channel
        ('byLimitLoginTime', c_char),       # 在线超时时间,为0表示不限制登陆,非0表示限制的分钟数;Online Timeout, Not Limited Access to 0, not 0 Minutes Limit Said
        ('byLeftLogTimes', c_char),         # 当登陆失败原因为密码错误时,通过此参数通知用户,剩余登陆次数,为0时表示此参数无效; When login failed due to password error, notice user via this parameter, remaining login times, is 0 means this parameter is invalid
        ('bReserved', c_char * 2),          # 保留字节,字节对齐;keep bytes, bytes aligned
        ('nLockLeftTime', c_int),           # 当登陆失败,用户解锁剩余时间（秒数）, -1表示设备未设置该参数;when log in failed, the left time for users to unlock (seconds), -1 indicate the device haven't set the parameter
        ('Reserved', c_char * 24),          # 保留;reserved
    ]


class NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY(Structure):
    """
    LoginWithHighLevelSecurity 输入参数;LoginWithHighLevelSecurity input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),          # 结构体大小;Structrue size
        ('szIP', c_char*64),          # IP地址;IP address
        ('nPort', c_int),             # 端口;Port
        ('szUserName', c_char * 64),  # 用户名;User name
        ('szPassword', c_char * 64),  # 密码;Password
        ('emSpecCap', c_int),         # 登录模式,具体信息见sdk_enum.py内的EM_LOGIN_SPAC_CAP_TYPE;Spec login cap，refer to EM_LOGIN_SPAC_CAP_TYPE in sdk_enum.py
        ('byReserved', c_ubyte*4),    # 保留字节;Reserved
        ('pCapParam', c_void_p)       # emSpecCap = 0,pCapParam:None;emSpecCap = 0,pCapParam:None
                                      # emSpecCap = 2,pCapParam:None;emSpecCap = 2,pCapParam:None
                                      # emSpecCap = 3,pCapParam:None;emSpecCap = 3,pCapParam:None
                                      # emSpecCap = 4,pCapParam:None;emSpecCap = 4,pCapParam:None
                                      # emSpecCap = 6,pCapParam:None;emSpecCap = 6,pCapParam:None
                                      # emSpecCap = 7,pCapParam:None;emSpecCap = 7,pCapParam:None
                                      # emSpecCap = 9,pCapParam:填入远程设备的名字的字符串;emSpecCap = 9,pCapParam is string of remote device name
                                      # emSpecCap = 12,pCapParam:None;emSpecCap = 12,pCapParam:None
                                      # emSpecCap = 13,pCapParam:None;emSpecCap = 13,pCapParam:None
                                      # emSpecCap = 14,pCapParam:None;emSpecCap = 14,pCapParam:None
                                      # emSpecCap = 15,pCapParam:Socks5服务器的IP&&port&&ServerName&&ServerPassword字符串;emSpecCap = 15,pCapParam:IP&&port&&ServerName&&ServerPassword string of Socket5 server
                                      # emSpecCap = 16,pCapParam:SOCKET值;emSpecCap = 16,pCapParam:SOCKET value
                                      # emSpecCap = 19,pCapParam:None;emSpecCap = 19,pCapParam:None
                                      # emSpecCap = 20,pCapParam:None;emSpecCap = 20,pCapParam:None
    ]


class NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY(Structure):
    """
       LoginWithHighLevelSecurity 输出参数;LoginWithHighLevelSecurity output param
       """
    _fields_ = [
        ('dwSize', C_DWORD),                               # 结构体大小;Structrue size
        ('stuDeviceInfo', NET_DEVICEINFO_Ex),              # 设备信息;Device info
        ('nError', c_int),                                 # 错误码，见 Login 接口错误码;Error
        ('byReserved', c_ubyte * 132)                      # 预留字段,;Reserved
    ]


class NET_IN_STARTSERACH_DEVICE(Structure):
    """
    StartSearchDevicesEx接口输入参数;StartSearchDevicesEx input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小;Structrue size
        ('szLocalIp', c_char*64),       # 发起搜索的本地IP;local IP
        ('cbSearchDevices', CB_FUNCTYPE(None, C_LLONG, POINTER(DEVICE_NET_INFO_EX2), c_void_p)),   #设备信息回调函数;search device call back
        ('pUserData', c_void_p),        # 用户自定义数据;user data
        ('emSendType', c_int)           # 下发搜索类型,对应EM_SEND_SEARCH_TYPE;send search type,refer to EM_SEND_SEARCH_TYPE
    ]


class NET_OUT_STARTSERACH_DEVICE(Structure):
    """
        StartSearchDevicesEx接口输出参数;StartSearchDevicesEx output param
        """
    _fields_ = [
        ('dwSize', C_DWORD)           # 结构体大小，ENGLISH_LANG:Structrue size
    ]


class DEVICE_IP_SEARCH_INFO_IP(Structure):
    """
    具体待搜索的IP信息;the IPs info for search
    """
    _fields_ = [
        ('IP', c_char*64)               # 具体待搜索的IP信息;the IP for search
    ]


class DEVICE_IP_SEARCH_INFO(Structure):
    """
    SearchDevicesByIPs接口输入参数; SearchDevicesByIPs input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),                      # 结构体大小;Structure size
        ('nIpNum', c_int),                        # 当前搜索的IP个数;the IPs number for search
        ('szIP', DEVICE_IP_SEARCH_INFO_IP * 256)  # 具体待搜索的IP信息;the IPs info for search
    ]


class NET_IN_INIT_DEVICE_ACCOUNT(Structure):
    """
       InitDevAccount接口输入参数;InitDevAccount interface input param
       """
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小;Structure size
        ('szMac', c_char*40),           # 设备mac地址;mac addr
        ('szUserName', c_char * 128),   # 用户名;user name
        ('szPwd', c_char * 128),        # 设备密码;password
        ('szCellPhone', c_char * 32),   # 预留手机号;cellphone
        ('szMail', c_char * 64),        # 预留邮箱;mail addr
        ('byInitStatus', c_ubyte),      # 该字段废弃;this field already abandoned
        ('byPwdResetWay', c_ubyte),     # 设备支持的密码重置方式：搜索设备接口(StartSearchDevicesEx、SearchDevicesByIPs回调函数)返回字段byPwdResetWay的值
                                          # 该值的具体含义见 DEVICE_NET_INFO_EX2 结构体，需要与设备搜索接口返回的 byPwdResetWay 值保持一致
                                          # bit0 : 1-支持预留手机号，此时需要在szCellPhone数组中填入预留手机号(如果需要设置预留手机) ;
                                          # bit1 : 1-支持预留邮箱，此时需要在szMail数组中填入预留邮箱(如果需要设置预留邮箱)
                                          # the way supported for reset password:byPwdResetWay value of StartSearchDevicesEx's , SearchDevicesByIPs's callback function
                                          # the meaning of this parameter refers to DEVICE_NET_INFO_EX2, the value must be same as byPwdResetWay returned by StartSearchDevicesEx,SearchDevicesByIPs
                                          # bit0 : 1-support reset password by cellphone, you should set cellphone in szCellPhone if you need to set cellphone
                                          # bit1 : 1-support reset password by mail, you should set mail address in szMail if you need to set mail address
        ('byReserved', c_ubyte*2)       # 保留字段;Reserve
    ]


class NET_OUT_INIT_DEVICE_ACCOUNT(Structure):
    """
    InitDevAccount接口输出参数;InitDevAccount interface output param
    """
    _fields_ = [
        ('dwSize', C_DWORD)           # 结构体大小;Structrue size
    ]


class NET_TIME(Structure):
    """
    时间;time
    """
    _fields_ = [
        ('dwYear', C_DWORD),    # 年;Year
        ('dwMonth', C_DWORD),   # 月;Month
        ('dwDay', C_DWORD),     # 日;Date
        ('dwHour', C_DWORD),    # 时;Hour
        ('dwMinute', C_DWORD),  # 分;Minute
        ('dwSecond', C_DWORD)   # 秒;Second
    ]

class NET_RECORDFILE_INFO(Structure):
    """
    录像文件信息; Record file information
    """
    _fields_ = [
        ('ch', c_uint),                # 通道号; Channel number
        ('filename', c_char * 124),    # 文件名; File name
        ('framenum', c_uint),          # 文件总帧数; the total number of file frames
        ('size', c_uint),              # 文件长度, 单位为Kbyte; File length, unit: Kbyte
        ('starttime', NET_TIME),       # 开始时间; Start time
        ('endtime', NET_TIME),         # 结束时间; End time
        ('driveno', c_uint),           # 磁盘号(区分网络录像和本地录像的类型,0－127表示本地录像,其中64表示光盘1,128表示网络录像); HDD number
        ('startcluster', c_uint),      # 起始簇号; Initial cluster number
        ('nRecordFileType', c_ubyte),  # 录象文件类型  0：普通录象；1：报警录象；2：移动检测；3：卡号录象；4：图片, 5: 智能录像, 19: POS录像, 255:所有录像; Recorded file type  0:general record;1:alarm record ;2:motion detection;3:card number record ;4:image ; 19:Pos record ;255:all
        ('bImportantRecID', c_ubyte),  # 0:普通录像 1:重要录像; 0:general record 1:Important record
        ('bHint', c_ubyte),            # 文件定位索引(nRecordFileType==4<图片>时,bImportantRecID<<8 +bHint ,组成图片定位索引 ); Document Indexing
        ('bRecType', c_ubyte)          # 0-主码流录像 1-辅码1流录像 2-辅码流2 3-辅码流3录像; 0-main stream record 1-sub1 stream record 2-sub2 stream record 3-sub3 stream record
    ]


class NET_TIME_EX(Structure):
    """
    时间;time
    """
    _fields_ = [
        ('dwYear', C_DWORD),        # 年;Year
        ('dwMonth', C_DWORD),       # 月;Month
        ('dwDay', C_DWORD),         # 日;Date
        ('dwHour', C_DWORD),        # 时;Hour
        ('dwMinute', C_DWORD),      # 分;Minute
        ('dwSecond', C_DWORD),      # 秒;Second
        ('dwMillisecond', C_DWORD), # 毫秒;Millisecond
        ('dwUTC', C_DWORD),         # utc时间(获取时0表示无效，非0有效,下发无效);utc query: zero means invaild, non-zero means vaild;  set:invalid
        ('dwReserved', C_DWORD)     # 预留字段;reserved data
    ]

class SDK_RECT(Structure):
    """
     区域；各边距按整长8192的比例;Zone;Each margin is total lenght :8192
     """
    _fields_ = [
        ('left', c_long),       # 左;left
        ('top', c_long),        # 顶;top
        ('right', c_long),      # 右;right
        ('bottom', c_long)      # 底;bottom
    ]

class SDK_POINT(Structure):
    """
     二维空间点;2 dimension point
     """
    _fields_ = [
        ('nx', c_short),        # x轴;x
        ('ny', c_short)         # y轴;y
    ]

class SDK_PIC_INFO(Structure):
    """
     物体对应图片文件信息;picture info
     """
    _fields_ = [
        ('dwOffSet', C_DWORD),      # 文件在二进制数据块中的偏移位置, 单位:字节;current picture file's offset in the binary file, byte
        ('dwFileLenth', C_DWORD),   # 文件大小, 单位:字节;current picture file's size, byte
        ('wWidth', c_ushort),       # 图片宽度, 单位:像素;picture width, pixel
        ('wHeight', c_ushort),      # 图片高度, 单位:像素;picture high, pixel
        ('pszFilePath', c_char_p),  # 文件路径;File path
                                    # 鉴于历史原因,该成员只在事件上报时有效,用户使用该字段时需要自行申请空间进行拷贝保存;User use this field need to apply for space for copy and storage,When submit to the server, the algorithm has checked the image or not
        ('bIsDetected', c_ubyte),   # 图片是否算法检测出来的检测过的提交识别服务器时,则不需要再时检测定位抠图,1:检测过的,0:没有检测过;When submit to the server, the algorithm has checked the image or not
        ('bReserved', C_BYTE * 2),  # 预留字节数;reserved data;
        ('byQulityScore', C_BYTE),  # 人脸抓拍质量分数, 0-100;Quality score of face capture, range: 0-100;
        ('nFilePathLen', c_int),    # 文件路径长度 既pszFilePath 用户申请的大小;File path Len of pszFilePath
        ('stuPoint', SDK_POINT),    # 小图左上角在大图的位置，使用绝对坐标系;The upper left corner of the figure is in the big picture. Absolute coordinates are used
        ('nIndexInData', C_UINT),   # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
    ]

class SDK_MSG_OBJECT(Structure):
    """
    视频分析物体信息结构体;Struct of object info for video analysis
    """
    _pack_ = 4  # 补齐
    _fields_ = [
        ('nObjectID', c_int),           # 物体ID,每个ID表示一个唯一的物体;Object ID,each ID represent a unique object
        ('szObjectType', c_char*128),   # 物体类型;Object type
        ('nConfidence', c_int),         # 置信度(0~255),值越大表示置信度越高;Confidence(0~255),a high value indicate a high confidence
        ('nAction', c_int),             # 物体动作:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;Object action:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename
        ('BoundingBox', SDK_RECT),      # 包围盒;BoundingBox
        ('Center', SDK_POINT),          # 物体型心;The shape center of the object
        ('nPolygonNum', c_int),         # 多边形顶点个数;the number of culminations for the polygon
        ('Contour', SDK_POINT * 16),    # 较精确的轮廓多边形;a polygon that have a exactitude figure
        ('rgbaMainColor', C_DWORD),     # 表示车牌、车身等物体主要颜色；按字节表示,分别为红、绿、蓝和透明度,例如:RGB值为(0,255,0),透明度为0时, 其值为0x00ff0000.
                                        # The main color of the object;the first byte indicate red value, as byte order as green, blue, transparence, for example:RGB(0,255,0),transparence = 0, rgbaMainColor = 0x00ff0000.
        ('szText', c_char * 128),       # 物体上相关的带0结束符文本,比如车牌,集装箱号等等;the interrelated text of object,such as number plate,container number
                                            # "ObjectType"为"Vehicle"或者"Logo"时（尽量使用Logo。Vehicle是为了兼容老产品）表示车标,支持："ObjectType","Vehicle" or "Logo", try to use Logo.Vehicle is used to be compatible with old product, means logo, support:
                                            # "Unknown"未知;Unknown
                                            # "Audi" 奥迪;Audi
                                            # "Honda" 本田;Honda
                                            # "Buick" 别克;Buick
                                            # "Volkswagen" 大众;Volkswagen
                                            # "Toyota" 丰田;Toyota
                                            # "BMW" 宝马;BMW
                                            # "Peugeot" 标致;Peugeot
                                            # "Ford" 福特;Ford
                                            # "Mazda" 马自达;Mazda
                                            # "Nissan" 尼桑(日产);Nissan
                                            # "Hyundai" 现代;Hyundai
                                            # "Suzuki" 铃木;Suzuki
                                            # "Citroen" 雪铁龙;Citroen
                                            # "Benz" 奔驰;Benz
                                            # "BYD" 比亚迪;BYD
                                            # "Geely" 吉利;Geely
                                            # "Lexus" 雷克萨斯;Lexus
                                            # "Chevrolet" 雪佛兰;Chevrolet
                                            # "Chery" 奇瑞;Chery
                                            # "Kia" 起亚;Kia
                                            # "Charade" 夏利;Charade
                                            # "DF" 东风;DF
                                            # "Naveco" 依维柯;Naveco
                                            # "SGMW" 五菱;SGMW
                                            # "Jinbei" 金杯;Jinbei
                                            # "JAC" 江淮;JAC
                                            # "Emgrand" 帝豪;Emgrand
                                            # "ChangAn" 长安;ChangAn
                                            # "Great Wall" 长城;Great Wall
                                            # "Skoda" 斯柯达;Skoda
                                            # "BaoJun" 宝骏;BaoJun
                                            # "Subaru" 斯巴鲁;Subaru
                                            # "LandWind" 陆风;LandWind
                                            # "Luxgen" 纳智捷;Luxgen
                                            # "Renault" 雷诺;Renault
                                            # "Mitsubishi" 三菱;Mitsubishi
                                            # "Roewe" 荣威;Roewe
                                            # "Cadillac" 凯迪拉克;Cadillac
                                            # "MG" 名爵;MG
                                            # "Zotye" 众泰;Zotye
                                            # "ZhongHua" 中华;ZhongHua
                                            # "Foton" 福田;Foton
                                            # "SongHuaJiang" 松花江;SongHuaJiang
                                            # "Opel" 欧宝;Opel
                                            # "HongQi" 一汽红旗;HongQi
                                            # "Fiat" 菲亚特;Fiat
                                            # "Jaguar" 捷豹;Jaguar
                                            # "Volvo" 沃尔沃;Volvo
                                            # "Acura" 讴歌;Acura
                                            # "Porsche" 保时捷;Porsche
                                            # "Jeep" 吉普;Jeep
                                            # "Bentley" 宾利;Bentley
                                            # "Bugatti" 布加迪;Bugatti
                                            # "ChuanQi" 传祺;ChuanQi
                                            # "Daewoo" 大宇;Daewoo
                                            # "DongNan" 东南;DongNan
                                            # "Ferrari" 法拉利;Ferrari
                                            # "Fudi" 福迪;Fudi
                                            # "Huapu" 华普;Huapu
                                            # "HawTai" 华泰;HawTai
                                            # "JMC" 江铃;JMC
                                            # "JingLong" 金龙客车;JingLong
                                            # "JoyLong" 九龙;JoyLong
                                            # "Karry" 开瑞;Karry
                                            # "Chrysler" 克莱斯勒;Chrysler
                                            # "Lamborghini" 兰博基尼;Lamborghini
                                            # "RollsRoyce" 劳斯莱斯;RollsRoyce
                                            # "Linian" 理念;Linian
                                            # "LiFan" 力帆;LiFan
                                            # "LieBao" 猎豹;LieBao
                                            # "Lincoln" 林肯;Lincoln
                                            # "LandRover" 路虎;LandRover
                                            # "Lotus" 路特斯;Lotus
                                            # "Maserati" 玛莎拉蒂;Maserati
                                            # "Maybach" 迈巴赫;Maybach
                                            # "Mclaren" 迈凯轮;Mclaren
                                            # "Youngman" 青年客车;Youngman
                                            # "Tesla" 特斯拉;Tesla
                                            # "Rely" 威麟;Rely
                                            # "Lsuzu" 五十铃;Lsuzu
                                            # "Yiqi" 一汽;Yiqi
                                            # "Infiniti" 英菲尼迪;Infiniti
                                            # "YuTong" 宇通客车;YuTong
                                            # "AnKai" 安凯客车;AnKai
                                            # "Canghe" 昌河;Canghe
                                            # "HaiMa" 海马;HaiMa
                                            # "Crown" 丰田皇冠;Crown
                                            # "HuangHai" 黄海;HuangHai
                                            # "JinLv" 金旅客车;JinLv
                                            # "JinNing" 精灵;JinNing
                                            # "KuBo" 酷博;KuBo
                                            # "Europestar" 莲花;Europestar
                                            # "MINI" 迷你;MINI
                                            # "Gleagle" 全球鹰;Gleagle
                                            # "ShiDai" 时代;ShiDai
                                            # "ShuangHuan" 双环;ShuangHuan
                                            # "TianYe" 田野;TianYe
                                            # "WeiZi" 威姿;WeiZi
                                            # "Englon" 英伦;Englon
                                            # "ZhongTong" 中通客车;ZhongTong
                                            # "Changan" 长安轿车;Changan
                                            # "Yuejin" 跃进;Yuejin
                                            # "Taurus" 金牛星;Taurus
                                            # "Alto" 奥拓;Alto
                                            # "Weiwang" 威旺;Weiwang
                                            # "Chenglong" 乘龙;Chenglong
                                            # "Haige" 海格;Haige
                                            # "Shaolin" 少林客车;Shaolin
                                            # "Beifang" 北方客车;Beifang
                                            # "Beijing" 北京汽车;Beijing
                                            # "Hafu" 哈弗;Hafu
                                            # "BeijingTruck" 北汽货车;BeijingTruck
                                            # "Besturn" 奔腾;Besturn
                                            # "ChanganBus" 长安客车;ChanganBus
                                            # "Dodge" 道奇;Dodge
                                            # "DongFangHong" 东方红;DongFangHong
                                            # "DongFengTruck" 东风货车;DongFengTruck
                                            # "DongFengBus" 东风客车;DongFengBus
                                            # "MultiBrand" 多品牌;MultiBrand
                                            # "FotonTruck" 福田货车;FotonTruck
                                            # "FotonBus" 福田客车;FotonBus
                                            # "GagcTruck" 广汽货车;GagcTruck
                                            # "HaFei" 哈飞;HaFei
                                            # "HowoBus" 豪沃客车;HowoBus
                                            # "JACTruck" 江淮货车;JACTruck
                                            # "JACBus" 江淮客车;JACBus
                                            # "JMCTruck" 江铃货车;JMCTruck
                                            # "JieFangTruck" 解放货车;JieFangTruck
                                            # "JinBeiTruck" 金杯货车;JinBeiTruck
                                            # "KaiMaTruck" 凯马货车;KaiMaTruck
                                            # "CoasterBus" 柯斯达客车;CoasterBus
                                            # "MudanBus" 牡丹客车;MudanBus
                                            # "NanJunTruck" 南骏货车;NanJunTruck
                                            # "QingLing" 庆铃;QingLing
                                            # "NissanCivilian" 日产碧莲客车;NissanCivilian
                                            # "NissanTruck" 日产货车;NissanTruck
                                            # "MitsubishiFuso" 三菱扶桑;MitsubishiFuso
                                            # "SanyTruck" 三一货车;SanyTruck
                                            # "ShanQiTruck" 陕汽货车;ShanQiTruck
                                            # "ShenLongBus" 申龙客车;ShenLongBus
                                            # "TangJunTruck" 唐骏货车;TangJunTruck
                                            # "MicroTruck" 微货车;MicroTruck
                                            # "VolvoBus" 沃尔沃客车;VolvoBus
                                            # "LsuzuTruck" 五十铃货车;LsuzuTruck
                                            # "WuZhengTruck" 五征货车;WuZhengTruck
                                            # "Seat" 西雅特;Seat
                                            # "YangZiBus" 扬子客车;YangZiBus
                                            # "YiqiBus" 一汽客车;YiqiBus
                                            # "YingTianTruck" 英田货车;YingTianTruck
                                            # "YueJinTruck" 跃进货车;YueJinTruck
                                            # "ZhongDaBus" 中大客车;ZhongDaBus
                                            # "ZxAuto" 中兴;ZxAuto
                                            # "ZhongQiWangPai" 重汽王牌;ZhongQiWangPai
                                            # "WAW" 奥驰;WAW
                                            # "BeiQiWeiWang" 北汽威旺;BeiQiWeiWang
                                            # "BYDDaimler"	比亚迪戴姆勒;BYDDaimler
                                            # "ChunLan" 春兰;ChunLan
                                            # "DaYun" 大运;DaYun
                                            # "DFFengDu" 东风风度;DFFengDu
                                            # "DFFengGuang" 东风风光;DFFengGuang
                                            # "DFFengShen" 东风风神;DFFengShen
                                            # "DFFengXing" 东风风行;DFFengXing
                                            # "DFLiuQi" 东风柳汽;DFLiuQi
                                            # "DFXiaoKang" 东风小康;DFXiaoKang
                                            # "FeiChi" 飞驰;FeiChi
                                            # "FordMustang" 福特野马;FordMustang
                                            # "GuangQi" 广汽;GuangQi
                                            # "GuangTong" 广通;GuangTong
                                            # "HuiZhongTruck" 汇众重卡;HuiZhongTruck
                                            # "JiangHuai" 江环;JiangHuai
                                            # "SunWin" 申沃;SunWin
                                            # "ShiFeng" 时风;ShiFeng
                                            # "TongXin" 同心;TongXin
                                            # "WZL" 五洲龙;WZL
                                            # "XiWo" 西沃;XiWo
                                            # "XuGong" 徐工;XuGong
                                            # "JingGong" 精工;JingGong
                                            # "SAAB" 萨博;SAAB
                                            # "SanHuanShiTong" 三环十通;SanHuanShiTong
                                            # "KangDi" 康迪;KangDi
                                            # "YaoLong" 耀隆;YaoLong
        ('szObjectSubType', c_char*62),     # 物体子类别,根据不同的物体类型,可以取以下子类型：
                                            # Vehicle Category:"Unknown"  未知,"Motor" 机动车,"Non-Motor":非机动车,"Bus": 公交车,"Bicycle" 自行车,"Motorcycle":摩托车,"PassengerCar":客车,
                                            # "LargeTruck":大货车,    "MidTruck":中货车,"SaloonCar":轿车,"Microbus":面包车,"MicroTruck":小货车,"Tricycle":三轮车,    "Passerby":行人
                                            # "DregsCar":渣土车, "Excavator":挖掘车, "Bulldozer":推土车, "Crane":吊车, "PumpTruck":泵车, "MachineshopTruck":工程车
                                            # Plate Category："Unknown" 未知,"Normal" 蓝牌黑牌,"Yellow" 黄牌,"DoubleYellow" 双层黄尾牌,"Police" 警牌"Armed" 武警牌,
                                            # "Military" 部队号牌,"DoubleMilitary" 部队双层,"SAR" 港澳特区号牌,"Trainning" 教练车号牌
                                            # "Personal" 个性号牌,"Agri" 农用牌,"Embassy" 使馆号牌,"Moto" 摩托车号牌,"Tractor" 拖拉机号牌,"Other" 其他号牌
                                            # "Civilaviation"民航号牌,"Black"黑牌
                                            # "PureNewEnergyMicroCar"纯电动新能源小车,"MixedNewEnergyMicroCar,"混合新能源小车,"PureNewEnergyLargeCar",纯电动新能源大车
                                            # "MixedNewEnergyLargeCar"混合新能源大车
                                            # HumanFace Category:"Normal" 普通人脸,"HideEye" 眼部遮挡,"HideNose" 鼻子遮挡,"HideMouth" 嘴部遮挡,"TankCar"槽罐车(装化学药品、危险品)
                                            # object sub type,different object type has different sub type:
                                            # Vehicle Category:"Unknown","Motor","Non-Motor","Bus","Bicycle","Motorcycle",
                                            # "DregsCar", "Excavator", "Bulldozer", "Crane", "PumpTruck", "MachineshopTruck"
                                            # Plate Category:"Unknown","mal","Yellow","DoubleYellow","Police","Armed",
                                            # "Military","DoubleMilitary","SAR","Trainning"
                                            # "Personal" ,"Agri","Embassy","Moto","Tractor","Other"
                                            # HumanFace Category:"Normal","HideEye","HideNose","HideMouth","TankCar"
        ('wColorLogoIndex', c_ushort),      # 车标索引;the index of car logo
        ('wSubBrand', c_ushort),            # 车辆子品牌 需要通过映射表得到真正的子品牌 映射表详见开发手册;Specifies the sub-brand of vehicle,the real value can be found in a mapping table from the development manual
        ('byReserved1', c_ubyte),           # 保留字段;Reserve
        ('bPicEnble', c_bool),              # 是否有物体对应图片文件信息; picture info enable
        ('stPicInfo', SDK_PIC_INFO),        # 物体对应图片信息;picture info
        ('bShotFrame', c_bool),             # 是否是抓拍张的识别结果;is shot frame
        ('bColor', c_bool),                 # 物体颜色(rgbaMainColor)是否可用; rgbaMainColor is enable
        ('byReserved2', c_ubyte),           # 保留字段;Reserve
        ('byTimeType', c_ubyte),            # 时间表示类型,详见EM_TIME_TYPE说明;Time indicates the type of detailed instructions, EM_TIME_TYPE
        ('stuCurrentTime', NET_TIME_EX),    # 针对视频浓缩,当前时间戳（物体抓拍或识别时,会将此识别智能帧附在一个视频帧或jpeg图片中,此帧所在原始视频中的出现时间）
                                            # in view of the video compression,current time(when object snap or reconfnition, the frame will be attached to the frame in a video or pictures,means the frame in the original video of the time)
        ('stuStartTime', NET_TIME_EX),      # 开始时间戳（物体开始出现时);strart time(object appearing for the first time)
        ('stuEndTime', NET_TIME_EX),        # 结束时间戳（物体最后出现时）;end time(object appearing for the last time)
        ('stuOriginalBoundingBox', SDK_RECT),  # 包围盒(绝对坐标);original bounding box(absolute coordinates)
        ('stuSignBoundingBox', SDK_RECT),   # 车标坐标包围盒;sign bounding box coordinate
        ('dwCurrentSequence', C_DWORD),     # 当前帧序号（抓下这个物体时的帧）; The current frame number (frames when grabbing the object)
        ('dwBeginSequence', C_DWORD),       # 开始帧序号（物体开始出现时的帧序号）;Start frame number (object appeared When the frame number,
        ('dwEndSequence', C_DWORD),         # 结束帧序号（物体消逝时的帧序号）;The end of the frame number (when the object disappearing Frame number)
        ('nBeginFileOffset', c_int64),      # 开始时文件偏移, 单位: 字节（物体开始出现时,视频帧在原始视频文件中相对于文件起始处的偏移）;At the beginning of the file offset, Unit: Word Section (when objects began to appear, the video frames in the original video file offset relative to the beginning of the file,
        ('nEndFileOffset', c_int64),        # 结束时文件偏移, 单位: 字节（物体消逝时,视频帧在原始视频文件中相对于文件起始处的偏移）;At the end of the file offset, Unit: Word Section (when the object disappeared, video frames in the original video file offset relative to the beginning of the file)
        ('byColorSimilar', c_ubyte*8),      # 物体颜色相似度,取值范围：0-100,数组下标值代表某种颜色,详见EM_COLOR_TYPE;Object color similarity, the range :0-100, represents an array subscript Colors, see EM_COLOR_TYPE,
        ('byUpperBodyColorSimilar', c_ubyte*8), # 上半身物体颜色相似度(物体类型为人时有效);When upper body color similarity (valid object type man ,
        ('byLowerBodyColorSimilar', c_ubyte*8), # 下半身物体颜色相似度(物体类型为人时有效);Lower body color similarity when objects (object type human valid ,
        ('nRelativeID', c_int),             # 相关物体ID;ID of relative object
        ('szSubText', c_char*20),           # "ObjectType"为"Vehicle"或者"Logo"时,表示车标下的某一车系,比如奥迪A6L,由于车系较多,SDK实现时透传此字段,设备如实填写。
                                            # "ObjectType"is "Vehicle" or "Logo",  means a certain brand under LOGO, such as Audi A6L, since there are so many brands, SDK sends this field in real-time ,device filled as real.
        ('wBrandYear', c_ushort)            # 车辆品牌年款 需要通过映射表得到真正的年款 映射表详见开发手册;Specifies the model years of vehicle. the real value can be found in a mapping table from the development manual
    ]

class SDK_EVENT_FILE_INFO(Structure):
    """
    事件对应文件信息;event file info
    """
    _fields_ = [
        ('bCount', c_ubyte),                # 当前文件所在文件组中的文件总数;the file count in the current file's group
        ('bIndex', c_ubyte),                # 当前文件在文件组中的文件编号(编号1开始);the index of the file in the group
        ('bFileTag', c_ubyte),              # 文件标签, EM_EVENT_FILETAG;file tag, see the enum struct EM_EVENT_FILETAG
        ('bFileType', c_ubyte),             # 文件类型,0-普通 1-合成 2-抠图;file type,0-normal 1-compose 2-cut picture
        ('stuFileTime', NET_TIME_EX),       # 文件时间;file time
        ('nGroupId', C_DWORD)               # 同一组抓拍文件的唯一标识;the only id of one group file
    ]

class SDK_RESOLUTION_INFO(Structure):
    """
    图片分辨率;pic resolution
    """
    _fields_ = [
        ('snWidth', c_ushort),      # 宽;width
        ('snHight', c_ushort)       # 高;hight
    ]

class EVENT_CUSTOM_WEIGHT_INFO(Structure):
    """
    建委地磅定制称重信息;custom weight info
    """
    _fields_ = [
        ('dwRoughWeight', C_DWORD),     # 毛重,车辆满载货物重量。单位KG;Rough Weight,unit:KG
        ('dwTareWeight', C_DWORD),      # 皮重,空车重量。单位KG;Tare Weight,unit:KG
        ('dwNetWeight', C_DWORD),       # 净重,载货重量。单位KG;Net Weight,unit:KG
        ('bReserved', c_ubyte*28)       # 预留字节;Rough Weight,unit:KG
    ]

class NET_RADAR_FREE_STREAM(Structure):
    """
    雷达自由流信息;Radar free stream information
    """
    _fields_ = [
        ('nABSTime', C_TP_U64),             # 1年1月1日0时起至今的毫秒数;millisecond from 0001-01-01 00:00:00
        ('nVehicleID', c_int),              # 车辆ID;Vehicle ID
        ('unOBUMAC', c_uint),               # OBU的MAC地址;MAC of on board unit
    ]

class NET_CUSTOM_MEASURE_TEMPER(Structure):
    """
    测温信息
    Measure temper
    """
    _fields_ = [
        ('fLeft', c_float),  # 车辆左侧温度值;The temperature of the left side of the vehicle;
        ('fRight', c_float),  # 车辆右侧温度值;The temperature of the right side of the vehicle;
        ('fHead', c_float),  # 车辆发动机位置温度值 (车头);Vehicle engine position temperature value;
        ('emUnit', C_ENUM),  # 温度单位 Refer: EM_TEMPERATURE_UNIT;Temperature unit Refer: EM_TEMPERATURE_UNIT;
    ]

class EVENT_JUNCTION_CUSTOM_INFO(Structure):
    """
    卡口事件专用定制上报内容，定制需求增加到Custom下;custom info in
    """
    _fields_ = [
        ('stuWeightInfo', EVENT_CUSTOM_WEIGHT_INFO),  # 原始图片信息;custom weight info;
        ('nCbirFeatureOffset', C_DWORD),    # 数据偏移，单位字节 （由于结构体保留字节有限的限制,添加在此处， 下同）;Content Based Image Retrieval Feature offset,Unit:Byte;
        ('nCbirFeatureLength', C_DWORD),    # 数据大小，单位字节;Content Based Image Retrieval Feature length,Unit:Byte;
        ('dwVehicleHeadDirection', C_DWORD),  # 车头朝向 0:未知 1:左 2:中 3:右;Head direction 0:Unknown 1:left 2:center 3:right;
        ('nAvailableSpaceNum', C_UINT), # 停车场车位余位数量 (出入口相机项目定制需求）;Number of available parking space(customized demand for entrance and exit camera project);
        ('stuRadarFreeStream', NET_RADAR_FREE_STREAM),  # 雷达自由流信息;Radar free stream info;
        ('stuMeasureTemper', NET_CUSTOM_MEASURE_TEMPER),  # 测温信息;Measure temperature.;
        ('bReserved', C_BYTE * 12),  # 预留字节;Reserved;
    ]

class NET_GPS_INFO(Structure):
    """
    GPS信息;GPS Infomation
    """
    _pack_ = 4                              # 补齐
    _fields_ = [
        ('nLongitude', c_uint),             # 经度(单位是百万分之一度);Longitude(unit:1/1000000 degree)
                                            # 西经：0 - 180000000	实际值应为: 180*1000000 – dwLongitude;west Longitude: 0 - 180000000 practical value = 180*1000000 - dwLongitude
                                            # 东经：180000000 - 360000000	实际值应为: dwLongitude – 180*1000000;east Longitude: 180000000 - 360000000    practical value = dwLongitude - 180*1000000
                                            # 如: 300168866应为（300168866 - 180 * 1000000）/ 1000000 即东经120.168866度;eg: Longitude:300168866  (300168866 - 180*1000000)/1000000  equal east Longitude 120.168866 degree
        ('nLatidude', c_uint),              # 纬度(单位是百万分之一度);Latidude(unit:1/1000000 degree)
                                            # 南纬：0 - 90000000 实际值应为: 90*1000000 – dwLatidude;north Latidude: 0 - 90000000				practical value = 90*1000000 - dwLatidude
                                            # 北纬：90000000 – 180000000	实际值应为: dwLatidude – 90*1000000;south Latidude: 90000000 - 180000000	practical value = dwLatidude - 90*1000000
                                            # 如: 120186268应为 (120186268 - 90*1000000)/1000000 即北纬30. 186268度;eg: Latidude:120186268 (120186268 - 90*1000000)/1000000 equal south Latidude 30. 186268 degree
        ('dbAltitude', c_double),           # 高度,单位为米;altitude,unit:m
        ('dbSpeed', c_double),              # 速度,单位km/H;Speed,unit:km/H
        ('dbBearing', c_double),            # 方向角,单位°;Bearing,unit:°
        ('bReserved', c_ubyte*8)            # 保留字段;Reserved bytes
    ]

class NET_COLOR_RGBA(Structure):
    """
    颜色RGBA;color RGBA
    """
    _fields_ = [
        ('nRed', c_int),            # 红;red
        ('nGreen', c_int),          # 绿;green
        ('nBlue', c_int),           # 蓝;blue
        ('nAlpha', c_int)           # 透明;transparent
    ]

class NET_EXTENSION_INFO(Structure):
    """
    事件扩展信息;Extension info
    """
    _fields_ = [
        ('szEventID', c_char*52),       # 国标事件ID;Chinese standard event ID
        ('byReserved', c_ubyte*80)      # 保留字节;Reserved
    ]

class DRIVING_DIRECTION(Structure):
    """
    行驶方向;Driving direction
    """
    _fields_ = [
        ('DrivingDirection', c_char*256)    # 行驶方向;Driving direction
    ]

class SDK_SIG_CARWAY_INFO_EX(Structure):
    """
    车检器冗余信息;Vehicle detector redundancy info
    """
    _fields_ = [
        ('byRedundance', c_ubyte*8),        # 由车检器产生抓拍信号冗余信息;The vehicle detector generates the snap signal redundancy info
        ('bReserved', c_ubyte * 120)        # 保留字段;Reserved
    ]


class NET_WHITE_LIST_AUTHORITY_LIST(Structure):
    """
    白名单权限列表;authority list of white list
    """
    _fields_ = [
        ('bOpenGate', c_int),      # 是否有开闸权限;true:having open gate authority,false:no having open gate authority
        ('bReserved', c_ubyte*16)  # 保留字节;reserved
    ]


class NET_TRAFFICCAR_WHITE_LIST(Structure):
    """
    白名单信息;white list information
    """
    _fields_ = [
        ('bTrustCar', c_int),         # 车牌是否属于白名单;true: the car is trust car,false:the car is not trust car
        ('stuBeginTime', NET_TIME),   # 白名单起始时间;begin time of white list
        ('stuCancelTime', NET_TIME),  # 白名单过期时间;cancel time of white list
        ('stuAuthorityList', NET_WHITE_LIST_AUTHORITY_LIST),  # 白名单权限列表;authority list of white list
        ('bReserved', c_ubyte*32)     # 保留字节;Reserved
    ]

class NET_TRAFFICCAR_BLACK_LIST(Structure):
    """
    黑名单信息;Blacklist information
    """
    _fields_ = [
        ('bEnable', c_int),          # 黑名单信息;Enable blacklist
        ('bIsBlackCar', c_int),      # 车牌是否属于黑名单;Whether is the plate on the blacklist or not
        ('stuBeginTime', NET_TIME),  # 黑名单起始时间;Begin time
        ('stuCancelTime', NET_TIME), # 黑名单过期时间;Cancel time
        ('bReserved', c_ubyte * 32)  # 保留字节;Reserved
    ]

class NET_RECT(Structure):
    """
    事件上报携带卡片信息;Incidents reported to carry the card information
    """
    _fields_ = [
        ('nLeft', c_int),       # 左;Left
        ('nTop', c_int),        # 顶;Top
        ('nRight', c_int),      # 右;Right
        ('nBottom', c_int)      # 底;Bottom
    ]

class DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO(Structure):
    """
    交通车辆信息;TrafficCar information
    """
    _fields_ = [
        ('szPlateNumber', c_char * 32),     # 车牌号码;plate number
        ('szPlateType', c_char * 32),       # 号牌类型 "Unknown" 未知; "Normal" 蓝牌黑牌; "Yellow" 黄牌; "DoubleYellow" 双层黄尾牌;Plate type: "Unknown" =Unknown; "Normal"=Blue and black plate. "Yellow"=Yellow plate. "DoubleYellow"=Double-layer yellow plate
                                            # "Police" 警牌; "Armed" 武警牌; "Military" 部队号牌; "DoubleMilitary" 部队双层;"Police"=Police plate ; "Armed"= =Military police plate; "Military"=Army plate; "DoubleMilitary"=Army double-layer
                                            # "SAR" 港澳特区号牌; "Trainning" 教练车号牌; "Personal" 个性号牌; "Agri" 农用牌;"SAR" =HK SAR or Macao SAR plate; "Trainning" =rehearsal plate; "Personal"=Personal plate; "Agri"=Agricultural plate
                                            # "Embassy" 使馆号牌; "Moto" 摩托车号牌; "Tractor" 拖拉机号牌; "Other" 其他号牌; "Embassy"=Embassy plate; "Moto"=Moto plate ; "Tractor"=Tractor plate; "Other"=Other plate
        ('szPlateColor', c_char * 32),      # 车牌颜色    "Blue","Yellow", "White","Black","YellowbottomBlackText","BluebottomWhiteText","BlackBottomWhiteText","ShadowGreen","YellowGreen"
                                            # plate color, "Blue","Yellow", "White","Black","YellowbottomBlackText","BluebottomWhiteText","BlackBottomWhiteText","ShadowGreen","YellowGreen"
        ('szVehicleColor', c_char * 32),    # 车身颜色    "White", "Black", "Red", "Yellow", "Gray", "Blue","Green";vehicle color, "White", "Black", "Red", "Yellow", "Gray", "Blue","Green"
        ('nSpeed', c_int),                  # 速度,单位Km/H;speed, Km/H
        ('szEvent', c_char*64),             # 触发的相关事件,参见事件列表Event List,只包含交通相关事件;trigger event type
        ('szViolationCode', c_char * 32),   # 违章代码;violation code
        ('szViolationDesc', c_char * 64),   # 违章描述;violation describe
        ('nLowerSpeedLimit', c_int),        # 速度下限;lower speed limit
        ('nUpperSpeedLimit', c_int),        # 速度上限;upper speed limit
        ('nOverSpeedMargin', c_int),        # 限高速宽限值,单位：km/h;over speed margin, km/h
        ('nUnderSpeedMargin', c_int),       # 限低速宽限值,单位：km/h;under speed margin, km/h
        ('nLane', c_int),                   # 车道,参见事件列表Event List中卡口和路口事件;lane
        ('nVehicleSize', c_int),            # 车辆大小,-1表示未知,否则按位;vehicle size, see VideoAnalyseRule's describe
                                             # 第0位:"Light-duty", 小型车;Bit 0:"Light-duty", small car
                                             # 第1位:"Medium", 中型车;Bit 1:"Medium", medium car
                                             # 第2位:"Oversize", 大型车;Bit 2:"Oversize", large car
                                             # 第3位:"Minisize", 微型车;Bit 3:"Minisize", mini car
                                             # 第4位:"Largesize", 长车;Bit 4:"Largesize", long car
        ('fVehicleLength', c_float),        # 车辆长度,单位米;vehicle length, Unit:m
        ('nSnapshotMode', c_int),           # 抓拍方式,0-未分类,1-全景,2-近景,4-同向抓拍,8-反向抓拍,16-号牌图像;snap mode 0-normal,1-globle,2-near,4-snap on the same side,8-snap on the reverse side,16-plant picture
        ('szChannelName', c_char*32),       # 本地或远程的通道名称,可以是地点信息,来源于通道标题配置ChannelTitle.Name;channel name
        ('szMachineName', c_char*256),      # 本地或远程设备名称,来源于普通配置General.MachineName;Machine name
        ('szMachineGroup', c_char * 256),   # 机器分组或叫设备所属单位,默认为空,用户可以将不同的设备编为一组,便于管理,可重复;machine group
        ('szRoadwayNo', c_char*64),         # 道路编号;road way number
        ('szDrivingDirection', DRIVING_DIRECTION * 3),      # 行驶方向 , "DrivingDirection" : ["Approach", "上海", "杭州"];DrivingDirection: for example ["Approach", "Shanghai", "Hangzhou"]
                                                            # "Approach"-上行,即车辆离设备部署点越来越近；"Leave"-下行;"Approach" means driving direction,where the car is more near;"Leave"-means where if mor far to the car
                                                            # 即车辆离设备部署点越来越远,第二和第三个参数分别代表上行和下行的两个地点;the second and third param means the location of the driving direction
        ('szDeviceAddress', c_char_p),      # 设备地址,OSD叠加到图片上的,来源于配置TrafficSnapshot.DeviceAddress,'\0'结束;device address,OSD superimposed onto the image,from TrafficSnapshot.DeviceAddress,'\0'means end.
        ('szVehicleSign', c_char*32),       # 车辆标识, 例如 "Unknown"-未知, "Audi"-奥迪, "Honda"-本田 ...;Vehicle identification, such as "Unknown" - unknown "Audi" - Audi, "Honda" - Honda ...
        ('stuSigInfo', SDK_SIG_CARWAY_INFO_EX),             # 由车检器产生抓拍信号冗余信息;Generated by the vehicle inspection device to capture the signal redundancy
        ('szMachineAddr', c_char_p),        # 设备部署地点;Equipment deployment locations
        ('fActualShutter', c_float),        # 当前图片曝光时间,单位为毫秒;Current picture exposure time, in milliseconds
        ('byActualGain', c_ubyte),          # 当前图片增益,范围为0~100;Current picture gain, ranging from 0 to 100
        ('byDirection', c_ubyte),           # 车道方向,0-南向北 1-西南向东北 2-西向东 3-西北向东南 4-北向南 5-东北向西南 6-东向西 7-东南向西北 8-未知 9-自定义;
                                            # Lane Direction,0 - south to north 1- Southwest to northeast 2 - West to east, 3 - Northwest to southeast 4 - north to south 5 - northeast to southwest 6 - East to West 7 - Southeast to northwest 8 - Unknown 9-customized
        ('byReserved', c_ubyte*2),          # 预留字节;Reserved
        ('szDetailedAddress', c_char_p),    # 详细地址, 作为szDeviceAddress的补充;Address, as szDeviceAddress supplement
        ('szDefendCode', c_char*64),        # 图片防伪码;waterproof
        ('nTrafficBlackListID', c_int),     # 关联黑名单数据库记录默认主键ID, 0,无效；> 0,黑名单数据记录;Link black list data recorddefualt main keyID, 0, invalid, > 0, black list data record
        ('stuRGBA', NET_COLOR_RGBA),        # 车身颜色RGBA;bofy color RGBA
        ('stSnapTime', NET_TIME),           # 抓拍时间;snap time
        ('nRecNo', c_int),                  # 记录编号;Rec No
        ('szCustomParkNo', c_char*33),      # 自定义车位号（停车场用）;self defined parking space number, for parking
        ('byReserved1', c_ubyte * 3),       # 预留字节;Reserved
        ('nDeckNo', c_int),                 # 车板位号;Metal plate No.
        ('nFreeDeckCount', c_int),          # 空闲车板数量;Free metal plate No.
        ('nFullDeckCount', c_int),          # 占用车板数量;Occupized metal plate No.
        ('nTotalDeckCount', c_int),         # 总共车板数量;Total metal plate No.
        ('szViolationName', c_char * 64),   # 违章名称;violation name
        ('nWeight', c_uint),                # 车重(单位 Kg);Weight of car(kg)
        ('szCustomRoadwayDirection', c_char * 32),  # 自定义车道方向,byDirection为9时有效;custom road way, valid when byDirection is 9
        ('byPhysicalLane', c_ubyte),        # 物理车道号,取值0到5;the physical lane number,value form 0 to 5
        ('byReserved2', c_ubyte * 3),       # 预留字节;Reserved
        ('emMovingDirection', c_int),       # 车辆行驶方向,值的意义见EM_TRAFFICCAR_MOVE_DIRECTION;moving direction
        ('stuEleTagInfoUTC', NET_TIME),     # 对应电子车牌标签信息中的过车时间(ThroughTime);corresponding to throughTime
        ('stuCarWindowBoundingBox', NET_RECT),          # 车窗包围盒，0~8191;The BoundingBox of car window , 0~8191
        ('stuWhiteList', NET_TRAFFICCAR_WHITE_LIST),    # 白名单信息;white list information
        ('emCarType', c_int),               # 车辆类型,详见EM_TRAFFICCAR_CAR_TYPE;car type,refer to EM_TRAFFICCAR_CAR_TYPE
        ('emLaneType', c_int),              # 车道类型,详见EM_TRAFFICCAR_LANE_TYPE;Lane type,refer to EM_TRAFFICCAR_LANE_TYPE
        ('szVehicleBrandYearText', c_char * 64),        # 车系年款翻译后文本内容;Translated year of vehicle
        ('szCategory', c_char * 32),        # 车辆子类型;category
        ('stuBlackList',NET_TRAFFICCAR_BLACK_LIST),     # 黑名单信息;Blacklist information
        ('emFlowDirection', C_ENUM),    # 车流量方向 Refer: EM_VEHICLE_DIRECTION;Traffic flow direction Refer: EM_VEHICLE_DIRECTION;
        ('emTollsVehicleType', C_ENUM), # 收费公路车辆通行费车型分类 Refer: EM_TOLLS_VEHICLE_TYPE;Classification of toll road vehicle types Refer: EM_TOLLS_VEHICLE_TYPE;
        ('nAxleType', C_UINT),  # 轴型代码,参考轴型国标 0代表其他;Shaft type code, refer to the national standard of shaft type, and 0 represents others;
        ('nAxleCount', C_UINT),  # 车轴数量;Number of axles;
        ('nWheelNum', C_UINT),  # 车轮数量;Number of wheels;
        ('bReserved', c_ubyte * 220)        # 保留字节,留待扩展;Reserved bytes.
    ]

class EVENT_CARD_INFO(Structure):
    """
    事件上报携带卡片信息;Incidents reported to carry the card information
    """
    _fields_ = [
        ('szCardNumber', c_char*36),       # 卡片序号字符串;Card number string
        ('bReserved', c_ubyte*32)          # 保留字节,留待扩展;Reserved bytes, leave extended
    ]

class SDK_MSG_OBJECT_EX(Structure):
    """
    视频分析物体信息扩展结构体;Video analysis object info expansion structure
    """
    _pack_ = 4  # 补齐
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小;Structure size
        ('nObjectID', c_int),           # 物体ID,每个ID表示一个唯一的物体;object ID, each ID means a exclusive object
        ('szObjectType', c_char * 128), # 物体类型;object type
        ('nConfidence', c_int),         # 置信度(0~255),值越大表示置信度越高;confidence coefficient (0~255),  value the bigger means  confidence coefficient the higher
        ('nAction', c_int),             # 物体动作:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;object  motion :1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename
        ('BoundingBox', SDK_RECT),      # 包围盒;box
        ('Center', SDK_POINT),          # 物体型心;object model center
        ('nPolygonNum', c_int),         # 多边形顶点个数;polygon vertex number
        ('Contour', SDK_POINT * 16),    # 较精确的轮廓多边形;relatively accurate outline the polygon
        ('rgbaMainColor', C_DWORD),     # 表示车牌、车身等物体主要颜色；按字节表示,分别为红、绿、蓝和透明度,例如:RGB值为(0,255,0),透明度为0时, 其值为0x00ff0000.;means plate, vehicle body and etc. object major color, by byte means , are red, green, blue and transparency , such as:RGB value is (0,255,0), transparency is 0, its value is 0x00ff0000.
        ('szText', c_char * 128),       # 同SDK_MSG_OBJECT相应字段;same as SDK_MSG_OBJECT corresponding field
        ('szObjectSubType', c_char * 64), # 物体子类别,根据不同的物体类型,可以取以下子类型,同NET_MSG_OBJECT相应字段;object sub type , according to different object  types , may use the following sub type,same as NET_MSG_OBJECT field
        ('byReserved1', c_ubyte * 3),   # 保留字节;Reserved
        ('bPicEnble', c_bool),          # 是否有物体对应图片文件信息;object corresponding to picture file info or not
        ('stPicInfo', SDK_PIC_INFO),    # 物体对应图片信息;object corresponding to picture info
        ('bShotFrame', c_bool),         # 是否是抓拍张的识别结果;snapshot recognition result or not
        ('bColor', c_bool),             # 物体颜色(rgbaMainColor)是否可用;object  color (rgbaMainColor) usable or not
        ('bLowerBodyColor', c_ubyte),   # 下半身颜色(rgbaLowerBodyColor)是否可用;lower color (rgbaLowerBodyColor) usable or not
        ('byTimeType', c_ubyte),        # 时间表示类型,详见EM_TIME_TYPE说明;time means type ,  see EM_TIME_TYPE note
        ('stuCurrentTime', NET_TIME_EX),# 针对视频浓缩,当前时间戳（物体抓拍或识别时,会将此识别智能帧附在一个视频帧或jpeg图片中,此帧所在原始视频中的出现时间）
                                        # for video compression,  current time stamp, object snapshot or recognition,  attach this recognition frame in one vire frame or jpegpicture, this frame appearance time in original video,
        ('stuStartTime', NET_TIME_EX),  # 开始时间戳（物体开始出现时）;start time stamp, object start appearance
        ('stuEndTime', NET_TIME_EX),    # 结束时间戳（物体最后出现时）;end time stamp, object last aapearance
        ('stuOriginalBoundingBox', SDK_RECT),   # 包围盒(绝对坐标);box(absolute coordinate)
        ('stuSignBoundingBox', SDK_RECT),       # 车标坐标包围盒;LGO coordinate box
        ('dwCurrentSequence', C_DWORD),         # 当前帧序号（抓下这个物体时的帧）;current frame no., snapshot this object frame
        ('dwBeginSequence', C_DWORD),   # 开始帧序号（物体开始出现时的帧序号）;start frame no., object start appearance frame no.
        ('dwEndSequence', C_DWORD),     # 结束帧序号（物体消逝时的帧序号）;end frame no., object disappearance frame no.
        ('nBeginFileOffset', C_LLONG),  # 开始时文件偏移, 单位: 字节（物体开始出现时,视频帧在原始视频文件中相对于文件起始处的偏移）
                                        # start file shift, unit: byte, object start appearance, video in original video file moves toward file origin
        ('nEndFileOffset', C_LLONG),    # 结束时文件偏移, 单位: 字节（物体消逝时,视频帧在原始视频文件中相对于文件起始处的偏移）
                                        # End file shift, unit: byte, object disappearance, video in original video file moves toward file origin
        ('byColorSimilar', c_ubyte * 8),            # 物体颜色相似度,取值范围：0-100,数组下标值代表某种颜色,详见 EM_COLOR_TYPE
                                                    # object  color similarity, take  value range :0-100, group subscript value represents certain color ,  see EM_COLOR_TYPE
        ('byUpperBodyColorSimilar', c_ubyte * 8),   # 上半身物体颜色相似度(物体类型为人时有效);upper object  color  similarity (object  type as human is valid )
        ('byLowerBodyColorSimilar', c_ubyte * 8),   # 下半身物体颜色相似度(物体类型为人时有效);lower object  color  similarity (object  type as human is valid )
        ('nRelativeID', c_int),                     # 相关物体ID;related object ID
        ('szSubText', c_char * 20),                 # "ObjectType"为"Vehicle"或者"Logo"时,表示车标下的某一车系,比如奥迪A6L,由于车系较多,SDK实现时透传此字段,设备如实填写。
                                                    # "ObjectType"is "Vehicle"or "Logo",  means LOGO lower brand, such as Audi A6L, since there are many brands, SDK shows this field in real-time,device filled as real.
        ('nPersonStature', c_int),                  # 入侵人员身高,单位cm;Intrusion staff height, unit cm
        ('emPersonDirection', c_int),               # 人员入侵方向,详见EM_MSG_OBJ_PERSON_DIRECTION;Staff intrusion direction,refer to EM_MSG_OBJ_PERSON_DIRECTION
        ('rgbaLowerBodyColor', C_DWORD)             # 使用方法同rgbaMainColor,物体类型为人时有效;Use direction same as rgbaMainColor,object  type as human is valid
    ]

class SDK_EXTRA_PLATE_NUMBER(Structure):
    """
    额外车牌信息;Extra plate number
    """
    _fields_ = [
        ('szNumber', c_char*32)  # 额外车牌信息;Extra plate number
    ]

class EVENT_COMM_STATUS(Structure):
    """
    违规状态;illegal state type of driver
    """
    _fields_ = [
        ('bySmoking', c_ubyte),     # 是否抽烟;smoking
        ('byCalling', c_ubyte),     # 是否打电话;calling
        ('szReserved', c_char*14),  # 预留字段;reversed
    ]

class EVENT_COMM_SEAT(Structure):
    """
    驾驶位违规信息;driver's illegal info
    """
    _fields_ = [
        ('bEnable', c_int),               # 是否检测到座驾信息;whether seat info detected
        ('emSeatType', c_int),            # 座驾类型, 0:未识别; 1:主驾驶; 2:副驾驶,详见EM_COMMON_SEAT_TYPE;seat type,refer to EM_COMMON_SEAT_TYPE
        ('stStatus', EVENT_COMM_STATUS),  # 违规状态;illegal state
        ('emSafeBeltStatus', c_int),      # 安全带状态,详见NET_SAFEBELT_STATE;safe belt state,refer to NET_SAFEBELT_STATE
        ('emSunShadeStatus', c_int),      # 遮阳板状态,详见NET_SUNSHADE_STATE;sun shade state,refer to NET_SUNSHADE_STATE
        ('emCallAction', C_ENUM),         # 打电话动作 Refer: EM_CALL_ACTION_TYPE;Call action Refer: EM_CALL_ACTION_TYPE;
        ('nSafeBeltConf', C_UINT),        # 安全带确信度;Safety belt confidence;
        ('nPhoneConf', C_UINT),           # 打电话置信度;Call confidence;
        ('nSmokeConf', C_UINT),           # 抽烟置信度;Smoking confidence;
        ('szReserved', c_ubyte * 8),      # 预留字节; reversed
    ]

class EVENT_COMM_ATTACHMENT(Structure):
    """
    车辆物件;car attachment
    """
    _fields_ = [
        ('emAttachmentType', c_int),    # 物件类型,详见EVENT_COMM_ATTACHMENT;type，refer to EVENT_COMM_ATTACHMENT
        ('stuRect', NET_RECT),          # 坐标;coordinate
        ('nConf', C_UINT),              # 置信度;Confidence;
        ('bReserved', c_ubyte * 16),      # 预留字节;reserved
    ]

class EVENT_PIC_INFO(Structure):
    """
    交通抓图图片信息;traffic event snap picture info
    """
    _fields_ = [
        ('nOffset', C_DWORD),  # 原始图片偏移，单位字节;offset,Unit:byte
        ('nLength', C_DWORD),  # 原始图片长度，单位字节;length of picture,Unit:byte
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
    ]

class NET_RFIDELETAG_INFO(Structure):
    """
    RFID 电子车牌标签信息;the info of RFID electronic tag
    """
    _fields_ = [
        ('szCardID', c_ubyte*16),       # 卡号;card ID
        ('nCardType', c_int),           # 卡号类型, 0:交通管理机关发行卡, 1:新车出厂预装卡;card type, 0:issued by transport administration offices, 1:new factory preloaded card
        ('emCardPrivince', c_int),      # 卡号省份,详见EM_CARD_PROVINCE;card privince,refer to EM_CARD_PROVINCE
        ('szPlateNumber', c_char*32),   # 车牌号码;plate number
        ('szProductionDate', c_char * 16),  # 出厂日期;production data
        ('emCarType', c_int),           # 车辆类型,详见EM_CAR_TYPE;car type,refer to EM_CAR_TYPE
        ('nPower', c_int),              # 功率,单位：千瓦时，功率值范围0~254；255表示该车功率大于可存储的最大功率值
                                        # power, unit:kilowatt-hour, range:0~254, 255 means larger than maximum power value can be stored
        ('nDisplacement', c_int),       # 排量,单位：百毫升，排量值范围0~254；255表示该车排量大于可存储的最大排量值
                                        # displacement, unit:100ml, range:0~254, 255 means larger than maximum displacement value can be stored
        ('nAntennaID', c_int),          # 天线ID，取值范围:1~4;antenna ID, range:1~4
        ('emPlateType', c_int),         # 号牌种类,详见EM_PLATE_TYPE;plate type,refer to EM_PLATE_TYPE
        ('szInspectionValidity', c_char*16),    # 检验有效期，年-月;validity of inspection, year-month
        ('nInspectionFlag', c_int),     # 逾期未年检标志, 0:已年检, 1:逾期未年检;the flag of inspetion, 0:already inspection, 1:not inspection
        ('nMandatoryRetirement', c_int), # 强制报废期，从检验有效期开始，距离强制报废期的年数;the years form effective inspection preiod to compulsory discarding preiod
        ('emCarColor', c_int),           # 车身颜色，详见EM_CAR_COLOR_TYPE;car color,refer to EM_CAR_COLOR_TYPE
        ('nApprovedCapacity', c_int),    # 核定载客量，该值<0时：无效；此值表示核定载客，单位为人;authorized capacity, unit:people, <0:incalid
        ('nApprovedTotalQuality', c_int), # 此值表示总质量，单位为百千克；该值<0时：无效；该值的有效范围为0~0x3FF，0x3FF（1023）表示数据值超过了可存储的最大值;total weight, unit:100kg, range:0~0x3FF,  0x3FF1023:larger than maximum value can be stored, <0:invalid
        ('stuThroughTime', NET_TIME_EX),  # 过车时间;the time when the car is pass
        ('emUseProperty', c_int),         # 使用性质,详见EM_USE_PROPERTY_TYPE;use property,refer to EM_USE_PROPERTY_TYPE
        ('szPlateCode', c_char*8),        # 发牌代号，UTF-8编码;Licensing code, UTF-8 encoding
        ('szPlateSN', c_char * 16),       # 号牌号码序号，UTF-8编码;Plate number, serial number, UTF-8 code
        ('szTID', c_char * 64),           # 标签(唯一标识), UTF-8编码;Label (Unique identifier), UTF-8 encoding
        ('bReserved', c_ubyte * 40),      # 保留字节,留待扩展;Reserved
    ]

class NET_EVENT_RADAR_INFO(Structure):
    """
    物体在雷达坐标系中的信息
    Radar Info
    """
    _fields_ = [
        ('fCoordinateX', c_float),  # X轴坐标(横向距离)，单位：米;X, unit: metre;
        ('fCoordinateY', c_float),  # Y轴坐标（纵向距离），单位：米;Y, unit: metre;
        ('bReserved', C_BYTE * 24),  # 预留字节;reserved;
    ]

class NET_EVENT_GPS_INFO(Structure):
    """
    触发事件时物体的GPS信息
    Event Gps Info
    """
    _fields_ = [
        ('dLongitude', c_double),  # 经度，单位：度,正为东经，负为西经，取值范围[-180,180];longitude,[-180, 180],unit:degree,negative:west longitude;
        ('dLatitude', c_double),  # 纬度，单位：度,正为北纬，负为南纬，取值范围[-90,90];latitude,[-90, 90],unit:degree,negative:south latitude;
        ('bReserved', C_BYTE * 24),  # 预留字节;reserved;
    ]

class NET_EXTRA_PLATES(Structure):
    """
    辅车牌信息
    Auxiliary license plate information
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 车牌图片在二进制数据内偏移，单位字节;The license plate picture is offset in binary data, in bytes;
        ('nLength', C_UINT),  # 车牌图片长度，单位字节;License plate picture length, in bytes;
        ('szText', c_char * 64),  # 辅车牌号码，UTF8格式;Auxiliary license plate number,UTF8;
        ('emCategory', C_ENUM),  # 车牌类型 Refer: EM_NET_PLATE_TYPE;License plate type Refer: EM_NET_PLATE_TYPE;
        ('emColor', C_ENUM),  # 车牌颜色 Refer: EM_NET_PLATE_COLOR_TYPE;License plate color Refer: EM_NET_PLATE_COLOR_TYPE;
        ('stuArea', NET_RECT),  # 辅车牌的包围盒，坐标已算上黑边高度车牌矩形框，绝对坐标，即真正的像素点坐标;The coordinates of the bounding box of the auxiliary license plate have been calculated into the height of the black edge, the rectangular box of the license plate, and the absolute coordinates, that is, the real pixel coordinates;
        ('bReserved', c_char * 32),  # 预留字节;reserved;
    ]

class EVENT_COMM_INFO(Structure):
    """
    事件上报携带卡片信息;Incidents reported to carry the card information
    """
    _fields_ = [
        ('emNTPStatus', c_int),      # NTP校时状态,详见EM_NTP_STATUS;NTP time sync status,refer to EM_NTP_STATUS
        ('nDriversNum', c_int),      # 驾驶员信息数;driver info number
        ('pstDriversInfo', POINTER(SDK_MSG_OBJECT_EX)),  # 保驾驶员信息数据;driver info data
        ('pszFilePath', c_char_p),   # 本地硬盘或者sd卡成功写入路径,为None时,路径不存在;writing path for local disk or sd card, or write to default path if None
        ('pszFTPPath', c_char_p),    # 设备成功写到ftp服务器的路径;ftp path
        ('pszVideoPath', c_char_p),  # 当前接入需要获取当前违章的关联视频的FTP上传路径;ftp path for assocated video
        ('stCommSeat', EVENT_COMM_SEAT*8),  # 驾驶位信息;Seat info
        ('nAttachmentNum', c_int),   # 车辆物件个数;Car Attachment number
        ('stuAttachment', EVENT_COMM_ATTACHMENT*8),   # 车辆物件信息;Car Attachment
        ('nAnnualInspectionNum', c_int),        # 年检标志个数;Annual Inspection number
        ('stuAnnualInspection', NET_RECT*8),    # 年检标志;Annual Inspection
        ('fHCRatio', c_float),       # HC所占比例，单位：%/1000000;The ratio of HC,unit,%/1000000
        ('fNORatio', c_float),       # NO所占比例，单位：%/1000000;The ratio of NO,unit,%/1000000
        ('fCOPercent', c_float),     # CO所占百分比，单位：% 取值0~100;The percent of CO,unit,% ,range from 0 to 100
        ('fCO2Percent', c_float),    # CO2所占百分比，单位：% 取值0~100;The percent of CO2,unit: % ,range from 0 to 100
        ('fLightObscuration', c_float), # 不透光度，单位：% 取值0~100;The obscuration of light,unit,% ,range from 0 to 100
        ('nPictureNum', c_int),      # 原始图片张数;Original pictures info number
        ('stuPicInfos', EVENT_PIC_INFO*6),  # 原始图片信息;Original pictures info data
        ('fTemperature', c_float),   # 温度值,单位摄氏度;Temperature,unit: centigrade
        ('nHumidity', c_int),        # 相对湿度百分比值;Humidity,unit: %
        ('fPressure', c_float),      # 气压值,单位Kpa;Pressure,unit: Kpa
        ('fWindForce', c_float),     # 风力值,单位m/s;Wind force,unit: m/s
        ('nWindDirection', c_uint),  # 风向,单位度,范围:[0,360];Wind direction,unit: degree,range:[0,360]
        ('fRoadGradient', c_float),  # 道路坡度值,单位度;Road gradient,unit: degree
        ('fAcceleration', c_float),  # 加速度值,单位:m/s2;Acceleration,unit: m/s2
        ('stuRFIDEleTagInfo', NET_RFIDELETAG_INFO),   # RFID 电子车牌标签信息;RFID electronics tag info
        ('stuBinarizedPlateInfo', EVENT_PIC_INFO),    # 二值化车牌抠图;Binarized plate matting
        ('stuVehicleBodyInfo', EVENT_PIC_INFO),       # 车身特写抠图;Vehicle body close-up matting
        ('emVehicleTypeInTollStation', c_int),        # 收费站车型分类,详见EM_VEHICLE_TYPE;Vehicle type inToll station,refer to EM_VEHICLE_TYPE
        ('emSnapCategory', c_int),                    # 抓拍的类型，默认为机动车，详见EM_SNAPCATEGORY;Snap Category;,refer to EM_SNAPCATEGORY
        ('nRegionCode', c_int),                       # 车牌所属地区代码,(孟加拉海外车牌识别项目),默认-1表示未识别;Location code of license plate,(Bangladesh Project),default -1 indicates unrecognized
        ('emVehicleTypeByFunc', c_int),               # 按功能划分的车辆类型，详见EM_VEHICLE_TYPE_BY_FUNC;Vehicle type by function,refer to EM_VEHICLE_TYPE_BY_FUNC
        ('emStandardVehicleType', c_int),             # 标准车辆类型，详见EM_STANDARD_VEHICLE_TYPE;Standard vehicle type,refer to EM_STANDARD_VEHICLE_TYPE
        ('nExtraPlateCount', c_uint),                 # 额外车牌数量;Count of extra plates
        ('szExtraPlateNumber', SDK_EXTRA_PLATE_NUMBER * 3),  # 额外车牌信息;Extra plate number
        ('emOverseaVehicleCategory', c_int),                # 海外车辆类型中的子类别，详见EM_OVERSEA_VEHICLE_CATEGORY_TYPE;oversea vehicle category,refer to EM_OVERSEA_VEHICLE_CATEGORY_TYPE
        ('szProvince', c_char*64),                          # 车牌所属国家的省、州等地区名;Province
        ('stuRadarInfo', NET_EVENT_RADAR_INFO),             # 物体在雷达坐标系中的信息,单位：米，设备视角：右手方向为X轴正向，正前方为Y轴正向;Radar Info;
        ('stuGPSInfo', NET_EVENT_GPS_INFO),                 # 触发事件时物体的GPS信息;gps info;
        ('stuExtraPlates', NET_EXTRA_PLATES * 2),           # 辅车牌信息，某些国家或地区一车多牌，比如港澳三地车，一车会有3个车牌，其中一个主车牌，一般是内地发给香港或澳门的能以此在内地行驶的"港澳牌"；另外两个分别是香港牌或澳门牌，是得以在香港或澳门行驶的牌照，而这两个则称为辅牌，有辅牌的车的车牌相关信息则填在此字段，目前最多2个辅车牌;Auxiliary license plate information;
        ('nExtraPlatesCount', c_int),                       # 辅车牌有效个数;Auxiliary license plate number;
        ('nPlateRecogniseConf', C_UINT),                    # 车牌识别置信度;License plate recognition confidence;
        ('nVecPostureConf', C_UINT),                        # 车辆姿态置信度;Vehicle attitude confidence;
        ('nVecColorConf', C_UINT),                          # 车身颜色置信度;Vehicle Body color confidence;
        ('nSpecialVehConf', C_UINT),                        # 特殊车辆识别结果置信度;special vehicle recognition results confidence;
        ('nIsLargeAngle', C_UINT),                          # 机动车是否为大角度;Is the motor vehicle at a large angle;
        ('nIsRelatedPlate', C_UINT),                        # 当前机动车车身是否曾经关联车牌;Has the current vehicle body ever been associated with a license plate;
        ('nDetectConf', C_UINT),                            # 机动车检测置信度;Vehicle detection confidence;
        ('nClarity', C_UINT),                               # 机动车清晰度分值;Motor vehicle definition score;
        ('nCompleteScore', C_UINT),                         # 机动车完整度评分;Motor vehicle integrity score;
        ('nQeScore', C_UINT),                               # 机动车优选分数;Motor vehicle preference score;
        ('bReserved', C_BYTE * 128),                        # 预留字节;reserved;
        ('szCountry', c_char*20)                            # 国家;Country
    ]

class NET_NONMOTOR_PIC_INFO(Structure):
    """
    非机动车抠图信息;Non-Motor Image
    """
    _fields_ = [
        ('uOffset', c_uint),            # 在二进制数据块中的偏移;Offset
        ('uLength', c_uint),            # 图片大小,单位：字节;Image size, Unit : Byte
        ('uWidth', c_uint),             # 图片宽度;Image Width
        ('uHeight', c_uint),            # 图片高度;Image Height
        ('szFilePath', c_char*260),     # 文件路径;FilePath
        ('nIndexInData', C_UINT),       # 在上传图片数据中的图片序号;Index in data;
        ('byReserved', c_ubyte*508),    # 保留字节;Reserved
    ]

class RIDER_FACE_IMAGE_INFO(Structure):
    """
    骑车人脸图片信息;face image information
    """
    _fields_ =[
        ('nOffSet', c_uint),    # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),    # 图片大小,单位字节;Image size, Unit : Byte
        ('nWidth', c_uint),     # 图片宽度(像素);Image width(pixel)
        ('nHeight', c_uint),    # 图片高度(像素);Image height(pixel)
        ('byReserved', c_ubyte*48), # 保留字节;Reserved
    ]

class NET_FACE_ATTRIBUTE_EX(Structure):
    """
    人脸属性;Face attribute
    """
    _fields_ =[
        ('emSex', c_uint),                  # 性别，详见EM_SEX_TYPE;Sex，refer to EM_SEX_TYPE
        ('nAge', c_int),                    # 年龄,-1表示该字段数据无效;age,-1 means invalid
        ('emComplexion', c_int),            # 肤色,详见EM_COMPLEXION_TYPE;Complexion,refer to EM_COMPLEXION_TYPE
        ('emEye', c_int),                   # 眼睛状态,详见EM_EYE_STATE_TYPE;Eye state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),                 # 嘴巴状态,详见EM_MOUTH_STATE_TYPE;Mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),                  # 口罩状态,详见EM_MASK_STATE_TYPE;Mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),                 # 胡子状态,详见EM_BEARD_STATE_TYPE;Beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),             # 魅力值, 0未识别，识别时范围1-100,得分高魅力高;Attractive, 0 Not distinguish,Range[1,100]
        ('emGlass', c_int),                 # 眼镜,详见EM_HAS_GLASS;Glasses,refer to EM_HAS_GLASS
        ('emEmotion', c_int),               # 表情,详见EM_EMOTION_TYPE;Emotion,refer to EM_EMOTION_TYPE
        ('stuBoundingBox', SDK_RECT),       # 包围盒(8192坐标系);BoundingBox(8192 Coordinate)
        ('bReserved1', C_BYTE*4),           # 保留字节;Reserved;
        ('emStrabismus', c_int),            # 斜视状态,详见EM_STRABISMUS_TYPE;Strabismus,refer to EM_STRABISMUS_TYPE
        ('nAngle', c_int * 3),              # 人脸抓拍角度, 三个角度依次分别是Pitch（仰俯角）, 指抬头低头的角度, 范围是-70~60;yaw（偏航角）, 指左右转头的角度, 范围是-90~90;Roll（翻滚角）, 指左右倾斜的角度, 范围是-90~90;[180,180,180]表示未识别到角度;Face capture angle, three angles are respectivelyPitch(pitch angle), refers to the angle of head up and head down, with the range of - 70 ~ 60;Yaw(yaw angle), refers to the angle of left and right turning head, and the range is - 90 ~ 90;Roll (roll angle), refers to the angle of left and right tilt, the range is - 90 ~ 90;[180180180] indicates the angle is not recognized;
        ('stuObjCenter', SDK_POINT),        # 物体型心(不是包围盒中心), 0-8191相对坐标, 相对于大图;Center of object(not center of bounding box), 0-8191 relative coordinates, relative to large graph;
        ('byReserved', c_ubyte*48),         # 保留字节,留待扩展;Reserved
    ]

class NET_FACE_FEATURE_VECTOR_INFO(Structure):
    """
    人脸特征值数据在二进制数据中的位置信息
    Location information of face characteristic value data in binary data
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 人脸特征值在二进制数据中的偏移, 单位:字节;Offset of face characteristic value data in binary data, unit: byte;
        ('nLength', C_UINT),  # 人脸特征值数据长度, 单位:字节;Length of face characteristic value data, unit: byte;
        ('bFeatureEnc', C_BOOL),  # 用于标识特征值是否加密;Identifies whether the characteristic value data is encrypted;
        ('byReserved', C_BYTE * 28),  # 保留字节;reserved;
    ]

class NET_HUMAN_FEATURE_VECTOR_INFO(Structure):
    """
    人体特征值数据在二进制数据中的位置信息
    Position info of human feature data in binary data
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 人体特征值在二进制数据中的偏移, 单位:字节;The offset of human feature data in binary data, unit:bytes;
        ('nLength', C_UINT),  # 人体特征值数据长度, 单位:字节;The length of human feature data, unit:bytes;
        ('bFeatureEnc', C_BOOL),  # 用于标识特征值是否加密;Identifies whether the characteristic value data is encrypted;
        ('byReserved', C_BYTE * 28),  # 保留字节;Reserved;
    ]

class NET_RIDER_INFO(Structure):
    """
    骑车人信息;Rider information
    """
    _fields_ = [
        ('bFeatureValid', c_int),       # 是否识别到特征信息, TRUE时下面数据才有效;Enable
        ('emSex', c_int),               # 性别,详见EM_SEX_TYPE;its sex,refer to EM_SEX_TYPE
        ('nAge', c_int),                # 年龄;its age
        ('emHelmet', c_int),            # 头盔状态,详见EM_NONMOTOR_OBJECT_STATUS;Whether or not wearing a helmet,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emCall', c_int),              # 是否在打电话,详见EM_NONMOTOR_OBJECT_STATUS;Whether on the phone,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emBag', c_int),               # 是否有背包,详见EM_NONMOTOR_OBJECT_STATUS; Whether or not have bag,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emCarrierBag', c_int),        # 有没有手提包,详见EM_NONMOTOR_OBJECT_STATUS;Whether or not have carrierbag,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emUmbrella', c_int),          # 是否打伞,详见EM_NONMOTOR_OBJECT_STATUS;Whether an umbrella,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emGlasses', c_int),           # 是否有带眼镜,详见EM_NONMOTOR_OBJECT_STATUS; Whether or not wear glasses,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emMask', c_int),              # 是否带口罩,详见EM_NONMOTOR_OBJECT_STATUS;Whether to wear a face mask,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emEmotion', c_int),           # 表情,详见EM_EMOTION_TYPE;Emotion,refer to EM_EMOTION_TYPE
        ('emUpClothes', c_int),         # 上衣类型,详见EM_CLOTHES_TYPE;UpClothes type,refer to EM_CLOTHES_TYPE
        ('emDownClothes', c_int),       # 下衣类型,详见EM_CLOTHES_TYPE;DownClothes type,refer to EM_CLOTHES_TYPE
        ('emUpperBodyColor', c_int),    # 上衣颜色,详见EM_OBJECT_COLOR_TYPE;UpClothes color,refer to EM_OBJECT_COLOR_TYPE
        ('emLowerBodyColor', c_int),    # 下衣颜色,详见EM_OBJECT_COLOR_TYPE;DownClothes color,refer to EM_OBJECT_COLOR_TYPE
        ('bHasFaceImage', c_int),       # 是否有骑车人人脸抠图信息;Whether rider's face image information is contained
        ('stuFaceImage', RIDER_FACE_IMAGE_INFO),    # 骑车人人脸特写描述;Rider face image
        ('bHasFaceAttributes', c_int),  # 是否有人脸属性;Whether rider's face Attributes is contained
        ('stuFaceAttributes', NET_FACE_ATTRIBUTE_EX),   # 人脸属性;face Attributes
        ('emHasHat', c_int),            # 是否戴帽子,详见EM_HAS_HAT;whether has hat,refer to EM_HAS_HAT
        ('emCap', c_int),               # 帽类型,详见EM_CAP_TYPE;Cap type,refer to EM_CAP_TYPE
        ('emHairStyle', c_int),         # 头发样式,详见EM_HAIR_STYLE; Hair style,refer to EM_HAIR_STYLE
        ('stuFaceFeatureVectorInfo', NET_FACE_FEATURE_VECTOR_INFO), # 人脸特征值数据在二进制数据中的位置信息;Location information of Face characteristic value data in binary data;
        ('emFaceFeatureVersion', C_ENUM),   # 人脸特征值版本号 Refer: EM_FEATURE_VERSION;Face feature versio Refer: EM_FEATURE_VERSION;
        ('stuHumanFeatureVectorInfo', NET_HUMAN_FEATURE_VECTOR_INFO),   # 人体特征值数据在二进制数据中的位置信息;Location information of Human characteristic value data in binary data;
        ('emHumanFeatureVersion', C_ENUM),  # 人体特征值版本号 Refer: EM_FEATURE_VERSION;Human feature versio Refer: EM_FEATURE_VERSION;
        ('nAgeConf', C_UINT),               # 年龄段置信度;Age confidence;
        ('nUpColorConf', C_UINT),           # 上衣颜色置信度;Jacket color confidence;
        ('nDownColorConf', C_UINT),         # 下衣颜色置信度;Lower garment color confidence;
        ('nUpTypeConf', C_UINT),            # 上衣种类置信度;Confidence of coat type;
        ('nDownTypeConf', C_UINT),          # 下衣种类置信度;nDownTypeConf;
        ('nHatTypeConf', C_UINT),           # 帽子类型置信度;Hat type confidence;
        ('nHairTypeConf', C_UINT),          # 发型种类置信度;Confidence of hairstyle type;
        ('emUpperPattern', C_ENUM),         # 上半身衣服图案 Refer: EM_CLOTHES_PATTERN;Upper garment pattern Refer: EM_CLOTHES_PATTERN;
        ('nUpClothes', C_UINT),             # 上衣类型 0:未知 1:长袖 2:短袖 3:长款大衣 4:夹克及牛仔服 5:T恤6:运动装 7:羽绒服 8:衬衫 9:连衣裙 10:西装 11:毛衣 12:无袖 13:背心;Type of coat 0:Unknown 1:Long sleeve 2:Short sleeve 3:Long coat 4:Jacket and jeans 5: T-shirt6:Sportswear 7:Down-filled coat 8:shirt 9:Dress 10:suit 11:sweater 12:Sleeveless 13:vest;
        ('emUniformStyle', C_ENUM),         # 制服类型 Refer: EM_UNIFORM_STYLE;Uniform type Refer: EM_UNIFORM_STYLE;
        ('nRainCoat', C_UINT),              # 是否有雨披 0:未识别 1:无 2:有;Poncho 0:unrecognized 1:none 2:Yes;
        ('emCoatStyle', C_ENUM),            # 上衣款式 Refer: EM_COAT_TYPE;Coat style Refer: EM_COAT_TYPE;
        ('emAgeSeg', C_ENUM),               # 年龄段 Refer: EM_AGE_SEG;Age segmentation Refer: EM_AGE_SEG;
        ('byReserved', C_BYTE * 164),       # 保留;Reserved;
    ]

class SCENE_IMAGE_INFO(Structure):
    """
    全景广角图;Scene image
    """
    _fields_ = [
        ('nOffSet', c_uint),            # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),            # 图片大小,单位字节;image data length
        ('nWidth', c_uint),             # 图片宽度(像素);image width(pixel)
        ('nHeight', c_uint),            # 图片高度(像素);image Height(pixel)
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('byReserved', c_ubyte*52),     # 预留字节;Reserved
    ]

class FACE_SCENE_IMAGE(Structure):
    """
   人脸全景图; Face scene image
    """
    _fields_ = [
        ('nOffSet', c_uint),    # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),    # 图片大小,单位字节;image data length
        ('nWidth', c_uint),     # 图片宽度(像素);image width(pixel)
        ('nHeight', c_uint),    # 图片高度(像素);image Height(pixel)
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('byReserved', c_ubyte * 52),  # 预留字节;Reserved
    ]

class NET_NONMOTOR_FEATURE_VECTOR_INFO(Structure):
    """
    非机动车特征值数据在二进制数据中的位置信息;Position info of non-motor feature data in binary data
    """
    _fields_ = [
        ('nOffset', c_uint),            # 非机动车特征值在二进制数据中的偏移, 单位:字节;The offset of non-motor feature data in binary data, unit:bytes
        ('nLength', c_uint),            # 非机动车特征值数据长度, 单位:字节;The length of non-motor feature data, unit:bytes
        ('bFeatureEnc', C_BOOL),  # 用于标识特征值是否加密;Identifies whether the feature is encrypted;
        ('byReserved', c_ubyte*28),     # 保留字节;Reserved
    ]

class NET_NONMOTOR_PLATE_IMAGE(Structure):
    """
    非机动车车牌图片信息;The plate image of no-motor
    """
    _fields_ = [
        ('nOffset', c_uint),            # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),            # 图片大小,单位字节;image data length，Unit:byte
        ('nWidth', c_uint),             # 图片宽度;image width
        ('nHeight', c_uint),            # 图片高度;image Height
        ('nIndexInData', C_UINT),       # 在上传图片数据中的图片序号;Index in data;
        ('byReserved', c_ubyte * 508),  # 预留字节;Reserved
    ]


class NET_NONMOTOR_PLATE_INFO(Structure):
    """
    非机动车配牌信息;Plate info of nomotor
    """
    _fields_ = [
        ('szPlateNumber', c_char*128),                  # 非机动车车牌号;plate number
        ('stuBoundingBox', NET_RECT),                   # 包围盒， 非机动车矩形框，0~8191相对坐标;BoundingBox Rect, 0~8192
        ('stuOriginalBoundingBox', NET_RECT),           # 包围盒， 非机动车矩形框，绝对坐标;BoundingBox Rect, absolute coordinates
        ('stuPlateImage', NET_NONMOTOR_PLATE_IMAGE),    # 非机动车车牌抠图;plate image info
        ('emPlateColor', c_int),                        # 车牌颜色; Plate color
        ('byReserved', c_ubyte*132),                    # 保留;Reserved

    ]


class EVENT_INTELLI_COMM_INFO(Structure):
    """
    智能报警事件公共信息;intelli event comm info
    """
    _fields_ = [
        ('emClassType', c_int),             # 智能事件所属大类,详见EM_CLASS_TYPE;class type，refer to EM_CLASS_TYPE
        ('nPresetID', c_int),               # 该事件触发的预置点，取值范围为0~255，大于0表示在此预置点时有效。
                                            # Preset ID, value range is 0~255 and when the value is greater than 0 is valied
        ('bReserved', c_ubyte*124),         # 保留字节,留待扩展;reserved
    ]

class EVENT_PLATE_INFO(Structure):
    """
    车辆信息，记录了车头、车尾车牌号和车牌颜色;Plate info, Record the plate number and color of the front and back of the car
    """
    _fields_ = [
        ('szFrontPlateNumber', c_char*64),      # 车头车牌号码;front plate number
        ('emFrontPlateColor', c_int),           # 车头车牌颜色,详见EM_PLATE_COLOR_TYPE;front plate color,refer to EM_PLATE_COLOR_TYPE
        ('szBackPlateNumber', c_char * 64),     # 车尾车牌号码;back plate number
        ('emBackPlateColor', c_int),            # 车尾车牌颜色,详见EM_PLATE_COLOR_TYPE;back plate color,refer to EM_PLATE_COLOR_TYPE
        ('reversed', c_ubyte*128),              # 保留;reserved
    ]

class VA_OBJECT_NONMOTOR(Structure):
    """
    非机动车对象;Nonmotor
    """
    _fields_ = [
        ('nObjectID', c_int),           # 物体ID,每个ID表示一个唯一的物体;Object id
        ('emCategory', c_int),          # 非机动车子类型,详见EM_CATEGORY_NONMOTOR_TYPE;Non-motor type,refer to EM_CATEGORY_NONMOTOR_TYPE
        ('stuBoundingBox', SDK_RECT),   # 包围盒， 非机动车矩形框，0~8191相对坐标;BoundingBox Rect, 0~8192
        ('stuOriginalBoundingBox', SDK_RECT),   # 包围盒， 非机动车矩形框，绝对坐标;BoundingBox Rect, absolute coordinates
        ('stuMainColor', NET_COLOR_RGBA),       # 非机动车颜色, RGBA;Non-motor color (RGBA value)
        ('emColor', c_int),                     # 非机动车颜色, 枚举,详见EM_OBJECT_COLOR_TYPE;Non-motor color enumeration，refer to EM_OBJECT_COLOR_TYPE
        ('bHasImage', c_int),                   # 是否有抠图; whether has image or not
        ('stuImage', NET_NONMOTOR_PIC_INFO),    # 物体截图;Image information
        ('nNumOfCycling', c_int),               # 骑车人数量;The number of rider
        ('stuRiderList', NET_RIDER_INFO*16),    # 骑车人特征,个数和nNumOfCycling关联;The information of rider
        ('stuSceneImage', SCENE_IMAGE_INFO),    # 全景广角图;SceneImage
        ('stuFaceSceneImage', FACE_SCENE_IMAGE),    # 人脸全景广角图; Face SceneImage
        ('nNumOfFace', c_int),                      # 检测到的人脸数量;The number of face
        ('fSpeed', c_float),                        # 物体速度，单位为km/h;Object speed, Unit:km/h
        ('stuNonMotorFeatureVectorInfo', NET_NONMOTOR_FEATURE_VECTOR_INFO), #  非机动车特征值数据在二进制数据中的位置信息
                                                                            # Position info of non-motor feature data in binary data
        ('emNonMotorFeatureVersion', c_int),    #  非机动车特征值版本号,详见EM_FEATURE_VERSION;Non-motor feature data version，refer to EM_FEATURE_VERSION
        ('stuNomotorPlateInfo', NET_NONMOTOR_PLATE_INFO),  #  非机动车牌信息;Plate info of nomotor
        ('stuObjCenter', SDK_POINT),            # 物体型心(不是包围盒中心), 0-8191相对坐标, 相对于大图; Center of object(not center of bounding box), 0-8191 relative coordinates, relative to large graph
        ('stuFaceFeatureVectorInfo', NET_FACE_FEATURE_VECTOR_INFO), # 人脸特征值数据在二进制数据中的位置信息, 废弃;(Discard)Location information of face characteristic value data in binary data;
        ('emFaceFeatureVersion', C_ENUM),           # 人脸特征值版本号, 废弃 Refer: EM_FEATURE_VERSION;(Discard)face feature version Refer: EM_FEATURE_VERSION;
        ('nCategoryConf', c_int),                   # 非机动车类型置信度;Non motor vehicle type confidence;
        ('szNonMotorFeatureVersion', c_char * 32),  # 非机动车特征值版本号-字符串;Non-motor feature data version-string;
        ('emNonMotorAngle', C_ENUM),                # 非机动车的角度 Refer: EM_OBJECT_NONMOTORANGLE_TYPE;Non Motor vehicle angle Refer: EM_OBJECT_NONMOTORANGLE_TYPE;
        ('emBasket', C_ENUM),                       # 非机动车车篮 Refer: EM_OBJECT_BASKET_TYPE;Non Motor vehicle basket Refer: EM_OBJECT_BASKET_TYPE;
        ('emStorageBox', C_ENUM),                   # 非机动车后备箱 Refer: EM_OBJECT_STORAGEBOX_TYPE;Non Motor vehicle StorageBox Refer: EM_OBJECT_STORAGEBOX_TYPE;
        ('nCompleteScore', C_UINT),                 # 非机动车完整度评分，范围[0,100]，越大越完整;Non motor vehicle integrity score, range [0,100];
        ('nClarityScore', C_UINT),                  # 非机动车清晰度分值 取值范围为[1,100], 越大越清晰, 0为无效值;The value range of non motor vehicle definition score is [1,100];
        ('nStartSequence', C_UINT),                 # 目标出现的帧号;The frame number of the target start;
        ('nEndSequence', C_UINT),                   # 目标消失的帧号;The frame number of the target end;
        ('bIsErrorDetect', C_BOOL),                 # 非机动车车身及骑手整体，是否虚检，0: 否，1: 是;Whether the whole non motor vehicle body and rider are falsely inspected, 0: No, 1: Yes;
        ('nImageLightType', C_UINT),                # 图像成像光源类型, 0:未知, 1:可见光成像, 2:近红外成像(灰度图), 3:热红外成像(伪彩色);Image imaging light source type,0:unknown, 1:visible imaging, 2:near infrared imaging(gray image), 3:thermal infrared imaging (pseudo color);
        ('nAbsScore', C_UINT),                      # 非机动车综合质量评分，范围[0,100]，越大质量越好;Non motor vehicle comprehensive quality score, range [0,100], the larger the score, the better the quality;
        ('emRainShedType', C_ENUM),                 # 雨棚（伞）类型 Refer: EM_RAIN_SHED_TYPE;Canopy (umbrella) type Refer: EM_RAIN_SHED_TYPE;
        ('byReserved', C_BYTE * 2948),              # 保留;reserved;
    ]

class SCENE_IMAGE_INFO_EX(Structure):
    """
    全景广角图; Scene image
    """
    _fields_ = [
        ('nOffSet', c_uint),             # 在二进制数据块中的偏移;mage offset in the data
        ('nLength', c_uint),             # 图片大小,单位字节;image data length
        ('nWidth', c_uint),              # 图片宽度(像素);image width(pixel)
        ('nHeight', c_uint),             # 图片高度(像素);image Height(pixel)
        ('szFilePath', c_char*260),      # 全景图片路径;file path
        ('nIndexInData', C_UINT),        # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('byReserved', c_char*508),      # 预留字节;Reserved
    ]

class NET_IMAGE_INFO_EX2(Structure):
    """
    图片信息
    image information
    """
    _fields_ = [
        ('emType', C_ENUM),  # 图片类型 Refer: EM_IMAGE_TYPE_EX2;Picture type Refer: EM_IMAGE_TYPE_EX2;
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移;Offset in the binary data block;
        ('nLength', C_UINT),  # 图片大小,单位:字节;Picture size, unit: byte;
        ('byReserverd', c_char * 4),  # 用于字节对齐;for byte alignment;
        ('szPath', c_char * 256),  # 图片存储位置;Picture storage location;
    ]

class DEV_EVENT_TRAFFICJUNCTION_INFO(Structure):
    """
    事件类型TRAFFICJUNCTION(交通路口老规则事件/视频电警上的交通卡口老规则事件)对应的数据块描述信息;Event Type TRAFFICJUNCTION (transportation card traffic junctions old rule event / video port on the old electric alarm event rules) corresponding to the description of the data block
    """
    _fields_ = [
        ('nChannelID', c_int),              # 通道号;ChannelId
        ('szName', c_char*128),             # 事件名称;event name
        ('byMainSeatBelt', c_ubyte),        # 主驾驶座,系安全带状态,1-系安全带,2-未系安全带;main driver, seat, safety belt , 1-fastened, 2-unfastened
        ('bySlaveSeatBelt', c_ubyte),       # 副驾驶座,系安全带状态,1-系安全带,2-未系安全带;co-drvier, seat, safety belt, 1-fastened, 2-unfastened
        ('byVehicleDirection', c_ubyte),    # 当前被抓,拍到的车辆是车头还是车尾,具体请见 EM_VEHICLE_DIRECTION;Current snapshot is head or rear, see  EM_VEHICLE_DIRECTION
        ('byOpenStrobeState', c_ubyte),     # 开闸状态,具体请见EM_OPEN_STROBE_STATE;Open status, see EM_OPEN_STROBE_STATE
        ('PTS', c_double),                  # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),               # 事件发生的时间;the event happen time
        ('nEventID', c_int),                # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),      # 检测到的物体;have being detected object
        ('nLane', c_int),                   # 对应车道号;road number
        ('dwBreakingRule', C_DWORD),        # 违反规则掩码,第一位:闯红灯;BreakingRule's mask,first byte: crash red light;
                                            # 第二位:不按规定车道行驶;secend byte:break the rule of driving road number;
                                            # 第三位: 逆行;the third byte:converse;
                                            # 第四位：违章掉头;the forth byte:break rule to turn around;
                                            # 第五位: 交通堵塞;the five byte:traffic jam;
                                            # 第六位: 交通异常空闲;the six byte:traffic vacancy;
                                            # 第七位:压线行驶;否则默认为: 交通路口事件;the seven byte: Overline; defalt:trafficJunction
        ('RedLightUTC', NET_TIME_EX),       # 红灯开始UTC时间;the begin time of red light
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info
        ('nSequence', c_int),               # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1,1 means the last one,0 means there has some exception and snap stop
        ('nSpeed', c_int),                  # 车辆实际速度Km/h;car's speed (km/h)
        ('bEventAction', c_ubyte),          # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byDirection', c_ubyte),           # 路口方向,1-表示正向,2-表示反向;Intersection direction 1 - denotes the forward 2 - indicates the opposite
        ('byLightState', c_ubyte),          # LightState表示红绿灯状态:0 未知,1 绿灯,2 红灯,3 黄灯;LightState means red light status:0 unknown,1 green,2 red,3 yellow
        ('byReserved', c_ubyte),            # 保留字节;reserved
        ('byImageIndex', c_ubyte),          # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('stuVehicle', SDK_MSG_OBJECT),     # 车身信息;vehicle info
        ('dwSnapFlagMask', C_DWORD),        # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout"
                                            # snap flags(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('stuResolution', SDK_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution
        ('szRecordFile', c_char*128),            # 报警对应的原始录像文件信息;Alarm corresponding original video file information
        ('stuCustomInfo', EVENT_JUNCTION_CUSTOM_INFO),  # 报警对应的原始录像文件信息;custom info
        ('byPlateTextSource', c_ubyte),     # 车牌识别来源, 0:本地算法识别,1:后端服务器算法识别;the source of plate text, 0:Local,1:Server
        ('bReserved1', c_ubyte*3),          # 保留字节,留待扩展.;Reserved bytes, leave extended_
        ('stuGPSInfo', NET_GPS_INFO),       # GPS信息 车载定制;GPS info ,use in mobile DVR/NVR
        ('byNoneMotorInfo', c_ubyte),       # 0-无非机动车人员信息信息,1-有非机动车人员信息信息;specified the person info of none motor
                                            # 此字段为1时下面11个字段生效;1 means 11 fields followed is valid
        ('byBag', c_ubyte),                 # 是否背包, 0-未知 1-不背包   2-背包;0-unknown 1-no bag   2-bag
        ('byUmbrella', c_ubyte),            # 是否打伞, 0-未知 1-不打伞   2-打伞;0-unknown 1-no umbrella   2-Umbrella
        ('byCarrierBag', c_ubyte),          # 手提包状态,0-未知 1-没有 2-有;0-unknown 1-no carrierBag 2-carrierBag
        ('byHat', c_ubyte),                 # 是否戴帽子, 0-未知 1-不戴帽子 2-戴帽子;0-unknown 1-no helmet 2-helmet
        ('byHelmet', c_ubyte),              # 头盔状态,0-未知 1-没有 2-有;0-unknown 1-no hat 2-hat
        ('bySex', c_ubyte),                 # 性别,0-未知 1-男性 2-女性;0-unknown 1-man 2-woman
        ('byAge', c_ubyte),                 # 年龄;age
        ('stuUpperBodyColor', NET_COLOR_RGBA),      # 上身颜色;upper body color
        ('stuLowerBodyColor', NET_COLOR_RGBA),      # 下身颜色;lower body color
        ('byUpClothes', c_ubyte),                   # 上身衣服类型 0:未知 1:长袖 2:短袖 3:长裤 4:短裤 5:裙子 6:背心 7:超短裤 8:超短裙;upper clothes 0:unknown 1:long sleeve 2:short sleeve 3:trousers 4:breeches 5:skirt 6:vest 7:minipants 8:miniskirt
        ('byDownClothes', c_ubyte),                 # 下身衣服类型 0:未知 1:长袖 2:短袖 3:长裤 4:短裤 5:裙子 6:背心 7:超短裤 8:超短裙;lower clothes 0:unknown 1:long sleeve 2:short sleeve 3:trousers 4:breeches 5:skirt 6:vest 7:minipants 8:miniskirt
        ('stuExtensionInfo', NET_EXTENSION_INFO),   # 扩展信息;Extension info
        ('bReserved', c_ubyte*22),                  # 保留字节,留待扩展;Reserved bytes, leave extended
        ('nTriggerType', c_int),                    # TriggerType:触发类型,0车检器,1雷达,2视频,3RSU;Trigger Type:0 vehicle inspection device, 1 radar, 2 video, 3 RSU
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),         # 交通车辆信息;Traffic vehicle info
        ('dwRetCardNumber', C_DWORD),           # 卡片个数;Card Number
        ('stuCardInfo', EVENT_CARD_INFO*16),    # 卡片信息;Card information
        ('stCommInfo', EVENT_COMM_INFO),        # 公共信息;public info
        ('bNonMotorInfoEx', c_int),             # 是否有非机动车信息;Non-motor info enable
        ('stuNonMotor', VA_OBJECT_NONMOTOR),    # 非机动车信息;Non-motor information
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('stuPlateInfo', EVENT_PLATE_INFO),     # 车辆信息，记录了车头、车尾车牌号和车牌颜色;Plate info, Record the plate number and color of the front and back of the car;
        ('bSceneImage', C_BOOL),                # 全景图是否有效;Scene Image valid or invalid;
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),  # 全景图;Scene Image;
        ('pstObjects', POINTER(SDK_MSG_OBJECT)),  # 检测到的多个车牌信息;detected objects;
        ('nObjectNum', c_int),                  # 检测到的多个车牌个数;detected objects numbers;
        ('emVehiclePosture', C_ENUM),           # 车辆姿势 Refer: EM_VEHICLE_POSTURE_TYPE;vehicle posture Refer: EM_VEHICLE_POSTURE_TYPE;
        ('nVehicleSignConfidence', C_UINT),     # 车标置信度（范围：0~100）;vehicle sign confidence(range:0~100);
        ('nVehicleCategoryConfidence', C_UINT),  # 车型置信度（范围：0~100）;vehicle category confidence(range:0~100);
        ('emCarDrivingDirection', C_ENUM),      # 规则区内车辆行驶方向 Refer: EM_CAR_DRIVING_DIRECTION;Driving direction of vehicles in the regular area Refer: EM_CAR_DRIVING_DIRECTION;
        ('stuImageInfo', NET_IMAGE_INFO_EX2 * 32),  # 图片信息数组;image information array;
        ('nImageInfoNum', c_int),               # 图片信息个数;the number of image information;
        ('szSerialNo', c_char * 128),           # 和客户端请求的抓图序列号对应;Corresponds to the snapshot serial number requested by the client;
        ('byReserved2', c_char * 896),          # 保留字节;Reserved;
    ]

class EVENT_INFO(Structure):
    """
    事件信息;Event info
    """
    _fields_ = [
        ('nEvent', c_int),                  # 事件类型,参见智能事件类型，如 EVENT_IVS_ALL;Event type, see intelligent analysis event type,like EVENT_IVS_ALL
        ('arrayObejctType', c_int * 16),    # 支持的物体类型，当前支持 EM_OBJECT_TYPE.HUMAN, EM_OBJECT_TYPE.VECHILE, EM_OBJECT_TYPE.NOMOTOR, EM_OBJECT_TYPE.ALL,参考EM_OBJECT_TYPE;object type, currently support EM_OBJECT_TYPE_HUMAN, EM_OBJECT_TYPE_VECHILE, EM_OBJECT_TYPE_NOMOTOR, EM_OBJECT_TYPE_ALL
        ('nObjectCount', c_int),            # szObejctType 数量;szObejctType's count
        ('byReserved', c_ubyte * 512),      # 预留字段;reserved
    ]

class NET_IN_PLAY_BACK_BY_TIME_INFO(Structure):
    """
    录像回放入参信息; record play back parameter in
    """
    _fields_ = [
        ('stStartTime', NET_TIME),                      # 开始时间; Begin time
        ('stStopTime', NET_TIME),                       # 结束时间; End time
        ('hWnd', C_LLONG),                              # 播放窗格, 可为NULL; Play window
        ('cbDownLoadPos', CB_FUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, C_LDWORD)), # 进度回调，对应SDK_Callback的fDownLoadPosCallBack; Download pos callback，corresponding to SDK_Callback's fDownLoadPosCallBack
        ('dwPosUser', C_LDWORD),                        # 进度回调用户信息; Pos user
        ('fDownLoadDataCallBack', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(c_ubyte), C_DWORD, C_LDWORD)), # 数据回调，对应SDK_Callback的fDataCallBack; Download data callback，corresponding to SDK_Callback's fDataCallBack
        ('dwDataUser', C_LDWORD),                       # 数据回调用户信息; Data user
        ('nPlayDirection', c_int),                      # 播放方向, 0:正放; 1:倒放; Playback direction
        ('nWaittime', c_int),                           # 接口超时时间, 目前倒放使用; Watiting time
        ('pstuEventInfo', POINTER(EVENT_INFO)),         # 事件信息（定制），用户分配内存，不用时赋值为NULL; Event info(customized), user allocate memory
        ('nEventInfoCount', c_uint),                    # pstuEventInfo 个数，最大为 16; pstuEventInfo's count, max num is 16
        ('bReserved', c_ubyte * 1012),                  # 预留字段; reserved
    ]

class NET_OUT_PLAY_BACK_BY_TIME_INFO(Structure):
    """
    录像回放出参信息; record play back parameter out
    """
    _fields_ = [
        ('bReserved', c_ubyte * 1024),                # 预留字节; reserved
    ]

class SNAP_PARAMS(Structure):
    """
    抓图参数结构体;Snapshot parameter structure
    """
    _fields_ = [
        ('Channel', c_uint),            # 抓图的通道；Snapshot channel
        ('Quality', c_uint),            # 画质；1~6；Image quality:level 1 to level 6
        ('ImageSize', c_uint),          # 画面大小；0：QCIF,1：CIF,2：D1；Video size;0:QCIF,1:CIF,2:D1
        ('mode', c_uint),               # 抓图模式；-1:表示停止抓图, 0：表示请求一帧, 1：表示定时发送请求, 2：表示连续请求；Snapshot mode;0:request one frame,1:send out requestion regularly,2: Request consecutively
        ('InterSnap', c_uint),          # 时间单位秒；若mode=1表示定时发送请求时,只有部分特殊设备(如：车载设备)支持通过该字段实现定时抓图时间间隔的配置
                                        # Time unit is second.If mode=1, it means send out requestion regularly. The time is valid.
        ('CmdSerial', c_uint),          # 请求序列号，有效值范围 0~65535，超过范围会被截断为 unsigned short；Request serial number，valid value:0~65535
        ('Reserved', c_uint*4),         # 预留字节;reserved
    ]

class NET_MOTIONDETECT_REGION_INFO(Structure):
    """
    动检区域信息;Region info of motion detection
    """
    _fields_ = [
        ('nRegionID', c_uint),          # 区域ID;region ID
        ('szRegionName', c_char*64),    # 区域名称;region name
        ('bReserved', c_ubyte*508),     # 保留字节;reserved
    ]

class ALARM_MOTIONDETECT_INFO(Structure):
    """
    报警事件类型SDK_ALARM_TYPE.EVENT_MOTIONDETECT(视频移动侦测事件)对应的数据描述信息;alarm event type SDK_ALARM_TYPE.EVENT_MOTIONDETECT (video motion detection event) corresponding data description info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小；Structure size
        ('nChannelID', c_int),                          # 通道号;channel
        ('PTS', c_double),                              # 时间戳(单位是毫秒);timestamp (unit is millisecond)
        ('UTC', NET_TIME_EX),                           # 事件发生的时间;event occurrence time
        ('nEventID', c_int),                            # 事件ID;event ID
        ('nEventAction', c_int),                        # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;event action, 0 means pulse event, 1 means continuous event begin, 2 means continuous event end;
        ('nRegionNum', c_uint),                         # 动检区域个数;count of region
        ('stuRegion', NET_MOTIONDETECT_REGION_INFO*32),    # 动检区域信息;region info of motion detection
        ('bSmartMotionEnable', c_int),                  # 智能动检是否使能;smart motion detection is enable or not
        ('nDetectTypeNum', c_uint),                     # 动检触发类型个数;count of triggeing motion detection type
        ('emDetectType', c_int*32),                     # 动检触发类型, 当nRegionNum大于0时，和stuRegion数组一一对应,参考枚举EM_MOTION_DETECT_TYPE;triggeing motion detection type, when nRegionNum>0，one-to-one correspondence with stuRegion if nRegionNum is biger than 0，refer to EM_MOTION_DETECT_TYPE
                                                        # 若nRegionNum为0，触发区域未知，不与窗口绑定，默认第一个元素表示触发类型;the type is the first value of emDetectType if nRegionNum is 0
    ]

class NET_FACE_INFO(Structure):
    """
    多人脸检测信息; multi faces detect info
    """
    _fields_ = [
        ('nObjectID', c_int),               # 物体ID,每个ID表示一个唯一的物体;object id
        ('szObjectType', c_char * 128),     # 物体类型;object type
        ('nRelativeID', c_int),             # 这张人脸抠图所属的大图的ID;same with the source picture id
        ('BoundingBox', SDK_RECT),          # 包围盒;bounding box
        ('Center', SDK_POINT),              # 物体中心;object center
    ]

class NET_FEATURE_VECTOR(Structure):
    """
    存储IVSS项目招行VIP需求,特征值信息; Feature data Information
    """
    _fields_ = [
        ('dwOffset', C_DWORD),  # 人脸小图特征值在二进制数据块中的偏移;Face feature data offset in data block(Unit:BYTE)
        ('dwLength', C_DWORD),  # 人脸小图特征值长度，单位:字节;Face feature data length(Unit:BYTE)
        ('byReserved', c_ubyte * 120),  # 保留;Reserved
    ]

class NET_EULER_ANGLE(Structure):
    """
    姿态角数据; euler angle
    """
    _fields_ = [
        ('nPitch', c_int),      # 仰俯角;pitch
        ('nYaw', c_int),        # 偏航角;yaw
        ('nRoll', c_int),       # 翻滚角;roll
    ]

class NET_HUMAN_TEMPERATURE_INFO(Structure):
    """
    人体温信息; Information of human body temperature
    """
    _fields_ = [
        ('dbTemperature', c_double),        # 温度;Temperature
        ('emTemperatureUnit', c_int),       # 温度单位，参考EM_HUMAN_TEMPERATURE_UNIT;Temperature unit,refer to EM_HUMAN_TEMPERATURE_UNIT
        ('bIsOverTemp', c_int),             # 是否超温;Is over temperature
        ('bIsUnderTemp', c_int),            # 是否低温;Is under temperature
        ('bReserved', c_ubyte * 132),       # 预留字段;Reserved
    ]

class DEV_EVENT_FACEDETECT_INFO(Structure):
    """
    事件类型FACEDETECT(人脸检测事件)对应的数据块描述信息; the describe of FACEDETECT's data
    """
    _fields_ = [
        ('nChannelID', c_int),                          # 通道号；channel ID
        ('szName', c_char * 128),                       # 事件名称;event name
        ('bReserved1', c_char * 4),                     # 字节对齐;byte alignment
        ('PTS', c_double),                              # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),                           # 事件发生的时间;the event happen time
        ('nEventID', c_int),                            # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),                  # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),           # 事件对应文件信息;event file info
        ('bEventAction', c_ubyte),                      # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action: 0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('reserved', c_ubyte * 2),                      # 保留字节;reserved
        ('byImageIndex', c_ubyte),                      # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('nDetectRegionNum', c_int),                    # 规则检测区域顶点数;detect region point number
        ('DetectRegion', SDK_POINT * 20),               # 规则检测区域;detect region
        ('dwSnapFlagMask', C_DWORD),                    # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON
        ('szSnapDevAddress', c_char * 260),             # 抓拍当前人脸的设备地址,如：滨康路37号;snapshot current face device address
        ('nOccurrenceCount', c_uint),                   # 事件触发累计次数;event trigger accumilated times
        ('emSex', c_int),                               # 性别，参考EM_DEV_EVENT_FACEDETECT_SEX_TYPE;sex type,refer to EM_DEV_EVENT_FACEDETECT_SEX_TYPE
        ('nAge', c_ubyte),                              # 年龄,-1表示该字段数据无效;age, invalid if it is -1
        ('nFeatureValidNum', c_uint),                   # 人脸特征数组有效个数,与 emFeature 结合使用;invalid number in array emFeature
        ('emFeature', c_uint * 32),                     # 人脸特征数组,与 nFeatureValidNum 结合使用，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;human face features,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('nFacesNum', c_int),                           # 指示stuFaces有效数量;number of stuFaces
        ('stuFaces', NET_FACE_INFO * 10),               # 多张人脸时使用,此时没有Object;when nFacesNum > 0, stuObject invalid
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),# 智能事件公共信息;public info
        ('emRace', c_int),                              # 参考EM_RACE_TYPE;race,refer to EM_RACE_TYPE
        ('emEye', c_int),                               # 眼睛状态，参考EM_EYE_STATE_TYPE;eyes state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),                             # 嘴巴状态，参考EM_MOUTH_STATE_TYPE;mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),                              # 口罩状态，参考EM_MASK_STATE_TYPE;mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),                             # 胡子状态，参考EM_BEARD_STATE_TYPE;beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),                         # 魅力值, -1表示无效, 0未识别，识别时范围1-100,得分高魅力高;Attractive value, -1: invalid, 0:no disringuish，range: 1-100, the higher value, the higher charm
        ('szUID', c_char * 32),                         # 抓拍人员写入数据库的唯一标识符;The unique identifier of the snap person to write to the database
        ('bReserved2', C_BYTE*4),
        ('stuFeatureVector', NET_FEATURE_VECTOR),       # 特征值信息;Feature data information
        ('szFeatureVersion', c_char * 32),              # 特征值算法版本;The version of the feature data algorithm
        ('emFaceDetectStatus', c_int),                  # 人脸在摄像机画面中的状态，参考EM_FACE_DETECT_STATUS;The status of person in camera picture,refer to EM_FACE_DETECT_STATUS
        ('stuFaceCaptureAngle', NET_EULER_ANGLE),       # 人脸在抓拍图片中的角度信息, nPitch:抬头低头的俯仰角, nYaw左右转头的偏航角, nRoll头在平面内左偏右偏的翻滚角;euler angle of face in the capture picture, nPitch:pitch of the head, nYaw: yaw of the head, nRoll:roll of the head
                                                        # 角度值取值范围[-90,90], 三个角度值都为999表示此角度信息无效;range of the angle value is [-90,90], stuFaceCaptureAngle is invalid if the three angles are 999.
        ('dHumanSpeed', c_double),                      # 人的运动速度, km/h;human speed, km/h
        ('nFaceAlignScore', c_int),                     # 人脸对齐得分分数,范围 0~10000,-1为无效值;The score of face picture align.The range is 0~10000,-1 is invalid
        ('nFaceClarity', c_int),                        # 人脸清晰度分数,范围 0~10000,-1为无效值;The score of face picture clarity.The range is 0~10000,-1 is invalid
        ('bHumanTemperature', c_int),                   # 人体温信息是否有效;Whether the information of human body temperature is valid
        ('stuHumanTemperature', NET_HUMAN_TEMPERATURE_INFO),        # 人体温信息, bHumanTemperature为TURE时有效;Information of human body temperature, It is valid whne bHumanTemperature is TURE
        ('bReserved', c_ubyte * 480),                   # 保留字节,留待扩展;Reserved
    ]

class FACERECOGNITION_PERSON_INFO(Structure):
    """
    人员信息; person info
    """
    _fields_ = [
        ('szPersonName', c_char * 16),      # 姓名,此参数作废；name
        ('wYear', c_ushort),                # 出生年,作为查询条件时,此参数填0,则表示此参数无效;birth year
        ('byMonth', c_ubyte),               # 出生月,作为查询条件时,此参数填0,则表示此参数无效;birth month
        ('byDay', c_ubyte),                 # 出生日,作为查询条件时,此参数填0,则表示此参数无效;birth day
        ('szID', c_char * 32),              # 人员唯一标示(身份证号码,工号,或其他编号);the unicle ID for the person
        ('bImportantRank', c_ubyte),        # 人员重要等级,1~10,数值越高越重要,作为查询条件时,此参数填0,则表示此参数无效;importance level,1~10,the higher value the higher level
        ('bySex', c_ubyte),                 # 性别,1-男,2-女,作为查询条件时,此参数填0,则表示此参数无效;sex, 0-man, 1-female
        ('wFacePicNum', c_ushort),          # 图片张数;picture number
        ('szFacePicInfo', SDK_PIC_INFO * 48),  # 当前人员对应的图片信息;picture info
        ('byType', c_ubyte),                # 人员类型,详见 EM_PERSON_TYPE;Personnel types, see EM_PERSON_TYPE
        ('byIDType', c_ubyte),              # 证件类型,详见 EM_CERTIFICATE_TYPE;Document types, see EM_CERTIFICATE_TYPE
        ('byGlasses', c_ubyte),             # 是否戴眼镜，0-未知 1-不戴 2-戴;Whether wear glasses or not,0-unknown,1-not wear glasses,2-wear glasses
        ('byAge', c_ubyte),                 # 年龄,0表示未知;Age,0 means unknown
        ('szProvince', c_char * 64),        # 省份;flag(by bit),see NET_RESERVED_COMMON;province
        ('szCity', c_char * 64),            # 城市;snapshot current face device address;city
        ('szPersonNameEx', c_char * 64),    # 姓名,因存在姓名过长,16字节无法存放问题,故增加此参数,;Name, the name is too long due to the presence of 16 bytes can not be Storage problems, the increase in this parameter
        ('szUID', c_char * 32),             # 人员唯一标识符,首次由服务端生成,区别于ID字段,修改,删除操作时必填;person unique ID
        ('szCountry', c_char * 3),          # 国籍,符合ISO3166规范;country
        ('byIsCustomType', c_ubyte),        # 人员类型是否为自定义: 0 使用Type规定的类型 1 自定义,使用szPersonName字段;using person type: 0 using byType, 1 using szPersonName
        ('pszComment', c_char_p),           # 备注信息, 用户自己申请内存的情况时;comment info, when the memory is alloced by user,
                                                # 下方bCommentLen需填写对应的具体长度值，推荐长度 NET_COMMENT_LENGTH;the value of bCommentLen needs to be filled in，recommended length is NET_COMMENT_LENGTH
        ('pszGroupID', c_char_p),           # 人员所属组ID, 用户自己申请内存的情况时;group ID, when the memory is alloced by user,
                                                # 下方bGroupIdLen需填写对应的具体长度值，推荐长度 NET_GROUPID_LENGTH;the value of bGroupIdLen needs to be filled in，recommended length is NET_GROUPID_LENGTH
        ('pszGroupName', c_char_p),         # 人员所属组名, 用户自己申请内存的情况时;group name, when the memory is alloced by user,
                                            # 下方bGroupNameLen需填写对应的具体长度值，推荐长度 NET_GROUPNAME_LENGTH;the value of bGroupNameLen needs to be filled in，recommended length is NET_GROUPNAME_LENGTH
        ('pszFeatureValue', c_char_p),      # 人脸特征, 用户自己申请内存的情况时;the face feature , when the memory is alloced by user,
                                            # 下方bFeatureValueLen需填写对应的具体长度值，推荐长度 NET_FEATUREVALUE_LENGTH;the value of bFeatureValueLen needs to be filled in，recommended length is NET_FEATUREVALUE_LENGTH
        ('bGroupIdLen', c_ubyte),           # pszGroupID的长度;len of pszGroupID
        ('bGroupNameLen', c_ubyte),         # pszGroupName的长度;len of pszGroupName
        ('bFeatureValueLen', c_ubyte),      # pszFeatureValue的长度;len of pszFeatureValue
        ('bCommentLen', c_ubyte),           # pszComment的长度;len of pszComment
        ('emEmotion', c_int),               # 表情，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;Emotion,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
    ]

class CUSTOM_PERSON_INFO(Structure):
    """
    注册人员信息扩展结构体; extension of registered personnel information
    """
    _fields_ = [
        ('szPersonInfo', c_char * 64),      # 人员扩展信息;personnel extension information
        ('byReserved', c_ubyte * 124),      # 保留字节;Reserved bytes
    ]

class FACERECOGNITION_PERSON_INFOEX(Structure):
    """
    人员信息扩展结构体; expansion of  personnel information
    """
    _fields_ = [
        ('szPersonName', c_char * 64),      # 姓名；name
        ('wYear', c_ushort),                # 出生年,作为查询条件时,此参数填0,则表示此参数无效;birth year
        ('byMonth', c_ubyte),               # 出生月,作为查询条件时,此参数填0,则表示此参数无效;birth month
        ('byDay', c_ubyte),                 # 出生日,作为查询条件时,此参数填0,则表示此参数无效;birth day
        ('bImportantRank', c_ubyte),        # 人员重要等级,1~10,数值越高越重要,作为查询条件时,此参数填0,则表示此参数无效;importance level,1~10,the higher value the higher level
        ('bySex', c_ubyte),                 # 性别,1-男,2-女,作为查询条件时,此参数填0,则表示此参数无效;sex, 0-man, 1-female
        ('szID', c_char * 32),              # 人员唯一标示(身份证号码,工号,或其他编号);the unicle ID for the person
        ('wFacePicNum', c_ushort),          # 图片张数;picture number
        ('szFacePicInfo', SDK_PIC_INFO * 48),  # 当前人员对应的图片信息;picture info
        ('byType', c_ubyte),                # 人员类型,详见 EM_PERSON_TYPE;Personnel types, see EM_PERSON_TYPE
        ('byIDType', c_ubyte),              # 证件类型,详见 EM_CERTIFICATE_TYPE;Document types, see EM_CERTIFICATE_TYPE
        ('byGlasses', c_ubyte),             # 是否戴眼镜，0-未知 1-不戴 2-戴;Whether wear glasses or not,0-unknown,1-not wear glasses,2-wear glasses
        ('byAge', c_ubyte),                 # 年龄,0表示未知;Age,0 means unknown
        ('szProvince', c_char * 64),        # 省份;flag(by bit),see NET_RESERVED_COMMON;province
        ('szCity', c_char * 64),            # 城市;snapshot current face device address;city
        ('szUID', c_char * 32),             # 人员唯一标识符,首次由服务端生成,区别于ID字段,修改,删除操作时必填;person unique ID
        ('szCountry', c_char * 3),          # 国籍,符合ISO3166规范;country
        ('byIsCustomType', c_ubyte),        # 人员类型是否为自定义: 0 使用Type规定的类型 1 自定义,使用szCustomType字段;using person type: 0 using byType, 1 using szCustomType
        ('szCustomType', c_char * 16),      # 人员自定义类型;custom type of person
        ('szComment', c_char * 100),        # 备注信息;comment info
        ('szGroupID', c_char * 64),         # 人员所属组ID;group ID
        ('szGroupName', c_char * 128),      # 人员所属组名, 用户自己申请内存的情况时;group name
        ('emEmotion', c_int),               # 表情，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;Emotion,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('szHomeAddress', c_char * 128),    # 注册人员家庭地址;home address of the person
        ('emGlassesType', c_int),           # 眼镜类型，参考EM_GLASSES_TYPE;glasses type,refer to EM_GLASSES_TYPE
        ('emRace', c_int),                  # 参考EM_RACE_TYPE;race,refer to EM_RACE_TYPE
        ('emEye', c_int),                   # 眼睛状态，参考EM_EYE_STATE_TYPE;eye state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),                 # 嘴巴状态，参考EM_MOUTH_STATE_TYPE;mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),                  # 口罩状态，参考EM_MASK_STATE_TYPE;mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),                 # 胡子状态，参考EM_BEARD_STATE_TYPE;beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),             # 魅力值, -1表示无效, 0未识别，识别时范围1-100,得分高魅力高;attractive, -1:invalid, 0:unknown，1-100
        ('emFeatureState', c_int),          # 人员建模状态, 详见EM_PERSON_FEATURE_STATE;person feature state,refer to EM_PERSON_FEATURE_STATE
        ('bAgeEnable', c_int),              # 是否指定年龄段;age range is enabled
        ('nAgeRange', c_int * 2),           # 年龄范围;age range
        ('nEmotionValidNum', c_int),        # 人脸特征数组有效个数,与 emFeature 结合使用, 如果为0则表示查询所有表情;invalid number in array emEmotion, 0 means all emotion
        ('emEmotions', c_int * 32),         # 人脸特征数组,与 byFeatureValidNum 结合使用  设置查询条件的时候使用，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;human emotion  set the query condition，refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('nCustomPersonInfoNum', c_int),    # 注册人员信息扩展个数;extension number of registered personnel information
        ('szCustomPersonInfo', CUSTOM_PERSON_INFO * 4),  # 注册人员信息扩展;extension of registered personnel information
        ('emRegisterDbType', c_int),        # 注册库类型，参考EM_REGISTER_DB_TYPE;type of register face DB
        ('stuEffectiveTime', NET_TIME),     # 有效期时间;effective time
        ('emFeatureErrCode', c_int),        # 建模失败原因，参考EM_PERSON_FEATURE_ERRCODE;error code of person feature,refer to EM_PERSON_FEATURE_ERRCODE
        ('byReserved', c_ubyte * 1112),     # 保留字节;Reserved bytes
    ]

class SDK_PIC_INFO_EX3(Structure):
    """
    物体对应图片文件信息(包含图片路径); picture info
    """
    _fields_ = [
        ('dwOffSet', C_DWORD),          # 文件在二进制数据块中的偏移位置, 单位:字节;current picture file's offset in the binary file, byte
        ('dwFileLenth', C_DWORD),       # 文件大小, 单位:字节;current picture file's size, byte
        ('wWidth', c_ushort),           # 图片宽度, 单位:像素;picture width, pixel
        ('wHeight', c_ushort),          # 图片高度, 单位:像素;picture high, pixel
        ('szFilePath', c_char * 64),    # 文件路径; File path
        ('bIsDetected', c_ubyte),       # 图片是否算法检测出来的检测过的提交识别服务器时, 则不需要再时检测定位抠图,1:检测过的,0:没有检测过;When submit to the server, the algorithm has checked the image or not
        ('bReserved', c_ubyte * 11),    # 预留字段;Reserved
    ]

class CANDIDATE_INFO(Structure):
    """
    候选人员信息; cadidate person info
    """
    _fields_ = [
        ('stPersonInfo', FACERECOGNITION_PERSON_INFO),          # 人员信息;person info
                                                                    # 布控（黑名单）库, 指布控库中人员信息；
                                                                    # 历史库, 指历史库中人员信息
                                                                    # 报警库, 指布控库的人员信息
        ('bySimilarity', c_ubyte),                              # 和查询图片的相似度,百分比表示,1~100;similarity
        ('byRange', c_ubyte),                                   # 人员所属数据库范围,详见EM_FACE_DB_TYPE; Range officer's database, see EM_FACE_DB_TYPE
        ('byReserved1', c_ubyte * 2),                           # 预留字段;Reserved
        ('stTime', NET_TIME),                                   # 当byRange为历史数据库时有效,表示查询人员出现的时间;When byRange historical database effectively, which means that the query time staff appeared
        ('szAddress', c_ubyte * 260),                           # 当byRange为历史数据库时有效,表示查询人员出现的地点;When byRange historical database effectively, which means that people place a query appears
        ('bIsHit', c_int),                                      # 是否有识别结果,指这个检测出的人脸在库中有没有比对结果;Is hit, means the result face has compare result in database
        ('stuSceneImage', SDK_PIC_INFO_EX3),                    # 人脸全景图;Scene Image
        ('nChannelID', c_int),                                  # 通道号;Channel Id
        ('byReserved', c_ubyte * 32),                           # 保留字节;Reserved bytes
    ]

class NET_HISTORY_HUMAN_IMAGE_INFO(Structure):
    """
    历史库人体图片信息; Image info of human in history data base
    """
    _fields_ = [
        ('nLength', c_int),             # 图片大小,单位:字节;Image, unit:byte
        ('nWidth', c_int),              # 图片宽度;Image width
        ('nHeight', c_int),             # 图片高度;Image height
        ('szFilePath', c_char * 260),   # 文件路径;Image path
    ]

class NET_HISTORY_HUMAN_INFO(Structure):
    """
    历史库人体信息; Human info in history data base
    """
    _fields_ = [
        ('emCoatColor', c_int),             # 上衣颜色,参考EM_CLOTHES_COLOR; Coat color,refer to EM_CLOTHES_COLOR
        ('emCoatType', c_int),              # 上衣类型，参考EM_COAT_TYPE; Coat type, refer to EM_COAT_TYPE
        ('emTrousersColor', c_int),         # 裤子颜色,参考EM_CLOTHES_COLOR; Trousers color,refer to EM_CLOTHES_COLOR
        ('emTrousersType', c_int),          # 裤子类型，参考EM_TROUSERS_TYPE; Trousers type,refer to EM_TROUSERS_TYPE
        ('emHasHat', c_int),                # 是否戴帽子，参考EM_HAS_HAT; Has hat or not,refer to EM_HAS_HAT
        ('emHasBag', c_int),                # 是否带包，参考EM_HAS_BAG; Has bag or not,refer to EM_HAS_BAG
        ('stuBoundingBox', NET_RECT),       # 包围盒(8192坐标系); Bounding box
        ('nAge', c_int),                    # 年龄;Age
        ('emSex', c_int),                   # 性别，参考EM_SEX_TYPE;Sex,refer to EM_SEX_TYPE
        ('emAngle', c_int),                 # 角度，参考EM_ANGLE_TYPE;Angle,refer to EM_ANGLE_TYPE
        ('emHasUmbrella', c_int),           # 是否打伞，参考EM_HAS_UMBRELLA;Has umbrella or not,refer to EM_HAS_UMBRELLA
        ('emBag', c_int),                   # 包类型，参考EM_BAG_TYPE;Bag type,refer to EM_BAG_TYPE
        ('emUpperPattern', c_int),          # 上半身衣服图案，参考EM_CLOTHES_PATTERN;Upper pattern,refer to EM_CLOTHES_PATTERN
        ('emHairStyle', c_int),             # 头发样式，参考EM_HAIR_STYLE;Hair style,refer to EM_HAIR_STYLE
        ('emCap', c_int),                   # 帽类型，参考EM_CAP_TYPE;Cap type,refer to EM_CAP_TYPE
        ('emHasBackBag', c_int),            # 是否有背包，参考EM_HAS_BACK_BAG;Has back bag or not,refer to EM_HAS_BACK_BAG
        ('emHasCarrierBag', c_int),         # 是否带手提包，参考EM_HAS_CARRIER_BAG;Has carrier bag or not,refer to EM_HAS_CARRIER_BAG
        ('emHasShoulderBag', c_int),        # 是否有肩包，参考EM_HAS_SHOULDER_BAG;Has shoulder bag or not,refer to EM_HAS_SHOULDER_BAG
        ('emMessengerBag', c_int),          # 是否有斜跨包，参考EM_HAS_MESSENGER_BAG;Has messenger bag or not,refer to EM_HAS_MESSENGER_BAG
        ('stuImageInfo', NET_HISTORY_HUMAN_IMAGE_INFO),         # 人体图片信息;Human image info
        ('stuFaceImageInfo', NET_HISTORY_HUMAN_IMAGE_INFO),     # 人脸图片信息;Face image info
        ('byReserved', c_ubyte * 256),      # 保留字节;Reserved bytes
    ]


class CANDIDATE_INFOEX(Structure):
    """
    候选人员信息扩展结构体; cadidate person info
    """
    _fields_ = [
        ('stPersonInfo', FACERECOGNITION_PERSON_INFOEX),        # 人员信息;person info
                                                                    # 布控（黑名单）库, 指布控库中人员信息；
                                                                    # 历史库, 指历史库中人员信息
                                                                    # 报警库, 指布控库的人员信息
        ('bySimilarity', c_ubyte),                              # 和查询图片的相似度,百分比表示,1~100;similarity
        ('byRange', c_ubyte),                                   # 人员所属数据库范围,详见EM_FACE_DB_TYPE; Range officer's database, see EM_FACE_DB_TYPE
        ('byReserved1', c_ubyte * 2),                           # 预留字段;Reserved
        ('stTime', NET_TIME),                                   # 当byRange为历史数据库时有效,表示查询人员出现的时间;When byRange historical database effectively, which means that the query time staff appeared
        ('szAddress', c_ubyte * 260),                           # 当byRange为历史数据库时有效,表示查询人员出现的地点;When byRange historical database effectively, which means that people place a query appears
        ('bIsHit', c_int),                                      # 是否有识别结果,指这个检测出的人脸在库中有没有比对结果;Is hit, means the result face has compare result in database
        ('stuSceneImage', SDK_PIC_INFO_EX3),                    # 人脸全景图;Scene Image
        ('nChannelID', c_int),                                  # 通道号;Channel Id
        ('szFilePathEx', c_char * 256),                         # 文件路径;File path
        ('stuHistoryHumanInfo', NET_HISTORY_HUMAN_INFO),        # 历史库人体信息;Human info in history data base
        ('byReserved', c_ubyte * 136),                          # 保留字节;Reserved bytes
    ]

class NET_FACE_DATA(Structure):
    """
    人脸数据; the data of face
    """
    _fields_ = [
        ('emSex', c_int),               # 性别，参考EM_DEV_EVENT_FACEDETECT_SEX_TYPE;sex type,refer to EM_DEV_EVENT_FACEDETECT_SEX_TYPE
        ('nAge', c_int),                # 年龄,-1表示该字段数据无效;age, invalid if it is -1
        ('nFeatureValidNum', c_uint),   # 人脸特征数组有效个数,与 emFeature 结合使用; invalid number in array emFeature
        ('emFeature', c_int * 32),      # 人脸特征数组,与 nFeatureValidNum 结合使用，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;human face features,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('emRace', c_int),              # 参考EM_RACE_TYPE;race,refer to EM_RACE_TYPE
        ('emEye', c_int),               # 眼睛状态，参考EM_EYE_STATE_TYPE;eyes state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),             # 嘴巴状态，参考EM_MOUTH_STATE_TYPE;mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),              # 口罩状态，参考EM_MASK_STATE_TYPE;mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),             # 胡子状态，参考EM_BEARD_STATE_TYPE;beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),         # 魅力值, -1表示无效, 0未识别，识别时范围1-100,得分高魅力高;Attractive value, -1: invalid, 0:no disringuish，range: 1-100, the higher value, the higher charm
        ('bReserved1', C_BYTE*4),
        ('stuFaceCaptureAngle', NET_EULER_ANGLE),  # 人脸在抓拍图片中的角度信息,角度值取值范围[-90,90], 三个角度值都为999表示此角度信息无效; euler angle of face in the capture picture,range of the angle value is [-90,90], stuFaceCaptureAngle is invalid if the three angles are 999.
        ('nFaceQuality', c_uint),       # 人脸抓拍质量分数;quality about capture picture
        ('nFaceAlignScore', c_int),     # 人脸对齐得分分数,范围 0~10000,-1为无效值;The score of face picture align.The range is 0~10000,-1 is invalid
        ('nFaceClarity', c_int),        # 人脸清晰度分数,范围 0~10000,-1为无效值;The score of face picture clarity.The range is 0~10000,-1 is invalid
        ('dbTemperature', c_double),    # 温度, bAnatomyTempDetect 为TRUE时有效;Temperature, it is valid when bAnatomyTempDetect is true
        ('bAnatomyTempDetect', c_int),  # 是否人体测温;Is anatomy temperature detection
        ('emTemperatureUnit', c_int),   # 温度单位, bAnatomyTempDetect 为TRUE时有效,参考EM_HUMAN_TEMPERATURE_UNIT;Temperature unit, it is valid when bAnatomyTempDetect is true,refer to EM_HUMAN_TEMPERATURE_UNIT
        ('bIsOverTemp', c_int),         # 是否超温, bAnatomyTempDetect 为TRUE时有效;Is over temperature, it is valid when bAnatomyTempDetect is true
        ('bIsUnderTemp', c_int),        # 是否低温, bAnatomyTempDetect 为TRUE时有效;Is under temperature, it is valid when bAnatomyTempDetect is true
        ('bReserved', c_ubyte * 76),    # 保留字节,留待扩展;Reserved bytes

    ]

class NET_PASSERBY_INFO(Structure):
    """
    路人信息; passerby info
    """
    _fields_ = [
        ('szPasserbyUID', c_char * 32),             # 路人唯一标识符;The unique identifier of the passerby to write to the database
        ('szPasserbyGroupId', c_char * 64),         # 路人库ID;Passerby group ID
        ('szPasserbyGroupName', c_char * 128),      # 路人库名称;Passerby group name
        ('byReserved', c_ubyte * 128),              # 保留;Reserved
    ]


class NET_FACECOMPARISON_PTZ_INFO(Structure):
    """
    人脸比对事件触发对应球机信息; Face matching event triggers corresponding ball machine information
    """
    _fields_ = [
        ('szPresetName', c_char * 64),             # 球机抓拍到人脸时预置点名称;Preset point name when the ball machine captures the face
        ('dwPresetNumber', C_DWORD),         # 球机抓拍到人脸时预置点编号;Preset point number when the ball machine captures the face
        ('byReserved1', c_ubyte * 4),           # 字节对齐;Byte alaginment
        ('byReserved', c_ubyte * 256),           # 保留字节;Reserved
    ]

class NET_CUSTOM_PROJECTS_INFO(Structure):
    """
    项目定制信息; Custom project info
    """
    _fields_ = [
        ('stuGPSInfo', NET_GPS_INFO),             # GPS位置信息;GPS info
        ('stuFaceComparisonPTZInfo', NET_FACECOMPARISON_PTZ_INFO),         # 人脸比对事件触发对应球机信息;Face matching event triggers corresponding ball machine information
        ('szPlateNumber', c_char * 64),           # 人脸比对时车牌信息;License plate information in face comparison
        ('byReserved', c_ubyte * 1024),           # 保留;Reserved
    ]


class DEV_EVENT_FACERECOGNITION_INFO(Structure):
    """
    事件类型FACERECOGNITION(人脸识别)对应的数据块描述信息; the describe of FACERECOGNITION's data
    """
    _fields_ = [
        ('nChannelID', c_int),                          # 通道号；channel ID
        ('szName', c_char * 128),                       # 事件名称;event name
        ('nEventID', c_int),                            # 事件ID;event ID
        ('UTC', NET_TIME_EX),                           # 事件发生的时间;the event happen time
        ('stuObject', SDK_MSG_OBJECT),                  # 检测到的物体;have being detected object
        ('nCandidateNum', c_int),                       # 当前人脸匹配到的候选对象数量;candidate number
        ('stuCandidates', CANDIDATE_INFO * 50),         # 当前人脸匹配到的候选对象信息;candidate info
        ('bEventAction', c_ubyte),                      # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byImageIndex', c_ubyte),                      # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('byReserved1', c_ubyte * 2),                   # 字节对齐;byte alignment
        ('bGlobalScenePic', c_int),                     # 全景图是否存在;The existence panorama
        ('stuGlobalScenePicInfo', SDK_PIC_INFO),        # 全景图片信息;Panoramic Photos
        ('szSnapDevAddress',  c_char * 260),            # 抓拍当前人脸的设备地址,如：滨康路37号;Snapshot current face aadevice address
        ('nOccurrenceCount', c_uint),                   # 事件触发累计次数;event trigger accumilated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),# 智能事件公共信息;intelligent things info
        ('stuFaceData', NET_FACE_DATA),                 # 人脸数据;the data of face
        ('szUID', c_char * 32),                         # 抓拍人员写入数据库的唯一标识符;The unique identifier of the snap person to write to the database
        ('stuFeatureVector', NET_FEATURE_VECTOR),       # 特征值信息;Feature data information
        ('szFeatureVersion', c_char * 32),              # 特征值算法版本;The version of the feature data algorithm
        ('emFaceDetectStatus', c_int),                  # 人脸在摄像机画面中的状态,参考EM_FACE_DETECT_STATUS;The status of person in camera picture,refer to EM_FACE_DETECT_STATUS
        ('szSourceID', c_char * 32),                    # 事件关联ID,同一个物体或图片生成多个事件时SourceID相同;Correlate event ID, events arising from same object or picture could have same correlate event ID
        ('stuPasserbyInfo', NET_PASSERBY_INFO),         # 路人库信息;passerby info
        ('nStayTime', c_uint),                          # 路人逗留时间 单位：秒;stay time Unit:s
        ('stuGPSInfo', NET_GPS_INFO),                   # GPS信息;GPS info
        ('bReserved', c_ubyte * 432),                   # 保留字节,留待扩展;Reserved
        ('nRetCandidatesExNum', c_int),                 # 当前人脸匹配到的候选对象数量实际返回值;the actual return number of stuCandidatesEx
        ('stuCandidatesEx', CANDIDATE_INFOEX * 50),     # 当前人脸匹配到的候选对象信息扩展;the expansion of candidate information
        ('szSerialUUID', c_char * 22),                  # 级联物体ID唯一标识;szSerial UUID
                                                            # 格式如下：前2位%d%d:01-视频片段,02-图片,03-文件,99-其他;The format is as follows：Front 2:%d%d:01-video,02-picture,03-file,99-other;
                                                            # 中间14位YYYYMMDDhhmmss:年月日时分秒;后5位%u%u%u%u%u：物体ID，如00001;Middle 14:YYYYMMDDhhmmss:year,month,day,hour,minute,second;Last 5:%u%u%u%u%u：object ID，as 00001
        ('byReserved', c_ubyte * 2),                    # 对齐;reserved
        ('stuCustomProjects', NET_CUSTOM_PROJECTS_INFO),  # 项目定制信息;Custom project info
        ('bIsDuplicateRemove', c_int),                  # 智慧零售，是否符合去重策略（TRUE：符合 FALSE：不符合）;Smart retail, whether it conforms to the de duplication strategy (true: conforms to false: does not conform to)
        ('byReserved2', c_ubyte * 4),                   # 字节对齐;byte alaginment
    ]


class PLAY_FRAME_INFO(Structure):
    """
    事件类型FACERECOGNITION(人脸识别)对应的数据块描述信息; the describe of FACERECOGNITION's data
    """
    _fields_ = [
        ('nWidth', c_int),                          # Width, unit is pixel, 0 for audio data.
        ('nHeight', c_int),                         # height, 0 for audio data
        ('nStamp', c_int),                          # Time stamp info, unit is ms
        ('nType', c_int),                           # Video frame type,T_AUDIO16,T_RGB32,T_IYUV
        ('nFrameRate', c_int),                      # Video represents frame rate,audio represents sampling rate
    ]

class NET_VAOBJECT_NUMMAN(Structure):
    """
    检测到的人信息; Human info
    """
    _fields_ = [
        ('nObjectID', c_uint),             # 物体ID，每个ID表示一个唯一的物体;Object ID
        ('emUniformStyle', c_int),         # 制服样式,参考EM_UNIFORM_STYLE;Uniform style，refer to EM_UNIFORM_STYLE
        ('stuBoundingBox', NET_RECT),         # 包围盒,手套对象在全景图中的框坐标,为0~8191相对坐标;Bounding box(8192 coordinate system)
        ('stuOriginalBoundingBox', NET_RECT), # 包围盒,绝对坐标;BoundingBox Rect, absolute coordinates
        ('byReserved', c_byte*128),           # 预留字节;Reserved
    ]


class DEV_EVENT_CROSSLINE_INFO(Structure):
    """
    事件类型CROSSLINEDETECTION(警戒线)对应的数据块描述信息; the describe of CROSSLINEDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),              # 通道号;Channel
        ('szName', c_char * 128),           # 事件名称;event name
        ('bReserved1', c_char * 4),         # 字节对齐;byte alignment
        ('PTS', c_double),                  # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),               # 事件发生的时间;the event happen time
        ('nEventID', c_int),                # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),      # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),   # 事件对应文件信息;event file info
        ('DetectLine', SDK_POINT*20),           # 规则检测线;rule detect line
        ('nDetectLineNum', c_int),          # 规则检测线顶点数;rule detect line's point number
        ('TrackLine', SDK_POINT*20),        # 物体运动轨迹;object moveing track
        ('nTrackLineNum', c_int),           # 物体运动轨迹顶点数;object moveing track's point number
        ('bEventAction', c_byte),           # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('bDirection', c_byte),             # 表示入侵方向, 0-由左至右, 1-由右至左;direction, 0-left to right, 1-right to left
        ('byReserved', c_byte),             # 字节对齐;byte alignment
        ('byImageIndex', c_byte),           # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('dwSnapFlagMask', C_DWORD),        # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout";flag(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('nSourceIndex', c_int),            # 事件源设备上的index,-1表示数据无效,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', c_char*260),     # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nOccurrenceCount', c_uint),       # 事件触发累计次数;event trigger accumulated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),    # 智能事件公共信息;intelli comm info
        ('stuExtensionInfo', NET_EXTENSION_INFO),       # 扩展信息;Extension info
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),         # 全景广角图;Scene image
        ('nObjetcHumansNum', c_uint),                   # 检测到人的数量;Number of people detected
        ('stuObjetcHumans', NET_VAOBJECT_NUMMAN * 100), # 检测的到人;People detected
        ('byReserved1', c_byte*512),                    # 预留字节;Reserved
    ]


class NET_IN_GET_CAMERA_STATEINFO(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_GET_CAMERA_STATE 命令入参;QueryDevInfo interface NET_QUERY_GET_CAMERA_STATE command to input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小;Struct size
        ('bGetAllFlag', c_bool),    # 是否查询所有摄像机状态,若该成员为 TRUE,则 nChannels 成员无需设置;
                                    # if it is to check all the cameras status, if the member is TRUE, then nChannels member is unnecessary to set.
        ('nValidNum', c_int),       # 该成员,bGetAllFlag 为 FALSE时有效,表示 nChannels 成员有效个数
                                    # the member is valid when bGetAllFlag is FALSE, which means valid number of nChannels member
        ('nChannels', c_int*1024),  # 该成员,bGetAllFlag 为 FALSE时有效,将需要查询的通道号依次填入
                                    # The member is valid when bGetAllFlag is FALSE, it is to fill in the channel numbers in turn which needs inquiry.
    ]

class NET_CAMERA_STATE_INFO(Structure):
    """
    摄像机通道信息; Camera state info
    """
    _fields_ = [
        ('nChannel', c_int),            # 摄像机通道号, -1表示通道号无效;camera channel number, -1 means invalid channel number
        ('emConnectionState', c_int),   # 连接状态,参见SDK_Enum.py内的EM_CAMERA_STATE_TYPE;connection state，refer to EM_CAMERA_STATE_TYPE in SDK.Enum.py
        ('szReserved', c_char*1024),    # 保留字节;byte reserved
    ]

class NET_OUT_GET_CAMERA_STATEINFO(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_GET_CAMERA_STATE 命令出参;QueryDevInfo interface NET_QUERY_GET_CAMERA_STATE command to output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                        # 结构体大小;Struct size
        ('nValidNum', c_int),                                       # 查询到的摄像机通道状态有效个数,由sdk返回;valid number of camera channel state, returned by sdk
        ('nMaxNum', c_int),                                         # pCameraStateInfo 数组最大个数,由用户填写;max number of array, filled in by user
        ('pCameraStateInfo', POINTER(NET_CAMERA_STATE_INFO)),       # 摄像机通道信息数组,由用户分配,大小为sizeof(NET_CAMERA_STATE_INFO)*nMaxNum;camera channel info array, distributed by user,apply to sizeof(NET_CAMERA_STATE_INFO)*nMaxNum;
    ]

class DEV_ACCESS_CTL_IMAGE_INFO(Structure):
    """
    图片信息; access control image info
    """
    _fields_ = [
        ('emType', C_ENUM),             # 图片类型, 参考 EM_ACCESS_CTL_IMAGE_TYPE; Image type, Please refer to EM_ACCESS_CTL_IMAGE_TYPE
        ('nOffSet', C_UINT),            # 二进制块偏移字节; Offset in binary block
        ('nLength', C_UINT),            # 图片大小; Image size
        ('nWidth', C_UINT),             # 图片宽度(单位:像素); Image width(Unit:pixel)
        ('nHeight', C_UINT),            # 图片高度(单位:像素); Image height(Unit:pixel)
        ('stuBoundingBox', NET_RECT),   # 包围盒; Bounding box
        ('byReserved', C_BYTE * 48),    # 保留字节; Reserved
    ]

class DEV_ACCESS_CTL_CUSTOM_WORKER_INFO(Structure):
    """
    定制人员信息; custom worker info
    """
    _fields_ = [
        ('emSex', C_ENUM),                              # 性别, 参考 NET_ACCESSCTLCARD_SEX; sex, Please refer to NET_ACCESSCTLCARD_SEX
        ('szRole', c_char * 32),                        # 角色; role
        ('szProjectNo', c_char * 32),                   # 项目ID; project No.
        ('szProjectName', c_char * 64),                 # 项目名称; project name
        ('szBuilderName', c_char * 64),                 # 施工单位全称; builder name
        ('szBuilderID', c_char * 32),                   # 施工单位ID; builder ID
        ('szBuilderType', c_char * 32),                 # 施工单位类型;builder type
        ('szBuilderTypeID', c_char * 8),                # 施工单位类别ID; builder type ID
        ('szPictureID', c_char * 64),                   # 人员照片ID; picture ID
        ('szContractID', c_char * 16),                  # 原合同系统合同编号; contract ID in original contract system
        ('szWorkerTypeID', c_char * 8),                 # 工种ID; worker type ID
        ('szWorkerTypeName', c_char * 32),              # 工种名称; worker type name
        ('bPersonStatus', C_BOOL),                      # 人员状态, TRUE:启用, FALSE:禁用; person status, TRUE:enable, FALSE:forbidden
        ('byReserved', C_BYTE * 256),                   # 保留字节; Reserved
    ]

class NET_MAN_TEMPERATURE_INFO(Structure):
    """
    人员温度信息; Human temperature info
    """
    _fields_ = [
        ('fCurrentTemperature', c_float),               # 人员体温, 参考 EM_HUMAN_TEMPERATURE_UNIT; Human temperature, Please refer to EM_HUMAN_TEMPERATURE_UNIT
        ('emTemperatureUnit', C_ENUM),                  # 温度单位; Temperature unit
        ('bIsOverTemperature', C_BOOL),                 # 是否超温; Is over temperature or not
        ('emTemperatureStatus', C_ENUM),                # 人体测温状态 Refer: EM_HUMAN_TEMPERATURE_STATUS;Human body temperature measurement status Refer: EM_HUMAN_TEMPERATURE_STATUS;
        ('byReserved', C_BYTE * 256),                   # 预留字节; Reserved
    ]

class NET_COMPANION_INFO(Structure):
    """
    人员温度信息; Human temperature info
    """
    _fields_ = [
        ('szCompanionCard', c_char * 32),               # 陪同者卡号; card
        ('szCompanionUserID', c_char * 32),             # 陪同者ID	; user id
        ('szCompanionName', c_char * 120),              # 陪同者姓名; name
        ('szCompanionCompany', c_char * 200),           # 陪同者单位;Company;
        ('byReserved', C_BYTE * 56),                   # 预留字段; Reserved
    ]

class NET_TEST_RESULT(Structure):
    """
    ESD阻值测试结果
    ESD resistance test result
    """
    _fields_ = [
        ('nHandValue', C_UINT),  # k欧姆（阻值单位）;k ohm (resistance unit);
        ('nLeftFootValue', C_UINT),  # k欧姆（阻值单位）;k ohm (resistance unit);
        ('nRightFootValue', C_UINT),  # k欧姆（阻值单位）;k ohm (resistance unit));
        ('emEsdResult', C_ENUM),  # 测试结果 Refer: EM_ESD_RESULT;Test Result Refer: EM_ESD_RESULT;
        ('bReserved', C_BYTE * 128),  # 预留字节;Reserved byte;
    ]

class NET_VACCINE_INFO(Structure):
    """
    新冠疫苗接种信息
    New crown vaccination information
    """
    _fields_ = [
        ('nVaccinateFlag', c_int),  # 是否已接种新冠疫苗, 0: 否, 1: 是;Have you been vaccinated against the new crown vaccine, 0: No, 1: Yes;
        ('szVaccineName', c_char * 128),  # 新冠疫苗名称;New crown vaccine name;
        ('nDateCount', c_int),  # 历史接种日期有效个数;Valid number of historical vaccination dates;
        ('szVaccinateDate', c_char * 256),  # 历史接种日期 (yyyy-MM-dd). 如提供不了时间, 则填"0000-00-00", 表示已接种;Historical vaccination date(yyyy-MM-dd). If you cannot provide the time, fill in "0000-00-00", which means that you have been vaccinated;
        ('nVaccineIntensifyFlag', c_int),   # 是否已接种新冠疫苗加强针, 0: 未知, 1:否  2: 是;Have you been vaccinated Intensify against the new crown vaccine, 0: unKnown, 1:No, 2: Yes;
        ('szReserved', c_char * 1020),  # 保留字节;Reserved;
    ]

class NET_HSJC_INFO(Structure):
    """
    核酸检测信息
    Nucleic acid detection information
    """
    _fields_ = [
        ('szHSJCReportDate', c_char * 32),  # 核酸检测报告日期 (yyyy-MM-dd);Date of nucleic acid test report (yyyy-MM-dd);
        ('nHSJCExpiresIn', c_int),  # 核酸检测报告有效期(天);Nucleic acid test report validity period (days);
        ('nHSJCResult', c_int),  # 核酸检测报告结果, 0: 阳性, 1: 阴性, 2: 未检测, 3: 过期;Nucleic acid test report result, 0: positive, 1: negative, 2: not tested, 3: expired;
        ('szHSJCInstitution', c_char * 256),  # 核酸检测机构;Nucleic acid testing institutions;
        ('szReserved', c_char * 768),  # 保留字节;Reserved;
    ]

class NET_ANTIGEN_INFO(Structure):
    """
    抗原检测信息
    Antigen Test Information
    """
    _fields_ = [
        ('szAntigenReportDate', c_char * 32),  # 抗原检测报告日期;Antigen test report date;
        ('nAntigenStatus', c_int),  # 抗原检测报告结果:  0:阳性 1:阴性 2:未检测 3:过期;Antigen Test Report Result: 0: Positive 1: Negative 2: Not Tested 3: Expired;
        ('nAntigenExpiresIn', c_int),  # 抗原检测报告有效期(单位:天);Validity period of antigen test report (unit: day);
        ('szResvered', c_char * 256),  # 保留字节;Reserved;
    ]

class NET_TRAVEL_INFO(Structure):
    """
    行程码信息
    Travel Info
    """
    _fields_ = [
        ('emTravelCodeColor', C_ENUM),  # 行程码状态 Refer: EM_TRAVEL_CODE_COLOR;Travel Code Color Refer: EM_TRAVEL_CODE_COLOR;
        ('nCityCount', c_int),  # 最近14天经过的城市个数;Number of cities passed in the last 14 days;
        ('szPassingCity', c_char * 2048),  # 最近14天经过的城市名. 按时间顺序排列, 最早经过的城市放第一个;The names of the cities that have passed in the last 14 days. In chronological order, the earliest passing city is placed first;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class DEV_EVENT_ACCESS_CTL_INFO(Structure):
    """
    事件类型 ACCESS_CTL(门禁事件)对应数据块描述信息; Corresponding data description info of event type ACCESS_CTL (Access control info event)
    """
    _fields_ = [
        ('nChannelID', c_int),                  # 门通道号;Door Channel Number
        ('szName', c_char * 128),               # 事件名称;Entrance Guard Name
        ('bReserved1', c_char * 4),             # 字节对齐;Align byte
        ('PTS', c_double),                      # 时间戳(单位是毫秒);Time stamp (Unit:ms)
        ('UTC', NET_TIME_EX),                   # 事件发生的时间;Event occurrence time
        ('nEventID', c_int),                    # 事件ID;Event ID
        ('stuObject', SDK_MSG_OBJECT),          # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),   # 事件对应文件信息;The corresponding file info of the event
        ('emEventType', C_ENUM),                # 门禁事件类型,参考 NET_ACCESS_CTL_EVENT_TYPE; Entrance Guard Event Type,Please refer to NET_ACCESS_CTL_EVENT_TYPE
        ('bStatus', C_BOOL),                    # 刷卡结果,TRUE表示成功,FALSE表示失败;Swing Card Result,True is Success,False is Fail
        ('emCardType', C_ENUM),                 # 卡类型,参考 NET_ACCESSCTLCARD_TYPE;Card Type,Please refer to NET_ACCESSCTLCARD_TYPE
        ('emOpenMethod', C_ENUM),               # 开门方式,参考 NET_ACCESS_DOOROPEN_METHOD;Open The Door Method,Please refer to NET_ACCESS_DOOROPEN_METHOD
        ('szCardNo', c_char * 32),              # 卡号;Card Number
        ('szPwd', c_char * 64),                 # 密码;Password
        ('szReaderID', c_char * 32),            # 门读卡器ID;Reader ID
        ('szUserID', c_char * 64),              # 开门用户;unlock user
        ('szSnapURL', c_char * 128),            # 抓拍照片存储地址;snapshot picture storage address
        ('nErrorCode', c_int),                  # 开门操作码，配合 bStatus 使用;Open door operate code, use with bStatus
                                                    # 0x00 没有错误;no error
                                                    # 0x10 未授权;unauthorized
                                                    # 0x11 卡挂失或注销;card lost or cancelled
                                                    # 0x12 没有该门权限;no door right
                                                    # 0x13 开门模式错误;unlock mode error
                                                    # 0x14 有效期错误;valid period error
                                                    # 0x15 防反潜模式;anti sneak into mode
                                                    # 0x16 胁迫报警未打开;forced alarm not unlocked
                                                    # 0x17 门常闭状态;door NC status
                                                    # 0x18 AB互锁状态;AB lock status
                                                    # 0x19 巡逻卡;patrol card
                                                    # 0x1A 设备处于闯入报警状态;device is under intrusion alarm status
                                                    # 0x20 时间段错误;period error
                                                    # 0x21 假期内开门时间段错误;unlock period error in holiday period
                                                    # 0x30 需要先验证有首卡权限的卡片;first card right check required
                                                    # 0x40 卡片正确,输入密码错误;card correct, input password error
                                                    # 0x41 卡片正确,输入密码超时;card correct, input password timed out
                                                    # 0x42 卡片正确,输入指纹错误;card correct, input fingerprint error
                                                    # 0x43 卡片正确,输入指纹超时;card correct, input fingerprint timed out
                                                    # 0x44 指纹正确,输入密码错误;fingerprint correct, input password error
                                                    # 0x45 指纹正确,输入密码超时;fingerprint correct, input password timed out
                                                    # 0x50 组合开门顺序错误;group unlock sequence error
                                                    # 0x51 组合开门需要继续验证;test required for group unlock
                                                    # 0x60 验证通过,控制台未授权;test passed, control unauthorized
                                                    # 0x61 卡片正确,人脸错误;card correct, input face error
                                                    # 0x62 卡片正确,人脸超时;card correct, input face timed out
                                                    # 0x63 重复进入;repeat enter
                                                    # 0x64 未授权,需要后端平台识别;unauthorized, requiring back-end platform identification
                                                    # 0x65 体温过高;high body temperature
                                                    # 0x66	未戴口罩;no mask
                                                    # 0x67 健康码获取失败;get health code fail
                                                    # 0x68 黄码禁止通行;No Entry because of yellow code
                                                    # 0x69 红码禁止通行;No Entry because of red code
                                                    # 0x6a 健康码无效;health code is invalid
                                                    # 0x6b 绿码验证通过;entry because of green code
                                                    # 0x70 获取健康码信息;get health code info
                                                    # 0x71 校验身份证信息（平台下发对应身份证号的校验结果）;verify citizenId (platform issues the verification result of the corresponding citizenId)
                                                    # 0xA8 未佩戴安全帽（定制）;not wear safety helmet (customized)
        ('nPunchingRecNo', c_int),              # 刷卡记录集中的记录编号;punching record number
        ('nNumbers', c_int),                    # 抓图张数;picture Numbers
        ('byImageIndex', c_ubyte),              # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('byReserved', c_ubyte * 3),            # 字节对齐;Align byte
        ('dwSnapFlagMask', C_DWORD),            # 抓图标志(按位),具体见 NET_RESERVED_COMMON;Snap flag(by bit)0 bit:"*",1 bit:"Timing",2 bit:"Manual",3 bit:"Marked",4 bit:"Event",5 bit:"Mosaic",6 bit:"Cutout"
        ('emAttendanceState', C_ENUM),          # 考勤状态,参考 NET_ATTENDANCESTATE;Attendance state,Please refer to NET_ATTENDANCESTATE
        ('szClassNumber', c_char * 32),         # 班级（定制，废弃，建议用szClassNumberEx）;Class number(customized, depricated, please use szClassNumberEx)
        ('szPhoneNumber', c_char * 16),         # 电话（定制）;Phone number(customized)
        ('szCardName', c_char * 64),            # 卡命名;Card name
        ('uSimilarity', c_uint),                # 人脸识别相似度,范围为0~100;Face recognition similarity,range is 0~100
        ('stuImageInfo', DEV_ACCESS_CTL_IMAGE_INFO * 6),                # 图片信息;Image information
        ('nImageInfoCount', c_int),             # 图片信息数量;Image information count
        ('szCitizenIDNo',  c_char * 20),        # 身份证号;Citizen ID
        ('nGroupID', c_uint),                   # 事件组ID;Event group ID
        ('nCompanionCardCount', c_int),         # 陪同者卡号个数;Companion card count
        ('szCompanionCards', c_char * 6 * 32),  # 陪同者卡号信息（废弃，使用 stuCompanionInfo）;Companion card information
        ('stuCustomWorkerInfo', DEV_ACCESS_CTL_CUSTOM_WORKER_INFO),     # 定制人员信息;custom worker info
        ('emCardState', C_ENUM),                # 当前事件是否为采集卡片,参考 EM_CARD_STATE;Weather to collect cards,Please refer to EM_CARD_STATE
        ('szSN', c_char * 32),                  # 设备序列号;Device serial number
        ('emHatStyle', C_ENUM),                 # 帽子类型,参考EM_HAT_STYLE;hat style,Please refer to EM_HAT_STYLE
        ('emHatColor', C_ENUM),                 # 帽子颜色,参考EM_UNIFIED_COLOR_TYPE ;hat color,Please refer to EM_UNIFIED_COLOR_TYPE
        ('emLiftCallerType', C_ENUM),           # 梯控方式触发者,参考 EM_LIFT_CALLER_TYPE; lift caller type,Please refer to EM_LIFT_CALLER_TYPE
        ('bManTemperature', C_BOOL),            # 人员温度信息是否有效;Whether the information of human body temperature is valid
        ('stuManTemperatureInfo', NET_MAN_TEMPERATURE_INFO),            # 人员温度信息, bManTemperature 为TRUE时有效;Information of human body temperature, It is valid whne bManTemperature is TURE
        ('szCitizenName', c_char * 256),        # 身份证姓名;citizen name
        ('nCompanionInfo', c_int),              # 陪同人员 stuCompanionInfo 个数;stuCompanionInfo's count
        ('stuCompanionInfo', NET_COMPANION_INFO * 12),                  # 陪同人员信息;companion info
        ('emMask', C_ENUM),                     # 口罩状态,参考EM_MASK_STATE_TYPE;mask( EM_MASK_STATE_UNKNOWN、EM_MASK_STATE_NOMASK、EM_MASK_STATE_WEAR is valid ),Please refer to EM_MASK_STATE_TYPE
        ('nFaceIndex', C_UINT),                 # 一人多脸的人脸序号;face index
        ('bClassNumberEx', C_BOOL),             # szClassNumberEx 是否有效，为TRUE时，szClassNumberEx 有效;whether szClassNumberEx is valid. TRUE : szClassNumberEx is valid, else invalid
        ('szClassNumberEx', c_char * 512),      # 班级（定制）;ClassNumber extended(customized)
        ('szDormitoryNo', c_char * 64),         # 宿舍号（定制）;dormitory no (customized)
        ('szStudentNo', c_char * 64),  # 学号（定制）;student no (customized)
        ('emUserType', C_ENUM),                 # 用户类型( EM_USER_TYPE.ORDINARY 至 EM_USER_TYPE.DISABLED 有效 ); user type( from EM_USER_TYPE.ORDINARY to EM_USER_TYPE.DISABLED is valid )
        ('bRealUTC', C_BOOL),                   # RealUTC 是否有效，bRealUTC 为 TRUE 时，用 RealUTC，否则用 UTC 字段; whether RealUTC is valid. when bRealUTC is TRUE, use RealUTC, otherwise use stuTime
        ('RealUTC', NET_TIME_EX),               # 事件发生的时间（标准UTC）; event occur time
        ('szQRCode', c_char * 512),             # 二维码信息; QRcode
        ('szCompanyName', c_char * 200),        # 公司名称; company name
        ('nScore', c_int),                      # 人脸质量评分; face quality score
        ('emFaceCheck', C_ENUM),                # 刷卡开门时，门禁后台校验人脸是否是同一个人(定制) Refer: EM_FACE_CHECK;When swiping the card to open the door, the access control background checks whether the face is the same person (customized) Refer: EM_FACE_CHECK;
        ('emQRCodeIsExpired', C_ENUM),          # 二维码是否过期。默认值0 (北美测温定制) Refer: EM_QRCODE_IS_EXPIRED;Whether the QR code has expired. Default value 0 (customized for temperature measurement in North America) Refer: EM_QRCODE_IS_EXPIRED;
        ('emQRCodeState', C_ENUM),              # 二维码状态(北美测试定制) Refer: EM_QRCODE_STATE;QR code status (North American test customization) Refer: EM_QRCODE_STATE;
        ('stuQRCodeValidTo', NET_TIME),         # 二维码截止日期;QR code deadline;
        ('nBlockId', C_UINT),                   # 上报事件数据序列号从1开始自增;The serial number of the reported event data increases from 1;
        ('szSection', c_char * 64),             # 部门名称;Department name;
        ('szWorkClass', c_char * 256),          # 工作班级;Work class;
        ('emTestItems', C_ENUM),                # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('stuTestResult', NET_TEST_RESULT),     # ESD阻值测试结果;ESD resistance test result;
        ('szDeviceID', c_char * 128),           # 门禁设备编号;Access control equipment number;
        ('szUserUniqueID', c_char * 128),       # 用户唯一表示ID;User unique ID;
        ('bUseCardNameEx', C_BOOL),             # 是否使用卡命名扩展;Whether to use the card name extension;
        ('szCardNameEx', c_char * 128),         # 卡命名扩展;Card name extension;
        ('nHSJCResult', c_int),                 # 核酸检测报告结果  0: 阳性 1: 阴性 2: 未检测 3: 过期;Nucleic acid test report result, 0: positive, 1: negative, 2: not tested, 3: expired;
        ('stuVaccineInfo', NET_VACCINE_INFO),   # 新冠疫苗接种信息;New crown vaccination information;
        ('stuTravelInfo', NET_TRAVEL_INFO),     # 行程码信息;Trip code information;
        ('szTrafficPlate', c_char * 32),        # 车牌;TrafficPlate;
        ('szQRCodeEx', c_char * 2048),          # 国康码项目，用来上传大二维码内容;Guokang code project, used to upload the content of the large QR code;
        ('szReversed', C_BYTE * 2048),          # 预留字节;Reserved byte;
    ]

class SDK_TSECT(Structure):
    """
    时间段结构; Time period structure
    """
    _fields_ = [
        ('bEnable', c_int),         # 当表示录像时间段时,按位表示四个使能,从低位到高位分别表示动检录象、报警录象、普通录象、动检和报警同时发生才录像; Current record period . Bit means the four Enable functions. From the low bit to the high bit:Motion detection record, alarm record and general record, when Motion detection and alarm happened at the same time can record.
                                        # 当表示布撤防时间段时, 表示使能; used in NET_POS_EVENT_LINK, it means enable;
                                        # 当表示推送时间段时, 表示使能：1表示使能，0表示非使能; used in NET_IN_ADD_MOBILE_PUSHER_NOTIFICATION, it means enable：1 means enable, 0 means disable
        ('iBeginHour', c_int),
        ('iBeginMin', c_int),
        ('iBeginSec', c_int),
        ('iEndHour', c_int),
        ('iEndMin', c_int),
        ('iEndSec', c_int),
    ]

class PASSERBY_DB_DUPLICATE_REMOVE_CONFIG_INFO(Structure):
    """
    路人库去重策略配置(选填); Passerby DB duplicate remove strategy config
    """
    _fields_ = [
        ('bEnable', C_DWORD),                   # 使能开关，TRUE：开 FALSE：关; Enable switch, true: on false: off
        ('emDuplicateRemoveType', C_ENUM),      # 路人库去重策略类型,详见 EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE; Passerby DB duplicate remove strategy, see EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE
        ('stuTimeSection', SDK_TSECT * 8 * 6),          # 时间段间隔(emDuplicateRemoveType 为 EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME_SLOT有效); Time period interval(emDuplicateRemoveType by EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME_SLOT Effective)
        ('dwInterval', C_DWORD),                # 时间间隔，单位分钟（emDuplicateRemoveType 为 EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME有效); time interval，Unit minute（emDuplicateRemoveType by EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME Effective）
        ('byReserved1', C_BYTE * 4),            # 字节对齐; byte alaginmen
        ('byReserved', C_BYTE * 256),           # 字节保留; byte reserved
    ]

class NET_PASSERBY_DB_CONFIG_INFO(Structure):
    """
    路人库配置（选填）; passerby  db config
    """
    _fields_ = [
        ('dwCapacity', C_DWORD),                                                        # 路人库最大注册数目; Maximum registration number of passer-by Library
        ('emOverWriteType', C_ENUM),                                                    # 路人库满时覆盖策略,详见 EM_PASSERBY_DB_OVERWRITE_TYPE; Coverage strategy when the passer-by library is full, see EM_PASSERBY_DB_OVERWRITE_TYPE
        ('stuDuplicateRemoveConfigInfo', PASSERBY_DB_DUPLICATE_REMOVE_CONFIG_INFO),     # 路人库去重策略配置(选填); Passerby DB duplicate remove strategy config
        ('dwFileHoldTime', C_DWORD),                                                    # 设置文件保留天数【范围：0~31】单位：天，超过时间将被删除 0：永不过期; Set the file retention days [range: 0-31] unit: days, which will be deleted if the time exceeds 0: never expire
        ('byReserved1', C_BYTE * 4),                                                    # 字节对齐; byte alaginmen
        ('byReserved', C_BYTE * 256),                                                   # 字节保留; byte reserved
    ]

class NET_FACERECONGNITION_GROUP_INFO(Structure):
    """
    人员组信息; staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                    # 结构体大小; Struct size
        ('emFaceDBType', C_ENUM),               # 人员组类型,详见 EM_FACE_DB_TYPE; staff group type, see EM_FACE_DB_TYPE
        ('szGroupId', c_char * 64),             # 人员组ID,唯一标识一组人员(不可修改,添加操作时无效); staff group ID, SN(cannot modify, invalid when adding operation)
        ('szGroupName', c_char * 128),          # 人员组名称; staff operation name
        ('szGroupRemarks', c_char * 256),       # 人员组备注信息; staff group note info
        ('nGroupSize', c_int),                  # 当前组内人员数; current group staff number
        ('nRetSimilarityCount', c_int),         # 实际返回的库相似度阈值个数; rect similarity count
        ('nSimilarity', c_int * 1024),                 # 库相似度阈值，人脸比对高于阈值认为匹配成功; library similarity threshold
        ('nRetChnCount', c_int),                # 实际返回的通道号个数; rect channel count
        ('nChannel', c_int * 1024),                    # 当前组绑定到的视频通道号列表; the list of channels
        ('nFeatureState', C_UINT * 4),              # 人脸组建模状态信息; feature state of the group:
                                                    # [0] - 准备建模的人员数量，不保证一定建模成功; the number of people ready to model, but no guarantee of sucess
                                                    # [1]-建模失败的人员数量，图片不符合算法要求，需要更换图片; the number of people who failed to model, need to change the picture
                                                    # [2]-已建模成功人员数量，数据可用于算法进行人脸识别; the number of people who success to model, the data can be used for face recognition
                                                    # [3]-曾经建模成功，但因算法升级变得不可用的数量，重新建模就可用; once modeling was successful, but became unusable after upgrading, need to abstract
        ('emRegisterDbType', C_ENUM),           # 注册库类型,详见 EM_REGISTER_DB_TYPE; type of register face DB, see EM_REGISTER_DB_TYPE
        ('byReserved1', C_BYTE * 4),                # 字节对齐; byte alagin
        ('stuPasserbyDBConfig', NET_PASSERBY_DB_CONFIG_INFO),       # 路人库配置（选填）; Configuration of pedestrian base (optional)
    ]

class NET_IN_FIND_GROUP_INFO(Structure):
    """
    FindGroupInfo接口输入参数; FindGroupInfo port input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                    # 结构体大小; Struct size
        ('szGroupId', c_char * 64),             # 人员组ID,唯一标识一组人员,为空表示查询全部人员组信息; staff ID, SN staff, as null means search all staff group info
    ]

class NET_OUT_FIND_GROUP_INFO(Structure):
    """
    FindGroupInfo接口输出参数; FindGroupInfo port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('pGroupInfos', POINTER(NET_FACERECONGNITION_GROUP_INFO)),              # 人员组信息,由用户申请空间,大小为sizeof(NET_FACERECONGNITION_GROUP_INFO)*nMaxGroupNum; staff group info , apply space by user, apply to sizeof(NET_FACERECONGNITION_GROUP_INFO)*nMaxGroupNum
        ('nMaxGroupNum', c_int),                                                # 当前申请的数组大小; current applied group size
        ('nRetGroupNum', c_int),                                                # 设备返回的人员组个数; device returned staff group number
    ]

class NET_ADD_FACERECONGNITION_GROUP_INFO(Structure):
    """
    添加人员组信息; add staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('stuGroupInfo', NET_FACERECONGNITION_GROUP_INFO),                      # 人员组信息; staff group info
    ]

class NET_MODIFY_FACERECONGNITION_GROUP_INFO(Structure):
    """
    修改人员组信息; modify staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('stuGroupInfo', NET_FACERECONGNITION_GROUP_INFO),                      # 人员组信息; staff group info
    ]

class NET_DELETE_FACERECONGNITION_GROUP_INFO(Structure):
    """
    删除人员组信息; delete staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                # 结构体大小; Struct size
        ('szGroupId', c_char * 64),                         # 人员组信息; staff group info
    ]

class NET_IN_OPERATE_FACERECONGNITION_GROUP(Structure):
    """
    OperateFaceRecognitionGroup接口输入参数; OperateFaceRecognitionGroup port input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('emOperateType', C_ENUM),                                              # 操作类型,参考 EM_OPERATE_FACERECONGNITION_GROUP_TYPE; operation type, the space application by the user,please refer to EM_OPERATE_FACERECONGNITION_GROUP_TYPE
        ('pOPerateInfo', c_void_p),                                             # 相关操作信息,由用户申请内存，申请大小参照操作类型对应的结构体; operation type, the space application by the user,please refer to the structure of operate type
                                                                                    # 若操作类型为EM_OPERATE_FACERECONGNITION_GROUP_TYPE.ADD,对应结构体为NET_ADD_FACERECONGNITION_GROUP_INFO; if operate type is EM_OPERATE_FACERECONGNITION_GROUP_TYPE.ADD,corresponding to NET_ADD_FACERECONGNITION_GROUP_INFO
                                                                                    # 若操作类型为EM_OPERATE_FACERECONGNITION_GROUP_TYPE.MODIFY,对应结构体为NET_MODIFY_FACERECONGNITION_GROUP_INFO; if operate type is EM_OPERATE_FACERECONGNITION_GROUP_TYPE.MODIFY,corresponding to NET_MODIFY_FACERECONGNITION_GROUP_INFO
                                                                                    # 若操作类型为EM_OPERATE_FACERECONGNITION_GROUP_TYPE.DELETE,对应结构体为NET_DELETE_FACERECONGNITION_GROUP_INFO; if operate type is EM_OPERATE_FACERECONGNITION_GROUP_TYPE.DELETE,corresponding to NET_DELETE_FACERECONGNITION_GROUP_INFO
    ]

class NET_OUT_OPERATE_FACERECONGNITION_GROUP(Structure):
    """
    OperateFaceRecognitionGroup接口输出参数; OperateFaceRecognitionGroup port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; Struct size
        ('szGroupId', c_char * 64),                     # 新增记录的人员组ID,唯一标识一组人员; new record staff group ID, SN staff
    ]

class NET_FACE_MATCH_OPTIONS(Structure):
    """
    人脸匹配信息结构体; Face Matching Options
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; Struct size
        ('nMatchImportant', c_uint),                    # 人员重要等级,1~10,数值越高越重要,(查询重要等级大于等于此等级的人员); Important level 1 to 10 staff, the higher the number the more important (check important level greater than or equal to this level of staff)
        ('emMode', C_ENUM),                             # 人脸比对模式,详见EM_FACE_COMPARE_MODE; Face comparison mode, see EM_FACE_COMPARE_MODE
        ('nAreaNum', c_int),                            # 人脸区域个数; Face the number of regional
        ('szAreas', C_ENUM),                            # 人脸区域组合,emMode为EM_FACE_COMPARE_MODE.AREA时有效,详见EM_FACE_AREA_TYPE; Regional groupings of people face is EM_FACE_COMPARE_MODE.AREA effective when emMode, see EM_FACE_AREA_TYPE
        ('nAccuracy', c_int),                           # 识别精度(取值1~10,随着值增大,检测精度提高,检测速度下降。最小值为1 表示检测速度优先,最大值为10表示检测精度优先。 暂时只对人脸检测有效); Recognition accuracy (ranging from 1 to 10, with the value increases, the detection accuracy is improved, the detection rate of decline. Minimum value of 1 indicates the detection speed priority, the maximum is 10, said detection accuracy preferred. Temporarily valid only for face detection)
        ('nSimilarity', c_int),                         # 相似度(必须大于该相识度才报告;百分比表示,1~100); Similarity (must be greater than the degree of acquaintance before the report; expressed as a percentage, from 1 to 100)
        ('nMaxCandidate', c_int),                       # 报告的最大候选个数(根据相似度进行排序,取相似度最大的候选人数报告); Reported the largest number of candidate (based on similarity to sort candidates to take the maximum number of similarity report)
        ('emQueryMode', C_ENUM),                        # 以图搜图查询模式,详见 EM_FINDPIC_QUERY_MODE; The query mode of searching face database by picture, see EM_FINDPIC_QUERY_MODE
        ('emOrdered', C_ENUM),                          # 以图搜图结果上报排序方式,详见 EM_FINDPIC_QUERY_ORDERED; The sort order of the result about searching face database by picture, see EM_FINDPIC_QUERY_ORDERED
    ]

class NET_FACE_FILTER_CONDTION(Structure):
    """
    查询过滤条件; Query filters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                # 结构体大小; Struct size
        ('stStartTime', NET_TIME),                          # 开始时间; Start time
        ('stEndTime', NET_TIME),                            # 结束时间; End Time
        ('szMachineAddress', c_char * 260),                 # 地点,支持模糊匹配; Place to support fuzzy matching
        ('nRangeNum', c_int),                               # 实际数据库个数; The actual number of database
        ('szRange', C_BYTE * 8),                            # 待查询数据库类型,详见 EM_FACE_DB_TYPE; To query the database type, see EM_FACE_DB_TYPE
        ('emFaceType', C_ENUM),                             # 待查询人脸类型,详见 EM_FACERECOGNITION; Face to query types, see EM_FACERECOGNITION
        ('nGroupIdNum', c_int),                             # 人员组数; staff group
        ('szGroupId', c_char * 128 * 64),                   # 人员组ID; staff group ID
        ('stBirthdayRangeStart', NET_TIME),                 # 生日起始时间; start birthday time
        ('stBirthdayRangeEnd', NET_TIME),                   # 生日结束时间; end birthday time
        ('byAge', C_BYTE * 2),                              # 年龄区间，当byAge[0]=0与byAge[1]=0时，表示查询全年龄; Age range, When byAge[0] is 0 and byAge[1] is 0, it means query all age
        ('byReserved', C_BYTE * 2),                         # 保留字节对齐; Reserved
        ('emEmotion', C_ENUM * 8),                          # 表情条件,详见 EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE; Emotion, see EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('nEmotionNum', c_int),                             # 表情条件的个数; Emotion num
        ('nUIDNum', c_int),                                 # 人员唯一标识数; UID num
        ('szUIDs', c_char * 64 *32),                        # 人员唯一标识列表; UID list
    ]

class NET_IN_STARTFIND_FACERECONGNITION(Structure):
    """
    StartFindFaceRecognition接口输入参数; StartFindFaceRecognitionInterface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('bPersonEnable', C_BOOL),                                              # 人员信息查询条件是否有效; Personnel information query is valid
        ('stPerson', FACERECOGNITION_PERSON_INFO),                              # 人员信息查询条件; Personnel information query
        ('stMatchOptions', NET_FACE_MATCH_OPTIONS),                             # 人脸匹配选项; Face Matching Options
        ('stFilterInfo', NET_FACE_FILTER_CONDTION),                             # 查询过滤条件; Query filters

        # 图片二进制数据
        ('pBuffer', c_char_p),                                                  # 缓冲地址; Buffer address
        ('nBufferLen', c_int),                                                  # 缓冲数据长度; Buffer data length

        ('nChannelID', c_int),                                                  # 通道号; Channel ID
        ('bPersonExEnable', C_BOOL),                                            # 人员信息查询条件是否有效, 并使用扩展结构体; use stPersonInfoEx when bUsePersonInfoEx is true, otherwise use stPersonInfo
        ('stPersonInfoEx', FACERECOGNITION_PERSON_INFOEX),                      # 人员信息扩展; expansion of personnel information
        ('nSmallPicIDNum', c_int),                                              # 小图ID数量; the count of small picture ID
        ('nSmallPicID', c_int * 32),                                            # 小图ID; small picture ID
        ('emObjectType', C_ENUM),                                               # 搜索的目标类型,详见 EM_OBJECT_TYPE; The type of object, see EM_OBJECT_TYPE
    ]

class NET_OUT_STARTFIND_FACERECONGNITION(Structure):
    """
    StartFindFaceRecognition接口输出参数; StartFindFaceRecognitionInterface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                        # 结构体大小; Struct size
        ('nTotalCount', c_int),                                     # 返回的符合查询条件的记录个数,-1表示总条数未生成,要推迟获取; Record number of returns that match the query criteria
        ('lFindHandle', C_LLONG),                                   # 查询句柄; Query handle
        ('nToken', c_int),                                          # 获取到的查询令牌; The search token received
    ]

class NET_UID_CHAR(Structure):
    """
    UID内容; UID contents
    """
    _fields_ = [
        ('szUID', c_char * 32),                                        # UID内容; UID contents
    ]

class NET_IN_OPERATE_FACERECONGNITIONDB(Structure):
    """
    OperateFaceRecognitionDB接口输入参数; OperateFaceRecognitionDBInterface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                    # 结构体大小; Struct size
        ('emOperateType', C_ENUM),                              # 操作类型,见 EM_OPERATE_FACERECONGNITIONDB_TYPE; Type of operation， see EM_OPERATE_FACERECONGNITIONDB_TYPE
        ('stPersonInfo', FACERECOGNITION_PERSON_INFO),          # 人员信息; Personnel information
        ('nUIDNum', C_DWORD),                                   # UID个数; UID amount

        ('stuUIDs', POINTER(NET_UID_CHAR)),                     # 人员唯一标识符,首次由服务端生成,区别于ID字段; Person unique mark. Generated by the client if it is the first time. Different from the ID string.
                                                                    # 由用户申请内存,大小为sizeof(NET_UID_CHAR)*nUIDNum; the space application by the user, apply to sizeof(NET_UID_CHAR)*nUIDNum
        ('pBuffer', c_char_p),                                  # 缓冲地址; Buffer address
        ('nBufferLen', c_int),                                  # 缓冲数据长度; Buffer data length
        ('bUsePersonInfoEx', C_BOOL),                           # 使用人员扩展信息; use stPersonInfoEx when bUsePersonInfoEx is true, otherwise use stPersonInfo
        ('stPersonInfoEx', FACERECOGNITION_PERSON_INFOEX),      # 人员信息扩展; expansion of personnel information
    ]

class NET_OUT_OPERATE_FACERECONGNITIONDB(Structure):
    """
    OperateFaceRecognitionDB接口输出参数; OperateFaceRecognitionDB port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; Struct size
        ('szUID', C_ENUM),                              # 人员唯一标识符, 只有在操作类型为EM_OPERATE_FACERECONGNITIONDB_TYPE.ADD时有效; Person unique mark. it is effective when emOperateType is EM_OPERATE_FACERECONGNITIONDB_TYPE.ADD

        # emOperateType操作类型为ET_FACERECONGNITIONDB_DELETE_BY_UID时使用
        # the following fields are effective when emOperateType is NET_FACERECONGNITIONDB_DELETE_BY_UID
        ('nErrorCodeNum', c_int),                       # 错误码个数; error code number
        ('emErrorCodes', C_ENUM * 512),                 # 错误码; error code
    ]
	
class NET_CUSTOM_INFO(Structure):
    """
    货物通道信息（IPC捷克物流定制）;Cargo Channel Info(IPC Jack Logistics)
    """
    _fields_ = [
        ('nCargoChannelNum', c_int),        # 货物通道个数;Cargo Channel Num
        ('fCoverageRate', c_float*8),       # 货物覆盖率;Cargo Coverage Rate
        ('byReserved', C_BYTE*40),          # 保留字节;Reserved bytes
    ]

class SDK_POLY_POINTS(Structure):
    """
    区域或曲线顶点信息;poly points
    """
    _fields_ =[
        ('nPointNum', c_int),            # 顶点数;point num
        ('stuPoints', SDK_POINT * 20),   # 顶点信息;points info
    ]

class DEV_EVENT_CROSSREGION_INFO(Structure):
    """
    事件类型CROSSREGIONDETECTION(警戒区事件)对应的数据块描述信息;the describe of CROSSREGIONDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),          # 通道号;ChannelId
        ('szName', c_char*128),         # 事件名称;event name
        ('bReserved2', c_char*4),       # 字节对齐;byte alignment
        ('PTS', c_double),              # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),           # 事件发生的时间;the event happen time
        ('nEventID', c_int),            # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info
        ('DetectRegion', SDK_POINT * 20),  # 规则检测区域;rule detect region
        ('nDetectRegionNum', c_int),    # 规则检测区域顶点数;rule detect region's point number
        ('TrackLine', SDK_POINT*20),    # 物体运动轨迹;object moving track
        ('nTrackLineNum', c_int),       # 物体运动轨迹顶点数;object moving track's point number
        ('bEventAction', C_BYTE),       # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('bDirection', C_BYTE),         # 表示入侵方向, 0-进入, 1-离开,2-出现,3-消失;direction, 0-in, 1-out,2-apaer,3-leave
        ('bActionType', C_BYTE),        # 表示检测动作类型,0-出现 1-消失 2-在区域内 3-穿越区域;action type,0-appear 1-disappear 2-in area 3-cross area
        ('byImageIndex', C_BYTE),       # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('dwSnapFlagMask', C_DWORD),    # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout"
                                        # snap flags(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('nSourceIndex', c_int),        # 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', c_char * 260),  # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nOccurrenceCount', c_uint),    # 事件触发累计次数;event trigger times
        ('stuCustom', NET_CUSTOM_INFO), # 货物通道信息;Cargo Channel Info
        ('stuExtensionInfo', NET_EXTENSION_INFO), #扩展信息;Extension info
        ('bReserved', C_BYTE*328),      # 保留字节,留待扩展;reserved
        ('nObjectNum', c_int),          # 检测到的物体个数;Detect object amount
        ('stuObjectIDs', SDK_MSG_OBJECT*16), # 检测到的物体;Detected object
        ('nTrackNum', c_int),               # 轨迹数(与检测到的物体个数对应);Locus amount(Corresponding to the detected object amount.)
        ('stuTrackInfo', SDK_POLY_POINTS*16),  # 轨迹信息(与检测到的物体对应);Locus info(Corresponding to the detected object)
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),    # 智能事件公共信息;intelli comm info
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),         # 全景广角图; scene image
        ('nObjetcHumansNum', c_uint),                    # 检测到人的数量;Number of people detected
        ('stuObjetcHumans', NET_VAOBJECT_NUMMAN * 100), # 检测的到人;People detected
        ('stuVehicle', SDK_MSG_OBJECT),  # 车身信息;vehicle info
        ('emTriggerType', C_ENUM),  # 触发类型,参考EM_TRIGGER_TYPE;Trigger type,refer to EM_TRIGGER_TYPE
        ('nMark', c_int),  # 标记抓拍帧;Used to mark capture frames
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of the video analysis
        ('nFrameSequence', c_int),  # 视频分析帧序号;Video analysis frame number
        ('emCaptureProcess', C_ENUM),  # 抓拍过程,参考EM_CAPTURE_PROCESS_END_TYPE;Capture process,refer to EM_CAPTURE_PROCESS_END_TYPE
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;public info
    ]

class DEV_EVENT_MOVE_INFO(Structure):
    """
    事件类型MOVEDETECTION(移动事件)对应的数据块描述信息;the describe of MOVEDETECTION's data
    """
    _fields_ =[
        ('nChannelID', c_int),  # 通道号;ChannelId
        ('szName', c_char * 128),  # 事件名称;event name
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time
        ('nEventID', c_int),  # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byReserved', C_BYTE * 2), # 对齐;Reserved
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('nDetectRegionNum', c_int),  # 规则检测区域顶点数;detect region point
        ('DetectRegion', SDK_POINT * 20),  # 规则检测区域;detect region
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON
        ('nSourceIndex', c_int),  # 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', c_char*260),    # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nTrackLineNum', c_int),  # 物体运动轨迹顶点数;Object trajectories vertices
        ('stuTrackLine', SDK_POINT * 20),  # 物体运动轨迹;Object trajectories
        ('nOccurrenceCount', c_uint),  # 事件触发累计次数;event trigger accumilated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('stuExtensionInfo', NET_EXTENSION_INFO),  # 扩展信息;Extension info
        ('bReserved', C_BYTE * 272),  # 保留字节,留待扩展;Reserved bytes, leave extended
    ]

class DEV_EVENT_FIGHT_INFO(Structure):
    """
    事件类型FIGHTDETECTION(斗殴事件)对应的数据块描述信息;the describe of FIGHTDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),          # 通道号;ChannelId
        ('szName', c_char*128),         # 事件名称;event name
        ('bReserved1', c_char * 4),     # 字节对齐;byte alignment
        ('PTS', c_double),              # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),           # 事件发生的时间;the event happen time
        ('nEventID', c_int),            # 事件ID;event ID
        ('nObjectNum', c_int),          # 检测到的物体个数;have being detected object number
        ('stuObjectIDs', SDK_MSG_OBJECT*16), # 检测到的物体列表;have being detected object list
        ('stuFileInfo', SDK_EVENT_FILE_INFO),   # 事件对应文件信息;event file info
        ('bEventAction', C_BYTE),       # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byReserved', C_BYTE*2),       # 保留字节;Reserved
        ('byImageIndex', C_BYTE),       # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('nDetectRegionNum', c_int),    # 规则检测区域顶点数;detect region point
        ('DetectRegion', SDK_POINT * 20), # 规则检测区域;detect region
        ('dwSnapFlagMask', C_DWORD),    # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout"
                                        # snap flags(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('nSourceIndex', c_int),        # 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', C_BYTE*260), # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nOccurrenceCount', c_uint),    # 事件触发累计次数;event trigger accumilated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('stuExtensionInfo', NET_EXTENSION_INFO),   # 扩展信息;Extension info
        ('szSourceID', c_char*32),      # 事件关联ID。应用场景是同一个物体或者同一张图片做不同分析，产生的多个事件的SourceID相同
                                        # 缺省时为空字符串，表示无此信息
                                        # 格式：类型 + 时间 + 序列号，其中类型2位，时间14位，序列号5位
                                        # Event source ID. The application scenario is different analysis of the same object or the same picture, resulting in the same sourceid of multiple events
                                        # The default is an empty string, indicating no such information
                                        # Format: type + time + serial number, in which type 2 digits, time 14 digits and serial number 5 digits
        ('bReserved', c_char*328),      # 保留字节,留待扩展;Reserved
    ]

class NET_CROWD_LIST_INFO(Structure):
    """
    全局拥挤人群密度列表(圆形)信息;Crowd list info(circular description)
    """
    _fields_ = [
        ('stuCenterPoint', SDK_POINT),      #中心点坐标,8192坐标系;Center point
        ('nRadiusNum', c_uint),              #半径像素点个数;Radius num
        ('byReserved', C_BYTE*1024),        #保留字节;Reserved
    ]

class NET_CROWD_RECT_LIST_INFO(Structure):
    """
    全局拥挤人群密度列表(矩形)信息;crowd list info(rect description)
    """
    _fields_ = [
        ('stuRectPoint', SDK_POINT*2),      # 矩形的左上角点与右下角点,8192坐标系，表示矩形的人群密度矩形框
        ('byReserved', C_BYTE*32),          # 保留字节;Reserved
    ]

class DEV_EVENT_CROWD_DETECTION_INFO(Structure):
    """
    事件类型 CROWDDETECTION(人群密度检测事件）对应的数据块描述信息;CROWDDETECTION(CrowdDetection)corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),                  # 通道号;Channel ID
        ('nEventID', c_int),                    # 事件ID;Event ID
        ('PTS', c_double),                      # 时间戳(单位是毫秒);Time stamp (Unit:ms)
        ('UTC', NET_TIME_EX),                   # 事件发生的时间;Event occurrence time
        ('nEventAction', c_int),                # 事件动作,1表示持续性事件开始,2表示持续性事件结束;Event action,1 means continues event start,2 means continuous event stop
        ('emAlarmType', C_ENUM),                 # 报警业务类型,参考EM_ALARM_TYPE；Alarm Type,refer to EM_ALARM_TYPE
        ('szName', c_char*128),                 # 事件名称;Event name
        ('nCrowdListNum', c_int),               # 返回的全局拥挤人群密度列表个数 （圆形描述）;Crowd list num (circular description)
        ('nRegionListNum', c_int),              # 返回的人数超限的报警区域ID列表个数;Region list num
        ('stuCrowdList', NET_CROWD_LIST_INFO * 5), # 全局拥挤人群密度列表信息（圆形描述）;Crowd list info(circular description)
        ('stuRegionList', NET_CROWD_LIST_INFO * 8), # 人数超限的报警区域ID列表信息;Region list info
        ('stuExtensionInfo', NET_EXTENSION_INFO),   # 扩展信息; Extension info
        ('nCrowdRectListNum', c_int),               # 返回的全局拥挤人群密度列表个数 (矩形描述);Crowd list num (rect description)
        ('stuCrowdRectList', NET_CROWD_RECT_LIST_INFO * 5), # 全局拥挤人群密度列表信息(矩形描述);Crowd list info(rect description)
        ('nGlobalPeopleNum', c_int),                # 检测区全局总人数;The total number of people
        ('byReserved', C_BYTE*692),                 # 保留扩展字节;Reserved
    ]

class NET_VIDEOSTAT_SUBTOTAL(Structure):
    """
    视频统计小计信息;video statistical subtotal
    """
    _fields_ = [
        ('nTotal', c_int),          #设备运行后人数统计总数;count since device operation
        ('nHour', c_int),           #小时内的总人数;count in the last hour
        ('nToday', c_int),          #当天的总人数, 不可手动清除;count for today
        ('nOSD', c_int),            #统计人数, 用于OSD显示, 可手动清除;count for today, on screen display
        ('reserved', c_char*252),   #保留字节；reserved
    ]

class NET_EXITMAN_STAY_STAT(Structure):
    """
    离开人员的滞留时间信息;The stay time of the peoples left
    """
    _fields_ = [
        ('stuEnterTime', NET_TIME),     #人员进入区域时间;Time to enter the region
        ('stuExitTime', NET_TIME),      #人员离开区域时间;Time to exit the region
        ('reserved', C_BYTE*128),       #保留字节;Reserved
    ]

class NET_VIDEOSTAT_SUMMARY(Structure):
    """
    视频统计摘要信息;Video statistical summary
    """
    _fields_ = [
        ('nChannelID', c_int),          #通道号;Channel ID
        ('szRuleName', c_char*32),      #规则名称;Rule name
        ('stuTime', NET_TIME_EX),       #统计时间;Time of this statistics
        ('stuEnteredSubtotal', NET_VIDEOSTAT_SUBTOTAL), #进入小计;Subtotal for the entered
        ('stuExitedSubtotal', NET_VIDEOSTAT_SUBTOTAL),  #出去小计;Subtotal for the exited
        ('nInsidePeopleNum', c_uint),                    #区域内人数;Total number of people in the area
        ('emRuleType', C_ENUM),                          #规则类型;Rule type,refer to EM_RULE_TYPE
        ('nRetExitManNum', c_int),                      #离开的人数个数;The count of peoples left
        ('stuExitManStayInfo', NET_EXITMAN_STAY_STAT*32), #离开人员的滞留时间信息;The stay time of the peoples left
        ('nPlanID', c_uint),                             #计划ID,仅球机有效,从1开始;Plan ID,Speed Dome use,start from 1
        ('nAreaID', c_uint),                             #区域ID(一个预置点可以对应多个区域ID);Area ID(a preset point can correspond to multiple area IDs)
        ('nCurrentDayInsidePeopleNum', c_uint),          #当天区域内总人数;Total number of people current day in the area
        ('reserved', C_BYTE*1012),                      #保留字节;Reserved
    ]

class NET_IN_ATTACH_VIDEOSTAT_SUM(Structure):
    """
    AttachVideoStatSummary 入参;input param for AttachVideoStatSummary
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小;Structure size
        ('nChannel', c_int),        # 视频通道号;video channel ID
        ('cbVideoStatSum', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_VIDEOSTAT_SUMMARY), C_DWORD, C_LDWORD)), # 视频统计摘要信息回调;video statistical summary callback
        ('dwUser', C_LDWORD),       # 用户数据;user data
    ]

class NET_OUT_ATTACH_VIDEOSTAT_SUM(Structure):
    """
    AttachVideoStatSummary 出参;output param for AttachVideoStatSummary
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size
    ]
class NET_TRAFFIC_FLOWSTAT_INFO_DIR(Structure):
    """
    车辆流量统计车辆行驶方向信息;Vehicle flow statistics lane direction information
    """
    _fields_ = [
        ('emDrivingDir', C_ENUM),              # 行驶方向,参考NET_FLOWSTAT_DIRECTION;Driving direction，refer to NET_FLOWSTAT_DIRECTION
        ('szUpGoing', c_char*16),           # 上行地点;Uplink locations
        ('szDownGoing', c_char*16),         # 下行地点;Go down location
        ('reserved', C_BYTE*32),            # 保留字节;Reserved bytes
    ]
class NET_TRAFFIC_FLOW_STATE(Structure):
    """
    流量状态;
    """
    _fields_ = [
        ('nLane', c_int),           # 车道号;Lane number
        ('dwState', C_DWORD),       # 状态值.若emJamState字段为有效值(不为 JAM_STATUS_UNKNOW) ,则dwState字段无效;State value,if emJamState is valid,then dwState is invalid
                                    # 1- 流量过大;1 - heavy traffic
                                    # 2- 流量过大恢复;2-heavy traffic recovery
                                    # 3- 正常;3-normal;
                                    # 4- 流量过小;4 - Flow is too  little
                                    # 5- 流量过小恢复;5-Traffic too low recovery
        ('dwFlow', C_DWORD),        # 流量值, 单位: 辆;Flow value, units: vehicles
        ('dwPeriod', C_DWORD),      # 流量值对应的统计时间, 单位:分钟。与dwPeriodByMili一起使用;Corresponding statistical time of the flow value,Unit:minute,Used with dwPeriodByMili.
        ('stTrafficFlowDir', NET_TRAFFIC_FLOWSTAT_INFO_DIR),  # 车道方向信息;Lane direction information
        ('nVehicles', c_int),       # 通过车辆总数;Total number of passing vehicles
        ('fAverageSpeed', c_float), # 平均车速,单位km/h;Average speed, unit km / h
        ('fAverageLength', c_float),    # 平均车长,单位米;The average vehicle length, unit meters
        ('fTimeOccupyRatio', c_float),  # 时间占有率,即单位时间内通过断面的车辆所用时间的总和占单位时间的比例;Share of the time , i.e., The ratio of the sum time for the vehicle passing the cross-section  in  the unit  time and per unit time
        ('fSpaceOccupyRatio', c_float), # 空间占有率,即按百分率计量的车辆长度总和除以时间间隔内车辆平均行驶距离;Share of the space ,is the result that the average driving distance intervals vehicle is divided the sum of the length of the vehicle measured by the percentage
        ('fSpaceHeadway', c_float),     # 车头间距,相邻车辆之间的距离,单位米/辆;Headway, the distance between adjacent vehicles in m / vehicle
        ('fTimeHeadway', c_float),      # 车头时距,单位秒/辆;Headway in seconds / vehicle
        ('fDensity', c_float),          # 车辆密度,每公里的车辆数,单位辆/km;Vehicle density, the number of vehicles per kilometer, unit vehicles / km
        ('nOverSpeedVehicles', c_int),  # 超速车辆数;The number of Speeding vehicles
        ('nUnderSpeedVehicles', c_int), # 低速车辆数;The number of low speeding vehicles
        ('nLargeVehicles', c_int),      # 大车交通量(9米<车长<12米),辆/单位时间;Carts traffic (9 m <car length <12 m), vehicle / unit time
        ('nMediumVehicles', c_int),     # 中型车交通量(6米<车长<9米),辆/单位时间;Medium car Traffic 6 m <car length <9 meters, vehicle / unit time
        ('nSmallVehicles', c_int),      # 小车交通量(4米<车长<6米),辆/单位时间;Car Traffic 4 m <car length <6 meters), vehicle / unit time
        ('nMotoVehicles', c_int),       # 摩托交通量(微型车,车长<4米),辆/单位时间;Motorized traffic (mini-car, car length <4 m, vehicle / unit time
        ('nLongVehicles', c_int),       # 超长交通量(车长>=12米),辆/单位时间;long traffic (car length> = 12 m), vehicle / unit time
        ('nVolume', c_int),             # 交通量, 辆/单位时间, 某时间间隔通过车道、道路或其他通道上一点的车辆数,常以1小时计;Traffic, vehicles / unit time, the number of vehicles which pass through the lane, the road and other vehicles, caculated in one hour
        ('nFlowRate', c_int),           # 流率小车当量,辆/小时, 车辆通过车道、道路某一断面或某一路段的当量小时流量;Flow rate of the car, Vehicles / hour, equivalent hours for Vehicle through the lane, a section or a section of the road
        ('nBackOfQueue', c_int),        # 排队长度,单位：米, 从信号交叉口停车线到上游排队车辆末端之间的距离(建议废掉 改用dBackOfQueue下面);Queue length, unit: m, distance from the signalized intersection stop line between the upstream end of the line vehicle)(proposed repeal)
        ('nTravelTime', c_int),         # 旅行时间,单位：秒, 车辆通过某一条道路所用时间。包括所有停车延误;Travel time, unit: second, a road vehicle used by a certain time. Including all parking delays
        ('nDelay', c_int),              # 延误,单位：秒,驾驶员、乘客或行人花费的额外的行程时间;Delay unit: seconds, extra travel time for the driver, passenger or pedestrian spend
        ('byDirection', C_BYTE*16),     # 车道方向, 详见NET_ROAD_DIRECTION;lane direction, see NET_ROAD_DIRECTION
        ('byDirectionNum', C_BYTE),     # 车道行驶方向个数;lane direction quantity
        ('reserved1', C_BYTE*3),        # 字节对齐;text align
        ('emJamState', C_ENUM),            # 道路拥挤状况,详见NET_TRAFFIC_JAM_STATUS，若此字段为有效值(不为 JAM_STATUS_UNKNOW) ,则以此字段为准, dwState字段无效;road jam status, refer to NET_TRAFFIC_JAM_STATUS. if emJamState is valid,then dwState is invalid
        #  按车辆类型统计交通量;Traffic statisitcs according to vehicle type
        ('nPassengerCarVehicles', c_int),  # 客车交通量(辆/单位时间);Passenger vehicle statistics amount (amount/hour)
        ('nLargeTruckVehicles', c_int), # 大货车交通量(辆/单位时间);Large truck statistics amount
        ('nMidTruckVehicles', c_int),   # 中货车交通量(辆/单位时间);Medium truck statistics amount (amount/hour)
        ('nSaloonCarVehicles', c_int),  # 轿车交通量(辆/单位时间);Car statistics amount (amount/hour)
        ('nMicrobusVehicles', c_int),   # 面包车交通量(辆/单位时间);Minivan statistics amount (amount/hour)
        ('nMicroTruckVehicles', c_int), # 小货车交通量(辆/单位时间);Small van statistics amount (amount/hour)
        ('nTricycleVehicles', c_int),   # 三轮车交通量(辆/单位时间);Tricycle statistics amount (amount/hour)
        ('nMotorcycleVehicles', c_int), # 摩托车交通量(辆/单位时间);Motor statistics amount (amount/hour)
        ('nPasserbyVehicles', c_int),   # 行人交通量(辆/单位时间);Pedestrian statistics amount (amount/hour)
        ('emRank', C_ENUM),              # 道路等级,详见NET_TRAFFIC_ROAD_RANK;road rank,refer to NET_TRAFFIC_ROAD_RANK
        ('nState', c_int),              # 流量状态;State value
                                        # 1- 流量过大(拥堵);1 - heavy traffic
                                        # 2- 流量过大恢复(略堵);2-heavy traffic recovery
                                        # 3- 正常;3-normal
                                        # 4- 流量过小(通畅);4 - Flow is too  little
                                        # 5- 流量过小恢复(良好);5-Traffic too low recovery
        ('bOccupyHeadCoil', C_BOOL),    # 车头虚拟线圈是否被占用 TURE表示占用，FALSE表示未占用;indicating whether the head coil is occupyied
        ('bOccupyTailCoil', C_BOOL),    # 车尾虚拟线圈是否被占用 TURE表示占用，FALSE表示未占用;indicating whether the tail coil is occupyied
        ('bStatistics', C_BOOL),        # 流量数据是否有效 TURE表示有效，FALSE表示无效;indicating whether the statistics is valid
        ('nLeftVehicles', c_int),       # 左转车辆总数,单位:分钟;Total nubmer of turn left Vehicles, unit: min
        ('nRightVehicles', c_int),      # 右转车辆总数,单位:分钟;Total number of turn right Vehicles, unit: min
        ('nStraightVehicles', c_int),   # 直行车辆总数,单位:分钟;Total number of straight-head Vehicles,unit: min
        ('nUTurnVehicles', c_int),      # 掉头车辆总数,单位:分钟;Total number of U-turn Vehicles,unit: min
        ('stQueueEnd', SDK_POINT),      # 每个车道的最后一辆车坐标,采用8192坐标系;the last car coordinate in a quene of lane,coordinate value 0~8192
        ('dBackOfQueue', c_double),     # 排队长度,单位：米, 从信号交叉口停车线到上游排队车辆末端之间的距离;Queue length, unit: m, distance from the signalized intersection stop line between the upstream end of the line vehicle
        ('dwPeriodByMili', C_DWORD),    # 流量值的毫秒时间,值不超过60000,和dwPeriod一起使用,流量值总时间:dwPeriod*60*1000+dwPeriodByMili(单位：毫秒);
                                        # Corresponding statistical time of the flow millisecond value,Value is not more than 60000.Used with dwPeriod,statistical total time of the flow value:dwPeriod*60*1000+dwPeriodByMili(Unit:millisecond)
        ('nBusVehicles', c_int),        # 公交车交通量(辆/单位时间);Bus vehicle statistics amount (amount/hour)
        ('nMPVVehicles', c_int),        # MPV交通量(辆/单位时间);MPV vehiclestatistics amount (amount/hour)
        ('nMidPassengerCarVehicles', c_int),  # 中客车交通量(辆/单位时间);midpassenger car vehicle statistics amount (amount/hour)
        ('nMiniCarriageVehicles', c_int),   # 微型轿车交通量(辆/单位时间);mini carriage vehicle statistics amount (amount/hour)
        ('nOilTankTruckVehicles', c_int),   # 油罐车交通量(辆/单位时间);oil tank trunk vehicle statistics amount (amount/hour)
        ('nPickupVehicles', c_int),         # 皮卡车交通量(辆/单位时间);pick up vehicle statistics amount (amount/hour)
        ('nSUVVehicles', c_int),        # SUV交通量(辆/单位时间);SUV vehicle statistics amount (amount/hour)
        ('nSUVorMPVVehicles', c_int),   # SUV或者MPV交通量(辆/单位时间);SUV or MPV vehicle statistics amount (amount/hour)
        ('nTankCarVehicles', c_int),    # 槽罐车交通量(辆/单位时间);tank car vehicle statistics amount (amount/hour)
        ('nUnknownVehicles', c_int),    # 未知车辆交通量(辆/单位时间);unknown vehicle statistics amount (amount/hour)
        ('emCustomFlowAttribute', C_ENUM),   # 车道流量信息属性,详见NET_EM_FLOW_ATTRIBUTE;Flow attribute,refer to NET_EM_FLOW_ATTRIBUTE
        ('nRoadFreeLength', c_int),     # 道路空闲长度，例：如设定路段长度为100米，实际检测到排队长度为30米，那么道路空闲长度就为70米，单位：米;Road Free Length. unit:meter;
        ('emOverflowState', C_ENUM),    # 溢出状态。例：如给当前路段设定允许排队长度阀值，实际排队长度超过阀值后就判定当前时刻该路段有溢出。 Refer: EM_A_NET_EM_OVER_FLOW_STATE;overflow state of car queue. Refer: EM_A_NET_EM_OVER_FLOW_STATE;
        ('reserved', C_BYTE * 712),     # 保留字节;Reserved
    ]

class NET_A_ALARM_TRAFFIC_FLOW_STAT_INFO(Structure):
    """
    交通路口车道统计事件 (对应 ALARM_TRAFFIC_FLOW_STAT)
    Statistical events of traffic intersection Lane (corresponding to ALARM_TRAFFIC_FLOW_STAT)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;0: pulse;
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;Time of event;
        ('nSequence', c_int),  # 序号;Indicates the capture sequence number. 1 indicates the normal end of the capture. 0 indicates the abnormal end of the capture;
        ('nStateNum', c_int),  # 流量状态数量;Number of flow states;
        ('stuStates', NET_TRAFFIC_FLOW_STATE * 8),  # 流量状态, 每个车道对应数组中一个元素;Flow status, each lane corresponds to an element in the array;
        ('nStopVehiclenum', c_int),  # 静止车辆数，当前时刻检测范围内车速小于某个阀值的车辆数，单位：辆;Number of stationary vehicles: the number of vehicles whose speed is less than a certain threshold within the detection range at the current time, unit: vehicle;
        ('nDetectionAreaVehicleNum', c_int),  # 车辆总数，当前时刻检测范围内检测到的所有车道内的车辆总数，单位：辆;Total number of vehicles: the total number of vehicles in all lanes detected within the detection range at the current time, unit: vehicles;
        ('szReserverd', c_char * 1024),  # 保留字节;Reserved;
    ]

class DEV_EVENT_TRAFFIC_FLOW_STATE(Structure):
    """
    事件类型 FLOWSTATE(交通流量事件)对应数据块描述信息;FLOWSTATE (Corresponding data block description)
    """
    _fields_ = [
        ('nChannelID', c_int),          # 通道号;Channel number
        ('szName', c_char*128),         # 事件名称;Event name
        ('nRuleID', c_uint),            # 规则编号, 用于标示哪个规则触发的事件，缺省时默认为0;Rule ID, used to indicate which rule triggers the event.
        ('bReserved1', c_char*4),       # 字节对齐;Byte alignment
        ('PTS', C_DWORD),               # 时间戳(单位是毫秒);Timestamp (in milliseconds)
        ('UTC', NET_TIME_EX),           # 事件发生的时间;Time for the event occurred
        ('nEventID', c_int),            # 事件ID;Event ID
        ('nSequence', c_int),           # 序号;No.
        ('nStateNum', c_int),           # 流量状态数量;the number of traffic state
        ('stuStates', NET_TRAFFIC_FLOW_STATE*8),  # 流量状态, 每个车道对应数组中一个元素;Flow state, each lane corresponding to an element in the array
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('bReserved', C_BYTE*892),      # 保留字节;Reserved bytes
    ]

class NET_IN_REALPLAY_BY_DATA_TYPE(Structure):
    """
    开始实时监视并指定回调数据格式入参;RealPlay By Stream Data Type (in param)
    """
    _fields_ = [
        ('dwSize', C_DWORD),                        # 结构体大小; struct size
        ('nChannelID', c_int),                      # 通道编号; channel id
        ('hWnd', C_LLONG),                          # 窗口句柄; play handle
        ('rType', C_ENUM),                          # 码流类型,详见SDK_RealPlayType; real play stream type,refer to SDK_RealPlayType
        ('cbRealData', CB_FUNCTYPE(None, C_LLONG, C_DWORD, POINTER(c_byte), C_DWORD, C_LLONG, C_LDWORD)),        # 数据回调函数,对应SDK_Callback的fRealDataCallBackEx; realplay data callback function prototype，corresponding to SDK_Callback's fRealDataCallBackEx
        ('emDataType', C_ENUM),                     # 回调的数据类型,详见EM_REAL_DATA_TYPE; stream data type,refer to EM_REAL_DATA_TYPE
        ('dwUser', C_LDWORD),                       # 用户数据; data user
        ('szSaveFileName', c_char_p),               # 转换后的文件名; file name to convert
        ('cbRealDataEx', CB_FUNCTYPE(None, C_LLONG, C_DWORD, POINTER(c_byte), C_DWORD, C_LLONG, C_LDWORD)),     # 数据回调函数-扩展,对应SDK_Callback的fRealDataCallBackEx2; realplay data callback function prototype-ex，corresponding to SDK_Callback's fRealDataCallBackEx2
        ('emAudioType', C_ENUM),                    # 音频格式,详见EM_AUDIO_DATA_TYPE; audio data type, refer to EM_AUDIO_DATA_TYPE
    ]

class NET_OUT_REALPLAY_BY_DATA_TYPE(Structure):
    """
    开始实时监视并指定回调数据格式出参;RealPlay By Stream Data Type (out param)
    """
    _fields_ = [
        ('dwSize', C_DWORD),                        # 结构体大小; struct size
    ]

class NET_DATA_CALL_BACK_TIME(Structure):
    """
    回调数据时间信息; callback data time information
    """
    _fields_ = [
        ('dwYear', C_DWORD),    # 年; year
        ('dwMonth', C_DWORD),   # 月; month
        ('dwDay', C_DWORD),     # 日; day
        ('dwHour', C_DWORD),    # 时; hour
        ('dwMinute', C_DWORD),  # 分; minute
        ('dwSecond', C_DWORD),  # 秒; second
        ('dwMillisecond', C_DWORD), # 毫秒; millisecond
        ('dwPTS', C_DWORD),     # pts时间戳; pts timestamp
        ('dwDTS', C_DWORD),     # dts时间戳; dts timestamp
        ('dwReserved', C_DWORD * 3),    # 预留字段; Reserved bytes
    ]

class NET_DATA_CALL_BACK_INFO(Structure):
    """
    回调数据信息; callback data information
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size
        ('dwDataType', C_DWORD),    # 数据类型; data type
        ('pBuffer', c_char_p),      # 数据; data
        ('dwBufSize', C_DWORD),     # 数据长度; data size
        ('stuTime', NET_DATA_CALL_BACK_TIME), # 时间戳; timestamp
        ('emFramType', C_ENUM),     # 帧类型 具体参考EM_DATA_CALL_BACK_FRAM_TYPE; Frame Type Specific Reference EM_DATA_CALL_BACK_FRAM_TYPE
        ('emFramSubType', C_ENUM),  # 帧子类型 具体参考EM_DATA_CALL_BACK_FRAM_SUB_TYPE; Frame Subtype Specific Reference EM_DATA_CALL_BACK_FRAM_SUB_TYPE
    ]

class NET_IN_PLAYBACK_BY_DATA_TYPE(Structure):
    """
    开始回放并指定回调数据格式入参;Start playback and specify the callback data format Input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size
        ('nChannelID', c_int),  # 通道编号; channel id
        ('stStartTime', NET_TIME),  # 开始时间; start time
        ('stStopTime', NET_TIME),   # 结束时间; end time
        ('hWnd', C_LLONG),  # 窗口句柄; play handle
        ('cbDownLoadPos', CB_FUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, C_LDWORD)),  # 进度回调;progress callback
        ('dwPosUser', C_LDWORD),    # 进度回调用户信息; Progress callback user information
        ('fDownLoadDataCallBack', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(c_ubyte), C_DWORD, C_LDWORD)),    # 数据回调; data callback
        ('emDataType', C_ENUM),  # 回调的数据类型,详见EM_REAL_DATA_TYPE; stream data type,refer to EM_REAL_DATA_TYPE
        ('dwDataUser', C_LDWORD),   # 数据回调用户信息; Data callback user information
        ('nPlayDirection', c_int),  # 播放方向, 0:正放; 1:倒放; Play direction, 0: play forward; 1: play backward
        ('emAudioType', C_ENUM),  # 音频格式,详见EM_AUDIO_DATA_TYPE; audio data type, refer to EM_AUDIO_DATA_TYPE
        ('fDownLoadDataCallBackEx', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_DATA_CALL_BACK_INFO), C_LDWORD)) # 数据回调（扩展带时间戳，帧类型）; Data callback (extended with timestamp, frame type)
    ]

class NET_OUT_PLAYBACK_BY_DATA_TYPE(Structure):
    """
    开始回放并指定回调数据格式出参;Start playback and specify the callback data format Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size
    ]

class NET_IN_DOWNLOAD_BY_DATA_TYPE(Structure):
    """
    开始下载并指定回调数据格式 入参; Start the download and specify the callback data format Input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小; struct size
        ('nChannelID', c_int),      # 通道编号; channel id
        ('emRecordType', C_ENUM),   # 录像类型 参考EM_QUERY_RECORD_TYPE; record type, refer to EM_QUERY_RECORD_TYPE
        ('szSavedFileName', c_char_p),  # 下载的文件路径; Downloaded file path
        ('stStartTime', NET_TIME),  # 开始时间; start time
        ('stStopTime', NET_TIME),  # 结束时间; end time
        ('cbDownLoadPos', CB_FUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, c_int, NET_RECORDFILE_INFO, C_LDWORD)),  # 进度回调;progress callback
        ('dwPosUser', C_LDWORD),  # 进度回调用户信息; Progress callback user information
        ('fDownLoadDataCallBack', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(c_ubyte), C_DWORD, C_LDWORD)),   # 数据回调; data callback
        ('emDataType', C_ENUM),  # 回调的数据类型,详见EM_REAL_DATA_TYPE; stream data type,refer to EM_REAL_DATA_TYPE
        ('dwDataUser', C_LDWORD),  # 数据回调用户信息; Data callback user information
        ('emAudioType', C_ENUM),  # 音频格式,详见EM_AUDIO_DATA_TYPE; audio data type, refer to EM_AUDIO_DATA_TYPE
    ]

class NET_OUT_DOWNLOAD_BY_DATA_TYPE(Structure):
    """
        开始下载并指定回调数据格式 出参; Start the download and specify the callback data format Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size
    ]

class NET_CTRL_RAINBRUSH_MOVEONCE(Structure):
    """
    雨刷来回刷一次,雨刷模式配置为手动模式时有效(对应命令CtrlType.RAINBRUSH_MOVEONCE); (corresponding to CtrlType.RAINBRUSH_MOVEONCE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannel', c_int),  # 表示雨刷的索引; Rain-brush channel;
    ]

class NET_CTRL_RAINBRUSH_MOVECONTINUOUSLY(Structure):
    """
    雨刷来回循环刷,雨刷模式配置为手动模式时有效(对应命令 CtrlType.RAINBRUSH_MOVECONTINUOUSLY); (corresponding to CtrlType.RAINBRUSH_MOVECONTINUOUSLY)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannel', c_int),  # 表示雨刷的索引; Rain-brush channel;
        ('nInterval', C_UINT),  # 雨刷间隔; Interval;
    ]

class NET_CTRL_RAINBRUSH_STOPMOVE(Structure):
    """
    雨刷停止刷,雨刷模式配置为手动模式时有效(对应命令 CtrlType.RAINBRUSH_STOPMOVE); (corresponding to CtrlType.RAINBRUSH_STOPMOVE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannel', c_int),  # 表示雨刷的索引; Rain-brush channel;
    ]

class NET_ANGEL_RANGE(Structure):
    """
    人脸抓拍角度范围; Face capture angle range
    """
    _fields_ = [
        ('nMin', c_int),    # 角度最小值; Minimum angle;
        ('nMax', c_int),    # 角度最大值; Maximum angle;
    ]

class NET_EVENT_WHOLE_FACE_INFO(Structure):
    """
    人脸抓拍角度范围; Face capture angle range
    """
    _fields_ = [
        ('stuFaceCaptureAngle', NET_EULER_ANGLE),       # 人脸在抓拍图片中的角度信息, nPitch:抬头低头的俯仰角, nYaw左右转头的偏航角, nRoll头在平面内左偏右偏的翻滚角,角度值取值范围[-90,90], 三个角度值都为999表示此角度信息无效; The angle information of the face in the captured image, nPitch: the pitch angle of the head up and down, the yaw angle of the nYaw left and right head, and the roll angle of the nRoll head in the plane left and right,Angle value range [-90,90], all three angle values are 999, indicating that the angle information is invalid;
        ('stuAngelRange', NET_ANGEL_RANGE * 3),         # 人脸抓拍角度范围(角度最小值,最大值),  三个角度依次分别是Pitch抬头低头,仰俯角;yaw是左右转头,偏航角;Roll是头在平面内左偏右偏，翻滚角; Face capture angle range (minimum angle, maximum angle), the three angles are Pitch up and down, pitch and pitch angles; yaw is left and right turn head, yaw angle; Roll is head left and right in the plane, roll angle;
        ('byReserved', C_BYTE * 256),                   # 保留字段; Reserved
    ]

class ALARM_EVENT_FACE_INFO(Structure):
    """
    人脸检测事件(对应事件 DH_EVENT_FACE_DETECTION); Human face detect event( corresponding to event DH_EVENT_FACE_DETECTION)
    """
    _fields_ = [
        ('dwSize', C_DWORD),							# 结构体大小;Structure size
        ('nChannelID', c_int),                          # 通道号; Channel No.;
        ('PTS', c_double),                              # 时间戳(单位是毫秒); Time stamp (Unit is ms);
        ('UTC', NET_TIME_EX),                           # 事件发生的时间; Event occurrence time;
        ('nEventID', c_int),                            # 事件ID; Event ID;
        ('nEventAction', c_int),                        # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;; Event operation. 0=pulse event.1=continues event begin. 2=continuous event stop;
        ('nFaceCount', c_int),                          # 人脸个数; face count
        ('stuFaces', NET_EVENT_WHOLE_FACE_INFO * 10),   # 人脸信息; face info
        ('nPresetID', C_UINT),                          # 事件触发的预置点号, 从1开始; Preset point number triggered by event, starting from 1
    ]
	
class AV_CFG_Color(Structure):
    """
    颜色;Color
    """
    _fields_ = [
        ('nStructSize', c_int), # 结构体大小;Structure size
        ('nRed', c_int), # 红; Red;
        ('nGreen', c_int), # 绿; Green;
        ('nBlue', c_int), # 蓝; Blue;
        ('nAlpha', c_int), # 透明; Transparent;
    ]

class AV_CFG_Rect(Structure):
    """
    区域;Zone
    """
    _fields_ = [
        ('nStructSize', c_int), # 结构体大小;Structure size
        ('nLeft', c_int), # 左; Left
        ('nTop', c_int), # 顶; Top
        ('nRight', c_int), # 右; Right
        ('nBottom', c_int),  # 底; Bottom
    ]

class AV_CFG_VideoWidgetChannelTitle(Structure):
    """
    编码物件-通道标题;Encode widget-channel title
    """
    _fields_ = [
        ('nStructSize', c_int),   # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Add to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191, 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点; Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
    ]

class AV_CFG_VideoWidgetTimeTitle(Structure):
    """
    编码物件-时间标题;Encode widget-Time title
    """
    _fields_ = [
        ('nStructSize', c_int),     # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Overlay to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191, 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点; Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('bShowWeek', C_BOOL), # 是否显示星期; Display week or not;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
    ]

class AV_CFG_VideoWidgetCover(Structure):
    """
    编码物件-区域覆盖配置;Encode widget-Privacy mask setup
    """
    _fields_ = [
        ('nStructSize', c_int),    # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Overlay to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191; Zone. The coordinates value ranges from 0 to 8191;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
    ]

class AV_CFG_VideoWidgetCustomTitle(Structure):
    """
    编码物件-自定义标题;Encode widget-Self-defined title
    """
    _fields_ = [
        ('nStructSize', c_int),    # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Overlay to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191, 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点; Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('szText', c_char * 1024), # 标题内容; Title contents;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
        ('szType', c_char * 32), # 标题类型 "Rtinfo" 实时刻录信息 "Custom" 自定义叠加、温湿度叠加 "Title" :片头信息 "Check" 校验码,地理信息 "Geography" ATM卡号信息 "ATMCardInfo" 摄像机编号 "CameraID"; Title type "Rtinfo" real-time recorder information, "Custom" custom overlay, temperature and humidity overlay, "Title": credit information "Check" check code,Geography info "Geography" ATM card info "ATMCardInfo" Camera ID "CameraID";
        ('emTextAlign', C_ENUM), # 标题对齐方式,参考枚举EM_TITLE_TEXT_ALIGN; Title alignment method,Please refer to EM_TITLE_TEXT_ALIGN;
    ]

class AV_CFG_VideoWidgetSensorInfo_Description(Structure):
    """
    编码物件-叠加传感器信息-叠加内容描述;Encoding object - overlay sensor information - superimposed Description
    """
    _fields_ = [
        ('nStructSize', c_int),   # 结构体大小;Structure size
        ('nSensorID', c_int), # 需要描述的传感器的ID(即模拟量报警通道号); Need to describe the sensor ID (analog alarm channel number);
        ('szDevID', c_char * 32), # 设备ID; 璁惧ID;
        ('szPointID', c_char * 32), # 测点ID; 娴嬬偣ID;
        ('szText', c_char * 256), # 需要叠加的内容; 闇€瑕佸彔鍔犵殑鍐呭;
    ]

class AV_CFG_VideoWidgetSensorInfo(Structure):
    """
    编码物件-叠加传感器信息;Encoding object - overlay sensor information
    """
    _fields_ = [
        ('nStructSize', c_int),     # 结构体大小;Structure size
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay the preview video;
        ('bEncodeBlend', C_BOOL), # 叠加到主码流视频编码; Stack to the main stream of video coding;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191; Area, coordinates ranging from 0 to 8191;
        ('nDescriptionNum', c_int), # 叠加区域描述数目; The Description number of stacking area;
        ('stuDescription', AV_CFG_VideoWidgetSensorInfo_Description * 4), # 叠加区域描述信息; Stacking area description information;
    ]

class AV_CFG_VideoWidget(Structure):
    """
    视频编码物件配置;Video encode widget config
    """
    _fields_ = [
        ('nStructSize', c_int),  # 结构体大小;Structure size
        ('stuChannelTitle', AV_CFG_VideoWidgetChannelTitle), # 通道标题; Channel title;
        ('stuTimeTitle', AV_CFG_VideoWidgetTimeTitle), # 时间标题; Time title;
        ('nConverNum', c_int), # 区域覆盖数量; Privacy mask zone amount;
        ('stuCovers', AV_CFG_VideoWidgetCover * 16), # 覆盖区域; Privacy mask zone;
        ('nCustomTitleNum', c_int), # 自定义标题数量; Self-defined title amount;
        ('stuCustomTitle', AV_CFG_VideoWidgetCustomTitle * 8), # 自定义标题; Self-defined title;
        ('nSensorInfo', c_int), # 传感器信息叠加区域数目; The number of sensor information overlay area;
        ('stuSensorInfo', AV_CFG_VideoWidgetSensorInfo * 2), # 传感器信息叠加区域信息; Sensor information overlay zone information;
        ('fFontSizeScale', c_double), # 叠加字体大小放大比例,当fFontSizeScale≠0时,nFontSize不起作用,当fFontSizeScale=0时,nFontSize起作用,设备默认fFontSizeScale=1.0,如果需要修改倍数，修改该值,如果需要按照像素设置，则置该值为0，nFontSize的值生效; overlay font size scale;
        ('nFontSize', c_int), # 叠加到主码流上的全局字体大小,单位 px.,和fFontSizeScale共同作用; global font size overlay to main stream, unit px.;
        ('nFontSizeExtra1', c_int), # 叠加到辅码流1上的全局字体大小,单位 px; global font size overlay to sub stream 1, unit px.;
        ('nFontSizeExtra2', c_int), # 叠加到辅码流2上的全局字体大小,单位 px; global font size overlay to sub stream 2, unit px.;
        ('nFontSizeExtra3', c_int), # 叠加到辅码流3上的全局字体大小,单位 px; global font size overlay to sub stream 3, unit px.;
        ('nFontSizeSnapshot', c_int), # 叠加到抓图流上的全局字体大小, 单位 px; global font size overlay to snapshot stream, unit px;
        ('nFontSizeMergeSnapshot', c_int), # 叠加到抓图流上合成图片的字体大小,单位 px; combination picture overlay to snapshot stream, unit px;
        ('emFontSolutionSnapshot', C_ENUM), # 叠加到抓图流上的字体方案,参考枚举EM_FONT_SOLUTION; combination picture overlay to font solution,Please refer to EM_FONT_SOLUTION;
    ]

class NET_ENCODE_CHANNELTITLE_INFO(Structure):
    """
    通道名称配置;channel title info
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小;Structure size
        ('szChannelName', c_char * 256),   # 通道名称;Channel name
    ]
	
class SDK_CPU_INFO(Structure):
    """
    CPU信息;CPU info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('nUsage', c_int), # CPU利用率; CPU usage;
    ]

class SDK_CPU_STATUS(Structure):
    """
    CPU状态;CPU status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # CPU数量; CPU amount;
        ('stuCPUs', SDK_CPU_INFO * 16), # CPU信息; CPU info;
    ]

class SDK_MEMORY_INFO(Structure):
    """
    内存信息;Memory info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('dwTotal', C_DWORD), # 总内存, M; Total memory, M;
        ('dwFree', C_DWORD), # 剩余内存, M; Free memory, M;
    ]

class SDK_MEMORY_STATUS(Structure):
    """
    内存状态;Memory status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('stuMemory', SDK_MEMORY_INFO), # 内存信息; Memory info;
    ]

class SDK_FAN_INFO(Structure):
    """
    风扇信息;Fan info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('szName', c_char * 64), # 名称; Name;
        ('nSpeed', C_DWORD), # 速度; Speed;
    ]

class SDK_FAN_STATUS(Structure):
    """
    风扇状态;Fan status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # 风扇数量; Fan amount;
        ('stuFans', SDK_FAN_INFO * 16), # 风扇状态; Fan status;
    ]

class SDK_POWER_INFO(Structure):
    """
    电源信息;Power info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bPowerOn', C_BOOL), # 电源状态, 0-关闭, 1-打开, 2-打开但有故障; Power is on or not;
        ('emCurrentState', C_ENUM), # 电源电流状态,参考枚举EM_CURRENT_STATE_TYPE; power current status,Please refer to EM_CURRENT_STATE_TYPE;
        ('emVoltageState', C_ENUM), # 电源电压状态,参考枚举EM_VOLTAGE_STATE_TYPE; power voltage status,Please refer to EM_VOLTAGE_STATE_TYPE;
    ]

class SDK_BATTERY_INFO(Structure):
    """
    电池信息;Battery Information
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('nPercent', c_int), # 电池容量百分比; Battery Capacity Percentage;
        ('bCharging', C_BOOL), # 是否正在充电; Whether real charging;
        ('emExistState', C_ENUM), # 电池在位状态,参考枚举EM_BATTERY_EXIST_STATE; battery in-place status,Please refer to EM_BATTERY_EXIST_STATE;
        ('emState', C_ENUM), # 电池电量状态,参考枚举EM_BATTERY_STATE; battery power status,Please refer to EM_BATTERY_STATE;
        ('fVoltage', c_float), # 电池电压; battery voltage;
    ]

class SDK_POWER_STATUS(Structure):
    """
    电源状态;Power status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # 电源数量; Power amount;
        ('stuPowers', SDK_POWER_INFO * 16), # 电源状态; Power status;
        ('nBatteryNum', c_int), # 电池数量; Battery Number;
        ('stuBatteries', SDK_BATTERY_INFO * 16), # 电池状态; Battery Status;
    ]

class SDK_TEMPERATURE_INFO(Structure):
    """
    温度信息;Temperature info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('szName', c_char * 64), # 传感器名称; Sensor name;
        ('fTemperature', c_float), # 温度; Temperature;
    ]

class SDK_TEMPERATURE_STATUS(Structure):
    """
    温度状态;Temperature status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # 温度数量; Temperature amount;
        ('stuTemps', SDK_TEMPERATURE_INFO * 256), # 温度信息; Temperature info;
    ]

class SDK_SYSTEM_STATUS(Structure):
    """
    系统状态;System status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('pstuCPU', POINTER(SDK_CPU_STATUS)), # CPU状态; CPU status;
        ('pstuMemory', POINTER(SDK_MEMORY_STATUS)), # 内存状态; Memory status;
        ('pstuFan', POINTER(SDK_FAN_STATUS)), # 风扇状态; Fan status;
        ('pstuPower', POINTER(SDK_POWER_STATUS)), # 电源状态; Power status;
        ('pstuTemp', POINTER(SDK_TEMPERATURE_STATUS)), # 温度状态; Temperature status;
    ]
	
class NET_DEV_DISKSTATE(Structure):
    """
    硬盘信息;HDD informaiton
    """
    _fields_ = [
        ('dwVolume', C_DWORD), # 硬盘的容量, 单位MB(B表示字节); HDD capacity;
        ('dwFreeSpace', C_DWORD), # 硬盘的剩余空间, 单位MB(B表示字节); HDD free space;
        ('dwStatus', C_BYTE),   # 高四位的值表示硬盘类型,具体见枚举类型EM_DISK_TYPE；低四位的值表示硬盘的状态,0-休眠,1-活动,2-故障等；将DWORD拆成四个BYTE;
                                # higher 4 byte instruct hdd type, see the enum struct EM_DISK_TYPE; lower four byte instruct HDD status,0-hiberation,1-active,2-malfucntion and etc.;Devide DWORD into four BYTE;
        ('bDiskNum', C_BYTE), # 硬盘号; HDD number;
        ('bSubareaNum', C_BYTE), # 分区号; Subarea number;
        ('bSignal', C_BYTE), # 标识,0为本地 1为远程; Symbol. 0:local. 1:remote;
    ]

class SDK_HARDDISK_STATE(Structure):
    """
    设备硬盘信息;Device HDD informaiton
    """
    _fields_ = [
        ('dwDiskNum', C_DWORD), # 个数; Amount;
        ('stDisks', NET_DEV_DISKSTATE * 256), # 硬盘或分区信息; HDD or subarea information;
    ]

class NET_VIDEOIN_EXPOSURE_NORMAL_INFO(Structure):
    """
    通用曝光属性配置;normal exposure config of video input
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('emCfgType', C_ENUM), # 配置类型，获取和设置时都要指定,参考枚举NET_EM_CONFIG_TYPE; config type, you need set the value wether set or get config,Please refer to NET_EM_CONFIG_TYPE;
        ('emExposureMode', C_ENUM), # 曝光模式,参考枚举NET_EM_EXPOSURE_MODE; exposure mode,Please refer to NET_EM_EXPOSURE_MODE;
        ('nAntiFlicker', c_int), # 防闪烁0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁; anti flicker 0-Outdoor 1-50Hz 2-60Hz;
        ('nCompensation', c_int), # 曝光补偿0-100; Compensation 0-100;
        ('nGain', c_int), # 增益值; gain value 0-100;
        ('nGainMin', c_int), # 增益下限0-100; the min value of Gain 0-100;
        ('nGainMax', c_int), # 增益上限0-100; the max value of gain 0-100;
        ('nExposureIris', c_int), # 光圈值，模式为光圈优先时有效，0-100; the value of iris(0-100), it is valid when mode is NET_EM_EXPOSURE_APERTUREFIRST;
        ('dbExposureValue1', c_double), # 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; Auto exposure value min limit or manual axposure custom, unit is millisecond (0.1ms~80ms).;
        ('dbExposureValue2', c_double), # 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms，且必须不小于"ExposureValue1"取值; Auto exposure time max limit, unit is millisecond (0.1ms~80ms);
        ('bIrisAuto', C_BOOL), # 自动光圈使能; Automatic aperture enabling;
        ('emDoubleExposure', C_ENUM), # 双快门的支持类型,参考枚举EM_DOUBLE_EXPOSURE_TYPE; Support Type of Double Shutter,Please refer to EM_DOUBLE_EXPOSURE_TYPE;
    ]

class NET_IN_GET_DISTANCE_RES(Structure):
    """
    CLIENT_GetDistanceRes 接口输入参数; Input param of CLIENT_GetDistanceRes
    """
    _fields_ = [
        ('dwSize', C_DWORD), # 结构体大小; struct size;
        ('nChannel', C_UINT), # 通道; Channel;
    ]

class NET_OUT_GET_DISTANCE_RES(Structure):
    """
    GetDistanceRes 接口输出参数; Output param of GetDistanceRes
    """
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小; struct size;
        ('nDistance', C_UINT),          # 目标距离，单位米; Target Distance, Unit Meter;
        ('nOverTimeStatus', c_int),     # 超时状态（0,超时 1未超时）; Timeout state (0, timeout 1 not timeout);
        ('emStatus', C_ENUM),           # 结果状态,参考枚举EM_GET_DISTANCE_RES_STATUS; Result status,Please refer to EM_GET_DISTANCE_RES_STATUS;
    ]

class CFG_NEARLIGHT_INFO(Structure):
    """
    近光灯信息; low beam info
    """
    _fields_ = [
        ('bEnable', C_BOOL), # 是否使能，TRUE使能，FALSE不使能; Whether enabled, TRUE enabled, FALSE does not enable;
        ('dwLightPercent', C_DWORD), # 灯光亮度百分比值(0~100); Light brightness percentage (0~100);
        ('dwAnglePercent', C_DWORD), # 灯光角度百分比值(0~100); Lighting angle in percentage (0~100);
    ]

class CFG_FARLIGHT_INFO(Structure):
    """
    远光灯信息; High beam information
    """
    _fields_ = [
        ('bEnable', C_BOOL), # 是否使能，TRUE使能，FALSE不使能; Whether enabled, TRUE enabled, FALSE does not enable;
        ('dwLightPercent', C_DWORD), # 灯光亮度百分比值(0~100); Light brightness percentage (0~100);
        ('dwAnglePercent', C_DWORD), # 灯光角度百分比值(0~100); Lighting angle in percentage (0~100);
    ]

class CFG_LIGHTING_DETAIL(Structure):
    """
    灯光设置详情; Light setting details
    """
    _fields_ = [
        ('nCorrection', c_int),  # 灯光补偿 (0~4) 倍率优先时有效; Light compensation (0 ~ 4) effective ratio is preferred;
        ('nSensitive', c_int),  # 灯光灵敏度(0~5)倍率优先时有效，默认为3; Light sensitivity (0 ~ 5) are effective ratio is preferred, the default value is 3 EM_CFG_LIGHTING_MODE emMode;  Light pattern;
        ('emMode', C_ENUM),  # 灯光模式,参考枚举EM_CFG_LIGHTING_MODE; Light mode,Please refer to EM_CFG_LIGHTING_MODE;
        ('nNearLight', c_int),  # 近光灯有效个数; Dipped headlights effective number;
        ('stuNearLights', CFG_NEARLIGHT_INFO * 16),  # 近光灯列表; Dipped headlight list;
        ('nFarLight', c_int),  # 远光灯有效个数; High beam effective number;
        ('stuFarLights', CFG_FARLIGHT_INFO * 16),  # 远光灯列表; High beam list;
    ]

class CFG_LIGHTING_INFO(Structure):
    """
     灯光设置(对应 CFG_CMD_TYPE.LIGHTING 命令); Light setting (corresponding CFG_CMD_TYPE.LIGHTING command)
    """
    _fields_ = [
        ('nLightingDetailNum', c_int),  # 灯光设置有效个数; Light setting effective number;
        ('stuLightingDetail', CFG_LIGHTING_DETAIL * 16),  # 灯光设置信息列表; Light setting information list;
    ]

class NET_PTZSPACE_UNNORMALIZED(Structure):
    """
    云台定位中非归一化坐标和变倍; unnormalized position and zoom
    """
    _fields_ = [
        ('nPosX', c_int),       # x坐标; x;
        ('nPosY', c_int),       # y坐标; y;
        ('nZoom', c_int),       # 放大倍率; Zoom;
        ('byReserved', C_BYTE * 52),        # 预留字节; Reserved;
    ]

class SDK_PTZ_LOCATION_INFO(Structure):
    """
    云台定位信息报警; PTZ positioning information alarm
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号; Channel number;
        ('nPTZPan', c_int),     # 云台水平运动位置,有效范围：[0,3600]; Horizontal movement of the head position, effective range: [0,3600];
        ('nPTZTilt', c_int),    # 云台垂直运动位置,有效范围：[-1800,1800]; PTZ vertical position, the effective range: [-1800,1800];
        ('nPTZZoom', c_int),    # 云台光圈变动位置,有效范围：[0,128]; PTZ iris position changes, effective range: [0,128];
        ('bState', C_BYTE),     # 云台运动状态, 0-未知 1-运动 2-空闲; PTZ motion, 0 - Unknown 1 - Movement 2 - Idle;
        ('bAction', C_BYTE),    # 云台动作,255-未知,0-预置点,1-线扫,2-巡航,3-巡迹,4-水平旋转,5-普通移动,6-巡迹录制,7-全景云台扫描,8-热度图,9-精确定位,10-设备校正,11-智能配置，12-云台重启; PTZ movement, 255- unknown,0 - preset ,1 - line scan, 2 - Cruise, 3 - patrol track, 4 - horizontal rotation,5 -GeneralMove,6-PatternRecord,7-WideViewScan,,8-HeatMap,9-AbsoluteMove,10-CheckDeviceOffset,11-IntelliConfigure，12-Restart;
        ('bFocusState', C_BYTE),    # 云台聚焦状态, 0-未知, 1-运动状态, 2-空闲; PTZ focus state, 0 - unknown 1 - state of motion 2 - Idle;
        ('bEffectiveInTimeSection', C_BYTE),    # 在时间段内预置点状态是否有效,如果当前上报的预置点是时间段内的预置点,则为1,其他情况为0; In the period of validity of the preset state,If the current is preset reported preset period of time, compared with one, otherwise 0;
        ('nPtzActionID', c_int),    # 巡航ID号; Cruise ID number;
        ('dwPresetID', C_DWORD),    # 云台所在预置点编号; PTZ preset number where;
        ('fFocusPosition', c_float),    # 聚焦位置; Focus position;
        ('bZoomState', C_BYTE),     # 云台ZOOM状态,0-未知,1-ZOOM,2-空闲; ZOOM PTZ status, 0 - Unknown,1-ZOOM, 2 - Idle;
        ('bReserved', C_BYTE * 3),  # 对齐; Alignment;
        ('dwSequence', C_DWORD),    # 包序号,用于校验是否丢包; Packet sequence number, used to verify whether the loss;
        ('dwUTC', C_DWORD),     # 对应的UTC(1970-1-1 00:00:00)秒数。; Corresponding UTC (1970-1-1 00:00:00) seconds.;
        ('emPresetStatus', C_ENUM),     # 预置点位置,参考枚举EM_SDK_PTZ_PRESET_STATUS; preset status,Please refer to EM_SDK_PTZ_PRESET_STATUS;
        ('nZoomValue', c_int),  # 真实变倍值 当前倍率（扩大100倍表示）; real zoom value ,expanded 100 times;
        ('stuAbsPosition', NET_PTZSPACE_UNNORMALIZED),  # 云台方向与放大倍数（扩大100倍表示）,第一个元素为水平角度，0-36000；,第二个元素为垂直角度，（-18000）-（18000）；,第三个元素为显示放大倍数，0-MaxZoom*100; Ptz abs position,First is horizontal angle,0-36000,Second is vertical angle,-18000-18000,nZoom is zoom factors,0-MaxZoom*100;
        ('nFocusMapValue', c_int),  # 聚焦映射值; Focus map value
        ('nZoomMapValue', c_int),  # 变倍映射值; Variable magnification mapping value
        ('emPanTiltStatus', C_ENUM),  # 云台P/T运动状态,参考 EM_SDK_PTZ_PAN_TILT_STATUS;  P/T movement status of gimbal.Please refer to EM_SDK_PTZ_PAN_TILT_STATUS
        ('reserved', c_int * 696),  # 保留字段; Reserved;
    ]

class PTZ_SPACE_UNIT(Structure):
    """
    云台控制位置单元; PTZ control position unit
    """
    _fields_ = [
        ('nPositionX', c_int),          # 云台水平运动位置,有效范围：[0,3600]; PTZ horizontal motion position, effective range:[0,3600];
        ('nPositionY', c_int),          # 云台垂直运动位置,有效范围：[-1800,1800]; PTZ vertical motion position, effective range:[-1800,1800];
        ('nZoom', c_int),               # 云台光圈变动位置,有效范围：[0,128]; PTZ aperture change position, the effective range:[0,128];
        ('szReserve', c_char * 32),     # 预留32字节; Reserved;
    ]

class PTZ_SPEED_UNIT(Structure):
    """
    云台控制速率单元; PTZ control speed unit
    """
    _fields_ = [
        ('fPositionX', c_float),        # 云台水平方向速率,归一化到-1~1; PTZ horizontal speed, normalized to -1~1;
        ('fPositionY', c_float),        # 云台垂直方向速率,归一化到-1~1; PTZ vertical speed, normalized to -1~1;
        ('fZoom', c_float),             # 云台光圈放大倍率,归一化到 0~1; PTZ aperture magnification, normalized to 0~1;
        ('szReserve', c_char * 32),     # 预留32字节; Reserved;
    ]

class PTZ_CONTROL_ABSOLUTELY(Structure):
    """
    绝对控制云台对应结构; Absolute control PTZ corresponding structure
    """
    _fields_ = [
        ('stuPosition', PTZ_SPACE_UNIT),    # 云台绝对移动位置; PTZ Absolute Speed;
        ('stuSpeed', PTZ_SPEED_UNIT),       # 云台运行速度; PTZ Operation Speed;
        ('szReserve', c_char * 64),         # 预留64字节; Reserved;
    ]

class CFG_PTZ_MOTION_RANGE(Structure):
    """
    云台转动角度范围，单位：度; PTZ rotation angle range, unit: degree
    """
    _fields_ = [
        ('nHorizontalAngleMin', c_int), # 水平角度范围最小值,单位:度; Minimum level angle range, unit: degree;
        ('nHorizontalAngleMax', c_int), # 水平角度范围最大值,单位:度; The maximum horizontal angle range, unit: degree;
        ('nVerticalAngleMin', c_int), # 垂直角度范围最小值,单位:度; Vertical angle range minimum, unit: degree;
        ('nVerticalAngleMax', c_int), # 垂直角度范围最大值,单位:度; Maximum vertical angle range, unit: degree;
    ]

class CFG_PTZ_LIGHTING_CONTROL(Structure):
    """
    云台转动角度范围，单位：度; PTZ rotation angle range, unit: degree
    """
    _fields_ = [
        ('szMode', c_char * 32),  # 手动灯光控制模式,on-off"：直接开关模式,,"adjustLight"：手动调节亮度模式; Manual Lighting Control Mode,On - off ": Direct Switch Mode,,"adjustLight":Manually Adjust Brightness Mode;
        ('dwNearLightNumber', C_DWORD),  # 近光灯组数量; The number of near light group;
        ('dwFarLightNumber', C_DWORD),  # 远光灯组数量; The number of beam group;
    ]

class CFG_PTZ_AREA_SCAN(Structure):
    """
    云台-区域扫描能力集; PTZ -Area Scan capability
    """
    _fields_ = [
        ('bIsSupportAutoAreaScan', C_BOOL),  # 是否支持区域扫描; Whether to support Area Scan;
        ('wScanNum', c_uint16),  # 区域扫描的个数; Area Scan Numbers;
    ]

class CFG_PTZ_PRIVACY_MASKING(Structure):
    """
    隐私遮挡能力集; the capability of privacy masking
    """
    _fields_ = [
        ('bPrivacyMasking', C_BOOL), # 是否支持隐私遮挡设置; support setting privacy masking or not;
        ('bSetColorSupport', C_BOOL), # 是否支持遮挡块颜色设置; support setting color of privacy masking or not;
        ('abMaskType', C_BOOL), # emMaskType是否有效; emMaskType is effective or not;
        ('nMaskTypeCount', c_int), # 实际支持的遮挡块形状个数; the count of mask types actual supported;
        ('emMaskType', C_ENUM * 8), # 支持的遮挡块形状，没有该项配置时默认支持矩形,参考枚举NET_EM_MASK_TYPE; the list os mask types supported, no value means support rect,Please refer to NET_EM_MASK_TYPE;
        ('bSetMosaicSupport', C_BOOL), # 是否支持马赛克遮挡块设置; support settingh mosaic or not;
        ('bSetColorIndependent', C_BOOL), # 是否支持遮挡块颜色相互独立(bSetColorSupport为true时该能力有效); support independent color of privacy masking or not(effective when bSetColorSupport is true);
        ('abMosaicType', C_BOOL), # emMosaicType是否有效; emMosaicType is effective or not;
        ('nMosaicTypeCount', c_int), # 实际支持的马赛克类型个数; the count of mosaic types actual support;
        ('emMosaicType', C_ENUM * 8), # 支持的马赛克类型(SetMosaicSupport为true时该能力有效，没有该项配置时默认支持24x24大小马赛克),参考枚举NET_EM_MOSAIC_TYPE; the list of mosaic types supported(effective SetMosaicSupport is true, no value means support 24x24),Please refer to NET_EM_MOSAIC_TYPE;
    ]

class CFG_PTZ_MEASURE_DISTANCE(Structure):
    """
    图像测距能力;the capability of measureing distance of the image
    """
    _fields_ = [
        ('bSupport', C_BOOL), # 是否支持图像测距; support measureing distance of the image or not;
        ('bOsdEnable', C_BOOL), # 是否将图像测距结果数据叠加至码流; support stack the result of measureing to the stream or not;
        ('nDisplayMin', c_int), # 图像测距信息的最小显示时长, 单位秒; the min time of display, unit:second;
        ('nDisplayMax', c_int), # 图像测距信息的最大显示时长, 单位秒; the max time of display, unit:second;
    ]

class CFG_PTZ_ACTION_CAPS(Structure):
    """
    支持的云台动作类型; Ptz action type
    """
    _fields_ = [
        ('bSupportPan', C_BOOL), # 是否支持水平移动; Whether to support PTZ horizontal swing;
        ('bSupportTile', C_BOOL), # 是否支持垂直移动; Whether to support PTZ vertical swing;
        ('bSupportZoom', C_BOOL), # 是否支持变倍; Whether to support PTZ changed times;
        ('byReserved', C_BYTE * 116), # 预留; Reserved;
    ]

class CFG_PTZ_ABSOLUTELY_CAPS(Structure):
    """
    支持的云台精确定位方式类型;Ptz absolutely type
    """
    _fields_ = [
        ('bSupportNormal', C_BOOL), # 是否支持归一化定位; Whether to support normalized move;
        ('bSupportReal', C_BOOL), # 是否支持实际参数值定位; Whether to support unnormalized move;
        ('byReserved', C_BYTE * 120), # 预留; Reserved;
    ]

class CFG_PTZ_MOVE_ABSOLUTELY_CAP(Structure):
    """
    绝对控制云台能力; The caps of ptz move absolutely
    """
    _fields_ = [
        ('stuPTZ', CFG_PTZ_ACTION_CAPS), # 支持的云台动作类型; Ptz action types supported;
        ('stuType', CFG_PTZ_ABSOLUTELY_CAPS), # 支持的云台精确定位方式类型; Ptz absolutely types supported;
        ('byReserved', C_BYTE * 768), # 预留; Reserved;
    ]

class CFG_PTZ_CONTINUOUSLY_TYPE(Structure):
    """
    连续移动方式类型; Continuously move type
    """
    _fields_ = [
        ('bSupportNormal', C_BOOL), # 是否支持归一化值定位; Whether to support normalized move;
        ('bSupportExtra', C_BOOL), # 是否支持非归一化值定位; Whether to support unnormalized move;
        ('byReserved', C_BYTE * 120), # 预留; Reserved;
    ]

class CFG_PTZ_MOVE_CONTINUOUSLY_CAPS(Structure):
    """
    云台连续运动能力; Continuously move caps
    """
    _fields_ = [
        ('stuPTZ', CFG_PTZ_ACTION_CAPS), # 支持的PTZ动作; Ptz action types supported;
        ('stuType', CFG_PTZ_CONTINUOUSLY_TYPE), # 连续移动方式类型; Ptz absolutely types supported;
        ('byReserved', C_BYTE * 1024), # 预留; Reserved;
    ]

class CFG_PTZ_PROTOCOL_CAPS_INFO(Structure):
    """
    获取云台能力集信息; Get PTZ capability set information
    """
    _fields_ = [
        ('nStructSize', c_int),
        ('bPan', C_BOOL), # 是否支持云台水平摆动; Whether to support PTZ horizontal swing;
        ('bTile', C_BOOL), # 是否支持云台垂直摆动; Whether to support PTZ vertical swinging;
        ('bZoom', C_BOOL), # 是否支持云台变倍; Whether to support PTZ changed times;
        ('bIris', C_BOOL), # 是否支持云台光圈调节; Whether to support PTZ aperture adjustment;
        ('bPreset', C_BOOL), # 是否支持预置点; Whether to support the preset point;
        ('bRemovePreset', C_BOOL), # 是否支持清除预置点; Whether to support removal of preset point;
        ('bTour', C_BOOL), # 是否支持自动巡航线路; Whether to support automatic cruise lines;
        ('bRemoveTour', C_BOOL), # 是否支持清除巡航; Whether to support Clear cruise;
        ('bPattern', C_BOOL), # 是否支持轨迹线路; Whether to support the track line;
        ('bAutoPan', C_BOOL), # 是否支持自动水平摆动; Whether to support automatic level swing;
        ('bAutoScan', C_BOOL), # 是否支持自动扫描; Whether to support automatic scanning;
        ('bAux', C_BOOL), # 是否支持辅助功能; Whether to support accessibility;
        ('bAlarm', C_BOOL), # 是否支持报警功能; Support alarm function;
        ('bLight', C_BOOL), # 是否支持灯光, 内容见下面"stuPtzLightingControl"，该字段已废除使用; Whether or not support the lighting, the contents see below "stuPtzLightingControl", this member is invalid;
        ('bWiper', C_BOOL), # 是否支持雨刷; Whether or not support the wipers;
        ('bFlip', C_BOOL), # 是否支持镜头翻转; Whether or not support Flip camera;
        ('bMenu', C_BOOL), # 是否支持云台内置菜单; Whether or not support PTZ built-in menus;
        ('bMoveRelatively', C_BOOL), # 是否支持云台按相对坐标定位; Whether or not support the PTZ by a relative coordinate positioning;
        ('bMoveAbsolutely', C_BOOL), # 是否支持云台按绝对坐标定位; Whether or not support PTZ in absolute coordinates;
        ('bMoveDirectly', C_BOOL), # 是否支持云台按三维坐标定位; Whether or not support ptz 3D point direct motion;
        ('bReset', C_BOOL), # 是否支持云台复位; Whether or not support PTZ reset;
        ('bGetStatus', C_BOOL), # 是否支持获取云台运动状态及方位坐标; Whether or not support Get the state of motion and orientation coordinates of PTZ;
        ('bSupportLimit', C_BOOL), # 是否支持限位; Whether or not support the limit;
        ('bPtzDevice', C_BOOL), # 是否支持云台设备; Whether or not support PTZ equipment;
        ('bIsSupportViewRange', C_BOOL), # 是否支持云台可视域; Whether or not support PTZ visible range;
        ('wCamAddrMin', c_uint16), # 通道地址的最小值; The minimum channel address;
        ('wCamAddrMax', c_uint16), # 通道地址的最大值; The maximum number of channel address;
        ('wMonAddrMin', c_uint16), # 监视地址的最小值; Minimum monitoring addresses;
        ('wMonAddrMax', c_uint16), # 监视地址的最大值; The maximum number of monitoring the address;
        ('wPresetMin', c_uint16), # 预置点的最小值; Minimum preset points;
        ('wPresetMax', c_uint16), # 预置点的最大值; The maximum preset points;
        ('wTourMin', c_uint16), # 自动巡航线路的最小值; The minimum value of automatic cruise lines;
        ('wTourMax', c_uint16), # 自动巡航线路的最大值; The maximum number of automatic cruise lines;
        ('wPatternMin', c_uint16), # 轨迹线路的最小值; The minimum value of track circuit;
        ('wPatternMax', c_uint16), # 轨迹线路的最大值; The maximum number of track circuit;
        ('wTileSpeedMin', c_uint16), # 垂直速度的最小值; The minimum value of vertical speed;
        ('wTileSpeedMax', c_uint16), # 垂直速度的最大值; The maximum vertical speed;
        ('wPanSpeedMin', c_uint16), # 水平速度的最小值; The minimum value of horizontal velocity;
        ('wPanSpeedMax', c_uint16), # 水平速度的最大值; The maximum horizontal velocity;
        ('wAutoScanMin', c_uint16), # 自动扫描的最小值; The minimum value of automatic scanning;
        ('wAutoScanMax', c_uint16), # 自动扫描的最大值; The maximum number of automatic scanning;
        ('wAuxMin', c_uint16), # 辅助功能的最小值; The minimum value of auxiliary functions;
        ('wAuxMax', c_uint16), # 辅助功能的最大值; The maximum number of auxiliary functions;
        ('dwInterval', C_DWORD), # 发送命令的时间间隔; Send the command time interval;
        ('dwType', C_DWORD), # 协议的类型，0-本地云台，1-远程云台; The type of agreement, 0 - Local PTZ 1 - Remote PTZ;
        ('dwAlarmLen', C_DWORD), # 协议的报警长度; The length of the alarm of the agreement;
        ('dwNearLightNumber', C_DWORD), # 近光灯组数量,0~4,为0时表示不支持; The number of near light group, 0-4, 0 means not supported;
        ('dwFarLightNumber', C_DWORD), # 远光灯组数量,0~4,为0时表示不支持; The number of beam group, 0-4, 0 means not supported;
        ('dwSupportViewRangeType', C_DWORD), # 支持的可视域数据获取方式掩码,从低位到高位依次数,目前支持,第1位:为1表示支持"ElectronicCompass" 电子罗盘方式; Visual field data acquisition mode supported by the mask, from low to high depending on the number , currently supported,The first 1: 1 expressed support the "ElectronicCompass" electronic compass mode;
        ('dwSupportFocusMode', C_DWORD), # 支持的支持的焦距模式掩码,从低位到高位依次数,见#EM_SUPPORT_FOCUS_MODE; Supported Focus mode mask, from low to high depending on the number, see # EM_SUPPORT_FOCUS_MODE;
        ('szName', c_char * 32), # 操作的协议名; The name of the protocol operations;
        ('szAuxs', c_char * 1024), # 云台辅助功能名称列表; PTZ auxiliary function names list;
        ('stuPtzMotionRange', CFG_PTZ_MOTION_RANGE), # 云台转动角度范围，单位：度; PTZ rotation angle range, unit: degree;
        ('stuPtzLightingControl', CFG_PTZ_LIGHTING_CONTROL), # 灯光控制内容，该字段已废除使用; Lighting control content, this member is invalid;
        ('bSupportPresetTimeSection', C_BOOL), # 是否支持预置点时间段配置的功能; Whether to support the function of the preset point time configuration;
        ('bFocus', C_BOOL), # 是否支持云台变焦; Whether to support to Ptz focus;
        ('stuPtzAreaScan', CFG_PTZ_AREA_SCAN), # 区域扫描能力集; Area Scan capability;
        ('stuPtzPrivacyMasking', CFG_PTZ_PRIVACY_MASKING), # 隐私遮挡能力集; privacy masking capability;
        ('stuPtzMeasureDistance', CFG_PTZ_MEASURE_DISTANCE), # 图像测距能力集; measure distance capability;
        ('bSupportPtzPatternOSD', C_BOOL), # 是否支持云台巡迹OSD叠加; support PTZ pattern OSD or not;
        ('bSupportPtzRS485DetectOSD', C_BOOL), # 是否支持云台RS485检测OSD叠加; support PTZ RS485 detect OSD or not;
        ('bSupportPTZCoordinates', C_BOOL), # 是否支持云台坐标叠加; support PTZ coordinates or not;
        ('bSupportPTZZoom', C_BOOL), # 是否支持云台变倍叠加; support PTZ zoom or not;
        ('bDirectionDisplay', C_BOOL), # 是否支持云台方向状态显示; support direction display or not;
        ('dwZoomMax', C_DWORD), # 变倍最大值; Zoom Maximum;
        ('dwZoomMin', C_DWORD), # 变倍最小值; Zoom Minimum;
        ('stuMoveAbsolutely', CFG_PTZ_MOVE_ABSOLUTELY_CAP), # 绝对控制云台能力，bMoveAbsolutely==TRUE 时有效; The caps of ptz move absolutely , Valid when bMoveAbsolutely==TRUE;
        ('bMoveContinuously', C_BOOL), # stuMoveContinuously 字段是否有效; Whether stuMoveContinuously is valid or not;
        ('stuMoveContinuously', CFG_PTZ_MOVE_CONTINUOUSLY_CAPS), # 云台连续运动能力; The caps of ptz move Continuously;
        ('nUnSupportDirections', c_int), # 云台不支持的转动方向个数; Number of rotation directions not supported by the gimbal;
        ('emUnSupportDirections', C_ENUM * 10), # 云台不支持的转动方向,参考枚举EM_PTZ_UNSUPPORT_DIRECTION; UnSupport Directions,Please refer to EM_PTZ_UNSUPPORT_DIRECTION;
    ]

class NET_IN_PTZBASE_MOVEABSOLUTELY_INFO(Structure):
    """
    设置云台方向; Move absolulety, Corresponding to BASE_MOVE_ABSOLUTELY
    """
    _fields_ = [
        ('dwSize', C_DWORD),            				# 结构体大小; struct size;
        ('nZoomFlag', c_int),    						# 1表示显示倍率; 2保留，内部用; 3表示映射倍率值；如为0则默认映射倍率值; 1 according to ratio, 2 Reserved, 3 Mapping radio; 0 default Mapping radio
        ('stuPosition', NET_PTZSPACE_UNNORMALIZED),    	# 云台绝对移动位置云台绝对定位参数,扩大10倍,云台水平坐标(0~3600),云台垂直坐标(-1800~1800),倍率值，范围：nZoomFlag为1时(0~最大显示倍率*10)，nZoomFlag为3时(0~16384); Ptz absolutely position,Horizontal angle(0~3600),Vertical angle(-1800~1800),Zoom(0~16384)
        ('stuSpeed', NET_PTZSPACE_UNNORMALIZED),       	# 若无speed则表示默认速度运动 P，T，以0.01度/秒为单位，扩大100倍显示，范围与PtzSpeedLevel中的范围保持一致[0，100000]，水平和垂直分别最大不会超过PtzSpeedLevel中最大档位水平和垂直的最大值，zoom变倍速度为0~100;  If there is no speed, it means the default speed movement P, T, with 0.01 degree/second as the unit, enlarged by 100 times, the range is consistent with the range in PtzSpeedLevel [0, 100000], the maximum horizontal and vertical respectively will not exceed the maximum in PtzSpeedLevel The maximum value of the horizontal and vertical gears, the zoom speed is 0~100.
        ('szReserve', c_char * 448),         			# 预留字节; Reserved;
    ]

class NET_IN_PTZ_STATUS_PROC(Structure):
    """
    订阅云台元数据接口输入参数; Subscribe to PTZ metadata interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),   # 结构体大小; struct size;
        ('nChannel', c_int),   # 云台通道; PTZ Channel
        ('cbPTZStatusProc', CB_FUNCTYPE(None, C_LLONG, C_LLONG, c_void_p, c_int, C_LDWORD)),  # 状态回调函数; Callback function
        ('dwUser', C_LDWORD),  # 用户数据; User data
    ]

class NET_OUT_PTZ_STATUS_PROC(Structure):
    """
    订阅云台元数据接口输输出参数; Subscribe to PTZ metadata interface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
    ]

class NET_IN_PTZBASE_MOVEABSOLUTELY_ONLYPT_INFO(Structure):
    """
    绝对定位独立控制PT; Absolute positioning independent control Pt
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; struct size;
        ('nPositionP', c_int),                          # P轴坐标，范围0~36000（扩大100倍）;P-axis coordinate, range 0-36000 (expanded 100 times);
        ('nPositionT', c_int),                          # T轴坐标，范围-18000~18000（扩大100倍）;T-axis coordinate, range - 18000 ~ 18000 (expanded 100 times);
        ('nSpeedP', c_int),                             # P轴速度，以0.01度/秒为单位，扩大100倍显示，范围[0，100000];P-axis speed, in the unit of 0.01 deg / s, expanded 100 times display, range [0，100000];
        ('nSpeedT', c_int),                             # T轴速度，以0.01度/秒为单位，扩大100倍显示，范围[0，100000];T-axis speed, in the unit of 0.01 deg / s, expanded 100 times display, range [0，100000];
        ('szReserve', c_char * 1024),                   # 预留字节; Reserved;
    ]

class NET_IN_PTZBASE_MOVEABSOLUTELY_ONLYZOOM_INFO(Structure):
    """
    绝对定位独立控制zoom; Absolute positioning independent control zoom
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; struct size;
        ('nZoomFlag', c_int),                           # 1表示显示倍率; 2保留，内部用; 3表示映射倍率值；如为0则默认映射倍率值; 1 according to ratio, 2 Reserved, 3 Mapping radio; 0 default Mapping radio;
        ('nZoomValue', c_int),                          # 根据zoomFlag值确认Zoom位置范围：1：0~显示倍率最大值*100; 3:映射倍率值(0~16384);Confirm the zoom position range according to the zoom flag value: 1:0 ~ maximum display magnification * 100; 3: Mapping ratio value (0 ~ 16384);
        ('nZoomSpeed', c_int),                          # zoom变倍速度为0~100;Zoom speed is 0 ~ 100;
        ('szReserve', c_char * 1024),                   # 预留字节; Reserved;
    ]

class NET_IN_STORAGE_DEV_INFOS(Structure):
    """
    QueryDevInfo接口STORAGE_INFOS枚举接口输入参数; QueryDevInfo，STORAGE_INFOS port input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emVolumeType', C_ENUM),  # 要获取的卷类型,参考枚举NET_VOLUME_TYPE; volume type to get,Please refer to NET_VOLUME_TYPE;
    ]

class SDK_STORAGE_PARTITION(Structure):
    """
    存储分区信息; Storage partition info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称; Name;
        ('nTotalSpace', c_int64),  # 总空间, byte; Total space(MB);
        ('nFreeSpace', c_int64),  # 剩余空间, byte; free space(MB);
        ('szMountOn', c_char * 64),  # 挂载点; Mount point;
        ('szFileSystem', c_char * 16),  # 文件系统; File system;
        ('nStatus', c_int),  # 分区状态, 0-LV不可用, 1-LV可用; partition state, 0-LV not available, 1-LV available;
    ]

class NET_RAID_MEMBER_INFO(Structure):
    """
    RAID成员信息; RAID member info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),  # 磁盘号, 可用于描述磁盘在磁柜的槽位; disk no., may use to describe disk cabinet slot;
        ('bSpare', C_BOOL),  # 是否局部热备, true-局部热备, false-RAID子盘; partial hot device, true-partial hot device, false-RAID sub disk;
    ]

class SDK_STORAGE_RAID(Structure):
    """
    RAID信息; RAID Info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nLevel', c_int),  # 等级; level;
        ('nState', c_int),  # RAID状态组合, 如 DH_RAID_STATE_ACTIVE | DH_RAID_STATE_DEGRADED; RAID state combinationDH_RAID_STATE_ACTIVE | DH_RAID_STATE_DEGRADED;
        ('nMemberNum', c_int),  # 成员数量; member amount;
        ('szMembers', c_char * 4096),  # RAID成员; RAID member;
        ('fRecoverPercent', c_float),  # 同步百分比, 0~100, RAID状态中有"Recovering"或"Resyncing"时有效; Sync percentage, 0~100, RAID status has"Recovering" or "Resyncing" valid;
        ('fRecoverMBps', c_float),  # 同步速度, 单位MBps, RAID状态中有"Recovering"或"Resyncing"时有效; Sync speed, unit MBps, RAID status has"Recovering" or "Resyncing" valid;
        ('fRecoverTimeRemain', c_float),  # 同步剩余时间, 单位分钟, RAID状态中有"Recovering"或"Resyncing"时有效; Sync remaining time, unit minute, RAID status has "Recovering" or "Resyncing" valid;
        ('stuMemberInfos', NET_RAID_MEMBER_INFO * 32),  # RAID成员信息; RAID member info;
        ('nRaidDevices', c_int),  # RAID设备个数; The number of RAID device;
        ('nTotalDevices', c_int),  # RAID设备总数; The total count of RAID device;
        ('nActiveDevices', c_int),  # 活动设备个数; The number of active device;
        ('nWorkingDevices', c_int),  # 工作设备个数; The number of working device;
        ('nFailedDevices', c_int),  # 失败设备个数; The number of failed device;
        ('nSpareDevices', c_int),  # 热备设备个数; The number of hot-spare device;
        ('szAliasName', c_char * 24),  # RAID别名,UTF-8编码; Alias Name,UTF-8 code;
    ]

class SDK_ISCSI_TARGET(Structure):
    """
    ISCSI Target信息; ISCSI Target Info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称; Name;
        ('szAddress', c_char * 64),  # 服务器地址; service address;
        ('szUser', c_char * 128),  # 用户名; user name;
        ('nPort', c_int),  # 端口; port;
        ('nStatus', C_UINT),  # 状态, 0-未知, 1-已连接, 2-未连接, 3-连接失败, 4-认证失败, 5-连接超时, 6-不存在; status, 0- unknow, 1-connected, 2-un connected, 3-connect failed, 4-authentication failed, 5-connect time out;
    ]

class SDK_STORAGE_TANK(Structure):
    """
    扩展柜信息; storage tank info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nLevel', c_int),  # 级别, 主机是第0级,其它下属级别类推; level, the host is 0 level;
        ('nTankNo', c_int),  # 同一级扩展柜内的扩展口编号, 从0开始; extend port number from 0;
        ('nSlot', c_int),  # 对应主柜上的板卡号, 从0开始编号; Corresponding cabinet board card no., start from 0;
    ]

class SDK_STORAGE_DEVICE(Structure):
    """
    存储设备信息; Storage device info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称; name;
        ('nTotalSpace', c_int64),  # 总空间, byte; Total space, byte;
        ('nFreeSpace', c_int64),  # 剩余空间, byte; free space, byte;
        ('byMedia', C_BYTE),  # 介质, 0-DISK, 1-CDROM, 2-FLASH; Media, 0-DISK, 1-CDROM, 2-FLASH medium,;
        ('byBUS', C_BYTE),  # 总线, 0-ATA, 1-SATA, 2-USB, 3-SDIO, 4-SCSI; BUS, 0-ATA, 1-SATA, 2-USB, 3-SDIO, 4-SCSI main line 0-ATA, 1-SATA, 2-USB, 3-SDIO, 4-SCSI;
        ('byVolume', C_BYTE),  # 卷类型, 0-物理卷, 1-Raid卷, 2-VG虚拟卷, 3-ISCSI, 4-独立物理卷, 5-全局热备卷, 6-NAS卷(包括FTP, SAMBA, NFS); volume type, 0-physics, 1-Raid, 2- VG virtual 3-ISCSI, 4-Invidual Physical Volume, 5-VolumeGroup, 6-NAS ( FTP, SAMBA, NFS), 7-Invidual Raid Volume;
        ('byState', C_BYTE),  # 物理硬盘状态, 取值为 NET_STORAGE_DEV_OFFLINE 和 NET_STORAGE_DEV_RUNNING 等; Physics disk state, 0-physics disk offline state 1-physics disk 2- RAID activity 3- RAID sync 4-RAID hotspare 5-RAID invalidation 6- RAID re-creation 7- RAID delete;
        ('nPhysicNo', c_int),  # 同类设备存储接口的物理编号; storage interface of devices of same type logic number;
        ('nLogicNo', c_int),  # 同类设备存储接口的逻辑编号; storage interface of devices of same type physics number;
        ('szParent', c_char * 128),  # 上级存储组名称; superior storage group name;
        ('szModule', c_char * 128),  # 设备模块; device module;
        ('szSerial', c_char * 48),  # 设备序列号; device serial number;
        ('szFirmware', c_char * 64),  # 固件版本; Firmware version;
        ('nPartitionNum', c_int),  # 分区数; partition number;
        ('stuPartitions', SDK_STORAGE_PARTITION * 32),  # 分区信息; partition info;
        ('stuRaid', SDK_STORAGE_RAID),  # RAID信息, 只对RAID有效(byVolume == 1); Raid info, for RAID use only(byVolume == 1);
        ('stuISCSI', SDK_ISCSI_TARGET),  # ISCSI信息, 只对ISCSI盘有效(byVolume == 3); Iscsi info, for iscsi use only (byVolume == 2);
        ('abTank', C_BOOL),  # 扩展柜使能; tank enable;
        ('stuTank', SDK_STORAGE_TANK),  # 硬盘所在扩展柜信息, abTank为TRUE时有效; tank info, effective when abTank = TRUE;
        ('emPowerMode', C_ENUM),  # 硬盘电源状态,参考枚举EM_STORAGE_DISK_POWERMODE; hard disk power mode,Please refer to EM_STORAGE_DISK_POWERMODE;
        ('emPreDiskCheck', C_ENUM),  # 硬盘预检状态(EVS定制字段，配合磁盘预检功能使用),参考枚举EM_STORAGE_DISK_PREDISKCHECK; pre disk check(EVS),Please refer to EM_STORAGE_DISK_PREDISKCHECK;
    ]

class NET_OUT_STORAGE_DEV_INFOS(Structure):
    """
    QueryDevInfo , STORAGE_INFOS接口输出参数; QueryDevInfo , STORAGE_INFOS port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nDevInfosNum', c_int),  # 获取到设备的存储模块信息列表; device storage moduleinfo list to get;
        ('stuStoregeDevInfos', SDK_STORAGE_DEVICE * 128),  # 设备信息列表,SDK_STORAGE_DEVICE的dwsize需赋值; device info list, dwsize of SDK_STORAGE_DEVICE need to assign value;
    ]

class NET_IN_GET_TEMPERATUREEX(Structure):
    """
    FaceBoard_GetTemperatureEx的入参; FaceBoard_GetTemperatureEx input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure size;
        ('emTemperatureType', C_ENUM),  # 温度类型,参考枚举EM_TEMPERATUREEX_TYPE; Temperature Type,Please refer to EM_TEMPERATUREEX_TYPE;
    ]

class NET_TEMPERATUREEX_VALUE(Structure):
    """
    每个监测点的温度; Each monitor point temperature
    """
    _fields_ = [
        ('emTemperatureType', C_ENUM),  # 温度类型,参考枚举EM_TEMPERATUREEX_TYPE; Temperature Type,Please refer to EM_TEMPERATUREEX_TYPE;
        ('nRetTemperatureNum', c_int),  # 返回的有效温度值个数; The number of return valid temperature value;
        ('fTemperature', c_float * 64),  # 温度值,单位:摄氏度; Temperature value,unit:centigrade;
        ('byReserved', C_BYTE * 128),  # 保留字节; Reserved byte;
    ]

class NET_OUT_GET_TEMPERATUREEX(Structure):
    """
    FaceBoard_GetTemperatureEx的出参; FaceBoard_GetTemperatureEx output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure size;
        ('nRetMonitorPointNum', c_int),  # 返回的有效温度监测点的个数,num>1时,对应emTemperatureType为ALL; The number of return valid monitor point temperature, when num>1,emTemperatureType is ALL;
        ('stuTemperatureEx', NET_TEMPERATUREEX_VALUE * 12),  # 监测点温度; monitor point temperature;
    ]

class NET_RADIOMETRY_CONDITION(Structure):
    """
    获取测温项温度的条件;Conditions for obtaining the temperature of the temperature measurement item
    """
    _fields_ = [
        ('nPresetId', c_int),   # 预置点编号;Preset point number
        ('nRuleId', c_int),     # 规则编号;Rule number
        ('nMeterType', c_int),  # 测温项类别,见 NET_RADIOMETRY_METERTYPE ;Types of temperature measurement items, see NET_RADIOMETRY_METERTYPE
        ('szName', c_char*64),  # 测温项的名称,从测温配置规则名字中选取;The name of the temperature measurement item, selected from the name of the temperature measurement configuration rule
        ('nChannel', c_int),    # 通道号;Channel number
        ('reserved', c_char*256),# 保留字节;byte reserved
    ]

class NET_IN_RADIOMETRY_GETTEMPER(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_DEV_RADIOMETRY_TEMPER 命令入参;QueryDevInfo interface NET_QUERY_DEV_RADIOMETRY_TEMPER command to input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小;Struct size
        ('stCondition', NET_RADIOMETRY_CONDITION),  # 获取测温项温度的条件;Conditions for obtaining the temperature of the temperature measurement item
    ]

class NET_RADIOMETRYINFO(Structure):
    """
    测温信息;Temperature measurement information
    """
    _fields_ = [
        ('nMeterType', c_int),      # 返回测温类型,见 NET_RADIOMETRY_METERTYPE ;Return temperature measurement type, see NET_RADIOMETRY_METERTYPE
        ('nTemperUnit', c_int),     # 温度单位(当前配置的温度单位),见 NET_TEMPERATURE_UNIT ;Temperature unit (temperature unit currently configured), see NET_TEMPERATURE_UNIT
        ('fTemperAver', c_float),   # 点的温度或者平均温度点的时候,只返回此字段;Point temperature or average temperature point, only return this field
        ('fTemperMax', c_float),    # 最高温度;Maximum temperature
        ('fTemperMin', c_float),    # 最低温度;lowest temperature
        ('fTemperMid', c_float),    # 中间温度值;Intermediate temperature value
        ('fTemperStd', c_float),    # 标准方差值;Standard deviation
        ('reserved', c_char*64),    # 保留字节;byte reserved
    ]

class NET_OUT_RADIOMETRY_GETTEMPER(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_DEV_RADIOMETRY_TEMPER 命令出参;QueryDevInfo interface NET_QUERY_DEV_RADIOMETRY_TEMPER command to output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('stTempInfo', NET_RADIOMETRYINFO), # 获取测温参数值;Get the temperature measurement parameter value
    ]

class NET_IN_RADIOMETRY_GETPOINTTEMPER(Structure):
    """
    QueryDevInfo 接口 RADIOMETRY_POINT_TEMPER 命令入参;QueryDevInfo interface RADIOMETRY_POINT_TEMPER command to input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小; Struct size
        ('nChannel', c_int),        # 通道号; Channel number
        ('stCoordinate', SDK_POINT), # 测温点的坐标,坐标值 0~8192; The coordinates of the temperature measuring point, the coordinate value is 0~8192
    ]

class NET_OUT_RADIOMETRY_GETPOINTTEMPER(Structure):
    """
    QueryDevInfo 接口 RADIOMETRY_POINT_TEMPER 命令出参;QueryDevInfo interface RADIOMETRY_POINT_TEMPER command to output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Struct size
        ('stPointTempInfo', NET_RADIOMETRYINFO), # 获取测温参数值;Get the temperature measurement parameter value
    ]

class CFG_POLYGON(Structure):
    """
    区域顶点信息; Area vertex information
    """
    _fields_ = [
        ('nX', c_int),  # 0~8191
        ('nY', c_int),
    ]

class CFG_RECT(Structure):
    """
    区域信息; Area information
    """
    _fields_ = [
        ('nLeft', c_int),
        ('nTop', c_int),
        ('nRight', c_int),
        ('nBottom', c_int),
    ]

class CFG_VIDEO_IN_NIGHT_OPTIONS(Structure):
    """
     视频输入夜晚特殊配置选项，在晚上光线较暗时自动切换到夜晚的配置参数;
     Video input night special configuration options, automatically switch to night configuration parameters when the light is dark at night
    """
    _fields_ = [
        ('bySwitchMode', C_BYTE),   # 已废弃,使用CFG_VIDEO_IN_OPTIONS里面的bySwitchMode; Obsolete, use bySwitchMode in CFG_VIDEO_IN_OPTIONS
        ('byProfile', C_BYTE),      # 当前使用的配置文件; The currently used configuration file
                                    # 0-白天;1-晚上;2-Normal;0、1、2都为临时配置,使图像生效，便于查看图像调试效果，不点击确定，离开页面不保存至设备,3-非临时配置，点击确定后保存至设备，与SwitchMode结合使用，根据SwitchMode决定最终生效的配置。
                                    # SwitchMode=0，Profile=3，设置白天配置到设备;SwitchMode=1，Profile=3，则设置夜晚配置到设备; SwitchMode=2，Profile=3，根据日出日落时间段切换，白天时间段使用白天配置，夜晚时间段使用夜晚配置，保存至设备;SwitchMode=4，Profile=3；使用普通配置，保存至设备
        ('byBrightnessThreshold', C_BYTE), # 亮度阈值 0~100; Brightness threshold 0~100
        ('bySunriseHour', C_BYTE),  # 大致日出和日落时间，日落之后日出之前，将采用夜晚特殊的配置; Approximate sunrise and sunset time, after sunset and before sunrise, special night configuration will be adopted
        ('bySunriseMinute', C_BYTE),# 00:00:00 ~ 23:59:59
        ('bySunriseSecond', C_BYTE),
        ('bySunsetHour', C_BYTE),
        ('bySunsetMinute', C_BYTE),
        ('bySunsetSecond', C_BYTE),
        ('byGainRed', C_BYTE),      # 红色增益调节，白平衡为"Custom"模式下有效 0~100; Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),     # 蓝色增益调节，白平衡为"Custom"模式下有效 0~100; Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),    # 绿色增益调节，白平衡为"Custom"模式下有效 0~100; Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE),     # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                    # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float),# 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float),# 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('byWhiteBalance', C_BYTE), # 白平衡;White balance 0-"Disable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byGain', C_BYTE),         # 0~100增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; 0~100 Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('bGainAuto', c_bool),      # 自动增益; Automatic gain
        ('bIrisAuto', c_bool),      # 自动光圈; Auto iris
        ('fExternalSyncPhase', c_float),  # 外同步的相位设置 0~360; Phase setting of external synchronization 0~360
        ('byGainMin', C_BYTE),      # 增益下限; Gain lower limit
        ('byGainMax', C_BYTE),      # 增益上限; Gain upper limit
        ('byBacklight', C_BYTE),    # 背光补偿：取值范围取决于设备能力集：0-关闭1-启用2-指定区域背光补偿;Backlight compensation: The value range depends on the device capability set: 0-off 1-enable 2-specified area backlight compensation
        ('byAntiFlicker', C_BYTE),  # 防闪烁模式; Anti-flicker mode; 0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁
        ('byDayNightColor', C_BYTE),# 日/夜模式；0-总是彩色，1-根据亮度自动切换，2-总是黑白;Day/night mode; 0-always color, 1-automatically switch according to brightness, 2-always black and white
        ('byExposureMode', C_BYTE), # 曝光模式调节 曝光等级为自动曝光时有效，取值：0-默认自动，1-增益优先，2-快门优先; Exposure mode adjustment The exposure level is effective when the exposure level is automatic exposure, value: 0-default automatic, 1-gain priority, 2-shutter priority
        ('byRotate90', C_BYTE),     # 0-不旋转，1-顺时针90°，2-逆时针90°; 0-No rotation, 1-90°clockwise, 2-90°counterclockwise
        ('bMirror', c_bool),        # 镜像; Mirroring
        ('byWideDynamicRange', C_BYTE), # 宽动态值 0-关闭，1~100-为真实范围值; Wide dynamic value, 0-closed, 1~100-is the true range value
        ('byGlareInhibition', C_BYTE),  # 强光抑制 0-关闭， 1~100为范围值; Strong light suppression 0-off, 1~100 is the range value
        ('stuBacklightRegion', CFG_RECT),# 背光补偿区域; Backlight compensation area
        ('byFocusMode', C_BYTE),    # 0-关闭，1-辅助聚焦，2-自动聚焦; 0-off, 1-assisted focus, 2-auto focus
        ('bFlip', c_bool),          # 翻转; Flip
        ('reserved', C_BYTE*74)     # 保留; reserved
    ]

class CFG_FLASH_CONTROL(Structure):
    """
    闪光灯配置; Flash configuration
    """
    _fields_ = [
        ('byMode', C_BYTE),         # 工作模式，0-禁止闪光，1-始终闪光，2-自动闪光; Working mode, 0-flash prohibited, 1-always flash, 2-auto flash
        ('byValue', C_BYTE),        # 工作值, 0-0us, 1-64us, 2-128us, 3-192...15-960us; Working value, 0-0us, 1-64us, 2-128us, 3-192...15-960us
        ('byPole', C_BYTE),         # 触发模式, 0-低电平 1-高电平 2-上升沿 3-下降沿; Trigger mode, 0-low level 1-high level 2-rising edge 3-falling edge
        ('byPreValue', C_BYTE),     # 亮度预设值  区间0~100; Brightness preset value range 0~100
        ('byDutyCycle', C_BYTE),    # 占空比, 0~100; Duty cycle, 0~100
        ('byFreqMultiple', C_BYTE), # 倍频, 0~10; Frequency multiplier, 0~10
        ('reserved', C_BYTE*122),   # 保留; reserved
    ]

class CFG_VIDEO_IN_SNAPSHOT_OPTIONS(Structure):
    """
    抓拍参数特殊配置; Snapshot parameter special configuration
    """
    _fields_ = [
        ('byGainRed', C_BYTE),      # 红色增益调节，白平衡为"Custom"模式下有效 0~100; Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),     # 蓝色增益调节，白平衡为"Custom"模式下有效 0~100; Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),    # 绿色增益调节，白平衡为"Custom"模式下有效 0~100; Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE),     # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                    # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float),   # 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float),   # 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('byWhiteBalance', C_BYTE),     # 白平衡;White balance 0-"Disable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byColorTemperature', C_BYTE), # 色温等级, 白平衡为"CustomColorTemperature"模式下有效;Color temperature level, white balance is valid in "CustomColorTemperature" mode
        ('bGainAuto', c_bool),      # 自动增益; Automatic gain
        ('byGain', C_BYTE),         # 0~100增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; 0~100 Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('reversed', C_BYTE * 112), # 保留; reserved
    ]

class CFG_FISH_EYE(Structure):
    """
    鱼眼镜头配置; Fisheye lens configuration
    """
    _fields_ = [
        ('stuCenterPoint', CFG_POLYGON),    # 鱼眼圆心坐标,范围[0,8192]; Fisheye center coordinates, range [0,8192]
        ('nRadius', c_uint),                # 鱼眼半径大小,范围[0,8192]; Fisheye radius size, range [0,8192]
        ('fDirection', c_float),            # 镜头旋转方向,旋转角度[0,360.0]; Lens rotation direction, rotation angle [0,360.0]
        ('byPlaceHolder', C_BYTE),          # 镜头安装方式	1顶装，2壁装；3地装,默认1; Lens installation method 1 top installation, 2 wall installation; 3 floor installation, default 1
        ('byCalibrateMode', C_BYTE),        # 鱼眼矫正模式,详见CFG_CALIBRATE_MODE枚举值; Fisheye correction mode, see CFG_CALIBRATE_MODE enumeration value for details
        ('reversed', C_BYTE*31),            # 保留; reserved
    ]

class CFG_VIDEO_IN_NORMAL_OPTIONS(Structure):
    """
    普通参数; Common parameters
    """
    _fields_ = [
        ('byGainRed', C_BYTE),      # 红色增益调节，白平衡为"Custom"模式下有效 0~100; Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),     # 蓝色增益调节，白平衡为"Custom"模式下有效 0~100; Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),    # 绿色增益调节，白平衡为"Custom"模式下有效 0~100; Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE),     # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                    # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float),# 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float),# 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('byWhiteBalance', C_BYTE), # 白平衡;White balance 0-"Disable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byGain', C_BYTE),         # 0~100增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; 0~100 Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('bGainAuto', c_bool),      # 自动增益; Automatic gain
        ('bIrisAuto', c_bool),      # 自动光圈; Auto iris
        ('fExternalSyncPhase', c_float),  # 外同步的相位设置 0~360; Phase setting of external synchronization 0~360
        ('byGainMin', C_BYTE),      # 增益下限; Gain lower limit
        ('byGainMax', C_BYTE),      # 增益上限; Gain upper limit
        ('byBacklight', C_BYTE),    # 背光补偿：取值范围取决于设备能力集：0-关闭1-启用2-指定区域背光补偿;Backlight compensation: The value range depends on the device capability set: 0-off 1-enable 2-specified area backlight compensation
        ('byAntiFlicker', C_BYTE),  # 防闪烁模式; Anti-flicker mode; 0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁
        ('byDayNightColor', C_BYTE),# 日/夜模式；0-总是彩色，1-根据亮度自动切换，2-总是黑白;Day/night mode; 0-always color, 1-automatically switch according to brightness, 2-always black and white
        ('byExposureMode', C_BYTE), # 曝光模式调节 曝光等级为自动曝光时有效，取值：0-默认自动，1-增益优先，2-快门优先; Exposure mode adjustment The exposure level is effective when the exposure level is automatic exposure, value: 0-default automatic, 1-gain priority, 2-shutter priority
        ('byRotate90', C_BYTE),     # 0-不旋转，1-顺时针90°，2-逆时针90°; 0-No rotation, 1-90°clockwise, 2-90°counterclockwise
        ('bMirror', c_bool),        # 镜像; Mirroring
        ('byWideDynamicRange', C_BYTE), # 宽动态值 0-关闭，1~100-为真实范围值; Wide dynamic value, 0-closed, 1~100-is the true range value
        ('byGlareInhibition', C_BYTE),  # 强光抑制 0-关闭， 1~100为范围值; Strong light suppression 0-off, 1~100 is the range value
        ('stuBacklightRegion', CFG_RECT),# 背光补偿区域; Backlight compensation area
        ('byFocusMode', C_BYTE),    # 0-关闭，1-辅助聚焦，2-自动聚焦; 0-off, 1-assisted focus, 2-auto focus
        ('bFlip', c_bool),          # 翻转; Flip
        ('reserved', C_BYTE*74)     # 保留; reserved
    ]

class CFG_VIDEO_IN_OPTIONS(Structure):
    """
     视频输入前端选项(对应 CFG_CMD_TYPE.VideoInOptions); Video input front-end options (corresponding CFG_CMD_TYPE.VideoInOptions)
    """
    _fields_ = [
        ('byBacklight', C_BYTE),    # 背光补偿：取值范围取决于设备能力集：0-关闭1-启用2-指定区域背光补偿;Backlight compensation: The value range depends on the device capability set: 0-off 1-enable 2-specified area backlight compensation
        ('byDayNightColor', C_BYTE),# 日/夜模式；0-总是彩色，1-根据亮度自动切换，2-总是黑白;Day/night mode; 0-always color, 1-automatically switch according to brightness, 2-always black and white
        ('byWhiteBalance', C_BYTE), # 白平衡;White balance 0-"Disable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byColorTemperature', C_BYTE), # 色温等级, 白平衡为"CustomColorTemperature"模式下有效;Color temperature level, white balance is valid in "CustomColorTemperature" mode
        ('bMirror', c_bool),        # 镜像; Mirroring
        ('bFlip', c_bool),          # 翻转; Flip
        ('bIrisAuto', c_bool), # 自动光圈; Auto iris
        ('bInfraRed', c_bool), # 根据环境光自动开启红外补偿灯; Automatically turn on the infrared compensation light according to the ambient light
        ('byGainRed', C_BYTE), # 红色增益调节，白平衡为"Custom"模式下有效 0~100;Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),# 蓝色增益调节，白平衡为"Custom"模式下有效 0~100;Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),# 绿色增益调节，白平衡为"Custom"模式下有效 0~100;Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE), # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float), # 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float), # 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('bGainAuto', c_bool),  # 自动增益; Automatic gain
        ('byGain', C_BYTE),     # 增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('bySignalFormat', C_BYTE), # 信号格式, 0-Inside(内部输入) 1-BT656 2-720p 3-1080p  4-1080i  5-1080sF; Signal format, 0-Inside (internal input) 1-BT656 2-720p 3-1080p 4-1080i 5-1080sF
        ('byRotate90', C_BYTE), # 0-不旋转，1-顺时针90°，2-逆时针90°; 0-No rotation, 1-90°clockwise, 2-90°counterclockwise
        ('fExternalSyncPhase', c_float), # 外同步的相位设置 0~360; Phase setting of external synchronization 0~360
        ('byExternalSync', C_BYTE), # 外部同步信号输入,0-内部同步 1-外部同步; External synchronization signal input, 0-internal synchronization 1-external synchronization
        ('bySwitchMode', C_BYTE), # 0-不切换，总是使用白天配置；1-根据亮度切换；2-根据时间切换；3-不切换，总是使用夜晚配置；4-使用普通配置;
                                  # 0-Do not switch, always use day configuration; 1- Switch according to brightness; 2- Switch according to time; 3- Don’t switch, always use night configuration; 4- Use normal configuration
        ('byDoubleExposure', C_BYTE), # 双快门, 0-不启用，1-双快门全帧率，即图像和视频只有快门参数不同，2-双快门半帧率，即图像和视频快门及白平衡参数均不同;
                                      # Double shutter, 0-not enabled, 1-double shutter full frame rate, that is, only the shutter parameters are different for image and video, 2-double shutter half frame rate, that is, the image and video shutter and white balance parameters are different
        ('byWideDynamicRange', C_BYTE), # 宽动态值; Wide dynamic value
        ('stuNightOptions', CFG_VIDEO_IN_NIGHT_OPTIONS),    # 夜晚参数; Night parameters
        ('stuFlash', CFG_FLASH_CONTROL),                    # 闪光灯配置; Flash configuration
        ('stuSnapshot', CFG_VIDEO_IN_SNAPSHOT_OPTIONS),     # 抓拍参数, 双快门时有效; Snapshot parameters, valid when double shutter
        ('stuFishEye', CFG_FISH_EYE),                       # 鱼眼镜头; Fisheye lens
        ('byFocusMode', C_BYTE),    # 0-关闭，1-辅助聚焦，2-自动聚焦; 0-off, 1-assisted focus, 2-auto focus
        ('reserved', C_BYTE*28),    # 保留; reserved
        ('byGainMin', C_BYTE),      # 增益下限; Gain lower limit
        ('byGainMax', C_BYTE),      # 增益上限; Gain upper limit
        ('byAntiFlicker', C_BYTE),  # 防闪烁模式; Anti-flicker mode; 0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁
        ('byExposureMode', C_BYTE), # 曝光模式调节 曝光等级为自动曝光时有效，取值：0-默认自动，1-增益优先，2-快门优先,4-手动;
                                    # Exposure mode adjustment. The exposure level is effective when the exposure level is automatic. Values: 0-default automatic, 1-gain priority, 2-shutter priority, 4-manual
        ('byGlareInhibition', C_BYTE),  # 强光抑制 0-关闭， 1~100为范围值; Strong light suppression 0-off, 1~100 is the range value
        ('stuBacklightRegion', CFG_RECT),  # 背光补偿区域; Backlight compensation area
        ('stuNormalOptions', CFG_VIDEO_IN_NORMAL_OPTIONS), # 普通参数; Common parameters
    ]

class NET_VIDEOIN_EXPOSURE_SHUTTER_INFO(Structure):
    """
    GetConfig和SetConfig接口,曝光快门属性配置; GetConfig and SetConfig interfaces,Exposure shutter property configuration
    """
    _fields_ = [
        ('dwSize',C_DWORD),         # 结构体大小; struct size
        ('bAutoSyncPhase', C_BOOL), # 自动相位调节使能; Automatic phase adjustment enable
        ('fShutter', c_float),      # 快门值，AutoSyncPhase为true时有效，毫秒为单位，取值0.1ms~80ms; Shutter value, valid when AutoSyncPhase is true, in milliseconds, the value is 0.1ms~80ms
                                    # 且必须不小于NET_VIDEOIN_EXPOSURE_NORMAL_INFO中的"ExposureValue1"、不大于"ExposureValue2"; And must be no less than "ExposureValue1" and no greater than "ExposureValue2" in NET_VIDEOIN_EXPOSURE_NORMAL_INFO
        ('nPhase', c_int),          # 相位值,取值0~360°; Phase value, value is 0~360°
    ]

class CFG_THERMO_GAIN(Structure):
    """
    增益设置; Gain setting
    """
    _fields_ = [
        ('nAgc', c_int),        # 自动增益控制 [0-255]具体取值范围由能力决定; Automatic gain control [0-255] The specific value range is determined by the ability
        ('nAgcMaxGain', c_int), # 最大自动增益 [0-255]具体取值范围由能力决定; Maximum automatic gain [0-255] The specific value range is determined by the ability
        ('nAgcPlateau', c_int), # 增益均衡 具体取值范围由能力决定; Gain equalization The specific value range is determined by ability
    ]

class CFG_THERMO_AUTO_GAIN(Structure):
    """
    热成像自动增益设置; Thermal imaging automatic gain setting
    """
    _fields_ = [
        ('nLowToHigh', c_int),  # 温度超过此设定值时，自动切换到高温模式; When the temperature exceeds this set value, it will automatically switch to high temperature mode
        ('nLHROI', c_int),      # 由低温切换到高温时的ROI 百分比0~100; ROI percentage when switching from low temperature to high temperature 0~100
        ('nHighToLow', c_int),  # 温度下降到此设定值时，自动切换到低温模式; When the temperature drops to this set value, it will automatically switch to low temperature mode
        ('nHLROI', c_int),      # 由高温切换到低温时的ROI 百分比0~100; ROI percentage when switching from high temperature to low temperature 0~100
    ]

class CFG_THERMOGRAPHY_OPTION(Structure):
    """
    热成像配置，单个模式的配置; Thermal imaging configuration, single mode configuration
    """
    _fields_ = [
        ('nEZoom', c_int),      # 倍数; multiple
        ('nThermographyGamma', c_int),  # 伽马值; Gamma value
        ('nColorization', c_int),       # 伪彩色，见 NET_THERMO_COLORIZATION; Pseudo color, see NET_THERMO_COLORIZATION
        ('nSmartOptimizer', c_int),     # 智能场景优化指数 0 ~100， 具体取值范围由能力决定; Intelligent scene optimization index 0 ~ 100, the specific value range is determined by ability
        ('bOptimizedRegion', C_BOOL),   # 是否开启感兴趣区域，只有感兴趣区域内的信息会被纳入统计用来做自动亮度调整（AGC）; Whether to enable the area of interest, only the information in the area of interest will be included in the statistics for automatic brightness adjustment (AGC)
        ('nOptimizedROIType', c_int),   # 感兴趣区域类型，见 NET_THERMO_ROI; Type of region of interest, see NET_THERMO_ROI
        ('nCustomRegion', c_int),       # 自定义区域个数; Number of custom regions
        ('stCustomRegions', NET_RECT*64),# 自定义区域，仅在 nOptimizedROIType 为 NET_THERMO_ROI_CUSTOM 时有效; Custom area, only valid when nOptimizedROIType is NET_THERMO_ROI_CUSTOM
        ('Reserved', c_char*256),       # 保留; reserved
        ('stuLowTempGain', CFG_THERMO_GAIN),    # 低温下的增益设置; Gain setting at low temperature
        ('nGainMode', c_int),                   # 增益模式，参见 CFG_THERMO_GAIN_MODE; Gain mode, see CFG_THERMO_GAIN_MODE
        ('stAutoGain', CFG_THERMO_AUTO_GAIN),   # 自动增益设置，只在增益模式为 CFG_THERMO_GAIN_MODE_AUTO 有效; Automatic gain setting, only valid when the gain mode is CFG_THERMO_GAIN_MODE_AUTO
        ('stuHighTempGain', CFG_THERMO_GAIN),   # 高温下的增益设置; Gain setting at high temperature
        ('nBaseBrightness', c_int),             # 基准亮度; Reference brightness
        ('nStretchIntensity', c_int),           # 拉伸强度; Tensile Strength
        ('stuContrastRect', NET_RECT),          # 区域增强位置,增加本区域与周边的对比度,8192坐标系; Area enhancement position, increase the contrast between this area and the surrounding area, 8192 coordinate system
    ]

class CFG_THERMOGRAPHY_INFO(Structure):
    """
    热成像配置; Thermal imaging configuration
    """
    _fields_ = [
        ('nModeCount', c_int),                      # 模式个数，目前只有一个; The number of modes, currently there is only one
        ('stOptions', CFG_THERMOGRAPHY_OPTION * 16),# 对应不同模式的配置; Corresponding to the configuration of different modes
    ]

class PTZ_LOCATION_SPEED_UNIT(Structure):
    """
    云台控制坐标,速度单元; PTZ control coordinates, speed unit
    """
    _fields_ = [
        ('nSpeedX', c_int),     # 云台水平角速度的真实值,无范围限定(超过云台最大速度时以云台最大速度移动),左为负、右为正,1000代表10°/s，扩大100倍表示
                                # The true value of the horizontal angular velocity of the gimbal, unlimited range (when the maximum speed of the gimbal is exceeded, it will move at the maximum speed of the gimbal), the left is negative, the right is positive, 1000 represents 10°/s, and it is enlarged by 100 times.
        ('nSpeedY', c_int),     # 云台垂直角速度的真实值,无范围限定(超过云台最大速度时以云台最大速度移动),上为负、下为正,1000代表10°/s，扩大100倍表示
                                # The true value of the vertical angular velocity of the gimbal, unlimited range (when the maximum speed of the gimbal is exceeded, it will move at the maximum speed of the gimbal), the upper is negative, the lower is positive, 1000 represents 10°/s, and it is expressed by a factor of 100
        ('szReserve', c_char*32)# 预留字节; Reserved byte
    ]

class PTZ_CONTROL_INTELLI_TRACKMOVE(Structure):
    """
    云台连续移动,枪球联动专用结构. 对应操作 DH_EXTPTZ_INTELLI_TRACKMOVE; The gimbal moves continuously, and the gun-ball linkage is a special structure. Corresponding operation DH_EXTPTZ_INTELLI_TRACKMOVE
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size;
        ('nChannelID', c_int),  # 通道号; Channel number
        ('nFlag', c_int),       # 移动标识位; Mobile logo
                                # 0:起始locate定位使用,speed速度无效,position的变倍值有效; 0: The initial locate is used, the speed is invalid, and the zoom value of position is valid
                                # 1:持续跟踪移动使用,speed速度无效,position的变倍值无效; 1: Continue to track and move, the speed speed is invalid, and the position zoom value is invalid
                                # 2:持续跟踪移动使用,speed速度有效,position的变倍值无效; 2: Continue to track the use of movement, the speed speed is valid, and the position zoom value is invalid
        ('stuPosition', PTZ_SPACE_UNIT),        # 云台绝对移动位置; Absolute moving position of gimbal
        ('stuSpeed', PTZ_LOCATION_SPEED_UNIT)   # 云台运行速度; PTZ operating speed
    ]


class NET_RADIOMETRY_METADATA(Structure):
    """
    热图元数据信息; Heat map metadata information
    """
    _fields_ = [
        ('nHeight', c_int),     # 高; height
        ('nWidth', c_int),      # 宽; width
        ('nChannel', c_int),    # 通道; channels
        ('stTime', NET_TIME),   # 获取数据时间; Time to get data
        ('nLength', c_int),     # 数据大小; data len
        ('szSensorType', c_char * 64),  # 机芯类型; Movement type
        ('nUnzipParamR', c_int),    # 解压缩参数R; Decompression parameter R
        ('nUnzipParamB', c_int),    # 解压缩参数B; Decompression parameter B
        ('nUnzipParamF', c_int),    # 解压缩参数F; Decompression parameter F
        ('nUnzipParamO', c_int),    # 解压缩参数O; Decompression parameter O
        ('Reserved', c_char * 256), # 保留字节;byte reserved
    ]

class NET_RADIOMETRY_DATA(Structure):
    """
    fRadiometryAttachCB 回调使用,热图数据; fRadiometryAttachCB callback use, heat map data
    """
    _fields_ = [
        ('stMetaData', NET_RADIOMETRY_METADATA), # 元数据; Metadata
        ('pbDataBuf', c_char_p),  # 热图数据缓冲区（压缩过的数据,里面是每个像素点的温度数据,可以使用元数据信息解压）;Heat map data buffer (compressed data, which contains the temperature data of each pixel, which can be decompressed using metadata information)
        ('dwBufSize', C_DWORD), # 热图数据缓冲区大小; Heat map data buffer size
        ('reserved', c_char * 512), # 保留字节;byte reserved
    ]

class NET_IN_RADIOMETRY_ATTACH(Structure):
    """
    CLIENT_RadiometryAttach 入参 ; CLIENT_RadiometryAttach input
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('nChannel', c_int),    # 视频通道号 -1 表示全部; Video channel number, -1 means all
        ('cbNotify', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_RADIOMETRY_DATA), c_int, C_LDWORD)),  # 状态回调函数指针; State callback function pointer
        ('dwUser', C_LDWORD),   # 用户数据; user data
    ]

class NET_OUT_RADIOMETRY_ATTACH(Structure):
    """
    CLIENT_RadiometryAttach 出参 ; CLIENT_RadiometryAttach output
    """
    _fields_ = [
        ('dwSize', C_DWORD)  # 结构体大小; Struct size
    ]

class NET_IN_RADIOMETRY_FETCH(Structure):
    """
    CLIENT_RadiometryFetch 入参; CLIENT_RadiometryFetch input
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('nChannel', c_int)     # 通道号, 通道号要与订阅时一致, -1除外; Channel number, the channel number should be the same as when subscribing, except -1
    ]

class NET_OUT_RADIOMETRY_FETCH(Structure):
    """
    CLIENT_RadiometryFetch 出参; CLIENT_RadiometryFetch output
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('nStatus', c_int)      # 0: 未知, 1: 空闲, 2: 获取热图中; 0: unknown, 1: idle, 2: get heat map
    ]

class CFG_RADIOMETRY_ALARMSETTING(Structure):
    """
    测温点报警设置; Temperature measuring point alarm setting
    """
    _fields_ = [
        ('nId', c_int), # 报警唯一编号 报警编号统一编码
        ('bEnable', C_BOOL),        # 是否开启该点报警
        ('nResultType', c_int),     # 测温报警结果类型，见 CFG_STATISTIC_TYPE，可取值
                                    # 点测温：具体值
                                    # 线测温：最大, 最小, 平均
                                    # 区域测温：最大, 最小, 平均, 标准, 中间, ISO
        ('nAlarmCondition', c_int), # 报警条件，见 CFG_COMPARE_RESULT
        ('fThreshold', c_float),    # 报警阈值温度 浮点数
        ('fHysteresis', c_float),   # 温度误差，浮点数，比如0.1 表示正负误差在0.1范围内
        ('nDuration', c_int)        # 阈值温度持续时间	单位：秒
    ]

class CFG_RADIOMETRY_LOCALPARAM(Structure):
    """
    测温规则本地参数配置; Local parameter configuration of temperature measurement rules
    """
    _fields_ = [
        ('bEnable', C_BOOL),    # 是否启用本地配置
        ('fObjectEmissivity', c_float), # 目标辐射系数 浮点数 0~1
        ('nObjectDistance', c_int),     # 目标距离
        ('nRefalectedTemp', c_int),     # 目标反射温度
    ]

class CFG_RADIOMETRY_RULE(Structure):
    """
    测温规则; Temperature measurement rules
    """
    _fields_ = [
        ('bEnable', C_BOOL),    # 测温使能
        ('nPresetId', c_int),   # 预置点编号
        ('nRuleId', c_int),     # 规则编号
        ('szName', c_char * 128), # 自定义名称
        ('nMeterType', c_int),  # 测温模式的类型，见 NET_RADIOMETRY_METERTYPE
        ('stCoordinates', CFG_POLYGON * 64), # 测温点坐标	使用相对坐标体系，取值均为0~8191
        ('nCoordinateCnt', c_int),  # 测温点坐标实际个数
        ('nSamplePeriod', c_int),   # 温度采样周期 单位 : 秒
        ('stAlarmSetting', CFG_RADIOMETRY_ALARMSETTING * 64),   # 测温点报警设置
        ('nAlarmSettingCnt', c_int), # 测温点报警设置实际个数
        ('stLocalParameters', CFG_RADIOMETRY_LOCALPARAM),   # 本地参数配置
        ('emAreaSubType', C_ENUM),     # 区域测温的子类型 EM_CFG_AREA_SUBTYPE
    ]

class CFG_RADIOMETRY_RULE_INFO(Structure):
    """
    测温规则配置结构; Temperature measurement rule configuration structure
    """
    _fields_ = [
        ('nCount', c_int),      # 规则个数; rule number
        ('stRule', CFG_RADIOMETRY_RULE * 512)   # 测温规则; Temperature measurement rules
    ]

class NET_COAXIAL_CONTROL_IO_INFO(Structure):
    """
    同轴IO信息结构体; Coaxial IO information structure
    """
    _fields_ = [
        ('emType', C_ENUM),     # 同轴IO控制类型 0:未知 1:白光灯 2:speak音频; Coaxial IO control type 0: unknown 1: white light 2: speak audio
        ('emSwicth', C_ENUM),   # 同轴IO控制开关 0:未知 1:开 2:关; Coaxial IO control switch 0: unknown 1: on 2: off
        ('emMode', C_ENUM),     # 同轴IO触发方式 0:未知 1:联动触发 2:手动触发; Coaxial IO trigger mode 0: unknown 1: linkage trigger 2: manual trigger
        ('byReserved', C_BYTE * 128),   # 预留字节; Reserved;
    ]

class NET_IN_CONTROL_COAXIAL_CONTROL_IO(Structure):
    """
    发送同轴IO控制命令, CLIENT_ControlDeviceEx 入参 对应 DH_CTRL_COAXIAL_CONTROL_IO;
    Send coaxial IO control command, CLIENT_ControlDeviceEx input parameter corresponds to DH_CTRL_COAXIAL_CONTROL_IO
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size;
        ('nChannel', c_int),    # 通道号; channel
        ('nInfoCount', c_int),  # 同轴IO信息个数; Number of coaxial IO information
        ('stInfo', NET_COAXIAL_CONTROL_IO_INFO * 8), # 同轴IO信息; coaxial IO information
    ]

class NET_OUT_CONTROL_COAXIAL_CONTROL_IO(Structure):
    """
    发送同轴IO控制命令, CLIENT_ControlDeviceEx 出参 对应 DH_CTRL_COAXIAL_CONTROL_IO;
    Send coaxial IO control command, CLIENT_ControlDeviceEx output parameter corresponds to DH_CTRL_COAXIAL_CONTROL_IO
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
    ]

class NET_IN_GET_SOFTWAREVERSION_INFO(Structure):
    """
    CLIENT_GetSoftwareVersion 入参; CLIENT_GetSoftwareVersion input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
    ]

class NET_PERIPHERAL_VERSIONS(Structure):
    """
    设备的外设软件版本; Peripheral software version of the device
    """
    _fields_ = [
        ('szVersion', c_char * 32),     # 对应外设的版本信息; Corresponding peripheral version information
        ('emPeripheralType', C_ENUM),   # 外设类型; Peripheral type
        ('byReserved', C_BYTE * 252),   # 预留字节; Reserved
    ]

class NET_OUT_GET_SOFTWAREVERSION_INFO(Structure):
    """
    CLIENT_GetSoftwareVersion 出参; CLIENT_GetSoftwareVersion output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
        ('szVersion', c_char * 64),     # 软件版本; software version
        ('stuBuildDate', NET_TIME),     # 日期; date
        ('szWebVersion', c_char * 16),  # web软件信息; web software version
        ('szSecurityVersion', c_char * 64),# 安全基线版本; Security Baseline Version
        ('nPeripheralNum', c_int),      # 返回的外设数量; Number of peripherals returned
        ('stuPeripheralVersions', NET_PERIPHERAL_VERSIONS * 32),    # 设备的外设软件版本; Peripheral software version of the device
    ]

class CFG_NTP_SERVER(Structure):
    """
    NTP服务器; ntp server
    """
    _fields_ = [
        ('bEnable', C_BOOL),    # enable
        ('szAddress', c_char * 256),    # IP地址或网络名; IP address or network name
        ('nPort', c_int),       # 端口号; port
    ]

class CFG_NTP_INFO(Structure):
    """
    时间同步服务器配置; Time synchronization server configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),        # 使能开关; enable switch
        ('szAddress', c_char * 256),# IP地址或网络名; IP address or network name
        ('nPort', c_int),           # 端口号; port
        ('nUpdatePeriod', c_int),   # 更新周期 单位为分钟; Update cycle, in minutes
        ('emTimeZoneType', C_ENUM), # 时区; time zone
        ('szTimeZoneDesc', c_char * 128),# 时区描述; time zone description
        ('nSandbyServerNum', c_int),    # 实际备用NTP服务器个数; Actual number of backup NTP servers
        ('stuStandbyServer', CFG_NTP_SERVER * 4), # 备选NTP服务器地址; Alternative NTP server address
        ('nTolerance', c_int),      # (机器人使用)表示设置的时间和当前时间的容差，单位为秒，如果设置的时间和当前的时间在容差范围内，则不更新当前时间。0 表示每次都修改
                                    # (Used by the robot) indicates the tolerance between the set time and the current time, in seconds.
                                    # If the set time and the current time are within the tolerance range, the current time will not be updated.0 means modify every time
    ]

class DH_VERSION_INFO(Structure):
    """
    设备软件版本信息,高16位表示主版本号,低16位表示次版本号
    Device software version information, the upper 16 bits represent the major version number, and the lower 16 bits represent the minor version number
    """
    _fields_ = [
        ('dwSoftwareVersion', C_DWORD),
        ('dwSoftwareBuildDate', C_DWORD),
        ('dwDspSoftwareVersion', C_DWORD),
        ('dwDspSoftwareBuildDate', C_DWORD),
        ('dwPanelVersion', C_DWORD),
        ('dwPanelSoftwareBuildDate', C_DWORD),
        ('dwHardwareVersion', C_DWORD),
        ('dwHardwareDate', C_DWORD),
        ('dwWebVersion', C_DWORD),
        ('dwWebBuildDate', C_DWORD),
    ]

class DH_DSP_ENCODECAP(Structure):
    """
    DSP能力描述,对应CLIENT_GetDevConfig接口; DSP capability description, corresponding to the CLIENT_GetDevConfig interface
    """
    _fields_ = [
        ('dwVideoStandardMask', C_DWORD),   # 视频制式掩码,按位表示设备能够支持的视频制式; Video format mask, bitwise indicates the video format that the device can support
        ('dwImageSizeMask', C_DWORD),       # 分辨率掩码,按位表示设备能够支持的分辨率设置; Resolution mask, bitwise representation of the resolution settings that the device can support
        ('dwEncodeModeMask', C_DWORD),      # 编码模式掩码,按位表示设备能够支持的编码模式设置; Encoding mode mask, bitwise indicates the encoding mode settings that the device can support
        ('dwStreamCap', C_DWORD),           # 按位表示设备支持的多媒体功能; A bitwise representation of the multimedia features supported by the device
                                            # 第一位表示支持主码流; The first bit indicates that the main stream is supported
                                            # 第二位表示支持辅码流1; The second digit indicates that auxiliary stream 1 is supported
                                            # 第三位表示支持辅码流2; The third digit indicates that auxiliary stream 2 is supported
                                            # 第五位表示支持jpg抓图; The fifth digit indicates that jpg snapshots are supported
        ('dwImageSizeMask_Assi', C_DWORD * 8), # 表示主码流为各分辨率时,支持的辅码流分辨率掩码; Indicates the supported sub-stream resolution mask when the primary stream is each resolution
        ('dwMaxEncodePower', C_DWORD),      # DSP支持的最高编码能力; Highest encoding capability supported by DSP
        ('wMaxSupportChannel', C_DWORD),    # 每块DSP支持最多输入视频通道数; Each DSP supports the maximum number of input video channels
        ('wChannelMaxSetSync', C_DWORD),    # DSP每通道的最大编码设置是否同步；0：不同步,1：同步;
                                            # Whether the maximum encoding setting of each channel of DSP is synchronized; 0: not synchronized, 1: synchronized
    ]

class DHDEV_SYSTEM_ATTR_CFG(Structure):
    """
    系统信息; system message
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size
        # 下面是设备的只读部分; Below is the read-only part of the device
        ('stVersion', DH_VERSION_INFO),
        ('stDspEncodeCap', DH_DSP_ENCODECAP), # DSP能力描述; DSP Capability Description
        ('szDevSerialNo', C_BYTE * 48),         # 序列号; serial number
        ('byDevType', C_BYTE),                  # 设备类型,见枚举NET_DEVICE_TYPE; Device type, see enumeration NET_DEVICE_TYPE
        ('szDevType', C_BYTE * 32),             # 设备详细型号,字符串格式,可能为空; The detailed model of the device, in string format, may be empty
        ('byVideoCaptureNum', C_BYTE),          # 视频口数量; Number of video ports
        ('byAudioCaptureNum', C_BYTE),          # 音频口数量; Number of audio ports
        ('byTalkInChanNum', C_BYTE),            # 对讲输入接口数量; Number of intercom input interfaces
        ('byTalkOutChanNum', C_BYTE),           # 对讲输出接口数量; Number of intercom output interfaces
        ('byDecodeChanNum', C_BYTE),            # NSP
        ('byAlarmInNum', C_BYTE),               # 报警输入口数; Number of alarm input ports
        ('byAlarmOutNum', C_BYTE),              # 报警输出口数; Number of alarm output ports
        ('byNetIONum', C_BYTE),                 # 网络口数; Number of network ports
        ('byUsbIONum', C_BYTE),                 # USB口数量; Number of usb ports
        ('byIdeIONum', C_BYTE),                 # IDE数量; Number of IDE
        ('byComIONum', C_BYTE),                 # 串口数量; Number of serial ports
        ('byLPTIONum', C_BYTE),                 # 并口数量; Number of parallel ports
        ('byVgaIONum', C_BYTE),                 # NSP
        ('byIdeControlNum', C_BYTE),            # NSP
        ('byIdeControlType', C_BYTE),           # NSP
        ('byCapability', C_BYTE),               # NSP,扩展描述; NSP, Extended Description
        ('byMatrixOutNum', C_BYTE),             # 视频矩阵输出口数; Number of video matrix output ports
        # 下面是设备的可写部分; Below is the writable part of the device
        ('byOverWrite', C_BYTE),                # 硬盘满处理方式(覆盖、停止); Disk full processing method (overwrite, stop)
        ('byRecordLen', C_BYTE),                # 录象打包长度; Video Packing Length
        ('byDSTEnable', C_BYTE),                # 是否实行夏令时 1-实行 0-不实行; Whether to implement daylight saving time 1-implement 0-do not implement
        ('wDevNo', c_short),                    # 设备编号,用于遥控; Device number, for remote control
        ('byVideoStandard', C_BYTE),            # 视频制式:0-PAL,1-NTSC; Video format: 0-PAL, 1-NTSC
        ('byDateFormat', C_BYTE),               # 日期格式; date format
        ('byDateSprtr', C_BYTE),                # 日期分割符(0：".",1："-",2："/"); date separator(0：".",1："-",2："/")
        ('byTimeFmt', C_BYTE),                  # 时间格式 (0-24小时,1－12小时); Time format (0-24 hours, 1-12 hours)
        ('byLanguage', C_BYTE),                 # 枚举值详见DH_LANGUAGE_TYPE; 枚举值详见DH_LANGUAGE_TYPE
    ]

class AV_CFG_ChannelName(Structure):
    """
    通道名称; channel name
    """
    _fields_ = [
        ('nStructSize', c_int),
        ('nSerial', c_int),             # 摄像头唯一编号; camera unique number
        ('szName', c_char * 256),       # 通道名; channel name
    ]

class NET_GPS_STATUS_INFO(Structure):
    """
    GPS状态信息; GPS statu information
    """
    _fields_ = [
        ('revTime', NET_TIME),  # 定位时间; time;
        ('DvrSerial', c_char * 50),  # 设备序列号; device number;
        ('byRserved1', C_BYTE * 6),  # 对齐字节; align;
        ('longitude', c_double),  # 经度(单位是百万分之度,范围0-360度); longitude(1/1000000,range[0-360]);
        ('latidude', c_double),  # 纬度(单位是百万分之度,范围0-180度); latitude(1/1000000,range[0-180]);
        ('height', c_double),  # 高度(米); highness(m);
        ('angle', c_double),  # 方向角(正北方向为原点,顺时针为正); angle(north is source point,clockwise is positive);
        ('speed', c_double),  # 速度(单位km/H); speed(sea mile,speed/1000*1.852km/h);
        ('starCount', c_uint16),  # 定位星数, emDateSource为 EM_DATE_SOURCE_GPS时有效; star count;
        ('byRserved2', C_BYTE * 2),  # 对齐字节; align;
        ('antennaState', C_ENUM),  # 天线状态, emDateSource为 EM_DATE_SOURCE_GPS时有效,参考枚举NET_THREE_STATUS_BOOL; antenna state(true good, false bad) valid when emDateSource is EM_DATE_SOURCE_GPS,Please refer to NET_THREE_STATUS_BOOL;
        ('orientationState', C_ENUM),   # 定位状态; positioning status
        ('workStae', c_int),  # 工作状态(0=未定位,1=非差分定位,2=差分定位,3=无效PPS,6=正在估算,emDateSource为 EM_DATE_SOURCE_GPS时有效; working state(true normal, false abnormity),valid when emDateSource is EM_DATE_SOURCE_GPS;
        ('nAlarmCount', c_int),  # 发生的报警位置个数; alarm count;
        ('nAlarmState', c_int * 128),  # 发生的报警位置,值可能多个, emDateSource为 EM_DATE_SOURCE_GPS时有效; alarm type valid when emDateSource is EM_DATE_SOURCE_GPS;
        ('bOffline', C_BYTE),  # 0-实时 1-补传; 0- real time 1-fill;
        ('bSNR', C_BYTE),  # GPS信噪比,表示GPS信号强度,值越大,信号越强 范围：0~100,0表示不可用; SNR for GPS, range: 0~100, 0 for unusable;
        ('byRserved3', C_BYTE * 2),  # 对齐字节; align;
        ('emDateSource', C_ENUM),  # 数据来源,参考枚举EM_DATE_SOURCE; source of date,Please refer to EM_DATE_SOURCE;
        ('byRserved', C_BYTE * 124),  # 保留字节; reserved bytes;
    ]

class ALARM_FRONTDISCONNET_INFO(Structure):
    """
    前端断网报警信息; Front-end disconnection alarm information
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size
        ('nChannelID', c_int),  # 通道号; channel number
        ('nAction', c_int),     # 0:开始 1:停止; 0:start 1:stop
        ('stuTime', NET_TIME),  # 事件发生时间; event time
        ('szIpAddress', c_char * 260), # 前端IPC的IP地址; IP address of the front-end IPC
        ('stGPSStatus', NET_GPS_STATUS_INFO), # GPS信息; GPS information
    ]

class ALARM_STORAGE_LOW_SPACE_INFO(Structure):
    """
    存储容量不足事件; Insufficient storage capacity event
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nAction', c_int),  # 0:开始 1:停止; 0:start 1:stop;
        ('szName', c_char * 128),  # 事件名称; name;
        ('szDevice', c_char * 128),  # 存储设备名称; device name;
        ('szGroup', c_char * 128),  # 存储组名称; group name;
        ('nTotalSpace', c_int64),  # 总容量, byte; total space byte;
        ('nFreeSpace', c_int64),  # 剩余容量, byte; free space byte;
        ('nPercent', c_int),  # 已经使用的百分比; used percent;
        ('stuTime', NET_TIME_EX),  # 事件触发时间; Event occurrence time;
        ('stGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息; GPS info;
    ]

class ALARM_STORAGE_FAILURE(Structure):
    """
    存储异常报警; Storage exception alarm
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
        ('ActionType', C_UINT),  # 0：停止, 1：开始; 0:stop 1:start;
        ('szProtocol', c_char * 128),  # 协议类型,目前只支持FTP; protocol type;
        ('szServerAddr', c_char * 64),  # 服务器IP地址; server device's ip;
        ('dwPort', C_DWORD),  # 端口号; port number;
        ('stuTime', NET_TIME),  # 事件发生时间; event happen time;
        ('nChannel', c_int),  # 通道号, 从1开始, 0表示不区分通道; channel, from 1, 0 means does not distinguish;
    ]

class ALARM_RECORD_CHANGED_INFO_EX(Structure):
    """
    录像状态变化报警(DH_ALARM_RECORD_CHANGED_EX); Recording state change alarm (DH_ALARM_RECORD_CHANGED_EX)
    """
    _fields_ = [
        ('nAction', c_int),  # 0:开始 1:停止; 0:start 1:stop;
        ('nChannel', c_int),  # 通道; channel;
        ('szStoragePoint', c_char * 64),  # 录像存储点; StoragePoint;
        ('emStreamType', C_ENUM),  # 录像码流,参考枚举NET_STREAM_TYPE; stream type,Please refer to NET_STREAM_TYPE;
        ('szUser', c_char * 128),  # 操作用户; username;
        ('byReserved', C_BYTE * 828),  # 保留; reserved;
    ]

class ALARM_REMOTE_ALARM_INFO(Structure):
    """
    远程外部报警信息; Remote external alarm information
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nChannelID', c_int),  # 通道号,从1开始; channel ID,from 1;
        ('nState', c_int),  # 报警状态,0-报警复位,1-报警置位; state,0-reset,1-setting;
    ]

class ALARM_RECORD_SCHEDULE_CHANGE_INFO(Structure):
    """
    录像计划改变事件(对应事件 DH_ALARM_RECORD_SCHEDULE_CHANGE); Recording plan change event (corresponding to event DH_ALARM_RECORD_SCHEDULE_CHANGE)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号; Channel ID;
        ('nEventID', c_int),  # 事件ID; Event ID;
        ('dbPTS', c_double),  # 时间戳(单位是毫秒); Time stamp (Unit:ms);
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('nEventAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束; Event operation. 0=pulse event.1=continues event begin. 2=continuous event stop;
        ('szUser', c_char * 128),  # 操作用户; Username;
        ('byReserved', C_BYTE * 1024),  # 保留字节; Reserved;
    ]

class NET_MEDIA_QUERY_TRAFFICCAR_PARAM_EX(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR对应的查询条件 参数扩展; Query conditions corresponding to DH_MEDIA_QUERY_TRAFFICCAR Parameter expansion
    """
    _fields_ = [
        ('szViolationCode', c_char * 16),  # 违法代码; Violation code;
        ('szCountry', c_char * 4),  # 国籍，2字节，符合ISO3166规范; Nationality, 2 bytes, in line with ISO3166 specification;
        ('byReserved', C_BYTE * 1020),  # 保留字节; Reserved;
    ]

class MEDIA_QUERY_TRAFFICCAR_PARAM(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR对应的查询条件; Query conditions corresponding to DH_MEDIA_QUERY_TRAFFICCAR
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号从0开始,-1表示查询所有通道; The channel number begins with 0. -1 is to search information of all channels .;
        ('StartTime', NET_TIME),  # 开始时间; Start time;
        ('EndTime', NET_TIME),  # 结束时间; End time;
        ('nMediaType', c_int),  # 文件类型,0:任意类型, 1:jpg图片, 2:dav文件; File type:0=search any type.1=search jpg file;
        ('nEventType', c_int),  # 事件类型,详见"智能分析事件类型", 0:表示查询任意事件,此参数废弃,请使用pEventTypes; deprecated, to get same info, use pEventType instead;
        ('szPlateNumber', c_char * 32),  # 车牌号, "\0"则表示查询任意车牌号; Vehicle plate. "\0" is to search any plate number.;
        ('nSpeedUpperLimit', c_int),  # 查询的车速范围; 速度上限 单位: km/h; The searched vehicle speed range. Max speed unit is km/h;
        ('nSpeedLowerLimit', c_int),  # 查询的车速范围; 速度下限 单位: km/h; The searched vehicle speed range. Min speed unit is km/h;
        ('bSpeedLimit', C_BOOL),  # 是否按速度查询; TRUE:按速度查询,nSpeedUpperLimit和nSpeedLowerLimit有效。; Search according to the speed or not. TRUE: search according to the speed.nSpeedUpperLimit and nSpeedLowerLimit is valid.;
        ('dwBreakingRule', C_DWORD),  # 违章类型：,当事件类型为 EVENT_IVS_TRAFFICGATE时,第一位:逆行; 第二位:压线行驶; 第三位:超速行驶;,第四位：欠速行驶; 第五位:闯红灯;,当事件类型为 EVENT_IVS_TRAFFICJUNCTION,第一位:闯红灯; 第二位:不按规定车道行驶;,第三位:逆行; 第四位：违章掉头;,第五位:压线行驶;; Illegal type:,When event type is EVENT_IVS_TRAFFICGATE,bit1: Retrograde; bit2: Overline;,bit3: Overspend; bit4:Under speed;,bit5: RunRedLight;,When event type is EVENT_IVS_TRAFFICJUNCTION,bit1: RunRedLight; bit2: WrongLan;,bit3: Retrograde; bit4:UTurn;,bit5: Overline;;
        ('szPlateType', c_char * 32),  # 车牌类型,"Unknown" 未知,"Normal" 蓝牌黑牌,"Yellow" 黄牌,"DoubleYellow" 双层黄尾牌,"Police" 警牌"Armed" ,,"Military" ,"DoubleMilitary" ,"SAR" 港澳特区号牌,"Trainning" 教练车号牌,"Personal" 个性号牌,"Agri" 农用牌,"Embassy" 使馆号牌,"Moto" 摩托车号牌,"Tractor" 拖拉机号牌,"Other" 其他号牌,"Civilaviation"民航号牌,"Black"黑牌,"PureNewEnergyMicroCar"纯电动新能源小车,"MixedNewEnergyMicroCar,"混合新能源小车,"PureNewEnergyLargeCar",纯电动新能源大车,"MixedNewEnergyLargeCar"混合新能源大车; Plate type: "Unknown" =Unknown; "Normal"=Blue and black plate. "Yellow"=Yellow plate. "DoubleYellow"=Double-layer yellow plate,"Police"=Police plate ; "Armed"; "Military"; "DoubleMilitary","SAR" =HK SAR or Macao SAR plate; "Trainning" =rehearsal plate; "Personal"=Personal plate; "Agri"=Agricultural plate,"Embassy"=Embassy plate; "Moto"=Moto plate ; "Tractor"=Tractor plate; "Other"=Other plate;
        ('szPlateColor', c_char * 16),  # 车牌颜色, "Blue"蓝色,"Yellow"黄色, "White"白色,"Black"黑色; plate color, "Blue","Yellow", "White","Black";
        ('szVehicleColor', c_char * 16),  # 车身颜色:"White"白色, "Black"黑色, "Red"红色, "Yellow"黄色, "Gray"灰色, "Blue"蓝色,"Green"绿色; vehicle color:"White", "Black", "Red", "Yellow", "Gray", "Blue","Green";
        ('szVehicleSize', c_char * 16),  # 车辆大小类型:"Light-duty":小型车;"Medium":中型车; "Oversize":大型车; "Unknown": 未知; vehicle type:"Light-duty";"Medium"; "Oversize";
        ('nGroupID', c_int),  # 事件组编号(此值>=0时有效); id of event group(it works when >= 0);
        ('byLane', c_short),  # 车道号(此值>=0时表示具体车道,-1表示所有车道,即不下发此字段); lane number(it works when >= 0);
        ('byFileFlag', C_BYTE),  # 文件标志, 0xFF-使用nFileFlagEx, 0-表示所有录像, 1-定时文件, 2-手动文件, 3-事件文件, 4-重要文件, 5-合成文件; file flag, 0xFF-use nFileFlagEx, 0-all record, 1-timing file, 2-manual, 3-event, 4-important, 5-mosaic;
        ('byRandomAccess', C_BYTE),  # 是否需要在查询过程中随意跳转,0-不需要,1-需要; The need for random jumps in the query process, 0 - no need 1 - need;
        ('nFileFlagEx', c_int),  # 文件标志, 按位表示: bit0-定时文件, bit1-手动文件, bit2-事件文件, bit3-重要文件, bit4-合成文件, bit5-黑名单图片 0xFFFFFFFF-所有录像; file flag, bit0-timing, bit1-manual, bit2-event, bit3-important, bit4-mosaic, 0xFFFFFFFF-all;
        ('nDirection', c_int),  # 车道方向（车开往的方向） 0-北 1-东北 2-东 3-东南 4-南 5-西南 6-西 7-西北 8-未知 -1-所有方向; direction(to the direction of car) 0-north 1-northeast 2-east 3-southeast 4-south 5-southwest 6-west 7-northwest 8-unknown -1-all directions;
        ('szDirs', c_void_p),  # 工作目录列表,一次可查询多个目录,为空表示查询所有目录。目录之间以分号分隔,如“/mnt/dvr/sda0;/mnt/dvr/sda1”,szDirs==null 或"" 表示查询所有; working directory list,can inquire multiple directory at a atime,separated by ";",example "/mnt/dvr/sda0;/mnt/dvr/sda1",if szDirs==null or szDirs == "" ,means search all;
        ('pEventTypes', c_void_p),  # 待查询的事件类型数组指针,事件类型,详见"智能分析事件类型",若为NULL则认为查询所有事件（缓冲需由用户申请）; Check the event type to be an array of pointers, event type, see "intelligent analysis event type", if the query is NULL considered all events (buffer required to apply by the user);
        ('nEventTypeNum', c_int),  # 事件类型数组大小; Event Type array size;
        ('pszDeviceAddress', c_void_p),  # 设备地址, NULL表示该字段不起作用; Device address, NULL indicates that the field does not work;
        ('pszMachineAddress', c_void_p),  # 机器部署地点, NULL表示该字段不起作用; Machine deployment locations, NULL indicates that the field does not work;
        ('pszVehicleSign', c_void_p),  # 车辆标识, 例如 "Unknown"-未知, "Audi"-奥迪, "Honda"-本田... NULL表示该字段不起作用; Vehicle identification, such as "Unknown" - unknown, "Audi" - Audi, "Honda" - Honda ... NULL indicates that the field does not work;
        ('wVehicleSubBrand', c_uint16),  # 车辆子品牌 需要通过映射表得到真正的子品牌 映射表详见开发手册; Specifies the sub-brand of vehicle,the real value can be found in a mapping table from the development manual;
        ('wVehicleYearModel', c_uint16),  # 车辆品牌年款 需要通过映射表得到真正的年款 映射表详见开发手册; Specifies the model years of vehicle. the real value can be found in a mapping table from the development manual;
        ('emSafeBeltState', C_ENUM),  # 安全带状态,参考枚举EM_SAFE_BELT_STATE; Safe belt state,Please refer to EM_SAFE_BELT_STATE;
        ('emCallingState', C_ENUM),  # 打电话状态,参考枚举EM_CALLING_STATE; Calling state,Please refer to EM_CALLING_STATE;
        ('emAttachMentType', C_ENUM),  # 车内饰品类型,参考枚举EM_ATTACHMENT_TYPE; Attachment type,Please refer to EM_ATTACHMENT_TYPE;
        ('emCarType', C_ENUM),  # 车辆类型,参考枚举EM_CATEGORY_TYPE; Car type,Please refer to EM_CATEGORY_TYPE;
        ('pstuTrafficCarParamEx', POINTER(NET_MEDIA_QUERY_TRAFFICCAR_PARAM_EX)),  # 参数扩展; parameter extension;
        ('bReserved', c_int * 4),  # 保留字段; Reserved field for future extension.;
    ]

class MEDIAFILE_TRAFFICCAR_INFO(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR查询出来的media文件信息; DH_MEDIA_QUERY_TRAFFICCAR查询出来的media文件信息
    """
    _fields_ = [
        ('ch', C_UINT),  # 通道号; Channel number;
        ('szFilePath', c_char * 128),  # 文件路径; File path;
        ('size', C_UINT),  # 文件长度,该字段废弃，请使用sizeEx; File length,This field is discarded,please use the sizeEx;
        ('starttime', NET_TIME),  # 开始时间; Start time;
        ('endtime', NET_TIME),  # 结束时间; End time;
        ('nWorkDirSN', C_UINT),  # 工作目录编号; Working directory serial number;
        ('nFileType', C_BYTE),  # 文件类型 1:图片 2:视频; File type. 1:picture 2:video;
        ('bHint', C_BYTE),  # 文件定位索引; File location index;
        ('bDriveNo', C_BYTE),  # 磁盘号; drive number;
        ('bReserved2', C_BYTE),  
        ('nCluster', C_UINT),  # 簇号; cluster number;
        ('byPictureType', C_BYTE),  # 图片类型或文件标记, 0-普通, 1-合成, 2-抠图。更多文件标记信息请参考 MEDIAFILE_TRAFFICCAR_INFO_EX 的 emFalgLists 字段; picture type or file flag, 0-Normal, 1-Mosaic, 2-Cutout. more flags information ref to MEDIAFILE_TRAFFICCAR_INFO_EX's filed emFalgLists;
        ('byVideoStream', C_BYTE),  # 视频码流 0-未知 1-主码流 2-辅码流1 3-辅码流2 4-辅码流; video stream 0-unknown 1-main 2-sub1 3-sub2 4-sub3;
        ('byPartition', C_BYTE),  # 精确定位号; accurate positioning No.;
        ('bReserved', C_BYTE * 1),  # 保留字段,以下是交通车辆信息; Reserved field for future extension.,The following contents is the vehicle information;
        ('szPlateNumber', c_char * 32),  # 车牌号码; Vehicle plate number;
        ('szPlateType', c_char * 32),  # 号牌类型"Unknown" 未知; "Normal" 蓝牌黑牌; "Yellow" 黄牌; "DoubleYellow" 双层黄尾牌,"Police" 警牌; "Armed" ; "Military"; "DoubleMilitary","SAR" 港澳特区号牌; "Trainning" 教练车号牌; "Personal" 个性号牌; "Agri" 农用牌,"Embassy" 使馆号牌; "Moto" 摩托车号牌; "Tractor" 拖拉机号牌; "Other" 其他号牌,"Civilaviation"民航号牌,"Black"黑牌,"PureNewEnergyMicroCar"纯电动新能源小车,"MixedNewEnergyMicroCar,"混合新能源小车,"PureNewEnergyLargeCar",纯电动新能源大车,"MixedNewEnergyLargeCar"混合新能源大车; Plate type: "Unknown" =Unknown; "Normal"=Blue and black plate. "Yellow"=Yellow plate. "DoubleYellow"=Double-layer yellow plate,"Police"=Police plate ; "Armed"; "Military"; "DoubleMilitary","SAR" =HK SAR or Macao SAR plate; "Trainning" =rehearsal plate; "Personal"=Personal plate; "Agri"=Agricultural plate,"Embassy"=Embassy plate; "Moto"=Moto plate ; "Tractor"=Tractor plate; "Other"=Other plate;
        ('szPlateColor', c_char * 16),  # 车牌颜色:"Blue","Yellow", "White","Black"; Plate color:"Blue","Yellow", "White","Black";
        ('szVehicleColor', c_char * 16),  # 车身颜色:"White", "Black", "Red", "Yellow", "Gray", "Blue","Green"; Vehicle color:"White", "Black", "Red", "Yellow", "Gray", "Blue","Green";
        ('nSpeed', c_int),  # 车速,单位Km/H; Speed. The unit is Km/H;
        ('nEventsNum', c_int),  # 关联的事件个数; Activation event amount;
        ('nEvents', c_int * 32),  # 关联的事件列表,数组值表示相应的事件,详见"智能分析事件类型"; Activation event list. The number refers to the corresponding event. Please refer to Intelligent Analytics Event Type.;
        ('dwBreakingRule', C_DWORD),  # 具体违章类型掩码,第一位:闯红灯; 第二位:不按规定车道行驶;,第三位:逆行; 第四位：违章掉头;否则默认为:交通路口事件; Detailed offense type subnet mask. The first bit means redlight offense, the second bit is illegal straight/left-turn/right-turn driving.,The third bit is the wrong way driving; the four bit is illegal U-turn. Otherwise default value is intersection accident.;
        ('szVehicleSize', c_char * 16),  # 车辆大小类型:"Light-duty":小型车;"Medium":中型车; "Oversize":大型车; Vehicle type:"Light-duty"=small;"Medium"=medium; "Oversize"=large;
        ('szChannelName', c_char * 32),  # 本地或远程的通道名称; Local or remote channel name;
        ('szMachineName', c_char * 16),  # 本地或远程设备名称; Local or remote device name;
        ('nSpeedUpperLimit', c_int),  # 速度上限 单位: km/h; up limit of speed, km/h;
        ('nSpeedLowerLimit', c_int),  # 速度下限 单位: km/h; lower limit of speed km/h;
        ('nGroupID', c_int),  # 事件里的组编号; id of event group;
        ('byCountInGroup', C_BYTE),  # 一个事件组内的抓拍张数; total count of the event group;
        ('byIndexInGroup', C_BYTE),  # 一个事件组内的抓拍序号; the index of this event;
        ('byLane', C_BYTE),  # 车道,参见MEDIA_QUERY_TRAFFICCAR_PARAM; lane number;
        ('bReserved1', C_BYTE * 21),  # 保留; reserved;
        ('stSnapTime', NET_TIME),  # 抓拍时间; snap time;
        ('nDirection', c_int),  # 车道方向,参见MEDIA_QUERY_TRAFFICCAR_PARAM; direction,MEDIA_QUERY_TRAFFICCAR_PARAM;
        ('szMachineAddress', c_char * 260),  # 机器部署地点; machine address;
        ('sizeEx', c_int64),  # 文件长度扩展，支持文件长度大于4G，单位字节; size of file extension, Support file length is greater than 4G,unit:Byte;
    ]

class NET_ATTACH_MENET_INFO(Structure):
    """
    车内饰品信息; Car interior accessories information
    """
    _fields_ = [
        ('emAttachMentType', C_ENUM),  # 车内物品类型,参考枚举EM_ATTACHMENT_TYPE; attachment type,Please refer to EM_ATTACHMENT_TYPE;
        ('bReserved1', C_BYTE * 128),  # 保留字节; Reserved;
    ]

class NET_UPLOAD_CLIENT_INFO(Structure):
    """
    客户端信息; client message
    """
    _fields_ = [
        ('szClientID', c_char * 20),  # 平台客户端的标识，当前是IPv4地址或者MAC地址; The id of clent, IPv4 address or MAC;
        ('emUploadFlag', C_ENUM),  # 平台上传标识,参考枚举EM_UPLOAD_FLAG; The upload flag of clent,Please refer to EM_UPLOAD_FLAG;
        ('stuUploadTime', NET_TIME),  # 上传到平台的UTC时间; The time to upload to clent;
        ('byReserved', C_BYTE * 64),  # 预留; Reserved bytes;
    ]

class MEDIAFILE_TRAFFICCAR_INFO_EX(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR_EX查询出来的文件信息; File information queried by DH_MEDIA_QUERY_TRAFFICCAR_EX
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('stuInfo', MEDIAFILE_TRAFFICCAR_INFO),  # 基本信息; Basic Information;
        ('szDeviceAddr', c_char * 256),  # 设备地址; Device Address;
        ('szVehicleSign', c_char * 32),  # 车辆标识, 例如 "Unknown"-未知, "Audi"-奥迪, "Honda"-本田...; Vehicle identification, such as "Unknown" - unknown, "Audi" - Audi, "Honda" - Honda ..;
        ('szCustomParkNo', c_char * 64),  # 自定义车位号（停车场用）; self defined parking space number, for parking,;
        ('wVehicleSubBrand', c_uint16),  # 车辆子品牌，需要通过映射表得到真正的子品牌; Specifies the sub-brand of vehicle,the real value can be found in a mapping table from the development manual;
        ('wVehicleYearModel', c_uint16),  # 车辆年款，需要通过映射表得到真正的年款; Specifies the model years of vehicle. the real value can be found in a mapping table from the development manual;
        ('stuEleTagInfoUTC', NET_TIME),  # 对应电子车牌标签信息中的过车时间(ThroughTime); corresponding to throughTime in electronic tag info;
        ('emFalgLists', C_ENUM * 128),  # 录像或抓图文件标志,参考枚举EM_RECORD_SNAP_FLAG_TYPE; record or snapshot file mark,Please refer to EM_RECORD_SNAP_FLAG_TYPE;
        ('nFalgCount', c_int),  # 标志总数; mark total;
        ('emSafeBelSate', C_ENUM),  # 安全带状态,参考枚举EM_SAFE_BELT_STATE; safe belt state,Please refer to EM_SAFE_BELT_STATE;
        ('emCallingState', C_ENUM),  # 打电话状态,参考枚举EM_CALLING_STATE; calling state,Please refer to EM_CALLING_STATE;
        ('nAttachMentNum', c_int),  # 车内物品个数; the count of attachment;
        ('stuAttachMent', NET_ATTACH_MENET_INFO * 8),  # 车内物品信息; attachment info;
        ('szCountry', c_char * 32),  # 车牌所属国家和地区; the country about the plate;
        ('emCarType', C_ENUM),  # 车辆类型,参考枚举EM_CATEGORY_TYPE; car type,Please refer to EM_CATEGORY_TYPE;
        ('emSunShadeState', C_ENUM),  # 遮阳板状态,参考枚举NET_SUNSHADE_STATE; sun shade state,Please refer to NET_SUNSHADE_STATE;
        ('emSmokingState', C_ENUM),  # 是否抽烟,参考枚举EM_SMOKING_STATE; smoking state,Please refer to EM_SMOKING_STATE;
        ('nAnnualInspection', c_int),  # 年检标个数; the count of annual inspections;
        ('byReserved', C_BYTE * 4),  # 字节对齐; Byte alignment;
        ('nPicIDHigh', c_int),  # PictureID高四字节; PictureID high 4 bytes;
        ('nPicIDLow', c_int),  # PictureID低四字节; PictureID low 4 bytes;
        ('stuClient1', NET_UPLOAD_CLIENT_INFO),  # 平台客户端1上传信息; The client 1 upload information;
        ('stuClient2', NET_UPLOAD_CLIENT_INFO),  # 平台客户端2上传信息; The client 2 upload information;
        ('szExtraPlateNumber', c_char * 96),  # 三地车牌; Three places license plate;
        ('nExtraPlateNumberNum', c_int),  # 车牌个数; Number of license plates;
        ('nEntranceTime', C_UINT),  # 车辆进站时间，时间格式：UTC时间(IVSS定制, 用于加油站场景); Vehicle entry time, time format: UTC time (IVSS customized, used for gas station scene);
        ('nOilTime', C_UINT),  # 车辆加油时间，时间格式：UTC时间(IVSS定制, 用于加油站场景); Vehicle refueling time, time format: UTC time (IVSS customized, used for gas station scenes);
        ('nExitTime', C_UINT),  # 车辆出站时间，时间格式：UTC时间(IVSS定制, 用于加油站场景); Vehicle exit time, time format: UTC time (IVSS customized, used for gas station scene);
    ]

class NET_IN_FIND_RECORD_PARAM(Structure):
    """
    FindRecord接口输入参数; FindRecord Interface Input Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; The Structure Size;
        ('emType', C_ENUM),  # 待查询记录类型,参考枚举EM_NET_RECORD_TYPE; The record type to query,Please refer to EM_NET_RECORD_TYPE;
        ('pQueryCondition', c_void_p),  # 查询类型对应的查询条件,由用户申请内存，根据查询记录类型，找到查询条件对应的结构体，进而确定内存大小; Query types corresponding to the query conditions,the space application by the user,according to query condition type,find corresponding structure,then ensure memory size;
    ]

class NET_OUT_FIND_RECORD_PARAM(Structure):
    """
    FindRecord接口输出参数; FindRecord Interface Output Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure Size;
        ('lFindeHandle', C_LLONG),  # 查询记录句柄,唯一标识某次查询; Query Log Handle,Uniquely identifies a certain query;
    ]

class NET_IN_FIND_NEXT_RECORD_PARAM(Structure):
    """
    FindNextRecord接口输入参数; FindNextRecord Interface Input Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure Size;
        ('lFindeHandle', C_LLONG),  # 查询句柄; Query Log Handle;
        ('nFileCount', c_int),  # 当前想查询的记录条数; The current number of records need query;
    ]

class NET_OUT_FIND_NEXT_RECORD_PARAM(Structure):
    """
    FindNextRecord接口输出参数; FindNextRecord Interface Output Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure Size;
        ('pRecordList', c_void_p),  # 记录列表,用户分配内存,根据NET_IN_FIND_RECORD_PARAM中的查询类型EM_NET_RECORD_TYPE，确定对应结构体，进入确定内存大小; Record List, the user allocates memory, ensure structure by query record type(EM_NET_RECORD_TYPE) of NET_IN_FIND_RECORD_PARAM,then ensure memory size;
        ('nMaxRecordNum', c_int),  # 最大查询列表记录数; Max list Record Number;
        ('nRetRecordNum', c_int),  # 查询到的记录条数,当查询到的条数小于想查询的条数时,查询结束; Query to the number of records, when the query to the article number less than want to query the number, end;
    ]

class NET_IN_OPERATE_TRAFFIC_LIST_RECORD(Structure):
    """
    CLIENT_OperateTrafficList 接口入参; CLIENT_OperateTrafficList interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('emOperateType', C_ENUM),  # 操作类型,参考枚举EM_RECORD_OPERATE_TYPE; Operate Type,Please refer to EM_RECORD_OPERATE_TYPE;
        ('emRecordType', C_ENUM),  # 要操作的记录信息类型（仅NET_RECORD_TRAFFICREDLIST和NET_RECORD_TRAFFICBLACKLIST有效）,参考枚举EM_NET_RECORD_TYPE; record type to operate (Just NET_RECORD_TRAFFICREDLIST and NET_RECORD_TRAFFICBLACKLIST is valid),Please refer to EM_NET_RECORD_TYPE;
        ('pstOpreateInfo', c_void_p),  # 由用户申请内存，参照操作类型emOperateType，得到操作类型对应的结构体，进而确定对应的内存大小; the space application by the user,please refer to emOperateType to ensure corresponding structure,then ensure memory size;
    ]

class NET_OUT_OPERATE_TRAFFIC_LIST_RECORD(Structure):
    """
    CLIENT_OperateTrafficList 接口出参; CLIENT_OperateTrafficList interface output parameters
    现阶段实现的操作接口中,只有返回nRecordNo的操作,stRetRecord暂时不可用; Among the operation interfaces implemented at this stage, only the operation that returns nRecordNo, stRetRecord is temporarily unavailable
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nRecordNo', c_int),  # 记录号; Record Number;
    ]

class FIND_RECORD_TRAFFICREDLIST_CONDITION(Structure):
    """
    交通可用名单账户记录查询条件; Traffic Availability List Account Record Query Conditions
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('szPlateNumber', c_char * 32),  # 车牌号; License Plate Number;
        ('szPlateNumberVague', c_char * 32),  # 车牌号码模糊查询; License Plate Number Fuzzy Query;
        ('nQueryResultBegin', c_int),  # 第一个条返回结果在查询结果中的偏移量; Offset in the query results of first results returned;
        ('bRapidQuery', C_BOOL),  # 是否快速查询, TRUE:为快速,快速查询时不等待所有增、删、改操作完成。默认为非快速查询; Whether support the quick query, TRUE: for quick, quick query time don't wait for all add, delete, change operation is completed. The default is non-quick query;
    ]

class NET_AUTHORITY_TYPE(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('emAuthorityType', C_ENUM),  # 权限类型,参考枚举EM_NET_AUTHORITY_TYPE; Permission Types,Please refer to EM_NET_AUTHORITY_TYPE;
        ('bAuthorityEnable', C_BOOL),  # 权限使能; Permission Enabled;
    ]

class NET_TRAFFIC_LIST_RECORD(Structure):
    """
    交通可用名单记录信息; Traffic availability list record information
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nRecordNo', c_int),  # 之前查询到的记录号; Queried Record Number;
        ('szMasterOfCar', c_char * 16),  # 车主姓名; Car Owner's Name;
        ('szPlateNumber', c_char * 32),  # 车牌号码; License Plate Number;
        ('emPlateType', C_ENUM),  # 车牌类型,参考枚举EM_NET_PLATE_TYPE; License Plate Type,Please refer to EM_NET_PLATE_TYPE;
        ('emPlateColor', C_ENUM),  # 车牌颜色,参考枚举EM_NET_PLATE_COLOR_TYPE; License Plate Color,Please refer to EM_NET_PLATE_COLOR_TYPE;
        ('emVehicleType', C_ENUM),  # 车辆类型,参考枚举EM_NET_VEHICLE_TYPE; Vehicle Type,Please refer to EM_NET_VEHICLE_TYPE;
        ('emVehicleColor', C_ENUM),  # 车身颜色,参考枚举EM_NET_VEHICLE_COLOR_TYPE; Car Body Color,Please refer to EM_NET_VEHICLE_COLOR_TYPE;
        ('stBeginTime', NET_TIME),  # 开始时间; Start Time;
        ('stCancelTime', NET_TIME),  # 撤销时间; Undo Time;
        ('nAuthrityNum', c_int),  # 权限个数; Permission Number;
        ('stAuthrityTypes', NET_AUTHORITY_TYPE * 16),  # 权限列表 , 白名单仅有; Permissions List, White List Only;
        ('emControlType', C_ENUM),  # 布控类型 ,黑名单仅有,参考枚举EM_NET_TRAFFIC_CAR_CONTROL_TYPE; Monitor Type, Black List Only,Please refer to EM_NET_TRAFFIC_CAR_CONTROL_TYPE;
    ]

class NET_UPDATE_RECORD_INFO(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pRecordInfo', POINTER(NET_TRAFFIC_LIST_RECORD)),  # 记录内容信息,由用户分配内存，大小为sizeof(NET_TRAFFIC_LIST_RECORD); Record the content information,the space application by the user,apply to sizeof(NET_TRAFFIC_LIST_RECORD);
    ]

class CFG_VIDEO_FORMAT(Structure):
    """
    视频格式; Video format
    """
    _fields_ = [
        ('abCompression', c_bool),  
        ('abWidth', c_bool),  
        ('abHeight', c_bool),  
        ('abBitRateControl', c_bool),  
        ('abBitRate', c_bool),  
        ('abFrameRate', c_bool),  
        ('abIFrameInterval', c_bool),  
        ('abImageQuality', c_bool),  
        ('abFrameType', c_bool),  
        ('abProfile', c_bool),  # 信息; Information;
        ('emCompression', C_ENUM),  # 视频压缩格式,参考枚举CFG_VIDEO_COMPRESSION; Video compression mode,Please refer to CFG_VIDEO_COMPRESSION;
        ('nWidth', c_int),  # 视频宽度; Video width;
        ('nHeight', c_int),  # 视频高度; Video height;
        ('emBitRateControl', C_ENUM),  # 码流控制模式,参考枚举CFG_BITRATE_CONTROL; Bit rate control mode,Please refer to CFG_BITRATE_CONTROL;
        ('nBitRate', c_int),  # 视频码流(kbps); Video bit rate (kbps);
        ('nFrameRate', c_float),  # 视频帧率; Frame Rate;
        ('nIFrameInterval', c_int),  # I帧间隔(1-100)，比如50表示每49个B帧或P帧，设置一个I帧。; I frame interval(1-100). For example, 50 means there is I frame in each 49 B frame or P frame.;
        ('emImageQuality', C_ENUM),  # 图像质量,参考枚举CFG_IMAGE_QUALITY; Video quality,Please refer to CFG_IMAGE_QUALITY;
        ('nFrameType', c_int),  # 打包模式，0－DHAV，1－"PS"; Sniffer mode,0-DHAV,1-"PS";
        ('emProfile', C_ENUM),  # H.264编码级别,参考枚举CFG_H264_PROFILE_RANK; H.264 Encode level,Please refer to CFG_H264_PROFILE_RANK;
        ('nMaxBitrate', c_int),  # 最大码流单位是kbps（博世专用）; The maximum stream unit is kbps (Bosch dedicated);
    ]

class CFG_AUDIO_ENCODE_FORMAT(Structure):
    """
    音频格式; audio format
    """
    _fields_ = [
        ('abCompression', c_bool),  
        ('abDepth', c_bool),  
        ('abFrequency', c_bool),  
        ('abMode', c_bool),  
        ('abFrameType', c_bool),  
        ('abPacketPeriod', c_bool),  
        ('abChannels', c_bool),  
        ('abMix', c_bool),  # 信息; Info;
        ('emCompression', C_ENUM),  # 音频压缩模式,参考枚举CFG_AUDIO_FORMAT; Audio compression mode,Please refer to CFG_AUDIO_FORMAT;
        ('nDepth', c_int),  # 音频采样深度; Audio sampling depth;
        ('nFrequency', c_int),  # 音频采样频率; Audio sampling frequency;
        ('nMode', c_int),  # 音频编码模式; Audio encode mode;
        ('nFrameType', c_int),  # 音频打包模式, 0-DHAV, 1-PS; 0-DHAV, 1-PS Audio pack mode;
        ('nPacketPeriod', c_int),  # 音频打包周期, ms; Audio pack period(ms);
        ('nChannelsNum', c_int),  # 视频通道的伴音通道号列表个数; Sound channels list num of video;
        ('arrChannels', C_UINT * 8),  # 视频通道的伴音通道号列表; Sound channels list of video;
        ('bMix', C_BOOL),  # 是否同源; Whether homology;
    ]

class CFG_VIDEOENC_OPT(Structure):
    """
    视频编码参数; Video coding parameters
    """
    _fields_ = [
        ('abVideoEnable', c_bool),  
        ('abAudioEnable', c_bool),  
        ('abSnapEnable', c_bool),  
        ('abAudioAdd', c_bool),  # 音频叠加能力; Audio overlay capacity;
        ('abAudioFormat', c_bool),  # 信息; Information;
        ('bVideoEnable', C_BOOL),  # 视频使能; Video enable;
        ('stuVideoFormat', CFG_VIDEO_FORMAT),  # 视频格式; Video format;
        ('bAudioEnable', C_BOOL),  # 音频使能; Audio enable;
        ('bSnapEnable', C_BOOL),  # 定时抓图使能; Schedule snapshot enable;
        ('bAudioAddEnable', C_BOOL),  # 音频叠加使能; Audio add enable;
        ('stuAudioFormat', CFG_AUDIO_ENCODE_FORMAT),  # 音频格式; Audio format;
    ]

class CFG_RGBA(Structure):
    """
    RGBA信息; RGBA message
    """
    _fields_ = [
        ('nRed', c_int),  
        ('nGreen', c_int),  
        ('nBlue', c_int),  
        ('nAlpha', c_int),  
    ]

class CFG_COVER_INFO(Structure):
    """
    遮挡信息; Occlusion information
    """
    _fields_ = [
        ('abBlockType', c_bool),  
        ('abEncodeBlend', c_bool),  
        ('abPreviewBlend', c_bool),  # 信息; Information;
        ('stuRect', CFG_RECT),  # 覆盖的区域坐标; The position (coordinates) of the mask zone;
        ('stuColor', CFG_RGBA),  # 覆盖的颜色; The mask color;
        ('nBlockType', c_int),  # 覆盖方式；0－黑块，1－马赛克; The mask mode ;0-black block,1-Mosaic;
        ('nEncodeBlend', c_int),  # 编码级遮挡；1－生效，0－不生效; Encode-level privacy mask;1-enable,0-disable;
        ('nPreviewBlend', c_int),  # 预览遮挡；1－生效，0－不生效; Preview mask;1-enable,0-disable;
    ]

class CFG_VIDEO_COVER(Structure):
    """
    多区域遮挡配置; Multi area occlusion configuration
    """
    _fields_ = [
        ('nTotalBlocks', c_int),  # 支持的遮挡块数; The supported privacy mask zone amount;
        ('nCurBlocks', c_int),  # 已设置的块数; The zone amount already set;
        ('stuCoverBlock', CFG_COVER_INFO * 16),  # 覆盖的区域; The mask zone;
    ]

class CFG_OSD_INFO(Structure):
    """
    OSD信息; OSD message
    """
    _fields_ = [
        ('abShowEnable', c_bool),  # 信息; Information;
        ('stuFrontColor', CFG_RGBA),  # 前景颜色; Front color;
        ('stuBackColor', CFG_RGBA),  # 背景颜色; Background color;
        ('stuRect', CFG_RECT),  # 矩形区域; Rectangle zone;
        ('bShowEnable', C_BOOL),  # 显示使能; Display enbale;
    ]

class CFG_COLOR_INFO(Structure):
    """
    画面颜色属性; Picture color attribute
    """
    _fields_ = [
        ('nBrightness', c_int),  # 亮度(0-100); Brgihtness(0-100);
        ('nContrast', c_int),  # 对比度(0-100); Contrast(0-100);
        ('nSaturation', c_int),  # 饱和度(0-100); Saturation (0-100);
        ('nHue', c_int),  # 色度(0-100); Hue (0-100);
        ('nGain', c_int),  # 增益(0-100); Gain(0-100);
        ('bGainEn', C_BOOL),  # 增益使能; Gain enable;
    ]

class CFG_ENCODE_INFO(Structure):
    """
    图像通道属性信息; Image channel attribute information
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号(0开始),获取时，该字段有效；设置时，该字段无效; Channel number(Begins with 0);
        ('szChnName', c_char * 64),  # 无效字段; Channel name;
        ('stuMainStream', CFG_VIDEOENC_OPT * 4),  # 主码流，0－普通录像，1-动检录像，2－报警录像; Main stream,0-General record,1-Motion detect,2-alarm record;
        ('nValidCountMainStream', c_int),  # 主码流数组中有效的个数; The valid count of MainStream array;
        ('stuExtraStream', CFG_VIDEOENC_OPT * 4),  # 辅码流，0－辅码流1，1－辅码流2，2－辅码流3; Extra stream,0-Extra stream 1,1-Extra stream 2,2-Extra stream 3;
        ('nValidCountExtraStream', c_int),  # 辅码流数组中有效的个数; The valid count of ExtraStream array;
        ('stuSnapFormat', CFG_VIDEOENC_OPT * 4),  # 抓图，0－普通抓图，1－动检抓图，2－报警抓图; Snapshot,0-General snapshot,1-Motion detect snapshot,2-alarm snapshot;
        ('nValidCountSnapFormat', c_int),  # 抓图数组中有效的个数; The valid count of SnapFormat array;
        ('dwCoverAbilityMask', C_DWORD),  # 无效字段; The subnet mask of the privacy mask competence. Use the bit to represent. There are local preview, record and network monitor.;
        ('dwCoverEnableMask', C_DWORD),  # 无效字段; The subnet mask of the privacy mask enable.Use the bit to represent. There are local preview, record and network monitor.;
        ('stuVideoCover', CFG_VIDEO_COVER),  # 无效字段; Privacy mask;
        ('stuChnTitle', CFG_OSD_INFO),  # 无效字段; Channel title;
        ('stuTimeTitle', CFG_OSD_INFO),  # 无效字段; Time title;
        ('stuVideoColor', CFG_COLOR_INFO),  # 无效字段; Video color;
        ('emAudioFormat', C_ENUM),          # 无效字段; Audio Format
        ('nProtocolVer', c_int),  # 协议版本号, 只读,获取时，该字段有效；设置时，该字段无效; Protocol Version No., read only;
    ]

class NET_HDDSMART_INFO(Structure):
    """
    硬盘Smart信息; Hard disk smart information
    """
    _fields_ = [
        ('nID', c_int),  # 属性ID; ID;
        ('nCurrent', c_int),  # 属性值; Current;
        ('szName', c_char * 64),  # 属性名; Name;
        ('nWorst', c_int),  # 最大出错值; Worst;
        ('nThreshold', c_int),  # 阈值; Threshold;
        ('szRaw', c_char * 32),  # 实际值,可能不仅是数字，需要字符串返回; Actual Value;
        ('nPredict', c_int),  # 状态,对硬盘状态的预测值,无实际意义; The predictive value of the state of HDD;
        ('emSync', C_ENUM),  # Raid同步状态,参考枚举EM_RAID_SYNC_STATE; Raid Sync State,Please refer to EM_RAID_SYNC_STATE;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class ALARM_HDD_HEALTHALARM_INFO(Structure):
    """
    硬盘健康状况报警事件( DH_ALARM_HDD_HEALTHALARM ); Hard disk health alarm event (dh_alarm_hdd_healthalarm)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作1:Start 2:Stop; Action:1:Start 2:Stop;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szHDDName', c_char * 64),  # 硬盘名称; HDD Name;
        ('stuHDDSmartInfo', NET_HDDSMART_INFO),  # 硬盘Smart信息; HDD Smart info;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class ALARM_DISK_CHECK_INFO(Structure):
    """
    磁盘巡检报警事件信息(对应 DH_ALARM_DISK_CHECK); Disk patrol alarm event information (corresponding to dh_alarm_disk_check)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;; Event operation.1=continues event begin. 2=continuous event stop;
        ('UTC', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szName', c_char * 128),  # 报警名称; Name;
        ('byReserved', C_BYTE * 1024),  # 保留字节; Reserved;
    ]

class ALARM_HDD_SHAKEALARM_INFO(Structure):
    """
    硬盘震动报警事件( DH_ALARM_HDD_SHAKEALARM ); Hard disk vibration alarm event (dh_alarm_hdd_shakealarm)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作1:Start 2:Stop; Action:1:Start 2:Stop;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szHDDName', c_char * 64),  # 硬盘名称; HDD Name;
        ('stuHDDSmartInfo', NET_HDDSMART_INFO),  # 硬盘Smart信息; HDD Smart info;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class ALARM_HDD_TEMPERATUREALARM_INFO(Structure):
    """
    硬盘温度报警事件( DH_ALARM_HDD_TEMPERATUREALARM ); Hard disk temperature alarm event (dh_alarm_hdd_temperaturealarm)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作1:Start 2:Stop; Action:1:Start 2:Stop;
        ('nTemperature', c_int),  # 硬盘当前温度值; HDD Temperature;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szHDDName', c_char * 64),  # 硬盘名称; HDD Name;
        ('stuHDDSmartInfo', NET_HDDSMART_INFO),  # 硬盘Smart信息; HDD Smart info;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class NET_RECORD_CARD_INFO(Structure):
    """
    卡号录像信息; Card number video information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nType', c_int),  # 类型, 0-Card, 1-Field; type, 0-Card, 1-Field;
        ('szCardNo', c_char * 256),  # 卡号; card no.;
        ('emTradeType', C_ENUM),  # 交易类型,参考枚举EM_ATM_TRADE_TYPE; transaction type,Please refer to EM_ATM_TRADE_TYPE;
        ('szAmount', c_char * 64),  # 交易金额, 空字符串表示不限金额; transaction amount, nullstring means no limit amount;
        ('nError', c_int),  # 错误码, 0-所有错误, 1-吞钞, 2-吞卡; error code, 0-all errors, 1-retain cash, 2-retain card;
        ('nFieldCount', c_int),  # 域数量, 按域查询时有效; domain quantity, by domain search is valid;
        ('szFields', c_char * 4096),  # 域信息, 按域查询时有效; domain info, by domain search is valid;
        ('szChange', c_char * 32),  # 零钱; change;
    ]

class NET_IN_MEDIA_QUERY_FILE(Structure):
    """
    录像信息对应 CLIENT_FindFileEx 接口的 DH_FILE_QUERY_FILE / DH_FILE_QUERY_FILE_EX 命令 查询条件, 目前支持通过路径查询
    Video information corresponding to client_ DH of findfileex interface_ FILE_ QUERY_ FILE / DH_ FILE_ QUERY_ FILE_ Ex command query criteria. Currently, path query is supported
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; size;
        ('szDirs', c_void_p),  # 工作目录列表,一次可查询多个目录,为空表示查询所有目录。目录之间以分号分隔,如“/mnt/dvr/sda0;/mnt/dvr/sda1”,szDirs==null 或"" 表示查询所有; working directory list,can inquire multiple directory at a atime,separated by ";",example "/mnt/dvr/sda0;/mnt/dvr/sda1",if szDirs==null or szDirs == "" ,means search all;
        ('nMediaType', c_int),  # 文件类型,0:查询任意类型,1:查询jpg图片,2:查询dav; file info,0:any type,1:search jpg image,2:search dav;
        ('nChannelID', c_int),  # 通道号从0开始,-1表示查询所有通道; Channel start from 0, -1 means search all channel;
        ('stuStartTime', NET_TIME),  # 开始时间; start time;
        ('stuEndTime', NET_TIME),  # 结束时间; end time;
        ('nEventLists', c_int * 256),  # 事件类型列表,参见智能分析事件类型; Event type list, see intelligent analysis event type;
        ('nEventCount', c_int),  # 事件总数; event total;
        ('byVideoStream', C_BYTE),  # 视频码流 0-未知 1-主码流 2-辅码流1 3-辅码流2 4-辅码流3 5-所有的辅码流类型; video stream 0-unknown; 1-main; 2-sub 1; 3-sub 2; 4- sub 3; 5-ExtraX;
        ('bReserved', C_BYTE * 3),  # 字节对齐; aligh text;
        ('emFalgLists', C_ENUM * 128),  # 录像或抓图文件标志, 不设置标志表示查询所有文件,参考枚举EM_RECORD_SNAP_FLAG_TYPE; Record or snapshot file mark, not set mark to search all files,Please refer to EM_RECORD_SNAP_FLAG_TYPE;
        ('nFalgCount', c_int),  # 标志总数; total mark;
        ('stuCardInfo', NET_RECORD_CARD_INFO),  # 卡号录像信息, emFalgLists包含卡号录像时有效; card no. record info, emFalgLists including card no. video is valid;
        ('nUserCount', c_int),  # 用户名有效个数; user total;
        ('szUserName', c_char * 512),  # 用户名; user name;
        ('emResultOrder', C_ENUM),  # 查询结果排序方式,参考枚举EM_RESULT_ORDER_TYPE; result order,Please refer to EM_RESULT_ORDER_TYPE;
        ('bTime', C_BOOL),  # 是否按时间查询; find file by time;
        ('emCombination', C_ENUM),  # 查询结果是否合并录像文件,参考枚举NET_EM_COMBINATION_MODE; Whether to combine video,Please refer to NET_EM_COMBINATION_MODE;
        ('stuEventInfo', EVENT_INFO * 16),  # 事件信息（定制），当查询为 DH_FILE_QUERY_FILE_EX 类型时有效; event info(customized),when query type in EM_FILE_QUERY_TYPE is DH_FILE_QUERY_FILE_EX valid;
        ('nEventInfoCount', c_int),  # stuEventInfo 个数; stuEventInfo's count;
    ]

class NET_FILE_SUMMARY_INFO(Structure):
    """
    文件摘要信息; Document summary information
    """
    _fields_ = [
        ('szKey', c_char * 64),  # 摘要名称; Abstract name;
        ('szValue', c_char * 512),  # 摘要内容; Abstract contents;
        ('bReserved', C_BYTE * 256),  # 保留字段; Reserved string;
    ]

class NET_OUT_MEDIA_QUERY_FILE(Structure):
    """
    录像信息对应 CLIENT_FindFileEx 接口的 DH_FILE_QUERY_FILE / DH_FILE_QUERY_FILE_EX 命令 查询结果
    Video information corresponding to client_ DH of findfileex interface_ FILE_ QUERY_ FILE / DH_ FILE_ QUERY_ FILE_ Ex command query results
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; size;
        ('nChannelID', c_int),  # 通道号从0开始,-1表示查询所有通道; channel ID,from 0,-1 means search all;
        ('stuStartTime', NET_TIME),  # 开始时间; start time;
        ('stuEndTime', NET_TIME),  # 结束时间; end time;
        ('nFileSize', C_UINT),  # 文件长度,该字段废弃,使用nFileSizeEx字段; size of file,This field is discarded,please use the nFileSizeEx;
        ('byFileType', C_BYTE),  # 文件类型 1:jpg图片, 2: dav; file type 1:jpg, 2: dav;
        ('byDriveNo', C_BYTE),  # 该字段已废弃,后续开发使用 nDriveNo成员; deprecated, to get same info, use nDriveNo instead;
        ('byPartition', C_BYTE),  # 分区号; zone no.;
        ('byVideoStream', C_BYTE),  # 视频码流 0-未知 1-主码流 2-辅码流1 3-辅码流 4-辅码流; video stream 0-unknown 1-main 2-sub 1 3-sub 4-sub;
        ('nCluster', C_UINT),  # 簇号; cluster;
        ('szFilePath', c_char * 260),  # 文件路径; FilePath;
        ('nEventLists', c_int * 256),  # 关联的事件列表,事件类型列表,参见智能分析事件类型; Link event list,see event intelligent analysis event type;
        ('nEventCount', c_int),  # 事件总数; event total;
        ('emFalgLists', C_ENUM * 128),  # 录像或抓图文件标志,参考枚举EM_RECORD_SNAP_FLAG_TYPE; record or snapshot file mark,Please refer to EM_RECORD_SNAP_FLAG_TYPE;
        ('nFalgCount', c_int),  # 标志总数; mark total;
        ('nDriveNo', C_UINT),  # 磁盘号,频浓缩文件相关信息; disk driver number;
        ('szSynopsisPicPath', c_char * 512),  # 预处理文件提取到的快照 文件路径,支持HTTP URL表示:"http:www.dahuate.com/1.jpg",支持FTP URL表示: "ftp:ftp.dahuate.com/1.jpg",支持服务器本地路径,a)"C:/pic/1.jpg",b)"/mnt2010/8/11/dav/15:40:50.jpg"; snap file path when pre-process the file;
        ('nSynopsisMaxTime', c_int),  # 支持浓缩视频最大时间长度,单位 秒; video synopsis max time. Unit is second.;
        ('nSynopsisMinTime', c_int),  # 支持浓缩视频最小时间长度,单位 秒,文件摘要信息; video synopsis min time. Unit is second.;
        ('nFileSummaryNum', c_int),  # 文件摘要信息数; file summary number;
        ('stFileSummaryInfo', NET_FILE_SUMMARY_INFO * 32),  # 文件摘要信息; file summary info;
        ('nFileSizeEx', c_int64),  # 文件长度扩展,支持文件长度大于4G，单位字节; size of file extension, Support file length is greater than 4G,unit:Byte;
        ('nTotalFrame', C_UINT),  # 查询录像段内所有帧总和，不区分帧类型(定制); all frames' num, not distinguish by frame type(customized);
        ('emFileState', C_ENUM),  # 录像文件的状态,参考枚举EM_VIDEO_FILE_STATE; video file status,Please refer to EM_VIDEO_FILE_STATE;
        ('szWorkDir', c_char * 256),  # 录像文件的存储目录; Storage directory of video files;
        ('szThumbnail', c_char * 260),  # 缩略图路径，可根据该路径下载缩略图; Thumbnail path, according to which thumbnails can be downloaded;
    ]

class CFG_NETWORK_INTERFACE(Structure):
    """
    网口配置; Network port configuration
    """
    _fields_ = [
        ('szName', c_char * 128),  # 网络接口名称; Network address name;
        ('szIP', c_char * 256),  # ip地址; IP address;
        ('szSubnetMask', c_char * 256),  # 子网掩码; Subnet mask;
        ('szDefGateway', c_char * 256),  # 默认网关; Default gateway;
        ('bDhcpEnable', C_BOOL),  # 是否开启DHCP; Enable DHCP or not.;
        ('bDnsAutoGet', C_BOOL),  # DNS获取方式，dhcp使能时可以设置为true，支持通过dhcp获取; DNS get way.,It is true if the dhcp is enabled. Support DHCP.;
        ('szDnsServers', c_char * 512),  # DNS服务器地址; DNS address;
        ('nMTU', c_int),  # 网络最大传输单元; Network max transmission unit.;
        ('szMacAddress', c_char * 256),  # mac地址; Mac address;
        ('bInterfaceEnable', C_BOOL),  # 网络接口使能开关，表示该网口配置是否生效。不生效时，IP地址不设置到网卡上。; Enable network interface,if false,ip address will not set for the config;
        ('bReservedIPEnable', C_BOOL),  # DHCP失败时是否使用保留IP，使用保留IP时还继续发DHCP请求; Enable to reserved ip when DHCP failed,true:continue to send DHCP ask;
        ('emNetTranmissionMode', C_ENUM),  # 网络传输模式，默认adapt自适应模式,参考枚举CFG_ENUM_NET_TRANSMISSION_MODE; Net transmission mode，default:adapt,Please refer to CFG_ENUM_NET_TRANSMISSION_MODE;
        ('emInterfaceType', C_ENUM),  # 网口类型,参考枚举CFG_ENUM_NET_INTERFACE_TYPE; Network interface type,Please refer to CFG_ENUM_NET_INTERFACE_TYPE;
        ('bBond', C_ENUM),  # 是否绑定虚拟网口,参考枚举CFG_THREE_STATUS_BOOL; enable to bond Network interface,Please refer to CFG_THREE_STATUS_BOOL;
    ]

class CFG_NETWORK_BOND_INTERFACE(Structure):
    """
    绑定虚拟网口; Bind virtual network port
    """
    _fields_ = [
        ('bBonding', C_BOOL),  # 是否绑定虚拟网口，只有网卡名是bondxx时，才允许有Bonding字段，其它网卡不能用,true-绑定网卡生效,物理网口对外不可用,false-解绑网卡(多址模式),使Members中的网卡可用; Whether to bind the virtual network port, the bonding field is allowed only when the network card name is bondxx, and other network cards cannot be used,true-the binding of the network card takes effect, and the physical network port is unavailable to the outside world,false-Unbind the network card (multi-access mode) to make the network card in Members available;
        ('emMode', C_ENUM),  # 网卡绑定模式,参考枚举CFG_ENUM_NET_BOND_MODE; NIC bonding mode,Please refer to CFG_ENUM_NET_BOND_MODE;
        ('emLacp', C_ENUM),  # 802.3ad链路聚合控制方式,参考枚举CFG_ENUM_NET_BOND_LACP; 802.3ad link aggregation control method,Please refer to CFG_ENUM_NET_BOND_LACP;
        ('nMTU', c_int),  # 网络最大传输单元; Network maximum transmission unit;
        ('szMembers', c_char * 256),  # 物理网口成员; Physical network port member;
        ('szIP', c_char * 256),  # ip地址; IP;
        ('szName', c_char * 128),  # 网络接口名称; Name;
        ('szAlias', c_char * 128),  # 网络接口名称; Alias;
        ('szDnsServers', c_char * 512),  # DNS服务器地址; DNS Servers;
        ('szMacAddress', c_char * 256),  # mac地址; mac Address;
        ('szSubnetMask', c_char * 256),  # 子网掩码; Subnet mask;
        ('szDefGateway', c_char * 256),  # 默认网关; Default gateway;
        ('bDhcpEnable', C_BOOL),  # 是否开启DHCP; Whether to enable DHCP;
    ]

class CFG_NETWORK_BR_INTERFACE(Structure):
    """
    网桥; bridge
    """
    _fields_ = [
        ('szName', c_char * 128),  # 网络接口名称; Network interface name;
        ('bEnable', C_BOOL),  # 使能; enable;
        ('nMTU', c_int),  # 网络最大传输单元; MTU;
        ('szMembers', c_char * 256),  # 物理网口成员; Physical network port member;
        ('szIP', c_char * 256),  # ip地址; IP;
        ('szSubnetMask', c_char * 256),  # 子网掩码; Subnet mask;
        ('szDefGateway', c_char * 256),  # 默认网关; Default gateway;
        ('szDnsServers', c_char * 512),  # DNS服务器地址; DNS Servers;
        ('bDhcpEnable', C_BOOL),  # 是否开启DHCP; Whether to enable DHCP;
        ('bReservedIPEnable', C_BOOL),  # DHCP失败时是否使用保留IP，使用保留IP时还继续发DHCP请求; Whether to use reserved IP when DHCP fails, and continue to send DHCP requests when reserved IP is used;
        ('bDnsAutoGet', C_BOOL),  # DNS获取方式，dhcp使能时可以设置为true，支持通过dhcp获取; DNS acquisition method, can be set to true when dhcp is enabled, and it can be acquired through dhcp;
    ]

class CFG_NETWORK_INFO(Structure):
    """
    网络接口配置; Network interface configuration
    """
    _fields_ = [
        ('szHostName', c_char * 128),  # 主机名称; Host name;
        ('szDomain', c_char * 128),  # 所属域; Belonging domain;
        ('szDefInterface', c_char * 128),  # 默认使用的网卡; Default network card;
        ('nInterfaceNum', c_int),  # 网卡数量; Network card amount;
        ('stuInterfaces', CFG_NETWORK_INTERFACE * 32),  # 网卡列表; Network card list;
        ('nBondInterfaceNum', c_int),  # 虚拟绑定网口数量; Number of virtual binding network ports;
        ('stuBondInterfaces', CFG_NETWORK_BOND_INTERFACE * 32),  # 虚拟绑定网口列表; Virtual bonding network port list;
        ('nBrInterfaceNum', c_int),  # 网桥数量; Number of bridges;
        ('stuBrInterfaces', CFG_NETWORK_BR_INTERFACE * 32),  # 网桥列表; List of bridges;
    ]

class NET_UTCTIME(Structure):
    _fields_ = [
        ('utc', C_UINT),  # utc时间; utc;
        ('tolerance', C_UINT),  # 容差，表示容许设置时间和当前差多少秒内不做修改 (下发时用到); tolerance, allows the setting time to be seconds away from the current time without modification; set:valid;
        ('reserved', c_char * 8),  # 预留字段; reserved data;
    ]

class NET_OPEN_INTELLI_OBJECT_ATTRIBUTE_INFO(Structure):
    """
    目标属性数组; Target attribute array
    """
    _fields_ = [
        ('szAttrTypeName', c_char * 128),  # 属性类型名称; attribute type name;
        ('szAttrValueName', c_char * 128),  # 属性值名称; attribute value name;
    ]

class NET_OPEN_INTELLI_OBJECT_INFO(Structure):
    """
    检测到的目标属性信息列表; List of detected target attribute information
    """
    _fields_ = [
        ('nObjectId', c_int),  # 目标id; target id;
        ('stuBoundingBox', NET_RECT),  # 包围盒 矩形类型,8192坐标系; Bounding box rectangle type, 8192 coordinate system;
        ('szObjectTypeName', c_char * 128),  # 目标类型名称; target type name;
        ('nObjectAttributeNums', c_int),  # 目标属性数组中的有效个数; valid number in the target attribute array;
        ('stuObjectAttributes', NET_OPEN_INTELLI_OBJECT_ATTRIBUTE_INFO * 128),  # 目标属性数组; Array of target attributes;
    ]

class NET_OPEN_INTELLI_USER_DATA_INFO(Structure):
    """
    用户数据; user data
    """
    _fields_ = [
        ('nAlarmId', c_int),  # 自定义报警id; custom alarm id;
        ('szReserved', c_char * 512),  # 保留字节; reserved bytes;
    ]

class DEV_EVENT_OPEN_INTELLI_INFO(Structure):
    """
    事件类型 EVENT_IVS_OPEN_INTELLI (开放智能事件)对应的数据块描述信息;
    Event type event_ IVS_ OPEN_ Data block description information corresponding to Intelli (open intelligent event)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号; channel number;
        ('nAction', c_int),  # 0:脉冲,1:开始, 2:停止; 0: pulse, 1: start, 2: stop;
        ('szOpenCode', c_char * 32),  # 所属开放算法的Id; Id of the open algorithm it belongs to;
        ('szOpenName', c_char * 128),  # 所属开放算法的名称; The name of the open algorithm to which it belongs;
        ('szRuleType', c_char * 32),  # 所属开放算法的规则类型, 仅支持: 拌线入侵CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION)、区域入侵CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION)、滞留检测StayDetection(EVENT_IVS_STAYDETECTION)、数量统计ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION); Rule type of the open algorithm, only supported: CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION)、CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION)、StayDetection(EVENT_IVS_STAYDETECTION)、ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION);
        ('pstuOpenData', c_void_p),  # 与开放算法的规则类型支持的带图事件类型对应的结构体对应(只解析Event Data中的字段),拌线入侵CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION) - DEV_EVENT_CROSSLINE_INFO,区域入侵CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION) - DEV_EVENT_CROSSREGION_INFO,滞留检测StayDetection(EVENT_IVS_STAYDETECTION) - DEV_EVENT_STAY_INFO,数量统计ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION) - DEV_EVENT_OBJECT_NUM_DETECTION_INFO; Corresponds to the structure corresponding to the event type with graph supported by the rule type of the open algorithm (only parses the fields in Event Data),CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION) - DEV_EVENT_CROSSLINE_INFO,CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION) - DEV_EVENT_CROSSREGION_INFO,StayDetection(EVENT_IVS_STAYDETECTION) - DEV_EVENT_STAY_INFO,ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION) - DEV_EVENT_OBJECT_NUM_DETECTION_INFO;
        ('nObjectNums', c_int),  # 检测到的目标属性信息列表的个数; number of detected target attribute information lists;
        ('stuObjects', NET_OPEN_INTELLI_OBJECT_INFO * 100),  # 检测到的目标属性信息列表; List of detected object attribute information;
        ('stuUserData', NET_OPEN_INTELLI_USER_DATA_INFO),  # 用户数据; User data;
        ('szReserved', c_char * 1024),  # 保留字节; reserved bytes;
    ]

class NET_FIND_RECORD_ACCESSCTLCARDREC_ORDER(Structure):
    """
    门禁出入记录排序规则详情
    Order rule of entrance guard access records
    """
    _fields_ = [
        ('emField', C_ENUM),  # 排序字段 Refer: EM_RECORD_ACCESSCTLCARDREC_ORDER_FIELD;field Refer: EM_RECORD_ACCESSCTLCARDREC_ORDER_FIELD;
        ('emOrderType', C_ENUM),  # 排序类型 Refer: EM_RECORD_ORDER_TYPE;order type Refer: EM_RECORD_ORDER_TYPE;
        ('byReverse', c_char * 64),  # 保留字节;Reserved;
    ]

class NET_FIND_RECORD_ACCESSCTLCARDREC_CONDITION_EX(Structure):
    """
    门禁出入记录查询条件
    A&C extry/exit search criteria
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('bCardNoEnable', C_BOOL),  # 启用卡号查询;Enable card search;
        ('szCardNo', c_char * 32),  # 卡号;Card No.;
        ('bTimeEnable', C_BOOL),  # 启用时间段查询;Enable search by period;
        ('stStartTime', NET_TIME),  # 起始时间;Start time;
        ('stEndTime', NET_TIME),  # 结束时间;End time;
        ('nOrderNum', c_int),  # 规则数;The number of rules;
        ('stuOrders', NET_FIND_RECORD_ACCESSCTLCARDREC_ORDER * 6),  # 规则数组;The array of rules;
    ]

class NET_CTRL_RECORDSET_PARAM(Structure):
    """
    记录集操作参数
    Query device recording information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emType', C_ENUM),  # 记录集信息类型 Refer: EM_NET_RECORD_TYPE;Record Information Type Refer: EM_NET_RECORD_TYPE;
        ('pBuf', c_void_p),  # 新增\更新\查询\导入时,为记录集信息缓存,详见 EM_NET_RECORD_TYPE 注释,由用户申请内存，长度为nBufLen删除时,为存放记录集编号的内存地址(类型为int*), 批量删除时，为NET_CTRL_RECORDSET_REMOVEEX_PARAM, 由用户申请内存, 长度为nBufLen;New/Renew/Inquire,It is Record Information Cache, the EM_NET_RECORD_TYPE Note is Details)Delete,It is memory address for storage Record Number(type is int*);
        ('nBufLen', c_int),  # 记录集信息缓存大小,大小参照记录集信息类型对应的结构体;Record Information Cache Size,please refer to the structure of EM_NET_RECORD_TYPE;
    ]

class NET_IN_DOWNLOAD_REMOTE_FILE(Structure):
    """
    CLIENT_DownloadRemoteFile 接口输入参数(文件下载)
    CLIENT_DownloadRemoteFile    Interface Input Parameters (the file download)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pszFileName', POINTER(c_char)),  # 需要下载的文件名;File Name Needs to Download;
        ('pszFileDst', POINTER(c_char)),  # 存放文件路径;File Path;
    ]

class NET_OUT_DOWNLOAD_REMOTE_FILE(Structure):
    """
    CLIENT_DownloadRemoteFile 接口输出参数(文件下载)
    CLIENT_DownloadRemoteFile Interface Output Parameters (the file download)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwMaxFileBufLen', C_DWORD),  # 文件缓存区pstFileBuf的大小, 由用户指定;The size of pstFileBuf, it is specified by user;
        ('pstFileBuf', POINTER(c_char)),  # 文件缓存区, 由用户申请和释放;File buf, application an release by user;
        ('dwRetFileBufLen', C_DWORD),  # 缓存区中返回的实际文件数据大小;The actual size of the file;
        ('byReserved', C_BYTE * 4),  # 字节对齐;Alignment;
    ]

class NET_RECORDSET_ACCESS_CTL_CARDREC(Structure):
    """
    门禁刷卡记录记录集信息
    Access control card swiping record set information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nRecNo', c_int),  # 记录集编号,只读;Record Number,Read-Only;
        ('szCardNo', c_char * 32),  # 卡号;Card Number;
        ('szPwd', c_char * 64),  # 密码;Password;
        ('stuTime', NET_TIME),  # 刷卡时间;Swing Card Time;
        ('bStatus', C_BOOL),  # 刷卡结果,TRUE表示成功,FALSE表示失败;Swing Card Result,True is Success,False is Fail;
        ('emMethod', C_ENUM),  # 开门方式 Refer: NET_ACCESS_DOOROPEN_METHOD;Open Door Method Refer: NET_ACCESS_DOOROPEN_METHOD;
        ('nDoor', c_int),  # 门号,即CFG_CMD_ACCESS_EVENT配置CFG_ACCESS_EVENT_INFO的数组下标;Door Number,That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('nReaderID', c_int),  # 读卡器ID (废弃,不再使用);card reader ID (abandoned);
        ('szSnapFtpUrl', c_char * 260),  # 开锁抓拍上传的FTP地址;unlock snap upload ftp url;
        ('szReaderID', c_char * 32),  # 读卡器ID              开门并上传抓拍照片,在记录集记录存储地址,成功才有;card reader ID;
        ('emCardType', C_ENUM),  # 卡类型 Refer: NET_ACCESSCTLCARD_TYPE;Card Type Refer: NET_ACCESSCTLCARD_TYPE;
        ('nErrorCode', c_int),  # 开门失败的原因,仅在bStatus为FALSE时有效0x00 没有错误0x10 未授权0x11 卡挂失或注销0x12 没有该门权限0x13 开门模式错误0x14 有效期错误0x15 防反潜模式0x16 胁迫报警未打开0x17 门常闭状态0x18 AB互锁状态0x19 巡逻卡0x1A 设备处于闯入报警状态0x20 时间段错误0x21 假期内开门时间段错误0x23 卡逾期0x30 需要先验证有首卡权限的卡片0x40 卡片正确,输入密码错误0x41 卡片正确,输入密码超时0x42 卡片正确,输入指纹错误0x43 卡片正确,输入指纹超时0x44 指纹正确,输入密码错误0x45 指纹正确,输入密码超时0x50 组合开门顺序错误0x51 组合开门需要继续验证0x60 验证通过,控制台未授权0x61 卡片正确,人脸错误0x62 卡片正确,人脸超时0x63 重复进入0x64 未授权,需要后端平台识别0x65 体温过高0x66 未戴口罩0x67 健康码获取失败0x68 黄码禁止通行0x69 红码禁止通行0x6a 健康码无效0x6b 绿码验证通过0x6c  绿码,核酸为阳性0x6d 绿码,未接种0x70 获取健康码信息;Reason of unlock failure, only because it is valid when bStatus is FALSE0x00 no error0x10 unauthorized0x11 card lost or cancelled0x12 no door right0x13 unlock mode error0x14 valid period error0x15 anti sneak into mode0x16 forced alarm not unlocked0x17 door NC status0x18 AB lock status0x19 patrol card0x1A device is under intrusion alarm status0x20 period error0x21 unlock period error in holiday period0x23 Card is overdue0x30 first card right check required0x40 card correct, input password error0x41 card correct, input password timed out0x42 card correct, input fingerprint error0x43 card correct, input fingerprint timed out0x44 fingerprint correct, input password error0x45 fingerprint correct, input password timed out0x50 group unlock sequence error0x51 test required for group unlock0x60 test passed, control unauthorized0x61 card correct, input face error0x62 card correct, input face timed out0x63 repeat enter0x64 unauthorized, requiring back-end platform identification0x65 High body temperature0x66 no mask0x67 get health code fail0x68 No Entry because of yellow code0x69 No Entry because of red code0x6a health code is invalid0x6b entry because of green code0x70 get health code info;
        ('szRecordURL', c_char * 128),  # 刷卡录像的地址;record url;
        ('nNumbers', c_int),  # 抓图的张数;snap picture numbers;
        ('emAttendanceState', C_ENUM),  # 考勤状态 Refer: NET_ATTENDANCESTATE;attendance state Refer: NET_ATTENDANCESTATE;
        ('emDirection', C_ENUM),  # 开门方向 Refer: NET_ENUM_DIRECTION_ACCESS_CTL;open door direction Refer: NET_ENUM_DIRECTION_ACCESS_CTL;
        ('szClassNumber', c_char * 32),  # 班级（考勤肯尼亚定制）;Class number(Kenya custom);
        ('szPhoneNumber', c_char * 16),  # 电话（考勤肯尼亚定制）;Phone number(Kenya custom);
        ('szCardName', c_char * 64),  # 卡命名;Card name;
        ('szSN', c_char * 32),  # 智能锁序列号,无线配件需要该字段;wireless device serial number;
        ('bCitizenIDResult', C_BOOL),  # 人证比对结果;Compare result;
        ('szCitizenIDName', c_char * 30),  # 名字;Name;
        ('byReserved1', C_BYTE * 2),  # 字节对齐;Align;
        ('emCitizenIDSex', C_ENUM),  # 性别 Refer: EM_CITIZENIDCARD_SEX_TYPE;Sex Refer: EM_CITIZENIDCARD_SEX_TYPE;
        ('emCitizenIDEthnicity', C_ENUM),  # 民族 Refer: EM_CITIZENIDCARD_ETHNICITY_TYPE;Ethnicity Refer: EM_CITIZENIDCARD_ETHNICITY_TYPE;
        ('stuCitizenIDBirth', NET_TIME),  # 出生日期(时分秒无效);Birth date;
        ('szCitizenIDAddress', c_char * 108),  # 住址;Address;
        ('szCitizenIDAuthority', c_char * 48),  # 签发机关;Authority;
        ('stuCitizenIDStart', NET_TIME),  # 有效起始日期(时分秒无效);Start time;
        ('stuCitizenIDEnd', NET_TIME),  # 有效截止日期(时分秒无效, 年为负数时表示长期有效);End time;
        ('bIsEndless', C_BOOL),  # 是否长期有效;Is end time unlimited;
        ('szSnapFaceURL', c_char * 128),  # 人脸图片保存地址;Face picture URL;
        ('szCitizenPictureURL', c_char * 128),  # 身份证图片保存地址;Citizen picture URL;
        ('szCitizenIDNo', c_char * 20),  # 身份证号码;Citizen card number;
        ('emSex', C_ENUM),  # 性别 Refer: NET_ACCESSCTLCARD_SEX;sex Refer: NET_ACCESSCTLCARD_SEX;
        ('szRole', c_char * 32),  # 角色;role;
        ('szProjectNo', c_char * 32),  # 项目ID;project No.;
        ('szProjectName', c_char * 64),  # 项目名称;project name;
        ('szBuilderName', c_char * 64),  # 施工单位全称;builder name;
        ('szBuilderID', c_char * 32),  # 施工单位ID;builder ID;
        ('szBuilderType', c_char * 32),  # 施工单位类型;builder type;
        ('szBuilderTypeID', c_char * 8),  # 施工单位类别ID;builder type ID;
        ('szPictureID', c_char * 64),  # 人员照片ID;picture ID;
        ('szContractID', c_char * 16),  # 原合同系统合同编号;contract ID in original contract system;
        ('szWorkerTypeID', c_char * 8),  # 工种ID;worker type ID;
        ('szWorkerTypeName', c_char * 32),  # 工种名称;worker type name;
        ('bPersonStatus', C_BOOL),  # 人员状态, TRUE:启用, FALSE:禁用;person status, TRUE:enable, FALSE:forbidden;
        ('emHatStyle', C_ENUM),  # 帽子类型 Refer: EM_HAT_STYLE;hat style Refer: EM_HAT_STYLE;
        ('emHatColor', C_ENUM),  # 帽子颜色 Refer: EM_UNIFIED_COLOR_TYPE;hat color Refer: EM_UNIFIED_COLOR_TYPE;
        ('stuManTemperatureInfo', NET_MAN_TEMPERATURE_INFO),  # 人员温度信息;human temperature info;
        ('nCompanionInfo', c_int),  # 陪同人员 stuCompanionInfo 个数;stuCompanionInfo's count;
        ('stuCompanionInfo', NET_COMPANION_INFO * 12),  # 陪同人员信息（定制）：姓名、卡号字段有效;companion info(customized):name and card valid;
        ('emMask', C_ENUM),  # 口罩状态（EM_MASK_STATE_UNKNOWN、EM_MASK_STATE_NOMASK、EM_MASK_STATE_WEAR 有效） Refer: EM_MASK_STATE_TYPE;mask ( EM_MASK_STATE_UNKNOWN,EM_MASK_STATE_NOMASK,EM_MASK_STATE_WEAR is valid ) Refer: EM_MASK_STATE_TYPE;
        ('nFaceIndex', C_UINT),  # 一人多脸的人脸序号;face index;
        ('nScore', c_int),  # 人脸质量评分;Face quality score;
        ('nLiftNo', c_int),  # 电梯编号;Elevator number;
        ('szQRCode', c_char * 512),  # 二维码;QRCode;
        ('emFaceCheck', C_ENUM),  # 定制功能，刷卡开门时，门禁后台校验人脸是否是同一个人 Refer: EM_FACE_CHECK;Customized function, when swiping the card to open the door, the access control background checks whether the face is the same person Refer: EM_FACE_CHECK;
        ('emQRCodeIsExpired', C_ENUM),  # 二维码是否过期。默认值0 (北美测温定制) Refer: EM_QRCODE_IS_EXPIRED;Whether the QR code has expired. Default value 0 (customized for temperature measurement in North America) Refer: EM_QRCODE_IS_EXPIRED;
        ('emQRCodeState', C_ENUM),  # 二维码状态(北美测试定制) Refer: EM_QRCODE_STATE;QR code status (North American test customization) Refer: EM_QRCODE_STATE;
        ('stuQRCodeValidTo', NET_TIME),  # 二维码截止日期;QR code deadline;
        ('emLiftCallerType', C_ENUM),  # 梯控方式触发者 Refer: EM_LIFT_CALLER_TYPE;Ladder control trigger Refer: EM_LIFT_CALLER_TYPE;
        ('nBlockId', C_UINT),  # 上报事件数据序列号从1开始自增;The serial number of the reported event data increases from 1;
        ('szSection', c_char * 64),  # 部门名称;Department name;
        ('szWorkClass', c_char * 256),  # 工作班级;Work class;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('stuTestResult', NET_TEST_RESULT),  # ESD阻值测试结果;ESD resistance test result;
        ('bUseCardNameEx', C_BOOL),  # 是否使用卡命名扩展;Whether to use the card name extension;
        ('szCardNameEx', c_char * 128),  # 卡命名扩展;Card name extension;
        ('nHSJCResult', c_int),  # 核酸检测报告结果  0: 阳性 1: 阴性 2: 未检测 3: 过期;Nucleic acid test report result, 0: positive, 1: negative, 2: not tested, 3: expired;
        ('nVaccinateFlag', c_int),  # 是否已接种新冠疫苗（0:否，1:是）;Have you been vaccinated against the new crown vaccine, 0: No, 1: Yes;
        ('szVaccineName', c_char * 128),  # 新冠疫苗名称;New crown vaccine name;
        ('nDateCount', c_int),  # 历史接种日期有效数;Valid number of historical vaccination dates;
        ('szVaccinateDate', c_char * 256),  # 历史接种日期  历史接种日期 (yyyy-MM-dd)。 ”0000-00-00”，表示已接种，但无具体日期。;Historical vaccination date(yyyy-MM-dd). If you cannot provide the time, fill in "0000-00-00", which means that you have been vaccinated;
        ('emTravelCodeColor', C_ENUM),  # 返回行程码状态信息 Refer: EM_TRAVEL_CODE_COLOR;Travel Code Color Refer: EM_TRAVEL_CODE_COLOR;
        ('nCityCount', c_int),  # 最近14天经过的城市名有效数;Number of cities passed in the last 14 days;
        ('szPassingCity', c_char * 2048),  # 最近14天经过的城市名（按照时间顺序排列）最早经过的城市放第一个。;The names of the cities that have passed in the last 14 days. In chronological order, the earliest passing city is placed first;
        ('szTrafficPlate', c_char * 32),  # 车牌;TrafficPlate;
    ]

class NET_IN_SNAP_MNG_SHOT(Structure):
    """
    即时抓图(又名手动抓图)入参, 对应命令DH_CTRL_SNAP_MNG_SNAP_SHOT
    realtime snapshot (manual snapshot) input parameter, corresponding command DH_CTRL_SNAP_MNG_SNAP_SHOT
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 该结构体大小;the structure size;
        ('nChannel', c_int),  # 通道号;channel number;
        ('nTime', c_int),  # 连拍次数, 0表示停止抓拍,正数表示连续抓拍的张数;continuous snapshot times, 0 means stopping snapshot, positive number means the number of continuous snapshot;
    ]

class NET_OUT_SNAP_MNG_SHOT(Structure):
    """
    即时抓图(又名手动抓图)出参, 对应命令DH_CTRL_SNAP_MNG_SNAP_SHOT
    realtime snapshot (manual snapshot) output parameter, corresponding command DH_CTRL_SNAP_MNG_SNAP_SHOT
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 该结构体大小;the structure size;
    ]

class NET_EVENT_MANUALSNAP_CUSTOM_DATA(Structure):
    """
    手动抓拍专用上报定制内容
    manual-snap custom data
    """
    _fields_ = [
        ('stuWeighInfo', EVENT_CUSTOM_WEIGHT_INFO),  # 建委地磅定制称重信息;custom weight info;
        ('byReserved', C_BYTE * 472),  # 保留字节;Reserved;
    ]

class NET_DEV_EVENT_TRAFFIC_MANUALSNAP_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_MANUALSNAP(交通手动抓拍事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_MANUALSNAP's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;lane number;
        ('szManualSnapNo', C_BYTE * 64),  # 手动抓拍序号;manual snap number;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', SDK_MSG_OBJECT),  # 检测到的车身信息;have being detected vehicle;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 表示交通车辆的数据库记录;TrafficCar info;
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byOpenStrobeState', C_BYTE),  # 开闸状态, 具体请见 EM_OPEN_STROBE_STATE;Open status, see EM_OPEN_STROBE_STATE;
        ('byReserved', C_BYTE * 1),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', SDK_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('bReserved', C_BYTE * 504),  # 保留字节,留待扩展.;
        ('stuCustom', NET_EVENT_MANUALSNAP_CUSTOM_DATA),  # 手动抓拍专用上报内容;Custom data;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_CTRL_OPEN_STROBE(Structure):
    """
    开启道闸参数(对应CTRL_OPEN_STROBE命令)
    open gateway parameter(corresponding to CTRL_OPEN_STROBE command)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelId', c_int),  # 通道号, nChannelId为-1时表示未使用通道号, 表示单通道设备;channel no., when nChannelId is -1,denotes unused channel no. and single channel device;
        ('szPlateNumber', c_char * 64),  # 车牌号码;plate no.;
        ('emOpenType', C_ENUM),  # 开闸类型 Refer: EM_OPEN_STROBE_TYPE;open strobe type Refer: EM_OPEN_STROBE_TYPE;
    ]

class NET_CTRL_CLOSE_STROBE(Structure):
    """
    关闭道闸参数(对应CTRL_CLOSE_STROBE命令)
    close gateway parameter(corresponding to CTRL_CLOSE_STROBE command)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelId', c_int),  # 通道号;channel no.;
    ]

class NET_A_COMM_STATE(Structure):
    """
    串口状态
    Serial port status
    """
    _fields_ = [
        ('uBeOpened', C_UINT),
        ('uBaudRate', C_UINT),
        ('uDataBites', C_UINT),
        ('uStopBits', C_UINT),
        ('uParity', C_UINT),
        ('bReserved', C_BYTE * 32),
    ]

class NET_SMARTDETECT_HUMAN_OBJECT(Structure):
    """
    智能动检(人)对象信息
    object info of smart motion detection about human
    """
    _fields_ = [
        ('nHumanID', C_UINT),  # 人动检ID;object ID about human;
        ('stuRect', NET_RECT),  # 人的位置;rect of human;
        ('bReserved', C_BYTE * 508),  # 保留字节;reserved;
    ]

class NET_A_DEV_EVENT_SMARTMOTION_HUMAN_INFO(Structure):
    """
    事件类型EVENT_ALARM_SMARTMOTION_HUMAN(智能视频移动侦测事件(人))对应的数据块描述信息
    Corresponding to data block description of event type EVENT_ALARM_SMARTMOTION_HUMAN(smart video motion detection event about human)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('nAction', c_int),  # 1:开始 2:停止;event action, 0:pulse, 1:start, 2:stop;;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;UTC;
        ('nEventID', C_UINT),  # 事件ID;event ID;
        ('stuSmartRegion', NET_MOTIONDETECT_REGION_INFO * 32),  # 智能动检区域信息;region info of smart motion detection;
        ('nSmartRegionNum', C_UINT),  # 智能动检区域个数;count of smart motion detection region;
        ('nHumanObjectNum', C_UINT),  # 智能动检(人)对象个数;count of smart motion detection objects about human;
        ('stuHumanObject', NET_SMARTDETECT_HUMAN_OBJECT * 64),  # 智能动检(人)对象信息;object info of smart motion detection about human;
        ('bReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class MANUAL_SNAP_PARAMETER(Structure):
    """
    智能交通, 手动抓拍 (对应结构体 MANUAL_SNAP_PARAMETER)
    manual snap (struct MANUAL_SNAP_PARAMETER)
    """
    _fields_ = [
        ('nChannel', c_int),  # 通道号;snap channel,start with 0
        ('bySequence', C_BYTE * 64),  # 抓图序列号字符串;snap sequence string
        ('byReserved', C_BYTE * 60), # 保留字段;reserved
    ]

class NET_OUT_ADD_ANALYSE_TASK(Structure):
    """
    CLIENT_AddAnalyseTask 接口输出参数
    output parameter of CLIENT_AddAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskID', C_UINT),  # 任务ID;task ID;
        ('nVirtualChannel', C_UINT),  # 任务对应的虚拟通道号;virtual channel;
        ('szUrl', c_char * 256),  # 智能码流rtsp地址;RTSP address of intelligent stream;
    ]

class NET_PUSH_PICFILE_BYRULE_INFO(Structure):
    """
    推送远程图片文件，添加任务时无规则和图片信息，通过推送图片接口，每张图片中带有不同的规则信息（目前能源场景中使用）
    Push remote picture file, add task without rules and picture information, through the push picture interface, each picture has different rule information (currently used in the energy scene)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('emStartRule', C_ENUM),  # 智能任务启动规则 Refer: EM_ANALYSE_TASK_START_RULE;Analyse tesk start rule Refer: EM_ANALYSE_TASK_START_RULE;
        ('szTaskUserData', c_char * 256),  # 任务数据;Task user data;
    ]

class NET_IN_FIND_ANALYSE_TASK(Structure):
    """
    CLIENT_FindAnalyseTask 接口输入参数
    input parameter of CLIENT_FindAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ANALYSE_TASKS_INFO(Structure):
    """
    智能分析任务信息
    info of analyse task
    """
    _fields_ = [
        ('nTaskID', C_UINT),  # 任务ID;task ID;
        ('emAnalyseState', C_ENUM),  # 分析状态 Refer: EM_ANALYSE_STATE;analyse state Refer: EM_ANALYSE_STATE;
        ('emErrorCode', C_ENUM),  # 错误码 Refer: EM_ANALYSE_TASK_ERROR;error code Refer: EM_ANALYSE_TASK_ERROR;
        ('byReserved1', C_BYTE * 4),  # 字节对齐;byte alignment;
        ('szTaskUserData', c_char * 256),  # 任务数据;task user date;
        ('nVideoAnalysisProcess', c_int),  # 录像分析进度，当任务添加接口CLIENT_AddAnalyseTask emDataSourceType参数为录像分析"EM_DATA_SOURCE_REMOTE_PICTURE_FILE"时有效 范围1~100，100表示分析完成;Video analysis progress, is is valid when task add interface CLIENT_AddAnalyseTask's parameter emDataSourceType is "EM_DATA_SOURCE_REMOTE_PICTURE_FILE", the valid range is 1 ~ 100100, indicating that the analysis is completed;
        ('szUrl', c_char * 256),  # 智能流rtsp地址，实时流时才填写;RTSP address of intelligent stream, which can be filled in only when real-time flow;
        ('emClassType', C_ENUM),  # 智能大类类型 Refer: EM_SCENE_CLASS_TYPE;Class type Refer: EM_SCENE_CLASS_TYPE;
        ('emSourceType', C_ENUM),  # 数据源类型 Refer: EM_DATA_SOURCE_TYPE;Source type Refer: EM_DATA_SOURCE_TYPE;
        ('nChipId', c_int),  # 任务使用的分析子卡ID.-1表示无效子卡，大于等于0的值表示子卡ID号emErrorCode为EM_ANALYSE_TASK_ERROR_ANALYZER_OFF_LINE或EM_ANALYSE_TASK_ERROR_ANALYZER_ON_LINE时此字段有效;The analysis sub card ID used by the task. - 1 represents the invalid sub card, and a value greater than or equal to 0 represents the sub card ID numberThis field is valid when the emErrorCode is EM_ANALYSE_TASK_ERROR_ANALYZER_OFF_LINE or EM_ANALYSE_TASK_ERROR_ANALYZER_ON_LINE;
        ('byReserved', C_BYTE * 428),  # 保留字节;reserved bytes;
    ]

class NET_OUT_FIND_ANALYSE_TASK(Structure):
    """
    CLIENT_FindAnalyseTask 接口输出参数
    out parameter of CLIENT_FindAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskNum', C_UINT),  # 智能分析任务个数;number of analyse tasks;
        ('stuTaskInfos', NET_ANALYSE_TASKS_INFO * 64),  # 智能分析任务信息;info of analyse tasks;
    ]

class NET_IN_REMOVE_ANALYSE_TASK(Structure):
    """
    CLIENT_RemoveAnalyseTask 接口输入参数
    input parameter of CLIENT_RemoveAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskID', C_UINT),  # 任务ID;task ID;
    ]

class NET_OUT_REMOVE_ANALYSE_TASK(Structure):
    """
    CLIENT_RemoveAnalyseTask 接口输出参数
    output parameter of CLIENT_RemoveAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ANALYSE_RULE_INFO(Structure):
    """
    智能分析规则信息
    info of analyse rule
    """
    _fields_ = [
        ('emClassType', C_ENUM),  # 分析大类类型 Refer: EM_SCENE_CLASS_TYPE;class type Refer: EM_SCENE_CLASS_TYPE;
        ('dwRuleType', C_DWORD),  # 规则类型, 详见dhnetsdk.h中"智能分析事件类型"
        ('pReserved', c_void_p),  # 规则配置, 具体结构体类型根据dwRuleType来确定, 具体信息见dwRuleType的注释;rule config, the rule config struct is determined by dwRuleType, see the comments of dwRuleType;
        ('nObjectTypeNum', C_UINT),  # 检测物体类型个数, 为0 表示不指定物体类型;count of object types, 0 means no types;
        ('emObjectTypes', C_ENUM * 16),  # 检测物体类型列表 Refer: EM_ANALYSE_OBJECT_TYPE;object types Refer: EM_ANALYSE_OBJECT_TYPE;
        ('szRuleName', c_char * 128),  # 规则名称，不带预置点的设备规则名称不能重名，带预置点的设备，同一预置点内规则名称不能重名，不同预置点之间规则名称可以重名;rule name;
        ('byReserved', C_BYTE * 828),  # 保留字节;reserved bytes;
    ]

class NET_ANALYSE_RULE(Structure):
    """
    智能分析规则
    analyse rule
    """
    _fields_ = [
        ('stuRuleInfos', NET_ANALYSE_RULE_INFO * 32),  # 分析规则信息;info of analyse rules;
        ('nRuleCount', C_UINT),  # 分析规则条数;number of analyse rules;
        ('byReserved', C_BYTE * 1028),  # 保留字节;reserved bytes;
    ]

class NET_REMOTE_STREAM_INFO(Structure):
    """
    远程实时视频源信息("analyseTaskManager.analysePushPictureFileByRule"协议使用)
    Remote real-time video source information (used in protocol "analyseTaskManager.analysePushPictureFileByRule")
    """
    _fields_ = [
        ('emStreamProtocolType', C_ENUM),  # 视频流协议类型 Refer: EM_STREAM_PROTOCOL_TYPE;Stream protocol type Refer: EM_STREAM_PROTOCOL_TYPE;
        ('byReserved1', C_BYTE * 4),  # 用于字节对齐;Used for byte alignment;
        ('szPath', c_char * 256),  # 视频流地址;Video streaming path;
        ('szIp', c_char * 64),  # IP 地址;IP;
        ('wPort', c_uint16),  # 端口号;port;
        ('szUser', c_char * 64),  # 用户名;user;
        ('szPwd', c_char * 64),  # 密码;password;
        ('nChannelID', c_int),  # 通道号;ChannelID;;
        ('nStreamType', C_UINT),  # 码流类型, 0:主码流; 1:辅1码流; 2:辅2码流;;Stream type, 0-main stream, 1-extra stream 1, 2-extra stream 2;
        ('byReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_PUSH_PICTURE_BYRULE_INFO(Structure):
    """
    智能分析图片信息
    Intelligent analysis of picture information
    """
    _fields_ = [
        ('szFileID', c_char * 128),  # 文件ID;File ID;
        ('nOffset', C_UINT),  # 文件数据在二进制数据中的偏移, 单位:字节 (URL和Offset/Length应该是两者有且只有一个);The Offset of the file data in binary data, in bytes (RemoteStreamInfo and Offset/Length should be both and only one).;
        ('nLength', C_UINT),  # 文件数据长度, 单位:字节 (URL和Offset/Length应该是两者有且只有一个);Length of file data, in bytes;
        ('stuRuleInfo', NET_ANALYSE_RULE),  # 分析规则信息;Analyze rule information;
        ('szUserDefineData', c_char * 512),  # 用户定义数据，通过client.notifyTaskResult回调中”UserDefineData”字段带回;User-defined data;
        ('szModelUrl', c_char * 512),  # 模型远程文件url地址，目前支持http方式下载;Model remote file URL address, currently support HTTP download;
        ('stuRemoteStreamInfo', NET_REMOTE_STREAM_INFO),  # 远程实时视频流信息;Remote real-time video streaming information;
        ('nDetectType', C_UINT),  # 能源SDT仪器仪表使用;0：深度学习 1：建模方式;Energy SDT instrument use; 0: Deep learning 1: modeling approach;
        ('byReserved', C_BYTE * 256),  # 保留字节;Reserved;
    ]

class NET_IN_PUSH_ANALYSE_PICTURE_FILE_BYRULE(Structure):
    """
    CLIENT_PushAnalysePictureFileByRule 接口输入参数
    CLIENT_PushAnalysePictureFileByRule input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('nTaskID', C_UINT),  # 任务ID;TaskID;
        ('pstuPushPicByRuleInfos', POINTER(NET_PUSH_PICTURE_BYRULE_INFO)),  # 推送图片信息，文件列表支持url路径和二进制数据两种方式，但是每次只能选择一种方式，即URL和Offset/Length应该是两者有且只有一个用户自定义空间;Push picture information, file list support URL path and binary data two ways, but can only choose one way at a timeUsers apply for their own memory;
        ('nPicNum', C_UINT),  # 推送图片数量,用户定义;Number of images to push, user-defined;
        ('nBinBufLen', C_UINT),  # 数据缓冲区长度, 单位:字节;BufLen;
        ('pBinBuf', POINTER(c_char)),  # 数据缓冲区, 由用户申请和释放,选择nOffset/nLength方式，需要传送图片数据;Data buffers, applied and released by the user;
    ]

class NET_OUT_PUSH_ANALYSE_PICTURE_FILE_BYRULE(Structure):
    """
    CLIENT_PushAnalysePictureFileByRule 接口输出参数
    CLIENT_PushAnalysePictureFileByRule output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
    ]

class NET_IMAGE_INFO(Structure):
    """
    图片信息
    Image info
    """
    _fields_ = [
        ('emPicType', C_ENUM),  # 图片类型 Refer: EM_PIC_TYPE;Picture type Refer: EM_PIC_TYPE;
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移;Offset in binary data;
        ('nLength', C_UINT),  # 图片大小,单位:字节;Length,Unit:Byte;
        ('szFilePath', c_char * 256),  # 图片路径;File path;
        ('byReserved', C_BYTE * 1024),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_DIALRECOGNITION_INFO(Structure):
    """
    仪表检测事件, 对应事件类型 EVENT_IVS_DIALRECOGNITION
    Instrument detection event, corresponding event type EVENT_IVS_DIALRECOGNITION
    """
    _fields_ = [
        ('nChannelID', C_UINT),  # 视频通道号,从0开始;ChannelID;
        ('nPresetID', C_UINT),  # 预置点ID,如果普通IPC则为0;PresetID,If normal IPC is 0;
        ('szTaskID', c_char * 64),  # 任务ID.添加时设备端生成;Task ID. Device generated;
        ('emType', C_ENUM),  # 仪表类型 Refer: EM_INSTRUMENT_TYPE;The instrument type Refer: EM_INSTRUMENT_TYPE;
        ('nRetImageInfoNum', c_int),  # 返回的图片信息个数;Number of image Info returned;
        ('stuImgaeInfo', NET_IMAGE_INFO * 8),  # 图片信息;Image info;
        ('szDialResult', c_char * 2048),  # 检测结果，根据Type的不同，格式也不同;Dial result;
        ('szReserved', c_char * 1024),  # 预留字节;Reserved;
    ]

class NET_A_POINTCOORDINATE(Structure):
    """
    景物点位置
    scenery position
    """
    _fields_ = [
        ('nX', c_int),  # 第一个元素表示景物点的x坐标(0~8191);X coordinate range: [0,8191];
        ('nY', c_int),  # 第二个元素表示景物点的y坐标(0~8191);Y coordinate range: [0,8191];
    ]

class NET_CFG_CALIBRATEBOX_INFO(Structure):
    """
    校准框信息
    Calibrate box info
    """
    _fields_ = [
        ('stuCenterPoint', NET_A_POINTCOORDINATE),  # 校准框中心点坐标(点的坐标归一化到[0,8191]区间);Calibrate box center point. range: [0,8191];
        ('fRatio', c_float),  # 相对基准校准框的比率(比如1表示基准框大小，0.5表示基准框大小的一半);The relative ratio of the calibrate box(such as 1 means the calibrate box,0.5 means the half size of the calibrate box);
    ]

class NET_CFG_SIZE(Structure):
    """
    物体尺寸
    Size
    """
    _fields_ = [
        ('nWidthOrnArea', c_float),  # 宽或面积;Width Or Area;
        ('nHeight', c_float),  # 高;Height;
    ]

class NET_CFG_SIZEFILTER_INFO(Structure):
    """
    尺寸过滤器
    Size filter
    """
    _fields_ = [
        ('nCalibrateBoxNum', c_int),  # 校准框个数;Calibration pane number;
        ('stuCalibrateBoxs', NET_CFG_CALIBRATEBOX_INFO * 10),  # 校准框(远端近端标定模式下有效);Calibration box (far and near-end calibration mode only);
        ('bMeasureModeEnable', c_bool),  # 计量方式参数是否有效;Measurement mode enabled or not;
        ('bMeasureMode', C_BYTE),  # 计量方式,0-像素，不需要远端、近端标定, 1-实际长度，单位：米, 2-远端近端标定后的像素;Measurement mode, 0-pixel, far and near-end calibration not necessary, 1- real length, unit: meter, 2- pixel after far and near-end calibration;
        ('bFilterTypeEnable', c_bool),  # 过滤类型参数是否有效;Filter type enabled or notByArea,ByRatio as compatible only, with independent ByArea and ByRatio alternatives as substitute 2012/03/06;
        ('bFilterType', C_BYTE),  # 过滤类型:0:"ByLength",1:"ByArea", 2"ByWidthHeight";Filter type:0:"ByLength",1:"ByArea", 2"ByWidthHeight";
        ('bFilterMinSizeEnable', c_bool),  # 物体最小尺寸参数是否有效;Min object size parameter is valid or not;
        ('bFilterMaxSizeEnable', c_bool),  # 物体最大尺寸参数是否有效;Max object size parameter is valid or not;
        ('abByArea', c_bool),
        ('abMinArea', c_bool),
        ('abMaxArea', c_bool),
        ('abMinAreaSize', c_bool),
        ('abMaxAreaSize', c_bool),
        ('bByArea', c_bool),  # 是否按面积过滤 通过能力ComplexSizeFilter判断是否可用;Filter by area or not. You can use ComplexSizeFilter to see it works or not.;
        ('stuFilterMinSize', NET_CFG_SIZE),  # 物体最小尺寸 "ByLength"模式下表示宽高的尺寸，"ByArea"模式下宽表示面积，高无效(远端近端标定模式下表示基准框的宽高尺寸)。;Min object size      size of length ratio under "ByLength" Mode,size of area under "ByArea" mode, invalid height (size of standard box lengths under far and near-end calibration mode);
        ('stuFilterMaxSize', NET_CFG_SIZE),  # 物体最大尺寸 "ByLength"模式下表示宽高的尺寸，"ByArea"模式下宽表示面积，高无效(远端近端标定模式下表示基准框的宽高尺寸)。;Max object size size of length ratio under "ByLength" mode, size of area under "ByArea" mode", invalid height (size of standard box lengths under far and near-end calibration mode);
        ('nMinArea', c_float),  # 最小面积;Min area;
        ('nMaxArea', c_float),  # 最大面积;Max area;
        ('stuMinAreaSize', NET_CFG_SIZE),  # 最小面积矩形框尺寸 "计量方式"为"像素"时，表示最小面积矩形框的宽高尺寸；"计量方式"为"远端近端标定模式"时，表示基准框的最小宽高尺寸；;Min area rectangle box.   When  "measurement method" is "pixel", it represents its sizes of lengths; when "measurement method" is "far and near-end calibration mode", it represents the min sizes of lengths of standard box;
        ('stuMaxAreaSize', NET_CFG_SIZE),  # 最大面积矩形框尺寸, 同上;Max area rectangle box, same as above;
        ('abByRatio', c_bool),
        ('abMinRatio', c_bool),
        ('abMaxRatio', c_bool),
        ('abMinRatioSize', c_bool),
        ('abMaxRatioSize', c_bool),
        ('bByRatio', c_bool),  # 是否按宽高比过滤 通过能力ComplexSizeFilter判断是否可用;Filter by length ratio or not   . You can use ComplexSizeFilter to see it works or not.;
        ('bReserved1', c_bool * 2),
        ('dMinRatio', c_double),  # 最小宽高比;Min W/H ratio;
        ('dMaxRatio', c_double),  # 最大宽高比;Max W/H ratio;
        ('stuMinRatioSize', NET_CFG_SIZE),  # 最小宽高比矩形框尺寸，最小宽高比对应矩形框的宽高尺寸。;Min W/H ratio rectangle box size, min W/H ratio corresponding to sizes of lengths of rectangle box;
        ('stuMaxRatioSize', NET_CFG_SIZE),  # 最大宽高比矩形框尺寸，同上;Max W/H ratio rectangle box size. See above information.;
        ('nAreaCalibrateBoxNum', c_int),  # 面积校准框个数;Area calibration box number;
        ('stuAreaCalibrateBoxs', NET_CFG_CALIBRATEBOX_INFO * 10),  # 面积校准框;Area calibration box;
        ('nRatioCalibrateBoxs', c_int),  # 宽高校准框个数;W/H calibration box number;
        ('stuRatioCalibrateBoxs', NET_CFG_CALIBRATEBOX_INFO * 10),  # 宽高校准框;W/H calibration box number;
        ('abBySize', c_bool),  # 长宽过滤使能参数是否有效;Valid filter by L/H ration parameter enabled or not;
        ('bBySize', c_bool),  # 长宽过滤使能;L/W filter enabled;
        ('bReserved', C_BYTE * 518),  # 保留字段;Reserved;
    ]

class NET_IVS_DIALRECOGNITION_RULE_INFO(Structure):
    """
    EVENT_IVS_DIALRECOGNITION(仪表检测事件)对应的规则配置
    Rule type : EVENT_IVS_DIALRECOGNITION(Dial recogntion) configuration
    """
    _fields_ = [
        ('emType', C_ENUM),  # 仪表类型 Refer: EM_DIALDETECT_TYPE;Instrument type Refer: EM_DIALDETECT_TYPE;
        ('bSizeFileter', C_BOOL),  # 规则特定的尺寸过滤器是否有效;Whether the stuSizeFileter is valid;
        ('stuSizeFileter', NET_CFG_SIZEFILTER_INFO),  # 规则特定的尺寸过滤器;Rule-specific size filter;
        ('stuDetectRegion', NET_A_POINTCOORDINATE * 20),  # 检测区域;Detect Region;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;Num of Detect Region;
        ('nKinfeOpenAngleThreshold', c_int),  # 敞开式隔离开关有效,分夹角阈值, 单位度,取值范围0~90, 建议20;The open-type isolating switch is valid, the sub-angle threshold value, unit degree, the value range is 0~90, 20 is recommended;
        ('nKinfeClossAngleThreshold', c_int),  # 敞开式隔离开关有效,合夹角阈值, 单位度,取值范围0~90, 建议10;Open-type isolating switch is valid, closing angle threshold, unit degree, value range 0~90, recommended 10;
        ('bReserved', c_char * 2044),  # 保留字节;Reserved;
    ]

class NET_AIRBORNE_DETECT(Structure):
    """
    挂空悬浮物检测异常输出结果
    Airborne Detect info
    """
    _fields_ = [
        ('emAirborneType', C_ENUM),  # 挂空悬浮物具体类型 Refer: EM_AIRBORNE_TYPE;Airborne type Refer: EM_AIRBORNE_TYPE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_NEST_DETECT(Structure):
    """
    鸟巢检测结果
    Nest Detect info
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_DIAL_DETECT(Structure):
    """
    表盘检测结果
    Dial Detect info
    """
    _fields_ = [
        ('emDialState', C_ENUM),  # 表盘状态 Refer: EM_DIAL_STATE;dial state Refer: EM_DIAL_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_LEAKAGE_DETECT(Structure):
    """
    渗漏检测结果
    Nest Detect info
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_DOOR_DETECT(Structure):
    """
    箱门检测结果
    Door Detect info
    """
    _fields_ = [
        ('emDoorState', C_ENUM),  # 箱门状态 Refer: EM_DOOR_STATE;door state Refer: EM_DOOR_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_RESPIRATOR_DETECT(Structure):
    """
    呼吸器检测结果
    Respirator Detect info
    """
    _fields_ = [
        ('emRespiratorState', C_ENUM),  # 呼吸器状态 Refer: EM_RESPIRATOR_STATE;Respirator state Refer: EM_RESPIRATOR_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_SMOKING_DETECT(Structure):
    """
    吸烟检测结果
    Smoking detect info
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_INSULATOR_DETECT(Structure):
    """
    绝缘子检测结果
    Insulator detect info
    """
    _fields_ = [
        ('emInsulatorState', C_ENUM),  # 绝缘子状态 Refer: EM_INSULATOR_STATE;insulator state Refer: EM_INSULATOR_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_COVER_PLATE_DETECT(Structure):
    """
    盖板检测结果
    Cover plate detect info
    """
    _fields_ = [
        ('emCoverPlateState', C_ENUM),  # 盖板状态 Refer: EM_COVER_PLATE_STATE;cover plate state Refer: EM_COVER_PLATE_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_PRESSING_PLATE_DETECT(Structure):
    """
    压板检测结果
    Pressing plate detect info
    """
    _fields_ = [
        ('emPressingPlateState', C_ENUM),  # 压板状态 Refer: EM_PRESSING_PLATE_STATE;pressing plate state Refer: EM_PRESSING_PLATE_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_METAL_CORROSION(Structure):
    """
    金属锈蚀结果
    The result of metal corrosion
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;Bounding box;
        ('bReserved', c_char * 128),  # 预留字段;Reserved;
    ]

class NET_A_DEV_EVENT_ELECTRICFAULTDETECT_INFO(Structure):
    """
    仪表类缺陷检测事件
    Electric fault detection
    """
    _fields_ = [
        ('emClassType', C_ENUM),  # 智能事件所属大类 Refer: EM_CLASS_TYPE;class type Refer: EM_CLASS_TYPE;
        ('nChannel', C_UINT),  # 视频通道号;channel id;
        ('nRuleID', C_UINT),  # 智能事件规则编号，用于标示哪个规则触发的事件;Rule id;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;PTS;
        ('nPresetID', C_UINT),  # 预置点ID;preset ID;
        ('nUTCMS', C_UINT),  # 事件时间毫秒数;UTCMS;
        ('emEnableRules', C_ENUM * 16),  # 对应设备所使能的检测规则 Refer: EM_A_ELECTRIC_FAULT_ENABLE_RULES;enable rules Refer: EM_A_ELECTRIC_FAULT_ENABLE_RULES;
        ('nEnableRulesNum', c_int),  # 设备所使能的检测规则个数;enable rules number;
        ('nAirborneDetectNum', c_int),  # 挂空悬浮物检测异常输出结果个数;Airborne Detect number;
        ('stuAirborneDetectInfo', NET_AIRBORNE_DETECT * 8),  # 挂空悬浮物检测异常输出结果;Airborne Detect info;
        ('stuNestDetectInfo', NET_NEST_DETECT * 8),  # 鸟巢检测结果;Nest Detect info;
        ('nNestDetectNum', c_int),  # 鸟巢检测结果个数;Nest Detect number;
        ('nDialDetectNum', c_int),  # 表盘检测结果个数;Dial Detect number;
        ('stuDialDetectInfo', NET_DIAL_DETECT * 8),  # 表盘检测结果;Dial Detect info;
        ('stuLeakageDetectInfo', NET_LEAKAGE_DETECT * 8),  # 渗漏检测结果;Leakage Detect info;
        ('nLeakageDetectNum', c_int),  # 渗漏检测结果个数;Leakage Detect number;
        ('nDoorDetectNum', c_int),  # 箱门检测结果个数;Door Detect number;
        ('stuDoorDetectInfo', NET_DOOR_DETECT * 8),  # 箱门检测结果;Door Detect info;
        ('stuRespiratorDetectInfo', NET_RESPIRATOR_DETECT * 8),  # 呼吸器检测结果;Respirator Detect info;
        ('nRespiratorDetectNum', c_int),  # 呼吸器检测个数;Respirator Detect number;
        ('nSmokingDetectNum', c_int),  # 吸烟检测结果个数;Smoking detect number;
        ('stuSmokingDetectInfo', NET_SMOKING_DETECT * 8),  # 吸烟检测结果;Smoking detect info;
        ('stuSceneImageInfo', SCENE_IMAGE_INFO),  # 大图;Scene image info;
        ('stuInsulatorDetectInfo', NET_INSULATOR_DETECT * 8),  # 绝缘子检测结果;Insulator detect info;
        ('nInsulatorDetectNum', c_int),  # 绝缘子检测结果个数;Insulator detect number;
        ('nCoverPlateDetectNum', c_int),  # 盖板检测结果个数;Cover plate detect number;
        ('stuCoverPlateDetectInfo', NET_COVER_PLATE_DETECT * 8),  # 盖板检测结果;Cover plate detect info;
        ('stuPressingPlateDetectInfo', NET_PRESSING_PLATE_DETECT * 8),  # 压板检测结果;Pressing plate detect info;
        ('nPressingPlateDetectNum', c_int),  # 压板检测结果个数;Pressing plate detect number;
        ('nMetalCorrosionNum', c_int),  # 金属锈蚀结果个数;Metal corrosion detect number;
        ('stuMetalCorrosionInfo', NET_METAL_CORROSION * 8),  # 金属锈蚀结果;Metal Corrosion detect Info;
        ('bReserved', C_BYTE * 1024),  # 预留字段;Reserved;
    ]

class NET_IVS_ELECTRICFAULT_DETECT_RULE_INFO(Structure):
    """
    EVENT_IVS_ELECTRICFAULT_DETECT(仪表类缺陷检测事件)对应的规则配置
    Rule type : EVENT_IVS_ELECTRICFAULT_DETECT(Electric fault detect)configuration
    """
    _fields_ = [
        ('bAirborneDetectEnable', C_BOOL),  # 挂空悬浮物检测使能;AirborneDetect enable;
        ('bNestDetectEnable', C_BOOL),  # 鸟巢检测使能;Nest detect enable;
        ('bDialDetectEnable', C_BOOL),  # 表盘检测(表盘模糊)使能;Dial detect enable;
        ('bLeakageDetectEnable', C_BOOL),  # 渗漏检测使能;Leakage detect enable;
        ('bDoorDetectEnable', C_BOOL),  # 箱门检测使能;Door detect enable;
        ('bRespiratorDetectEnable', C_BOOL),  # 呼吸器检测使能;Respirator detect enable;
        ('bSmokingDetectEnable', C_BOOL),  # 吸烟检测使能;Smoking detect enable;
        ('bInsulatorDetectEnable', C_BOOL),  # 绝缘子检测使能;Insulator detect enable;
        ('bCoverPlateDetectEnable', C_BOOL),  # 盖板检测使能;Cover plate detect enable;
        ('bPressingPlateDetectEnable', C_BOOL),  # 压板开合检测使能;Pressing plate detect enable;
        ('bMetalCorrosionEnable', C_BOOL),  # 金属锈蚀检测使能;Metal corrosion enable;
        ('bSizeFileter', C_BOOL),  # 规则特定的尺寸过滤器是否有效;Whether the stuSizeFileter is valid;
        ('stuSizeFileter', NET_CFG_SIZEFILTER_INFO),  # 规则特定的尺寸过滤器;Rule-specific size filter;
        ('stuDetectRegion', NET_A_POINTCOORDINATE * 20),  # 检测区域;Detect Region;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;Num of Detect Region;
        ('bReserved', c_char * 2048),  # 保留字节;Reserved;
    ]

class NET_CB_ANALYSE_TASK_STATE_INFO(Structure):
    """
    智能分析任务状态回调信息
    callback info of attach analyse state
    """
    _fields_ = [
        ('stuTaskInfos', NET_ANALYSE_TASKS_INFO * 64),  # 智能分析任务信息;info of analyse task;
        ('nTaskNum', C_UINT),  # 任务个数;number of task;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved bytes;
    ]

class NET_IN_ATTACH_ANALYSE_TASK_STATE(Structure):
    """
    CLIENT_AttachAnalyseTaskState 接口输入参数
    input parameter of CLIENT_AttachAnalyseTaskState
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskIDs', C_UINT * 64),  # 智能分析任务ID;task IDs;
        ('nTaskIdNum', C_UINT),  # 智能分析任务个数, 0表示订阅全部任务;number of analyse task, 0 is means attach all;
        ('cbAnalyseTaskState', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_CB_ANALYSE_TASK_STATE_INFO), C_LDWORD)),  # 智能分析任务状态订阅函数;callback function of attach analyse state;
        ('dwUser', C_LDWORD),  # 用户数据;user data;
    ]

class NET_ANALYSE_RESULT_FILTER(Structure):
    """
    智能分析结果订阅的过滤条件
    filter condition of attach analyse result
    """
    _fields_ = [
        ('dwAlarmTypes', C_DWORD * 64),  # 过滤事件, 详见dhnetsdk.h中"智能分析事件类型";event types, see "intelligent analyse event type" in dhnetsdk.h;
        ('nEventNum', C_UINT),  # 过滤事件数量;number of events which are used as filter condition;
        ('nImageDataFlag', c_int),  # 是否包含图片, 0-包含,  1-不包含;need image, 0-need, 1-no;
        ('byReserved1', C_BYTE * 4),  # 对齐;alignment;
        ('nImageTypeNum', c_int),  # pImageType有效个数;pImageType valid num;
        ('pImageType', POINTER(C_ENUM)),  # 过滤上报的图片类型 Refer: EM_FILTER_IMAGE_TYPE;image data type Refer: EM_FILTER_IMAGE_TYPE;
        ('byReserved', C_BYTE * 1004),  # 保留字节;reserved bytes;
    ]

class NET_SECONDARY_ANALYSE_EVENT_INFO(Structure):
    """
    二次录像分析事件信息
    the event info of secondary record analysis
    """
    _fields_ = [
        ('emEventType', C_ENUM),  # 事件类型 Refer: EM_ANALYSE_EVENT_TYPE;event type Refer: EM_ANALYSE_EVENT_TYPE;
        ('byReserved1', C_BYTE * 4),  # 字节对齐;byte alignment;
        ('pstEventInfo', c_void_p),  # 事件信息, 根据emEventType确定不同的结构体;event info, determine the specific struct according to emEventType;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_TASK_CUSTOM_DATA(Structure):
    """
    任务自定义数据
    Custorm data for task
    """
    _fields_ = [
        ('szClientIP', c_char * 128),  # 客户端IP;Client IP;
        ('szDeviceID', c_char * 128),  # 设备ID;Device ID;
        ('byReserved', C_BYTE * 256),  # 保留字节;Reserved;
    ]

class NET_ANALYSE_TASK_RESULT(Structure):
    """
    智能分析任务结果信息
    result of analyse task
    """
    _fields_ = [
        ('nTaskID', C_UINT),  # 任务ID;task ID;
        ('szFileID', c_char * 128),  # 文件ID, 分析文件时有效;file ID, used for file analyse;
        ('emFileAnalyseState', C_ENUM),  # 文件分析状态 Refer: EM_FILE_ANALYSE_STATE;file analyse state Refer: EM_FILE_ANALYSE_STATE;
        ('szFileAnalyseMsg', c_char * 256),  # 文件分析额外信息, 一般都是分析失败的原因;additional info about file analyse, usually it is failure info.;
        ('stuEventInfos', NET_SECONDARY_ANALYSE_EVENT_INFO * 8),  # 事件信息;info of events;
        ('nEventCount', c_int),  # 实际的事件个数;number of events;
        ('stuCustomData', NET_TASK_CUSTOM_DATA),  # 自定义数据;custorm data for task;
        ('szUserData', c_char * 64),  # 频源数据，标示视频源信息，对应addPollingTask中UserData字段。;user data.;
        ('szTaskUserData', c_char * 256),  # 任务数据;task user data;
        ('pstuEventInfosEx', POINTER(NET_SECONDARY_ANALYSE_EVENT_INFO)),  # 扩展事件信息;Extended event information;
        ('nRetEventInfoExNum', c_int),  # 返回扩展事件信息个数;Number of extended event information returned;
        ('szUserDefineData', c_char * 512),  # 用户定义数据，对应analyseTaskManager.analysePushPictureFileByRule中UserDefineData字段;User-defined data;
        ('byReserved', C_BYTE * 184),  # 保留字节;Reserved bytes;
    ]

class NET_CB_ANALYSE_TASK_RESULT_INFO(Structure):
    """
    智能分析任务结果回调信息
    callback info of analyse result
    """
    _fields_ = [
        ('stuTaskResultInfos', NET_ANALYSE_TASK_RESULT * 64),  # 智能分析任务结果信息;result of analyse tasks;
        ('nTaskResultNum', C_UINT),  # 任务个数;numbet of tasks;
        ('byReserved', C_BYTE * 1028),  # 保留字节;reserved bytes;
    ]

class NET_IN_ATTACH_ANALYSE_RESULT(Structure):
    """
    CLIENT_AttachAnalyseTaskResult 接口输入参数
    input parameter of CLIENT_AttachAnalyseTaskResult
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskIDs', C_UINT * 64),  # 智能分析任务ID;task IDs;
        ('nTaskIdNum', C_UINT),  # 智能分析任务个数, 0表示订阅全部任务;number of tasks, 0 is means attach all;
        ('stuFilter', NET_ANALYSE_RESULT_FILTER),  # 过滤条件;filter confition;
        ('byReserved', C_BYTE * 4),  # 对齐;for alignment;
        ('cbAnalyseTaskResult', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_CB_ANALYSE_TASK_RESULT_INFO), POINTER(c_char), C_DWORD, C_LDWORD)),  # 智能分析任务结果订阅函数;callback function of attach analyse result;
        ('dwUser', C_LDWORD),  # 用户数据;user data;
    ]

class NET_A_ALARM_EVENT_CROSSLINE_INFO(Structure):
    """
    警戒线事件(对应事件 EVENT_CROSSLINE_DETECTION)
    Warning line event (Corresponding to event  EVENT_CROSSLINE_DETECTION)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号;Channel No.;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp (Unit is ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nEventAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation. 0=pulse event.1=continious event begin. 2=continuous event stop;
        ('emCrossDirection', C_ENUM),  # 入侵方向 Refer: EM_A_NET_CROSSLINE_DIRECTION_INFO;Intrusion direction Refer: EM_A_NET_CROSSLINE_DIRECTION_INFO;
        ('nOccurrenceCount', c_int),  # 规则被触发生次数;Triggered amount;
        ('nLevel', c_int),  # 事件级别,GB30147需求项;Event type;
        ('bIsObjectInfo', C_BOOL),  # 是否检测到物体信息;Target information detection enablement;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体信息;Object information detected;
        ('nRetObjectNum', c_int),  # 实际返回多个检测到的物体信息;Actually returns multiple detected object information;
        ('stuObjects', SDK_MSG_OBJECT * 100),  # 多个检测到的物体信息;Multiple detected object information;
    ]

class NET_A_ALARM_EVENT_CROSSREGION_INFO(Structure):
    """
    警戒区事件(对应事件 EVENT_CROSSREGION_DETECTION)
    Warning zone event( Corresponding to event EVENT_CROSSREGION_DETECTION)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号;Channel No.;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp (Unit is ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nEventAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation. 0=pulse event.1=continues event begin. 2=continuous event stop;
        ('emDirection', C_ENUM),  # 警戒区入侵方向 Refer: EM_A_NET_CROSSREGION_DIRECTION_INFO;Warning zone intrusion direction Refer: EM_A_NET_CROSSREGION_DIRECTION_INFO;
        ('emActionType', C_ENUM),  # 警戒区检测动作类型 Refer: EM_A_NET_CROSSREGION_ACTION_INFO;Detected types in the warning zone Refer: EM_A_NET_CROSSREGION_ACTION_INFO;
        ('nOccurrenceCount', c_int),  # 规则被触发生次数;Rule triggered amount;
        ('nLevel', c_int),  # 事件级别,GB30147需求项;Event type;
        ('szName', c_char * 128),  # 名称;name;
        ('bIsObjectInfo', C_BOOL),  # 是否检测到物体信息;Target information detection enablement;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体信息;Object information detected;
        ('nRetObjectNum', c_int),  # 实际返回多个检测到的物体信息;Actually returns multiple detected object information;
        ('stuObjects', SDK_MSG_OBJECT * 100),  # 多个检测到的物体信息;Multiple detected object information;
    ]

class NET_A_ALARM_LOGIN_FAILIUR_INFO(Structure):
    """
    登陆失败事件
    login failed event
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nAction', c_int),  # 0:开始 1:停止;0:start 1:stop;
        ('nSequence', C_UINT),  # 序号;no.;
        ('szName', c_char * 128),  # 事件名,填用户名称;event name, fill in user name;
        ('szType', c_char * 128),  # 登录类型;login type;
        ('szAddr', c_char * 128),  # 来源IP地址;source IP address;
        ('nError', c_int),  # 用户登陆失败错误码;user login failed error code;
    ]

class NET_A_IN_MATRIX_GET_CAMERAS(Structure):
    """
    CLIENT_MatrixGetCameras接口的输入参数
    CLIENT_MatrixGetCameras's interface input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_SOURCE_STREAM_ENCRYPT(Structure):
    """
    显示源码流加密方式
    The encrypt of stream info
    """
    _fields_ = [
        ('emEncryptLevel', C_ENUM),  # 加密等级 Refer: EM_ENCRYPT_LEVEL;Encrypt level Refer: EM_ENCRYPT_LEVEL;
        ('emAlgorithm', C_ENUM),  # 加密算法 Refer: EM_ENCRYPT_ALGORITHM_TYPE;The type of stream encrypt algorithm Refer: EM_ENCRYPT_ALGORITHM_TYPE;
        ('emExchange', C_ENUM),  # 密钥交换方式 Refer: EM_KEY_EXCHANGE_TYPE;The type of exchange key Refer: EM_KEY_EXCHANGE_TYPE;
        ('bUnvarnished', C_BOOL),  # MTS使用场景,true为交互MIKEY后让数据不进行加/解密;MTS using scene,true is interacting with MIKEY and than donot encrypt data;
        ('szPSK', c_char * 1032),  # 密钥;key;
        ('byReserved', C_BYTE * 1024),  # 保留字节;Revered;
    ]

class NET_A_VIDEO_INPUTS(Structure):
    """
    视频输入通道信息
    channel info of video input
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szChnName', c_char * 64),  # 通道名称;channel name;
        ('bEnable', C_BOOL),  # 使能;enable;
        ('szControlID', c_char * 128),  # 控制ID;control ID;
        ('szMainStreamUrl', c_char * 260),  # 主码流url地址;main stream url;
        ('szExtraStreamUrl', c_char * 260),  # 辅码流url地址;extra stream url;
        ('nOptionalMainUrlCount', c_int),  # 备用主码流地址数量;spare main stream address quantity;
        ('szOptionalMainUrls', c_char * 2080),  # 备用主码流地址列表;spare main stream address list;
        ('nOptionalExtraUrlCount', c_int),  # 备用辅码流地址数量;spare sub stream address quantity;
        ('szOptionalExtraUrls', c_char * 2080),  # 备用辅码流地址列表;spare substream address list;
        ('szCaption', c_char * 32),  # 通道备注;caption;
        ('emServiceType', C_ENUM),  # 指码流传输的服务类型 Refer: EM_STREAM_TRANSMISSION_SERVICE_TYPE;service type Refer: EM_STREAM_TRANSMISSION_SERVICE_TYPE;
        ('stuSourceStreamEncrypt', NET_SOURCE_STREAM_ENCRYPT),  # 码流加密方式;The encrypt of stream info;
    ]

class NET_REMOTE_DEVICE_EX(Structure):
    """
    远程设备信息扩展
    info of remote device extend
    """
    _fields_ = [
        ('szPwdEx2', c_char * 128),  # 密码;password;
        ('bUsePwdEx2', C_BOOL),  # 是否使用szPwdEx2密码;use szPwdEx2 password;
        ('szReserved', c_char * 1020),  # 保留字节;Reserved;
    ]

class NET_A_REMOTE_DEVICE(Structure):
    """
    远程设备信息
    info of remote device
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('bEnable', C_BOOL),  # 使能;enable;
        ('szIp', c_char * 16),  # IP;IP;
        ('szUser', c_char * 8),  # 用户名,建议使用szUserEx;username;
        ('szPwd', c_char * 8),  # 密码,建议使用szPwdEx;password;
        ('nPort', c_int),  # 端口;port;
        ('nDefinition', c_int),  # 清晰度, 0-标清, 1-高清;definition. 0-standard definition, 1-high definition;
        ('emProtocol', C_ENUM),  # 协议类型 Refer: EM_A_DEVICE_PROTOCOL;protocol type Refer: EM_A_DEVICE_PROTOCOL;
        ('szDevName', c_char * 64),  # 设备名称;device name;
        ('nVideoInputChannels', c_int),  # 视频输入通道数;count channel of video input;
        ('nAudioInputChannels', c_int),  # 音频输入通道数;count channel of audio input;
        ('szDevClass', c_char * 32),  # 设备类型, 如IPC, DVR, NVR等;device type, such as IPC, DVR, NVR;
        ('szDevType', c_char * 32),  # 设备具体型号, 如IPC-HF3300;device type, such as IPC-HF3300;
        ('nHttpPort', c_int),  # Http端口;Http port;
        ('nMaxVideoInputCount', c_int),  # 视频输入通道最大数;max count of video input;
        ('nRetVideoInputCount', c_int),  # 返回实际通道个数;return count;
        ('pstuVideoInputs', POINTER(NET_A_VIDEO_INPUTS)),  # 视频输入通道信息,由用户申请内存，大小为sizeof(VIDEO_INPUTS)*nMaxVideoInputCount;max count of audion input, user malloc the memory,apply to sizeof(VIDEO_INPUTS)*nMaxVideoInputCount;
        ('szMachineAddress', c_char * 256),  # 设备部署地;machine address;
        ('szSerialNo', c_char * 48),  # 设备序列号;serial no.;
        ('nRtspPort', c_int),  # Rtsp端口;Rtsp Port;
        ('szUserEx', c_char * 32),  # 用户名;username;
        ('szPwdEx', c_char * 32),  # 密码，szPwdEx只支持31位密码长度，当密码需要大于等于32位时，使用pstuRemoteDevEx里的szPwdEx2;password,When the password needs to be greater than or equal to 32 bits, use szpwdex2 in pstuRemoteDevEx;
        ('szVendorAbbr', c_char * 32),  # 厂商缩写;vendor abbreviation;
        ('szSoftwareVersion', c_char * 64),  # 设备软件版本;software version;
        ('stuActivationTime', NET_TIME),  # 启动时间;activation time;
        ('szMac', c_char * 20),  # MAC地址;MAC;
        ('nHttpsPort', c_int),  # HttpsPort;HttpsPort;
        ('byReserved', C_BYTE * 4),  # 保留字段;Reserved;
        ('pstuRemoteDevEx', POINTER(NET_REMOTE_DEVICE_EX)),  # 用于REMOTE_DEVICE新增字段扩展,由用户申请内存，大小为sizeof(NET_REMOTE_DEVICE_EX);REMOTE_DEVICE extend,user malloc the memory,apply to sizeof(NET_REMOTE_DEVICE_EX);
    ]

class NET_A_MATRIX_CAMERA_INFO(Structure):
    """
    可用的显示源信息
    available according to the source of information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称;name;
        ('szDevID', c_char * 128),  # 设备ID;device ID;
        ('szControlID', c_char * 128),  # 控制ID;control ID;
        ('nChannelID', c_int),  # 通道号, DeviceID设备内唯一;channel ID, DeviceID is unique;
        ('nUniqueChannel', c_int),  # 设备内统一编号的唯一通道号;unique channel;
        ('bRemoteDevice', C_BOOL),  # 是否远程设备;support remote device or not;
        ('stuRemoteDevice', NET_A_REMOTE_DEVICE),  # 远程设备信息;info of remote device;
        ('emStreamType', C_ENUM),  # 视频码流类型 Refer: EM_A_NET_STREAM_TYPE;stream type Refer: EM_A_NET_STREAM_TYPE;
        ('emChannelType', C_ENUM),  # 通道类型 Refer: EM_A_NET_LOGIC_CHN_TYPE;Channel Types Refer: EM_A_NET_LOGIC_CHN_TYPE;
        ('bEnable', C_BOOL),  # 仅在使用DeviceID添加/删除设备时的使能，通过DeviceInfo操作不要使用;Enable only when using DeviceID to add/remove a device, do not use it through DeviceInfo operation;
        ('emVideoStream', C_ENUM),  # 视频码流 Refer: EM_VIDEO_STREAM;Video stream Refer: EM_VIDEO_STREAM;
    ]

class NET_A_OUT_MATRIX_GET_CAMERAS(Structure):
    """
    CLIENT_MatrixGetCameras接口的输出参数
    CLIENT_MatrixGetCameras's interface output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pstuCameras', POINTER(NET_A_MATRIX_CAMERA_INFO)),  # 显示源信息数组, 用户分配内存,大小为sizeof(MATRIX_CAMERA_INFO)*nMaxCameraCount;array;
        ('nMaxCameraCount', c_int),  # 显示源数组大小;size of source array,the space application by the user,apply to sizeof(MATRIX_CAMERA_INFO)*nMaxCameraCount;
        ('nRetCameraCount', c_int),  # 返回的显示源数量;return count;
    ]

class NET_CB_RTMP_MANAGER_INFO(Structure):
    """
    推送的数据内容
    Pushed data content
    """
    _fields_ = [
        ('nPushId', C_UINT),  # 推流ID;Push ID;
        ('emStatus', C_ENUM),  # 状态变化 Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;State change Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
        ('bReserved', C_BYTE * 256),  # 保留字段;Reserved;
    ]

class NET_CB_RTMP_STATUS_INFO(Structure):
    """
    回调函数RTMP状态信息
    Callback function RTMP status information
    """
    _fields_ = [
        ('nSID', C_UINT),  # 订阅id号;Subscription ID number;
        ('stuInfo', NET_CB_RTMP_MANAGER_INFO),  # 推送的数据内容;Pushed data content;
        ('bReserved', C_BYTE * 1024),  # 保留字段;Reserved;
    ]

class NET_IN_RTMP_MANAGER_ATTACH_STATUS(Structure):
    """
    CLIENT_AttachStatusRTMPManager入参
    CLIENT_AttachStatusRTMPManager Input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要订阅的推流ID;Push ID;
        ('cbRTMPAttachStatusCallBack', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_CB_RTMP_STATUS_INFO), C_LDWORD)),  # 入参回调函数;Parameter callback function;
        ('dwUser', C_LDWORD),  # 用户自定义参数;User defined parameters;
    ]

class NET_OUT_RTMP_MANAGER_ATTACH_STATUS(Structure):
    """
    CLIENT_AttachStatusRTMPManager出参
    CLIENT_AttachStatusRTMPManager Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nSID', C_UINT),  # 订阅id号;Subscription ID number;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_DETACH_STATUS(Structure):
    """
    CLIENT_DetachStatusRTMPManager 入参
    CLIENT_DetachStatusRTMPManager Input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要取消订阅的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_DETACH_STATUS(Structure):
    """
    CLIENT_DetachStatusRTMPManager出参
    CLIENT_DetachStatusRTMPManager Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
    ]

class NET_IN_RTMP_MANAGER_GETPUSHINFOS(Structure):
    """
    CLIENT_GetPushInfosRTMPManager 接口入参
    CLIENT_GetPushInfosRTMPManager Interface input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
    ]

class NET_RTMP_MANAGER_PUSHINFOS(Structure):
    """
    已创建推流任务的信息
    Information of created streaming task
    """
    _fields_ = [
        ('nPushId', C_UINT),  # 推流ID;Push flow ID;
        ('emType', C_ENUM),  # 推流地址类型 Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;Streaming address type Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;
        ('emStatus', C_ENUM),  # 推流状态 Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;Push flow state Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;
        ('szReserved', c_char * 1028),  # 预留字节;Reserved;
    ]

class NET_OUT_RTMP_MANAGER_GETPUSHINFOS(Structure):
    """
    CLIENT_GetPushInfosRTMPManager 接口出参
    CLIENT_GetPushInfosRTMPManager Interface output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushInfosNum', c_int),  # 已创建推流任务的信息个数;Number of information created for streaming task;
        ('stuPushInfos', NET_RTMP_MANAGER_PUSHINFOS * 32),  # 已创建推流任务的信息;Information of created streaming task;
    ]

class NET_IN_MANUAL_SNAP(Structure):
    """
    CLIENT_ManualSnap 接口输入参数
    Input param of CLIENT_ManualSnap
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nChannel', C_UINT),  # 抓图通道号;Capture channel number;
        ('nCmdSerial', C_UINT),  # 请求序列号;Serial number;
        ('szFilePath', c_char * 260),  # 抓图保存路径;Capture save path;
    ]

class NET_OUT_MANUAL_SNAP(Structure):
    """
    CLIENT_ManualSnap 接口输出参数
    Output param of CLIENT_ManualSnap
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nMaxBufLen', C_UINT),  # pRcvBuf的长度,由用户指定;The length of pRcvBuf. Its value is specified by the user;
        ('pRcvBuf', POINTER(c_char)),  # 接收图片缓冲, 用于存放抓图数据, 空间由用户申请和释放, 申请大小为nMaxBufLen;Buffer of capture, It is Used to store snapshot data.The space is applied and released by the user, and the application size is nmaxbuflen.;
        ('nRetBufLen', C_UINT),  # 实际接收到的图片大小;Actual received picture size;
        ('emEncodeType', C_ENUM),  # 图片编码格式 Refer: EM_SNAP_ENCODE_TYPE;Picture encoding format Refer: EM_SNAP_ENCODE_TYPE;
        ('nCmdSerial', C_UINT),  # 请求序列号;Serial number;
        ('bReserved', C_BYTE * 4),  # 字节对齐;Byte alignment;
    ]

class NET_A_OPR_RIGHT_EX(Structure):
    """
    权限信息
    Right information
    """
    _fields_ = [
        ('dwID', C_DWORD),
        ('name', c_char * 32),
        ('memo', c_char * 32),
    ]

class NET_A_USER_GROUP_INFO_EX(Structure):
    """
    用户组信息
    User group information
    """
    _fields_ = [
        ('dwID', C_DWORD),
        ('name', c_char * 16),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 100),
        ('memo', c_char * 32),
    ]

class NET_A_USER_INFO_EX(Structure):
    """
    用户信息
    User information
    """
    _fields_ = [
        ('dwID', C_DWORD),
        ('dwGroupID', C_DWORD),
        ('name', c_char * 16),
        ('passWord', c_char * 16),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 100),
        ('memo', c_char * 32),
        ('dwFouctionMask', C_DWORD),  # 掩码,0x00000001 - 支持用户复用;Subnet mask,0x00000001 - support reuse;
        ('byReserve', C_BYTE * 32),
    ]

class NET_A_USER_MANAGE_INFO_EX(Structure):
    """
    用户信息表
    User information sheet
    """
    _fields_ = [
        ('dwRightNum', C_DWORD),  # 权限信息;Right information;
        ('rightList', NET_A_OPR_RIGHT_EX * 100),
        ('dwGroupNum', C_DWORD),  # 用户组信息;User group information;
        ('groupList', NET_A_USER_GROUP_INFO_EX * 20),
        ('dwUserNum', C_DWORD),  # 用户信息;User information;
        ('userList', NET_A_USER_INFO_EX * 200),
        ('dwFouctionMask', C_DWORD),  # 掩码；0x00000001 - 支持用户复用,0x00000002 - 密码修改需要校验;Subnet mask;0x00000001 - support reuse, 0x00000002 - Password has been modified , it needs to be verified.;
        ('byNameMaxLength', C_BYTE),  # 支持的用户名最大长度;The supported user name max length;
        ('byPSWMaxLength', C_BYTE),  # 支持的密码最大长度;The supported password max length;
        ('byReserve', C_BYTE * 254),
    ]

class NET_IN_ADD_ONVIF_USER_INFO(Structure):
    """
    添加Onvif用户，CLIENT_AddOnvifUser 入参
    Add Onvif User, CLIENT_AddOnvifUser Input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szName', c_char * 128),  # 用户名;UserName;
        ('szPassword', c_char * 128),  # 密码;Password;
        ('emGroupType', C_ENUM),  # 用户所在的组 Refer: EM_GROUP_TYPE;User Group Refer: EM_GROUP_TYPE;
    ]

class NET_OUT_ADD_ONVIF_USER_INFO(Structure):
    """
    添加Onvif用户，CLIENT_AddOnvifUser 出参
    Add Onvif User, CLIENT_AddOnvifUser Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ONVIF_USER_INFO(Structure):
    """
    Onvif 新用户信息
    Onvif New user information
    """
    _fields_ = [
        ('szName', c_char * 128),  # 用户名;User name;
        ('szPassword', c_char * 128),  # 密码;password;
        ('stuPasswordModifiedTime', NET_TIME),  # 最近修改密码的时间;Recently modified password time;
        ('emGroupType', C_ENUM),  # 用户所在的组 Refer: EM_GROUP_TYPE;User Group Refer: EM_GROUP_TYPE;
        ('bReserved', C_BOOL),  # 用户是否为保留用户，保留用户不可删除;if the user keeps the user, the user must not be deleted;
        ('byReserved', C_BYTE * 512),  # 保留字节;reserved;
    ]

class NET_IN_MODIFYONVIF_USER_INFO(Structure):
    """
    修改 Onvif用户，CLIENT_ModifyOnvifUser 入参
    Modify onvif user, CLIENT_ModifyOnvifUser Entry parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szName', c_char * 128),  # 需要修改的用户名称;User name that needs to be modified;
        ('stUserInfo', NET_ONVIF_USER_INFO),  # 新用户信息;New user information;
    ]

class NET_OUT_MODIFYONVIF_USER_INFO(Structure):
    """
    修改 Onvif用户，CLIENT_ModifyOnvifUser 出参
    Modify onvif user, CLIENT_ModifyOnvifUser Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_IN_GETONVIF_USERINFO_ALL_INFO(Structure):
    """
    获取所有 Onvif 用户信息，CLIENT_GetOnvifUserInfoAll 入参
    Get all onvif user information, CLIENT_GetOnvifUserInfoAll Enter parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_GETONVIF_USERINFO_ALL_INFO(Structure):
    """
    获取所有 Onvif 用户信息， CLIENT_GetOnvifUserInfoAll 出参
    Get all onvif user information, CLIENT_GetOnvifUserInfoAll Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nRetUserInfoNumber', c_int),  # 本次已查询到的个数;The number of this query;
        ('stuUserInfo', NET_ONVIF_USER_INFO * 20),  # 用户信息列表(无法获取到密码信息);User information list(unable to get password information);
    ]

class NET_IN_MODIFYONVIF_PASSWORD_INFO(Structure):
    """
    修改 Onvif 用户密码， CLIENT_ModifyOnvifUserPassword 入参
    Modify the Onvif user password, CLIENT_ModifyOnvifUserPassword Enter parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szName', c_char * 128),  # 用户名称;User name;
        ('szPwd', c_char * 128),  # 用户密码;User password;
        ('szPwdOld', c_char * 128),  # 旧密码;old password;
    ]

class NET_OUT_MODIFYONVIF_PASSWORD_INFO(Structure):
    """
    修改 Onvif 用户密码，CLIENT_ModifyOnvifUserPassword 出参
    Modify the Onvif user password, CLIENT_ModifyOnvifUserPassword Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_IN_RTMP_MANAGER_GETCAPS(Structure):
    """
    获取设备RTMP推流能力入参
    Get the RTMP streaming capability input parameter of the device
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
    ]

class NET_OUT_RTMP_MANAGER_GETCAPS(Structure):
    """
    获取设备RTMP推流能力出参
    Get the RTMP streaming capability input parameter of the device
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nMaxLive', C_UINT),  # 最大实时流推流通道数;Maximum number of real-time streaming channels;
        ('nMaxRecord', C_UINT),  # 最大录像流推流通道数;Maximum number of video streaming channels;
    ]

class NET_RTMP_MANAGER_LIVE_STREAM(Structure):
    """
    Type为0表示实时流时，需要填写
    If the type is 0, it means real-time flow, which needs to be filled in
    """
    _fields_ = [
        ('nChannel', c_int),  # 通道号;channel id;
        ('emStreamType', C_ENUM),  # 码流类型 Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;stream type Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;
        ('byReserved', C_BYTE * 1024),  # 预留字节;reserved;
    ]

class NET_RTMP_MANAGER_RECORD_STREAM(Structure):
    """
    Type为1表示回放流时，需要填写
    When type is 1, it means that it is required to fill in when playing back the stream
    """
    _fields_ = [
        ('szFilePath', c_char * 260),  # 录像文件路径;Video file path;
        ('szStartTime', c_char * 20),  # 录像开始时间;video start time;
        ('szEndTime', c_char * 20),  # 录像结束时间;video stop time;
        ('nChannel', c_int),  # 通道号;channel id;
        ('emStreamType', C_ENUM),  # 码流类型，默认为主码流 Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;Code stream type. It is the main code stream by default Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;
        ('byReserved', C_BYTE * 1024),  # 预留字节;reserved;
    ]

class NET_IN_RTMP_MANAGER_ADD(Structure):
    """
    添加推流地址入参
    Add streaming address input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emType', C_ENUM),  # 添加推流地址类型 Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;Add streaming address type Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;
        ('stuLiveStream', NET_RTMP_MANAGER_LIVE_STREAM),  # Type为0表示实时流时，需要填写;If the type is 0, it means Live stream, which needs to be filled in;
        ('stuRecordStream', NET_RTMP_MANAGER_RECORD_STREAM),  # Type为1表示回放流时，需要填写;If the type is 1, it means Record stream, which needs to be filled in;
        ('szUrl', c_char * 512),  # 添加推流地址;Add streaming address;
    ]

class NET_OUT_RTMP_MANAGER_ADD(Structure):
    """
    添加推流地址出参
    Add streaming address output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 添加成功返回推流ID，失败时填0;The push stream ID is returned after adding successfully, and 0 is filled in if it fails;
        ('emErrCode', C_ENUM),  # Add 表示错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_ERRCODE;Add Indicates the error code Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_REMOVE(Structure):
    """
    删除推流地址入参
    Delete streaming address input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要删除的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_REMOVE(Structure):
    """
    删除推流地址出参
    Delete streaming address output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_START(Structure):
    """
    启动推流入参
    Start push in parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要启动的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_START(Structure):
    """
    启动推流出参
    Start push out parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_STOP(Structure):
    """
    停止推流入参
    Stop pushing input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要停止的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_STOP(Structure):
    """
    停止推流出参
    Stop pushing out parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_PAUSE(Structure):
    """
    暂停推流入参
    Pause push in parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要暂停的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_PAUSE(Structure):
    """
    暂停推流出参
    Pause pushing out parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_RESUME(Structure):
    """
    恢复推流入参
    Resume push in parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要恢复的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_RESUME(Structure):
    """
    恢复推流出参
    Resume push out parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_SET_SPEED(Structure):
    """
    设置倍速推流入参
    Set the double speed push parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要恢复的推流ID;Push ID;
        ('dbSpeed', c_double),  # 播放速度，正数表示正向播放，负数表示反向播放，数据表示倍数;Playback speed: >0:indicates forward playback, <0:indicates reverse playback,data indicates multiple;
    ]

class NET_OUT_RTMP_MANAGER_SET_SPEED(Structure):
    """
    设置倍速推流出参
    Set double speed push out parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_SCREEN_SHOW_INFO(Structure):
    """
    屏幕信息
    Screen information
    """
    _fields_ = [
        ('nScreenNo', C_UINT),  # 屏幕编号;Screen no;
        ('szText', c_char * 256),  # 显示文本(文本类型为EM_SCREEN_TEXT_TYPE_LOCAL_TIME时的时间格式,%Y 年%M 月%D 日%H 时(24小时机制)%h 时(12小时)%m 分%S 秒%W 星期%T 显示上午或下午%X 表示显示普通文本内容;
                              # Display text (time format for text type EM_SCREEN_TEXT_TYPE_LOCAL_TIME,%Y Year%M months%D day%H 24-hour mechanism%h 12 hours%m min%S seconds%W week%T  shows morning or afternoon%X means to display normal text content;
        ('emTextType', C_ENUM),  # 文本类型 Refer: EM_SCREEN_TEXT_TYPE;Text type Refer: EM_SCREEN_TEXT_TYPE;
        ('emTextColor', C_ENUM),  # 文本颜色 Refer: EM_SCREEN_TEXT_COLOR;Text color Refer: EM_SCREEN_TEXT_COLOR;
        ('emTextRollMode', C_ENUM),  # 文本滚动模式 Refer: EM_SCREEN_TEXT_ROLL_MODE;Text roll mode Refer: EM_SCREEN_TEXT_ROLL_MODE;
        ('nRollSpeed', C_UINT),  # 文本滚动速度由慢到快分为1~5;Text scrolling speed is divided into 1 ~ 5 from slow to fast;
        ('byReserved', C_BYTE * 252),  # 保留字节;Reserved;
    ]

class NET_BROADCAST_INFO(Structure):
    """
    播报信息
    Broadcast information
    """
    _fields_ = [
        ('szText', c_char * 256),  # 语音文本;Voice text;
        ('emTextType', C_ENUM),  # 文本类型 Refer: EM_BROADCAST_TEXT_TYPE;Text type Refer: EM_BROADCAST_TEXT_TYPE;
        ('byReserved', C_BYTE * 252),  # 保留字节;Reserved;
    ]

class NET_IN_SET_PARK_CONTROL_INFO(Structure):
    """
    设置停车控制信息(点阵屏和语音播报的控制) CLIENT_ControlDeviceEx入参(对应 CTRL_SET_PARK_CONTROL_INFO )
    Set parking control information(Control of dot matrix screen and voice broadcast) CLIENT_ControlDeviceEx in parameters (corresponding to CTRL_SET_PARK_CONTROL_INFO )
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nScreenShowInfoNum', c_int),  # 屏幕信息个数;Number of screen control information;
        ('stuScreenShowInfo', NET_SCREEN_SHOW_INFO * 16),  # 屏幕信息;Screen control information;
        ('byReserved', C_BYTE * 4),  # 字节补齐;Byte completion;
        ('nBroadcastInfoNum', c_int),  # 播报信息个数;Number of broadcast control information;
        ('stuBroadcastInfo', NET_BROADCAST_INFO * 16),  # 播报信息;Broadcast control information;
    ]

class NET_OUT_SET_PARK_CONTROL_INFO(Structure):
    """
    设置停车控制信息(点阵屏和语音播报的控制) CLIENT_ControlDeviceEx出参(对应 CTRL_SET_PARK_CONTROL_INFO)
    Set parking control information(Control of dot matrix screen and voice broadcast) CLIENT_ControlDeviceEx out parameters (corresponding to CTRL_SET_PARK_CONTROL_INFO )
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
    ]

class NET_CTRL_SET_PARK_INFO(Structure):
    """
    设置停车信息,对应CTRL_SET_PARK_INFO命令参数
    Set park info, corresponding CTRL_SET_PARK_INFO command parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szPlateNumber', c_char * 64),  # 车牌号码;Plate number;
        ('nParkTime', C_UINT),  # 停车时长,单位:分钟;park time,Unit:minute;
        ('szMasterofCar', c_char * 32),  # 车主姓名;Master of car;
        ('szUserType', c_char * 32),  # 用户类型,非通用,用于出入口抓拍一体机monthlyCardUser表示月卡用户,yearlyCardUser表示年卡用户,longTimeUser表示长期用户/VIP,casualUser表示临时用户/Visitor;User type,not general,Used in entrance capture machinemonthlyCardUser means monthly card user,yearlyCardUser means yearly card user,longTimeUser means long time user/VIP,casualUser means casual user/Visitor;
        ('nRemainDay', C_UINT),  # 到期天数;Remain day;
        ('szParkCharge', c_char * 32),  # 停车费;Park charge;
        ('nRemainSpace', C_UINT),  # 停车库余位数;Remain space;
        ('nPassEnable', C_UINT),  # 0:不允许车辆通过 1:允许车辆通过;0:car is not allowed to pass,1:car is allowed to pass;
        ('stuInTime', NET_TIME),  # 车辆入场时间;car in time;
        ('stuOutTime', NET_TIME),  # 车辆出场时间;car out time;
        ('emCarStatus', C_ENUM),  # 过车状态 Refer: EM_CARPASS_STATUS;car pass status Refer: EM_CARPASS_STATUS;
        ('szCustom', c_char * 128),  # 自定义显示字段，默认空;custom field,default:null;
        ('szSubUserType', c_char * 64),  # 用户类型（szUserType字段）的子类型;Sub user type of szUserType;
        ('szRemarks', c_char * 64),  # 备注信息;Remarks info;
        ('szResource', c_char * 64),  # 资源文件（视频或图片）视频支持:mp4格式; 图片支持:BMP/jpg/JPG/jpeg/JPEG/png/PNG格式;Resource file(video or picture) video support:mp4; picture support:BMP/jpg/JPG/jpeg/JPEG/png/PNG;
        ('nParkTimeout', C_UINT),  # 停车超时时间，单位分钟。为0表示未超时，不为0表示超时时间。;Parking timeout, in minutes. A value of 0 means no timeout, and a value of not 0 means timeout.;
    ]

class NET_A_OPR_RIGHT_NEW(Structure):
    """
    权限信息
    Rights info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('name', c_char * 32),
        ('memo', c_char * 32),
    ]

class NET_A_USER_GROUP_INFO_NEW(Structure):
    """
    用户组信息
    User group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('name', c_char * 16),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 1024),
        ('memo', c_char * 32),
    ]

class NET_A_USER_INFO_NEW(Structure):
    """
    用户信息
    User info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('dwGroupID', C_DWORD),
        ('name', c_char * 128),
        ('passWord', c_char * 128),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 1024),
        ('memo', c_char * 32),
        ('dwFouctionMask', C_DWORD),  # 掩码,0x00000001 - 支持用户复用;Sub mask,0x00000001 - Support account reusable;
        ('stuTime', NET_TIME),  # 最后修改时间;Last Revise Time;
        ('byIsAnonymous', C_BYTE),  # 是否可以匿名登录, 0:不可匿名登录, 1: 可以匿名登录;Whether Can Be Anonymous Login,0=Can't Be Anonymous Login,1=Can be Anonymous Login;
        ('byReserve', C_BYTE * 7),
    ]

class NET_A_USER_GROUP_INFO_EX2(Structure):
    """
    用户组信息扩展,用户组名加长
    user group information expand,user group lengthen
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('name', c_char * 128),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 1024),
        ('memo', c_char * 32),
    ]

class NET_A_USER_MANAGE_INFO_NEW(Structure):
    """
    用户信息表
    User info list
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwRightNum', C_DWORD),  # 权限信息;Rights info;
        ('rightList', NET_A_OPR_RIGHT_NEW * 1024),
        ('dwGroupNum', C_DWORD),  # 用户组数;User group info;
        ('groupList', NET_A_USER_GROUP_INFO_NEW * 20),  # 用户组信息,此参数废弃,请使用groupListEx;
        ('dwUserNum', C_DWORD),  # 用户信息;User info;
        ('userList', NET_A_USER_INFO_NEW * 200),
        ('dwFouctionMask', C_DWORD),  # 掩码；0x00000001 - 支持用户复用,0x00000002 - 密码修改需要校验;Sub mask; 0x00000001 - Support account reusable,0x00000002 - Verification needed when change password;
        ('byNameMaxLength', C_BYTE),  # 支持的用户名最大长度;Max user name length supported;
        ('byPSWMaxLength', C_BYTE),  # 支持的密码最大长度;Max password length supported;
        ('byReserve', C_BYTE * 254),
        ('groupListEx', NET_A_USER_GROUP_INFO_EX2 * 20),  # 用户组信息扩展;User Group Information Expand;
    ]

class NET_ALARM_SAFETY_ABNORMAL_INFO(Structure):
    """
    安全报警事件(对应 ALARM_SAFETY_ABNORMAL)
    Safety Abnormal alarm info(corresponding to ALARM_SAFETY_ABNORMAL)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 事件动作, 0: 脉冲;Event Action 0:Pulse;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;The time when the event occurred;
        ('emExceptionType', C_ENUM),  # 异常事件类型 Refer: EM_EXCEPTION_TYPE;Exception Type Refer: EM_EXCEPTION_TYPE;
        ('szAddress', c_char * 64),  # 来源IP地址;Source IP address;
        ('stuAbnormalTime', NET_TIME),  # 发生异常时间;Abnormal time;
        ('szUser', c_char * 128),  # 发生的用户名;User;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved bytes;
    ]

class NET_CTRL_RECORDSET_INSERT_IN(Structure):
    """
    记录集新增操作(insert)输入参数
    New Record Set Operation(Insert)Parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emType', C_ENUM),  # 记录集信息类型 Refer: EM_NET_RECORD_TYPE;Record Information Type Refer: EM_NET_RECORD_TYPE;
        ('pBuf', c_void_p),  # 记录集信息缓存,详见EM_NET_RECORD_TYPE注释，由用户申请内存.;Record Information Cache,The EM_NET_RECORD_TYPE Note is Details,the space application by the user;
        ('nBufLen', c_int),  # 记录集信息缓存大小,大小参照记录集信息类型对应的结构体;Record Information Cache Size,please refer to the structure of EM_NET_RECORD_TYPE;
    ]

class NET_CTRL_RECORDSET_INSERT_OUT(Structure):
    """
    记录集新增操作(insert)输出参数
    Record New Operation(Insert) Parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nRecNo', c_int),  # 记录编号(新增insert时设备返回);Record Number(The Device Come Back When New Insert );
    ]

class NET_CTRL_RECORDSET_INSERT_PARAM(Structure):
    """
    记录集新增操作(insert)参数
    Record New Operation (Insert)Parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('stuCtrlRecordSetInfo', NET_CTRL_RECORDSET_INSERT_IN),  # 记录集信息(用户填写);Record Information(User Write);
        ('stuCtrlRecordSetResult', NET_CTRL_RECORDSET_INSERT_OUT),  # 记录集信息(设备返回);Record Information(the Device Come Back);
    ]

class NET_A_FIND_RECORD_ACCESSCTLCARD_CONDITION(Structure):
    """
    门禁卡记录查询条件
    Entrance Card Record Query Conditions
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szCardNo', c_char * 32),  # 卡号;Card Number;
        ('szUserID', c_char * 32),  # 用户ID;User ID;
        ('bIsValid', C_BOOL),  # 是否有效, TRUE:有效,FALSE:无效;Whether effective, TRUE: effective, FALSE: invalid;
        ('abCardNo', C_BOOL),  # 卡号查询条件是否有效,针对成员 szCardNo;Card inquire condition effects or not, for member szCardNo;
        ('abUserID', C_BOOL),  # 用户ID查询条件是否有效,针对成员 szUserID;User ID inquire condition effects or not, for member  szUserID;
        ('abIsValid', C_BOOL),  # IsValid查询条件是否有效,针对成员 bIsValid;IsValid inquire condition effects or not, for member  bIsValid;
    ]

class NET_ACCESSCTLCARD_FINGERPRINT_PACKET(Structure):
    """
    指纹数据，只用于下发信息
    fingerprint data, for sending only
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nLength', c_int),  # 单个数据包长度,单位字节;length of a finger print packet, unit: byte;
        ('nCount', c_int),  # 包个数;packet number;
        ('pPacketData', POINTER(c_char)),  # 所有指纹数据包，用户申请内存并填充，长度为 nLength*nCount;all fingerprint packet in a single buffer, allocated and filled by user, nLength*nCount bytes;
    ]

class NET_ACCESSCTLCARD_FINGERPRINT_PACKET_EX(Structure):
    """
    指纹数据扩展，可用于下发和获取信息
    fingerprint data, for sending and receiving
    """
    _fields_ = [
        ('nLength', c_int),  # 单个数据包长度,单位字节;length of a finger print packet, unit: byte;
        ('nCount', c_int),  # 包个数;packet number;
        ('pPacketData', POINTER(c_char)),  # 所有指纹数据包, 用户申请内存,大小至少为nLength * nCount;all fingerprint packet in a single buffer, allocated by user,the space application is over nLength * nCount;
        ('nPacketLen', c_int),  # pPacketData 指向内存区的大小，用户填写;pPacketData buffer length, set by user;
        ('nRealPacketLen', c_int),  # 返回给用户实际指纹总大小;The actual fingerprint size returned to the user, equal to nLength*nCount;
        ('nDuressIndex', c_int),  # 胁迫指纹序号，范围1~nCount;duress index of fingerprint group, range: 1~nCount;
        ('byReverseed', C_BYTE * 1020),  # 保留大小;Reserved size;
    ]

class NET_FLOORS_INFO(Structure):
    """
    楼层号（梯控需求）
    Floor number (elevator control requirements)
    """
    _fields_ = [
        ('nFloorNumEx2', c_int),  # 有效的楼层数量再次扩展;The number of effective floors expanded again;
        ('szFloorEx', c_char * 2048),  # 楼层号(梯控需求)最多不超过256个，楼层号不超过999;Floor numbers (elevator control requirements) no more than 256, floor numbers no more than 999;
        ('byReserved', C_BYTE * 512),  # 保留字节;Reserved byte;
    ]

class NET_RECORDSET_ACCESS_CTL_CARD(Structure):
    """
    门禁卡记录集信息
    Access Control Card Info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nRecNo', c_int),  # 记录集编号,只读;Record Number,Read-Only;
        ('stuCreateTime', NET_TIME),  # 创建时间;Creat Time;
        ('szCardNo', c_char * 32),  # 卡号;Card number;
        ('szUserID', c_char * 32),  # 用户ID, 设备暂不支持;User's ID;
        ('emStatus', C_ENUM),  # 卡状态 Refer: EM_A_NET_ACCESSCTLCARD_STATE;Card Stetue Refer: EM_A_NET_ACCESSCTLCARD_STATE;
        ('emType', C_ENUM),  # 卡类型 Refer: EM_A_NET_ACCESSCTLCARD_TYPE;Card Type Refer: EM_A_NET_ACCESSCTLCARD_TYPE;
        ('szPsw', c_char * 64),  # 卡密码;Card Password;
        ('nDoorNum', c_int),  # 有效的门数目;;Valid Door Number;;
        ('sznDoors', c_int * 32),  # 有权限的门序号,即CFG_CMD_ACCESS_EVENT配置的数组下标;Privileged Door Number,That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('nTimeSectionNum', c_int),  # 有效的的开门时间段数目;the Number of Effective Open Time;
        ('sznTimeSectionNo', c_int * 32),  # 开门时间段索引,即CFG_ACCESS_TIMESCHEDULE_INFO的数组下标;Open Time Segment Index,That is CFG_ACCESS_TIMESCHEDULE_INFO Array subscript;
        ('nUserTime', c_int),  # 使用次数,仅当来宾卡时有效;Frequency of Use;
        ('stuValidStartTime', NET_TIME),  # 开始有效期, 设备暂不支持时分秒;Valid Start Time;
        ('stuValidEndTime', NET_TIME),  # 结束有效期, 设备暂不支持时分秒;Valid End Time;
        ('bIsValid', C_BOOL),  # 是否有效,TRUE有效;FALSE无效;Wether Valid,True =Valid,False=Invalid;
        ('stuFingerPrintInfo', NET_ACCESSCTLCARD_FINGERPRINT_PACKET),  # 下发指纹数据信息，仅为兼容性保留，请使用 stuFingerPrintInfoEx;fingerprint data info (send only), DEPRECATED! use stuFingerPrintInfoEx instead;
        ('bFirstEnter', C_BOOL),  # 是否拥有首卡权限;has first card or not;
        ('szCardName', c_char * 64),  # 卡命名;card naming;
        ('szVTOPosition', c_char * 64),  # 门口机关联位置;VTO link position;
        ('bHandicap', C_BOOL),  # 是否为残疾人卡;Card for handicap, TRUE:yes, FALSE:no;
        ('bEnableExtended', C_BOOL),  # 启用成员 stuFingerPrintInfoEx;Enabled member stuFingerPrintInfoEx;
        ('stuFingerPrintInfoEx', NET_ACCESSCTLCARD_FINGERPRINT_PACKET_EX),  # 指纹数据信息;fingerprint data info structure;
        ('nFaceDataNum', c_int),  # 人脸数据个数不超过20;face detection data number,can not > 20;
        ('szFaceData', c_char * 40960),  # 人脸模版数据;face detection data;
        ('szDynamicCheckCode', c_char * 16),  # 动态校验码。VTO等设备会保存此校验码，以后每次刷卡都以一定的算法生成新校验码并写入IC卡中，同时更新VTO设备的校验码，只有卡号和此校验码同时验证通过时才可开门。缺点：目前方案只支持一卡刷一个设备。;dynamic check code;
        ('nRepeatEnterRouteNum', c_int),  # 反潜路径个数;repeat enter route num;
        ('arRepeatEnterRoute', c_int * 12),  # 反潜路径;repeat enter route;
        ('nRepeatEnterRouteTimeout', c_int),  # 反潜超时时间;repeat enter route timeout;
        ('bNewDoor', C_BOOL),  # 是否启动新开门授权字段，TRUE表示使用nNewDoorNum和nNewDoors字段下发开门权限;enable to new field, TRUE: user nNewDoorNum,nNewDoors;
        ('nNewDoorNum', c_int),  # 有效的门数目;;Valid Door Number;;
        ('nNewDoors', c_int * 128),  # 有权限的门序号,即CFG_CMD_ACCESS_EVENT配置的数组下标;Privileged Door Number, That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('nNewTimeSectionNum', c_int),  # 有效的的开门时间段数目;the Number of Effective Open Time;
        ('nNewTimeSectionNo', c_int * 128),  # 开门时间段索引,即CFG_ACCESS_TIMESCHEDULE_INFO的数组下标;Open Time Segment Index,That is CFG_ACCESS_TIMESCHEDULE_INFO Array subscript;
        ('szCitizenIDNo', c_char * 32),  # 身份证号码;ID card no;
        ('nSpecialDaysScheduleNum', c_int),  # 假日计划表示数量;SpecialDaysSchedule Number;
        ('arSpecialDaysSchedule', c_int * 128),  # 假日计划标识;SpecialDaysSchedule Identification;
        ('nUserType', C_UINT),  # 用户类型, 0 普通用户, 1 黑名单用户;user type, 0:common, 1:blacklist;
        ('nFloorNum', c_int),  # 有效的楼层数量;floor number;
        ('szFloorNo', c_char * 256),  # 楼层号;floor;
        ('szSection', c_char * 64),  # 部门名称;Section name;
        ('nScore', c_int),  # 信用积分;credit score;
        ('szCompanyName', c_char * 200),  # 单位名称;company name;
        ('nSectionID', C_UINT),  # 部门ID;Section ID;
        ('emSex', C_ENUM),  # 性别 Refer: EM_A_NET_ACCESSCTLCARD_SEX;sex Refer: EM_A_NET_ACCESSCTLCARD_SEX;
        ('szRole', c_char * 32),  # 角色;Role;
        ('szProjectNo', c_char * 32),  # 项目ID;project No.;
        ('szProjectName', c_char * 64),  # 项目名称;project name;
        ('szBuilderName', c_char * 64),  # 施工单位全称;builder name;
        ('szBuilderID', c_char * 32),  # 施工单位ID;builder ID;
        ('szBuilderType', c_char * 32),  # 施工单位类型;builder type;
        ('szBuilderTypeID', c_char * 8),  # 施工单位类别ID;builder type ID;
        ('szPictureID', c_char * 64),  # 人员照片ID;picture ID;
        ('szContractID', c_char * 16),  # 原合同系统合同编号;contract ID in original contract system;
        ('szWorkerTypeID', c_char * 8),  # 工种ID;worker type ID;
        ('szWorkerTypeName', c_char * 32),  # 工种名称;worker type name;
        ('bPersonStatus', C_BOOL),  # 人员状态, TRUE:启用, FALSE:禁用;person status, TRUE:enable, FALSE:forbidden;
        ('emAuthority', C_ENUM),  # 用户权限 Refer: EM_A_NET_ACCESSCTLCARD_AUTHORITY;user authority Refer: EM_A_NET_ACCESSCTLCARD_AUTHORITY;
        ('szCompanionName', c_char * 120),  # 陪同人姓名;name of companion;
        ('szCompanionCompany', c_char * 200),  # 陪同人单位;company of companion;
        ('stuTmpAuthBeginTime', NET_TIME),  # 临时授权开始时间,当该时间和其他时间同时生效时，以此时间为最高优先级;temporary auth begin Time,high priority;
        ('stuTmpAuthEndTime', NET_TIME),  # 临时授权结束时间,当该时间和其他时间同时生效时，以此时间为最高优先级;temporary auth end Time,high priority;
        ('bFloorNoExValid', C_BOOL),  # 楼层号扩展 szFloorNoEx 是否有效;is szFloorNoEx valid, TRUE:valid, else invalid;
        ('nFloorNumEx', c_int),  # 有效的楼层数量扩展;floor number extended;
        ('szFloorNoEx', c_char * 2048),  # 楼层号扩展;floor info;
        ('szSubUserID', c_char * 32),  # 用户ID（定制）;sub user id(customized);
        ('szPhoneNumber', c_char * 32),  # 人员电话号码;phone number;
        ('szPhotoPath', c_char * 256),  # 人员照片对应在ftp上的路径;photo path;
        ('szCause', c_char * 64),  # 来访原因;cause for visit;
        ('szCompanionCard', c_char * 32),  # 陪同人员证件号（定制）;companion card(customized);
        ('szCitizenAddress', c_char * 128),  # 身份证地址;citizen address;
        ('stuBirthDay', NET_TIME),  # 出生日期（年月日有效）;birth day (year month day are valid);
        ('bFloorNoEx2Valid', C_BOOL),  # stuFloors2 是否有效;Is stuFloorsEx2 valid;
        ('pstuFloorsEx2', POINTER(NET_FLOORS_INFO)),  # 楼层号（再次扩展）;Floor number (extended again);
        ('szDefaultFloor', c_char * 8),  # 默认楼层号（梯控需求);Default floor number (elevator control requirements);
        ('nUserTimeSectionNum', c_int),  # 用户时间段有效个数;Number of valid user time periods;
        ('szUserTimeSections', c_char * 120),  # 针对用户自身的开门时间段校验，最多支持6个时间段;Check the user's own door opening time zone, supporting up to 6 time zones;
        ('szWorkClass', c_char * 256),  # 工作班别;Work class;
        ('stuStartTimeInPeriodOfValidity', NET_TIME),  # 有效时间段内启动时间;Start time in valid time period;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('nAuthOverdueTime', C_UINT),  # 授权时间、过期时间，时间单位: 小时;Authorization time, expiration time, time unit: hour;
        ('emGreenCNHealthStatus', C_ENUM),  # 人员健康状态（定制添加） Refer: EM_GREENCNHEALTH_STATUS;Staff health status Refer: EM_GREENCNHEALTH_STATUS;
        ('emAllowPermitFlag', C_ENUM),  # 电子通行证状态（定制添加） Refer: EM_ALLOW_PERMIT_FLAG;E-pass status Refer: EM_ALLOW_PERMIT_FLAG;
        ('emRentState', C_ENUM),  # 对接第三方平台数据, 秦皇岛保障房定制项目使用, 其他情况禁用 Refer: EM_RENT_STATE;Connect to third-party platform data, use Qinhuangdao security housing customized project, other circumstances disabled Refer: EM_RENT_STATE;
    ]

class NET_A_ALARM_ACCESS_CTL_EVENT_INFO(Structure):
    """
    门禁事件
    access control event
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nDoor', c_int),  # 门通道号;Door Channel Number;
        ('szDoorName', c_char * 128),  # 门禁名称;Entrance Guard Name;
        ('stuTime', NET_TIME),  # 报警事件发生的时间;Alarm Event Triggered Time;
        ('emEventType', C_ENUM),  # 门禁事件类型 Refer: EM_A_NET_ACCESS_CTL_EVENT_TYPE;Entrance Guard Event Type Refer: EM_A_NET_ACCESS_CTL_EVENT_TYPE;
        ('bStatus', C_BOOL),  # 刷卡结果,TRUE表示成功,FALSE表示失败;Swing Card Result,True is Success,False is Fail;
        ('emCardType', C_ENUM),  # 卡类型 Refer: EM_A_NET_ACCESSCTLCARD_TYPE;Card Type Refer: EM_A_NET_ACCESSCTLCARD_TYPE;
        ('emOpenMethod', C_ENUM),  # 开门方式 Refer: EM_A_NET_ACCESS_DOOROPEN_METHOD;Open The Door Method Refer: EM_A_NET_ACCESS_DOOROPEN_METHOD;
        ('szCardNo', c_char * 32),  # 卡号;Card Number;
        ('szPwd', c_char * 64),  # 密码;Password;
        ('szReaderID', c_char * 32),  # 门读卡器ID;Reader ID;
        ('szUserID', c_char * 64),  # 开门用户;unlock user;
        ('szSnapURL', c_char * 256),  # 抓拍照片存储地址;snapshot picture storage address;
        ('nErrorCode', c_int),  # 开门操作码，配合 bStatus 使用0x00 没有错误0x10 未授权0x11 卡挂失或注销0x12 没有该门权限0x13 开门模式错误0x14 有效期错误0x15 防反潜模式0x16 胁迫报警未打开0x17 门常闭状态0x18 AB互锁状态0x19 巡逻卡0x1A 设备处于闯入报警状态0x20 时间段错误0x21 假期内开门时间段错误0x23 卡逾期0x30 需要先验证有首卡权限的卡片0x40 卡片正确,输入密码错误0x41 卡片正确,输入密码超时0x42 卡片正确,输入指纹错误0x43 卡片正确,输入指纹超时0x44 指纹正确,输入密码错误0x45 指纹正确,输入密码超时0x50 组合开门顺序错误0x51 组合开门需要继续验证0x60 验证通过,控制台未授权0x61 卡片正确,人脸错误0x62 卡片正确,人脸超时0x63 重复进入0x64 未授权,需要后端平台识别0x65 体温过高0x66 未戴口罩0x67 健康码获取失败0x68 黄码禁止通行0x69 红码禁止通行0x6a 健康码无效0x6b 绿码验证通过0x6e 绿码,行程码非绿码0x6f 绿码，抗原为阳性0x70 获取健康码信息0x71 校验身份证信息（平台下发对应身份证号的校验结果）0xA8 未佩戴安全帽（定制）0xB1 授权信息不足，待补充;
                              # Open door operate code, use with bStatus0x00 no error0x10 unauthorized0x11 card lost or cancelled0x12 no door right0x13 unlock mode error0x14 valid period error0x15 anti sneak into mode0x16 forced alarm not unlocked0x17 door NC status0x18 AB lock status0x19 patrol card0x1A device is under intrusion alarm status0x20 period error0x21 unlock period error in holiday period0x23 Card is overdue0x30 first card right check required0x40 card correct, input password error0x41 card correct, input password timed out0x42 card correct, input fingerprint error0x43 card correct, input fingerprint timed out0x44 fingerprint correct, input password error0x45 fingerprint correct, input password timed out0x50 group unlock sequence error0x51 test required for group unlock0x60 test passed, control unauthorized0x61 card correct, face error0x62 card correct,face timeout0x63 repeat enter0x64 unauthorized, requiring back-end platform identification0x65 high body temperature0x66 no mask0x67 get health code fail0x68 No Entry because of yellow code0x69 No Entry because of red code0x6a health code is invalid0x6b entry because of green code0x6e Green code, travel code not green code0x6f Green code, antigen positive0x70 get health code info0x71 verify citizenId (platform issues the verification result of the corresponding citizenId)0xA8 not wear safety helmet (customized)0xB1 insufficient authorization information, to be supplemented;
        ('nPunchingRecNo', c_int),  # 刷卡记录集中的记录编号;punching record number;
        ('nNumbers', c_int),  # 抓图张数;pic Numbers;
        ('emStatus', C_ENUM),  # 卡状态 Refer: EM_A_NET_ACCESSCTLCARD_STATE;Card Status Refer: EM_A_NET_ACCESSCTLCARD_STATE;
        ('szSN', c_char * 32),  # 智能锁序列号;wireless deivce serial number;
        ('emAttendanceState', C_ENUM),  # 考勤状态 Refer: EM_A_NET_ATTENDANCESTATE;attend state Refer: EM_A_NET_ATTENDANCESTATE;
        ('szQRCode', c_char * 512),  # 二维码;QRcode;
        ('szCallLiftFloor', c_char * 16),  # 呼梯楼层号;Floor of Call Lift;
        ('emCardState', C_ENUM),  # 是否为采集卡片 Refer: EM_CARD_STATE;Collect as card or not Refer: EM_CARD_STATE;
        ('szCitizenIDNo', c_char * 20),  # 身份证号;Citizen card ID;
        ('szCompanionCards', c_char * 192),  # 陪同者卡号信息;The companion cards list;
        ('nCompanionCardCount', c_int),  # 陪同者卡号个数;The number of companion cards;
        ('emHatStyle', C_ENUM),  # 帽子类型 Refer: EM_HAT_STYLE;hat style Refer: EM_HAT_STYLE;
        ('emHatColor', C_ENUM),  # 帽子颜色 Refer: EM_UNIFIED_COLOR_TYPE;hat color Refer: EM_UNIFIED_COLOR_TYPE;
        ('emLiftCallerType', C_ENUM),  # 梯控方式触发者 Refer: EM_LIFT_CALLER_TYPE;lift caller type Refer: EM_LIFT_CALLER_TYPE;
        ('bManTemperature', C_BOOL),  # 人员温度信息是否有效;Whether the information of human body temperature is valid;
        ('stuManTemperatureInfo', NET_MAN_TEMPERATURE_INFO),  # 人员温度信息, bManTemperature 为TRUE 时有效;Information of human body temperature, It is valid whne bManTemperature is TURE;
        ('szCitizenName', c_char * 256),  # 身份证姓名;citizen name;
        ('emMask', C_ENUM),  # 口罩状态（EM_MASK_STATE_UNKNOWN、EM_MASK_STATE_NOMASK、EM_MASK_STATE_WEAR 有效） Refer: EM_MASK_STATE_TYPE;mask ( EM_MASK_STATE_UNKNOWN,EM_MASK_STATE_NOMASK,EM_MASK_STATE_WEAR is valid ) Refer: EM_MASK_STATE_TYPE;
        ('szCardName', c_char * 64),  # 卡命名;card name;
        ('nFaceIndex', C_UINT),  # 一人脸时的人脸序号;face index;
        ('emUserType', C_ENUM),  # 用户类型( EM_USER_TYPE_ORDINARY 至 EM_USER_TYPE_DISABLED 有效 ) Refer: EM_USER_TYPE;user type( from EM_USER_TYPE_ORDINARY to EM_USER_TYPE_DISABLED is valid ) Refer: EM_USER_TYPE;
        ('bRealUTC', C_BOOL),  # RealUTC 是否有效，bRealUTC 为 TRUE 时，用 RealUTC，否则用 stuTime 字段;whether RealUTC is valid. when bRealUTC is TRUE, use RealUTC, otherwise use stuTime;
        ('RealUTC', NET_TIME_EX),  # 事件发生的时间（标准UTC）;event occur time;
        ('szCompanyName', c_char * 200),  # 公司名称;Company Address;
        ('nScore', c_int),  # 人脸质量评分;Face Quality;
        ('nLiftNo', c_int),  # 电梯编号;Elevator number;
        ('emQRCodeIsExpired', C_ENUM),  # 二维码是否过期。默认值0 (北美测温定制) Refer: EM_QRCODE_IS_EXPIRED;Whether the QR code has expired. Default value 0 (customized for temperature measurement in North America) Refer: EM_QRCODE_IS_EXPIRED;
        ('emQRCodeState', C_ENUM),  # 二维码状态(北美测试定制) Refer: EM_QRCODE_STATE;QR code status (North American test customization) Refer: EM_QRCODE_STATE;
        ('stuQRCodeValidTo', NET_TIME),  # 二维码截止日期;QR code deadline;
        ('szDynPWD', c_char * 32),  # 平台通过密码校验权限。用于动态密码校验，动态密码由手机APP生成，设备仅透传给平台;The platform verifies permissions by password. Used for dynamic password verification. The dynamic password is generated by the mobile APP, and the device is only transparently transmitted to the platform;
        ('nBlockId', C_UINT),  # 上报事件数据序列号从1开始自增;The serial number of the reported event data increases from 1;
        ('szSection', c_char * 64),  # 部门名称;Department name;
        ('szWorkClass', c_char * 256),  # 工作班级;Work class;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('stuTestResult', NET_TEST_RESULT),  # ESD阻值测试结果;ESD resistance test result;
        ('szDeviceID', c_char * 128),  # 门禁设备编号;Access control equipment number;
        ('szUserUniqueID', c_char * 128),  # 用户唯一表示ID;User unique ID;
        ('bUseCardNameEx', C_BOOL),  # 是否使用卡命名扩展;Whether to use the card name extension;
        ('szCardNameEx', c_char * 128),  # 卡命名扩展;Card name extension;
        ('szTempPassword', c_char * 64),  # 临时密码;tmp passwd;
        ('szNote', c_char * 512),  # 摘要信息;Note;
        ('nHSJCResult', c_int),  # 核酸检测报告结果  -1: 未知 0: 阳性 1: 阴性 2: 未检测 3: 过期;Nucleic acid test report result, -1: Unknow 0: positive, 1: negative, 2: not tested, 3: expired;
        ('stuVaccineInfo', NET_VACCINE_INFO),  # 新冠疫苗接种信息;New crown vaccination information;
        ('stuTravelInfo', NET_TRAVEL_INFO),  # 行程码信息;Trip code information;
        ('szQRCodeEx', c_char * 2048),  # 国康码项目，用来上传大二维码内容;Guokang code project is used to upload large QR code content;
        ('stuHSJCInfo', NET_HSJC_INFO),  # 核酸信息;Nucleic acid detection information;
        ('stuAntigenInfo', NET_ANTIGEN_INFO),  # 抗原检测信息;Antigen Test Information;
    ]

class NET_CTRL_ACCESS_OPEN(Structure):
    """
    CLIENT_ControlDevice接口的 CTRL_ACCESS_OPEN 命令参数
    CLIENT_ControlDevice's param: CTRL_ACCESS_OPEN
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号(0开始);Channel ID (start from 0);
        ('szTargetID', POINTER(c_char)),  # 转发目标设备ID,为NULL表示不转发;Target ID, NULL equals to not transmit;
        ('szUserID', c_char * 32),  # 远程用户ID;remote user id;
        ('emOpenDoorType', C_ENUM),  # 开门方式 Refer: EM_OPEN_DOOR_TYPE;open door type Refer: EM_OPEN_DOOR_TYPE;
        ('emOpenDoorDirection', C_ENUM),  # 开门方向 Refer: EM_OPEN_DOOR_DIRECTION;open door direction Refer: EM_OPEN_DOOR_DIRECTION;
        ('emRemoteCheckCode', C_ENUM),  # 远程权限验证结果 Refer: EM_REMOTE_CHECK_CODE;remote check code Refer: EM_REMOTE_CHECK_CODE;
        ('szShortNumber', c_char * 16),  # 兼容字段;Compatible fields;
    ]

class NET_CTRL_ACCESS_CLOSE(Structure):
    """
    CLIENT_ControlDevice接口的 CTRL_ACCESS_CLOSE 命令参数
    CLIENT_ControlDevice's param: CTRL_ACCESS_CLOSE
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nChannelID', c_int),  # 通道号(0开始);Channel ID (start from 0);
    ]

class NET_ACCESS_USER_INFO_EX(Structure):
    """
    用户信息
    User Info extension
    """
    _fields_ = [
        ('szConsumptionTimeSections', c_char * 1428),  # 消费时间段每天最多6个时间段，每6个元素对应一天。一共7天。每个时段格式为"星期 时:分:秒-时:分:秒 消费类型 可消费次数 可消费金额"，星期从0开始，表示周日，前6个时段前面都是0，表示周日的6个时段，剩下依次周一，周二... 一共42个时段。消费类型包括：0为定额消费，1为非定额消费；可消费次数最大上限200次；可消费金额最高999900，也就是9999元;
                              # Consumption TimeSectionsevery day has six TimeSectionsthe TimeSection format is: "DayNo hour:minute:second-hour:minute:second type times amount"DayNo starts with 0, 0 means Sunday, the DayNo of the the first six TimeSections is 0type is the Consumption type, 0 means quota, 1 means nonquotatimes is the Consumable times, the max is 200amount is the Consumable amount, the max is 999900 cents;
        ('byReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_ACCESS_USER_INFO(Structure):
    """
    用户信息
    User Info
    """
    _fields_ = [
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('szName', c_char * 32),  # 人员名称;user name;
        ('emUserType', C_ENUM),  # 用户类型 Refer: EM_A_NET_ENUM_USER_TYPE;user type Refer: EM_A_NET_ENUM_USER_TYPE;
        ('nUserStatus', C_UINT),  # 用户状态, 0 正常, 1 冻结;user status, 0 normal, 1 freeze;
        ('nUserTime', c_int),  # 来宾卡的通行次数;user times of guest;
        ('szCitizenIDNo', c_char * 32),  # 身份证号码;CitizenID no;
        ('szPsw', c_char * 64),  # UserID+密码开门时密码;UserID+password;
        ('nDoorNum', c_int),  # 有效的门数目;;door number;;
        ('nDoors', c_int * 32),  # 有权限的门序号,即 CFG_CMD_ACCESS_EVENT 配置的数组下标;Privileged Door Number,That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('nTimeSectionNum', c_int),  # 有效的的开门时间段数目;the Number of Effective Open Time;
        ('nTimeSectionNo', c_int * 32),  # 开门时间段索引,即 CFG_ACCESS_TIMESCHEDULE_INFO 的数组下标;Open Time Segment Index,That is CFG_ACCESS_TIMESCHEDULE_INFO Array subscript;
        ('nSpecialDaysScheduleNum', c_int),  # 假日计划表示数量;the number of specialday;
        ('nSpecialDaysSchedule', c_int * 128),  # 假日计划标识, 即 NET_EM_CFG_ACCESSCTL_SPECIALDAYS_SCHEDULE 配置的下标;Open specialday index, That is NET_EM_CFG_ACCESSCTL_SPECIALDAYS_SCHEDULE Array subscript;
        ('stuValidBeginTime', NET_TIME),  # 开始有效期;Valid Begin Time;
        ('stuValidEndTime', NET_TIME),  # 结束有效期;Valid End Time;
        ('bFirstEnter', C_BOOL),  # 是否拥有首卡权限;has first card or not;
        ('nFirstEnterDoorsNum', c_int),  # 拥有首用户权限的门数量;has first card door number;
        ('nFirstEnterDoors', c_int * 32),  # 拥有首用户权限的门序号，bFirstEnter为TRUE时有效,-1表示全通道;has first card door No,FirstEnter-1 means all channels;
        ('emAuthority', C_ENUM),  # 用户权限，可选 Refer: EM_A_NET_ATTENDANCE_AUTHORITY;user authority Refer: EM_A_NET_ATTENDANCE_AUTHORITY;
        ('nRepeatEnterRouteTimeout', c_int),  # 反潜超时时间;repeatenter timeout time;
        ('nFloorNum', c_int),  # 有效的楼层数量;floor number;
        ('szFloorNo', c_char * 1024),  # 楼层号;floor;
        ('nRoom', c_int),  # 房间个数;room number;
        ('szRoomNo', c_char * 512),  # 房间号列表;room;
        ('bFloorNoExValid', C_BOOL),  # szFloorNoEx 是否有效;if szFloorNoEx is valid, TRUE:valid, else invalid;
        ('nFloorNumEx', c_int),  # 有效的楼层数量扩展;floor number extended;
        ('szFloorNoEx', c_char * 1024),  # 楼层号扩展;floor info;
        ('szClassInfo', c_char * 256),  # 班级信息;class info;
        ('szStudentNo', c_char * 64),  # 学号（定制）;student num(customized);
        ('szCitizenAddress', c_char * 128),  # 身份证地址;citizen address;
        ('stuBirthDay', NET_TIME),  # 出生日期（年月日有效）;birth day (year month day are valid);
        ('emSex', C_ENUM),  # 性别 Refer: EM_A_NET_ACCESSCTLCARD_SEX;sex Refer: EM_A_NET_ACCESSCTLCARD_SEX;
        ('szDepartment', c_char * 128),  # 部门;department;
        ('szSiteCode', c_char * 32),  # 站点码（定制）;site code(customized);
        ('szPhoneNumber', c_char * 32),  # 手机号码;PhoneNumber;
        ('szDefaultFloor', c_char * 8),  # 默认楼层号;Default floor number (elevator control requirements);
        ('bFloorNoEx2Valid', C_BOOL),  # 是否使用扩展结构体;stuFloorsEx2 wheather valid;
        ('pstuFloorsEx2', POINTER(NET_FLOORS_INFO)),  # 楼层号（再次扩展）;Floor number (extended again);
        ('bHealthStatus', C_BOOL),  # 人员健康状态 (定制);Personnel health status (customized);
        ('nUserTimeSectionsNum', c_int),  # 用户自身的开门时间段校验有效个数;The number of valid verifications for the user's own door opening time;
        ('szUserTimeSections', c_char * 120),  # 针对用户自身的开门时间段校验;Check the user's own door opening time period;
        ('szEthnicity', c_char * 64),  # 民族;Nation;
        ('emTypeOfCertificate', C_ENUM),  # 证件类型 Refer: EM_TYPE_OF_CERTIFICATE;type of certificate Refer: EM_TYPE_OF_CERTIFICATE;
        ('szCountryOrAreaCode', c_char * 8),  # 国籍或所在地区代码，符合GB/T 2659-2000的规范;Nationality or area code, in line with GB/T 2659-2000;
        ('szCountryOrAreaName', c_char * 64),  # 国籍或所在地区名称，符合GB/T 2659-2000的规范;Nationality or area name, in line with GB/T 2659-2000;
        ('szCertificateVersionNumber', c_char * 64),  # 永久居住证的证件版本号;The version number of the permanent residence permit;
        ('szApplicationAgencyCode', c_char * 64),  # 申请受理机关代码;Application acceptance agency code;
        ('szIssuingAuthority', c_char * 64),  # 签发机关;issuing authority;
        ('szStartTimeOfCertificateValidity', c_char * 64),  # 证件有效开始时间;Start time of certificate validity;
        ('szEndTimeOfCertificateValidity', c_char * 64),  # 证件有效结束时间;End time of certificate validity;
        ('nSignNum', c_int),  # 证件签发次数;Number of certificates issued;
        ('szActualResidentialAddr', c_char * 108),  # 实际家庭住址;Actual home address;
        ('szWorkClass', c_char * 256),  # 工作班别;Work class;
        ('stuStartTimeInPeriodOfValidity', NET_TIME),  # 有效时间段内启动时间;Start time within valid time period;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('bUseNameEx', C_BOOL),  # szNameEx 是否有效，为TRUE时，使用szNameEx字段;Whether to use the szNameEx field;
        ('szNameEx', c_char * 128),  # 人员名称扩展;Name extension;
        ('bUserInfoExValid', C_BOOL),  # 是否使用用户信息结构体;pstuUserInfoEx wheather valid;
        ('pstuUserInfoEx', POINTER(NET_ACCESS_USER_INFO_EX)),  # 扩展用户信息;User Info (extended);
        ('nAuthOverdueTime', C_UINT),  # 授权时间、过期时间，时间单位: 小时;Authorization time, expiration time, time unit: hour;
        ('emGreenCNHealthStatus', C_ENUM),  # 人员健康状态（定制添加） Refer: EM_GREENCNHEALTH_STATUS;Staff health status Refer: EM_GREENCNHEALTH_STATUS;
        ('emAllowPermitFlag', C_ENUM),  # 电子通行证状态（定制添加） Refer: EM_ALLOW_PERMIT_FLAG;E-pass status Refer: EM_ALLOW_PERMIT_FLAG;
        ('nHolidayGroupIndex', c_int),  # 工行定制专属 工行定制假日组HolidayGroup索引值;ICBC customized exclusive ICBC customized holiday group HolidayGroup index value;
        ('stuUpdateTime', NET_TIME),  # 信息更新时间,UTC时间;Info UpdateTime,UTC time;
        ('szValidFroms', c_char * 192),  # 用户的门通道起始有效期,每个通道设置一个有效期,数组元素与门通道一一对应;The initial validity period of the user's door channel, each channel is set to a validity period, and the array elements correspond to the door channels one-to-one;
        ('nValidFromsNum', c_int),  # 用户的门通道起始有效期有效个数, 最大值为8;The valid number of the user's door channel starting valid, the maximum value is 8;
        ('nValidTosNum', c_int),  # 用户的门通道截止有效期有效个数, 最大值为8;User's gate channel expiration valid number, the maximum value is 8;
        ('szValidTos', c_char * 192),  # 用户的门通道截止有效期,每个通道设置一个有效期,数组元素与门通道一一对应;The user's door channel expires valid period, each channel is set to a valid period, and the array elements correspond to the door channel one-to-one;
        ('byReserved', C_BYTE * (880 - sizeof(c_void_p))),  # 保留字节;Reserved;
    ]

class NET_IN_ACCESS_USER_SERVICE_INSERT(Structure):
    """
    新增或更新用户信息入参
    input of insert or update user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nInfoNum', c_int),  # 用户信息数量;user number;
        ('pUserInfo', POINTER(NET_ACCESS_USER_INFO)),  # 用户信息,内存由用户申请释放，申请大小不小于nInfoNum*sizeof(NET_ACCESS_USER_INFO);;user info;
    ]

class NET_OUT_ACCESS_USER_SERVICE_INSERT(Structure):
    """
    新增或更新用户信息出参
    output param of insert or update user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 申请的最大返回的错误信息数量,不小于NET_IN_ACCESS_USER_SERVICE_INSERT中nInfoNum;max return number, nInfoNum of NET_IN_ACCESS_USER_SERVICE_INSERT plus;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时，对应插入的每一项的结果,返回个数同NET_IN_ACCESS_USER_SERVICE_INSERT中nInfoNum Refer: EM_A_NET_EM_FAILCODE;errorcode when insert failed,return number is nInfoNum of NET_IN_ACCESS_USER_SERVICE_INSERT Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_USER_SERVICE_GET(Structure):
    """
    获取用户信息入参
    input param of Get user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nUserNum', c_int),  # 查询的数量;Get number;
        ('szUserID', c_char * 3200),  # 用户ID;user id;
    ]

class NET_OUT_ACCESS_USER_SERVICE_GET(Structure):
    """
    获取用户信息出参
    output param of Get user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 查询返回的最大数量;max number of return;
        ('pUserInfo', POINTER(NET_ACCESS_USER_INFO)),  # 用户信息,内存由用户申请释放，申请大小不小于 nUserNum*sizeof(NET_ACCESS_USER_INFO)                                                                            返回个数同NET_IN_ACCESS_USER_SERVICE_GET中nUserNum;user info,larger than nUserNum*sizeof(NET_ACCESS_USER_INFO);
        ('pFailCode', POINTER(C_ENUM)),  # 查询失败时，内存由用户申请释放,对应查询的每一项的结果，返回个数同NET_IN_ACCESS_USER_SERVICE_GET中nUserNum Refer: EM_A_NET_EM_FAILCODE;errorcode when failed,return number is nUserNum in NET_IN_ACCESS_USER_SERVICE_GET Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_USER_SERVICE_REMOVE(Structure):
    """
    删除指定ID人员信息入参
    input of  remove user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nUserNum', c_int),  # 删除的数量;remove number;
        ('szUserID', c_char * 3200),  # 用户ID;user ID;
    ]

class NET_OUT_ACCESS_USER_SERVICE_REMOVE(Structure):
    """
    删除指定ID人员信息出参
    output of remove user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 返回的最大数量,不小于 NET_IN_ACCESS_USER_SERVICE_REMOVE中nUserNum;max return number,nUserNum in NET_IN_ACCESS_USER_SERVICE_REMOVE;
        ('pFailCode', POINTER(C_ENUM)),  # 插入失败时，内存由用户申请释放,对应插入的每一项的结果,返回个数同NET_IN_ACCESS_USER_SERVICE_REMOVE中nUserNum Refer: EM_A_NET_EM_FAILCODE;errorcode when failed,return number is nUserNum in NET_IN_ACCESS_USER_SERVICE_REMOVE Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_USER_SERVICE_CLEAR(Structure):
    """
    删除所有人员信息入参
    input of clear user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_ACCESS_USER_SERVICE_CLEAR(Structure):
    """
    删除所有人员信息出参
    output of clear user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ACCESS_FACE_INFO(Structure):
    """
    人脸信息
    face info
    """
    _fields_ = [
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('nFaceData', c_int),  # 人脸模板数据个数,最大20;count of face data,the max number is 20;
        ('szFaceData', c_char * 40960),  # 人脸模板数据;face data;
        ('nFaceDataLen', c_int * 20),  # 人脸模版数据大小;face data length;
        ('nFacePhoto', c_int),  # 人脸照片个数,不超过5个;count of face photo,max size: 5;
        ('nInFacePhotoLen', c_int * 5),  # 用户申请的每张图片的大小;the size of each photo used by the user;
        ('nOutFacePhotoLen', c_int * 5),  # 每张图片实际的大小;the actual size of each photo;
        ('pFacePhoto', c_void_p * 5),  # 人脸照片数据,大小不超过200K;face photo data,max size: 120K;
        ('bFaceDataExEnable', C_BOOL),  # 是否使用扩展人脸模板数据;Whether to use extended face template data;
        ('nMaxFaceDataLen', c_int * 20),  # 用户申请的扩展人脸模板数据大小;Data size of the extended face template requested by the user;
        ('nRetFaceDataLen', c_int * 20),  # 实际人脸模板数据大小;Actual face template data size;
        ('pFaceDataEx', POINTER(c_char) * 20),  # 人脸模板数据扩展字段 当bFaceDataExEnable有效时，建议使用扩展字段pFaceDataEx;Face template data extension field,When bFaceDataExEnable is valid, it is recommended to use the extension field pFaceDataEx;
        ('stuUpdateTime', NET_TIME),  # 人脸信息更新时间,UTC时间;Info UpdateTime,UTC time;
        ('byReserved', C_BYTE * 1776),  # 保留字节;reserved;
    ]

class NET_IN_ACCESS_FACE_SERVICE_INSERT(Structure):
    """
    添加人脸记录信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    the input param of adding face data(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nFaceInfoNum', c_int),  # 人脸信息数量;face info number;
        ('pFaceInfo', POINTER(NET_ACCESS_FACE_INFO)),  # 人脸数据,用户自行分配数据;face info,user allocates memory;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_INSERT(Structure):
    """
    添加人脸记录信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    the output param of adding face data(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_INSERT 中的nFaceInfoNum;the max return number,not less than nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_INSERT;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存,添加失败时,对应插入的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_INSERT中的nFaceInfoNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when insert failed,the result of each item inserted,count is nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_INSERT Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_GET(Structure):
    """
    批量获取多用户多个人脸输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    the input param of getting face data(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nUserNum', c_int),  # 用户ID数量,最大100;user ID number,the max number is 100;
        ('szUserID', c_char * 3200),  # 用户ID;user ID;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_GET(Structure):
    """
    批量获取多用户多个人脸输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    the out param of getting face data(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_GET 中的 nUserNum;the max return number,not less than nUserNum in NET_IN_ACCESS_FACE_SERVICE_GET;
        ('pFaceInfo', POINTER(NET_ACCESS_FACE_INFO)),  # 人脸数据,用户分配内存,返回个数同NET_IN_ACCESS_FACE_SERVICE_GET中的nUserNum,只返回的人脸模版数据;face data,user allocates memory.count is nUserNum in NET_IN_ACCESS_FACE_SERVICE_GET,only return face data;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存,获取失败时,对应获取的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_GET中的nUserNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when get failed,the result of each item get,count is nUserNum in NET_IN_ACCESS_FACE_SERVICE_GET Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_UPDATE(Structure):
    """
    更新多用户多个人脸记录信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    the input param to update face data(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nFaceInfoNum', c_int),  # 人脸信息数量;face info number;
        ('pFaceInfo', POINTER(NET_ACCESS_FACE_INFO)),  # 人脸数据,用户分配内存;face data,user allocates memory;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_UPDATE(Structure):
    """
    更新多用户多个人脸记录信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    the output param to update face data(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_UPDATE中的nFaceInfoNum;the max return number,not less than nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_UPDATE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存.更新失败时,对应更新的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_UPDATE中的nFaceInfoNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when update failed,the result of each item updated,count is nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_UPDATE Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_REMOVE(Structure):
    """
    删除多用户的多个人脸信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    the input param of removing face data(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nUserNum', c_int),  # 用户ID数量,最大100;user ID number,the max number is 100;
        ('szUserID', c_char * 3200),  # 用户ID;user ID;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_REMOVE(Structure):
    """
    删除多用户的多个人脸信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    the output param of removing face data(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_REMOVE中的nUserNum;the max return number,not less than nUserNum in NET_IN_ACCESS_FACE_SERVICE_REMOVE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存.删除失败时,对应删除的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_REMOVE中的nUserNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when remove failed,the result of each item removed,count is nUserNum in NET_IN_ACCESS_FACE_SERVICE_REMOVE Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_CLEAR(Structure):
    """
    清空所有人脸记录信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    the input param of clear face data(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_CLEAR(Structure):
    """
    清空所有人脸记录信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    the output param of clear face data(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
    ]

class NET_ACCESS_CARD_INFO(Structure):
    """
    卡片信息
    card info
    """
    _fields_ = [
        ('szCardNo', c_char * 32),  # 卡号;card number;
        ('szUserID', c_char * 32),  # 用户ID;user id;
        ('emType', C_ENUM),  # 卡类型,只支持一般卡、胁迫卡和母卡 Refer: NET_ACCESSCTLCARD_TYPE;card type,only support General,Corce,Mother card Refer: NET_ACCESSCTLCARD_TYPE;
        ('szDynamicCheckCode', c_char * 16),  # 动态校验码;dynamic check code;
        ('stuUpdateTime', NET_TIME),  # 信息更新时间,UTC时间;Info UpdateTime,UTC time;
        ('byReserved', C_BYTE * 4072),  # 保留字节;reserve;
    ]

class NET_IN_ACCESS_CARD_SERVICE_INSERT(Structure):
    """
    新增卡片信息入参
    input of insert card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nInfoNum', c_int),  # 用户信息数量;card number;
        ('pCardInfo', POINTER(NET_ACCESS_CARD_INFO)),  # 卡片信息,用户分配释放内存,大小为sizeof(NET_ACCESS_CARD_INFO)*nInfoNum;card info;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_INSERT(Structure):
    """
    新增卡片信息出参
    output of insert card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 最大返回的用户信息数量,不小于NET_IN_ACCESS_CARD_SERVICE_INSERT中nInfoNum;return number ,greater than nInfoNum in NET_IN_ACCESS_CARD_SERVICE_INSERT;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时,对应插入的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_INSERT中nInfoNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nInfoNum in NET_IN_ACCESS_CARD_SERVICE_INSERT Refer: EM_A_NET_EM_FAILCODE;
        ('byReserved', C_BYTE * 4),
    ]

class NET_IN_ACCESS_CARD_SERVICE_GET(Structure):
    """
    获取卡片信息入参
    input of get card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nCardNum', c_int),  # 查询的数量;get number;
        ('szCardNo', c_char * 3200),  # 卡号;card No;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_GET(Structure):
    """
    获取卡片信息出参
    output of get card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 查询返回的最大数量;max return number;
        ('pCardInfo', POINTER(NET_ACCESS_CARD_INFO)),  # 卡片信息,内存由用户申请释放，申请大小不小于nCardNum*sizeof(NET_ACCESS_CARD_INFO);                                                                            返回个数同NET_IN_ACCESS_CARD_SERVICE_GET中nCardNum;card info;
        ('pFailCode', POINTER(C_ENUM)),  # 查询失败时，对应查询的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_GET中nCardNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nCardNum in NET_IN_ACCESS_CARD_SERVICE_GET Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_CARD_SERVICE_UPDATE(Structure):
    """
    更新卡片信息入参
    input of update card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nInfoNum', c_int),  # 用户信息数量;card number;
        ('pCardInfo', POINTER(NET_ACCESS_CARD_INFO)),  # 卡片信息,用户分配释放内存,大小为sizeof(NET_ACCESS_CARD_INFO)*nInfoNum;card info;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_UPDATE(Structure):
    """
    更新卡片信息出参
    output of update card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 最大返回的用户信息数量,不小于NET_IN_ACCESS_CARD_SERVICE_UPDATE中nInfoNum;max return number,greater than nInfoNum in NET_IN_ACCESS_CARD_SERVICE_UPDATE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时，对应插入的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_UPDATE中nInfoNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nInfoNum in NET_IN_ACCESS_CARD_SERVICE_UPDATE Refer: EM_A_NET_EM_FAILCODE;
        ('byReserved', C_BYTE * 4),  # reserved;
    ]

class NET_IN_ACCESS_CARD_SERVICE_REMOVE(Structure):
    """
    删除指定卡号信息入参
    input of remove card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nCardNum', c_int),  # 删除的数量;remove number;
        ('szCardNo', c_char * 3200),  # 卡号;card no;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_REMOVE(Structure):
    """
    删除指定卡号信息出参
    output of remove card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 最大返回信息数量,不小于 NET_IN_ACCESS_CARD_SERVICE_REMOVE中nCardNum;max retrun number,great than nCardNum in NET_IN_ACCESS_CARD_SERVICE_REMOVE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时,对应删除的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_REMOVE中nCardNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nCardNum in NET_IN_ACCESS_CARD_SERVICE_REMOVE Refer: EM_A_NET_EM_FAILCODE;
        ('byReserved', C_BYTE * 4),  # reserved;
    ]

class NET_IN_ACCESS_CARD_SERVICE_CLEAR(Structure):
    """
    删除所有卡片信息入参
    inout of clear card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_CLEAR(Structure):
    """
    删除所有卡片信息出参
    output of clear card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

