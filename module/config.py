# -*- coding:utf-8 -*-
from telnet import Telnet
import re

SERVER_CONFIG_PATH="./etc/server_config"
REMOTE_CONFIG_FILE="./etc/remote_config.xml"


GS_BASH_FILE ="./frame/GS/run_gs.sh"
GS_INI_FILE  ="./frame/GS/config.ini"

DBA_BASH_FILE="./frame/DBA/run_dba.sh"
DBA_INI_FILE ="./frame/DBA/config.ini"

DBU_BASH_FILE="./frame/DBU/run_dbu.sh"
DBU_INI_FILE ="./frame/DBU/config.ini"

BS_BASH_FILE="./frame/BS/run_bs.sh"
BS_INI_FILE ="./frame/BS/config.ini"

LS_BASH_FILE="./frame/LS/run_ls.sh"
LS_INI_FILE ="./frame/LS/config.ini"

SCS_BASH_FILE="./frame/SCS/run_scs.sh"
SCS_INI_FILE ="./frame/SCS/config.ini"

COMMON_CONFIG_FILE="./frame/common/common_config.lua"

TMP_GS_BASH_FILE ="./tmp/GS/run_gs.sh"
TMP_GS_INI_FILE  ="./tmp/GS/config.ini"

TMP_DBA_BASH_FILE="./tmp/DBA/run_dba.sh"
TMP_DBA_INI_FILE ="./tmp/DBA/config.ini"

TMP_DBU_BASH_FILE="./tmp/DBU/run_dbu.sh"
TMP_DBU_INI_FILE ="./tmp/DBU/config.ini"

TMP_BS_BASH_FILE="./tmp/BS/run_bs.sh"
TMP_BS_INI_FILE ="./tmp/BS/config.ini"

TMP_LS_BASH_FILE="./tmp/LS/run_ls.sh"
TMP_LS_INI_FILE ="./tmp/LS/config.ini"

TMP_SCS_BASH_FILE="./tmp/SCS/run_scs.sh"
TMP_SCS_INI_FILE ="./tmp/SCS/config.ini"

TMP_COMMON_CONFIG_FILE="./tmp/common/common_config.lua"

RMT_GS_BIN_FILE = "GS/GS"
RMT_GS_BASH_FILE ="GS/run_gs.sh"
RMT_GS_INI_FILE  ="GS/config.ini"

RMT_DBA_BIN_FILE ="DBA/DBA"
RMT_DBA_BASH_FILE="DBA/run_dba.sh"
RMT_DBA_INI_FILE ="DBA/config.ini"

RMT_DBU_BIN_FILE ="DBU/DBU"
RMT_DBU_BASH_FILE="DBU/run_dbu.sh"
RMT_DBU_INI_FILE ="DBU/config.ini"

RMT_BS_BIN_FILE ="BS/BS"
RMT_BS_BASH_FILE="BS/run_bs.sh"
RMT_BS_INI_FILE ="BS/config.ini"

RMT_LS_BIN_FILE ="LS/LS"
RMT_LS_BASH_FILE="LS/run_ls.sh"
RMT_LS_INI_FILE ="LS/config.ini"

RMT_SCS_BIN_FILE ="SCS/SCS"
RMT_SCS_BASH_FILE="SCS/run_scs.sh"
RMT_SCS_INI_FILE ="SCS/config.ini"

RMT_SCS_CONFIG_DIR=     "SCS/lua/config"
RMT_COMMON_CONFIG_FILE="lua/common/common_config.lua"
RMT_DBA_FIXED_FILE=	"SCS/lua/config/dba_fixed_config.lua"
RMT_DBU_FIXED_FILE=	"SCS/lua/config/dbu_fixed_config.lua"
RMT_SCS_FIXED_FILE=     "SCS/lua/config/"

GSS_up_load_bash_ini_dic={
    TMP_GS_BASH_FILE :RMT_GS_BASH_FILE,
    TMP_GS_INI_FILE  :RMT_GS_INI_FILE,

    TMP_BS_BASH_FILE:RMT_BS_BASH_FILE,
    TMP_BS_INI_FILE :RMT_BS_INI_FILE,

    TMP_LS_BASH_FILE:RMT_LS_BASH_FILE,
    TMP_LS_INI_FILE :RMT_LS_INI_FILE,
}



GDB_up_load_bash_ini_dic={
    TMP_DBA_BASH_FILE:RMT_DBA_BASH_FILE,
    TMP_DBA_INI_FILE :RMT_DBA_INI_FILE,

    TMP_DBU_BASH_FILE:RMT_DBU_BASH_FILE,
    TMP_DBU_INI_FILE :RMT_DBU_INI_FILE,

    TMP_SCS_BASH_FILE:RMT_SCS_BASH_FILE,
    TMP_SCS_INI_FILE :RMT_SCS_INI_FILE,
}

up_load_bash_ini_remote_dic={
    TMP_GS_BASH_FILE :RMT_GS_BASH_FILE,
    TMP_GS_INI_FILE  :RMT_GS_INI_FILE,

    TMP_BS_BASH_FILE:RMT_BS_BASH_FILE,
    TMP_BS_INI_FILE :RMT_BS_INI_FILE,

    TMP_LS_BASH_FILE:RMT_LS_BASH_FILE,
    TMP_LS_INI_FILE :RMT_LS_INI_FILE,

    TMP_DBA_BASH_FILE:RMT_DBA_BASH_FILE,
    TMP_DBA_INI_FILE :RMT_DBA_INI_FILE,

    TMP_DBU_BASH_FILE:RMT_DBU_BASH_FILE,
    TMP_DBU_INI_FILE :RMT_DBU_INI_FILE,

    TMP_SCS_BASH_FILE:RMT_SCS_BASH_FILE,
    TMP_SCS_INI_FILE :RMT_SCS_INI_FILE,
}

shutdown_gs_cmds=["cmd.clearuser()","cmd.printuser()","cmd.clearorder()","cmd.printorder()",\
                  "cmd.savetop()","cmd.printtop()","cmd.shutdown()"]

shutdown_bs_cmds=["cmd.shutdown()"]

shutdown_ls_cmds=["cmd.shutdown()"]

shutdown_dba_cmds=["cmd.shutdown()"]

shutdown_scs_cmds=["cmd.shutdown()"]

shutdown_dbu_cmds=["cmd.shutdown()"]

shutdown_gs_pairs=[("cmd.clearuser()",u"服务器状态更新:[正常->暂停]".encode("gb18030")),
                   ("cmd.printuser()",u"6      |\t0   |   在线用户".encode("gb18030")),
                   ("cmd.clearorder()",u"内存中没有未处理的订单，可以关闭服务器了!".encode("gb18030")),
                   ("cmd.printorder()",u"GS>".encode("gb18030")),
                   ("cmd.savetop()",u"GS>".encode("gb18030")),
                   ("cmd.printtop()",u"没有未保存的通用排行数据".encode("gb18030")),
                   ("cmd.shutdown()",u"GS>".encode("gb18030")),]

shutdown_bs_pairs = [("cmd.shutdown()","BS>")]

shutdown_ls_pairs = [("cmd.shutdown()","LS>")]

shutdown_dba_pairs = [("cmd.shutdown()","DBA>")]

shutdown_scs_pairs = [("cmd.shutdown()","SCS>")]

shutdown_dbu_pairs = [("cmd.shutdown()","DBU>")]

shutdown_cmd_dic = [("GS",shutdown_gs_pairs),
                    ("BS",shutdown_bs_pairs),
                    ("LS",shutdown_ls_pairs),
                    ("DBA",shutdown_dba_pairs),
                    ("SCS",shutdown_scs_pairs)
                    ]

gs_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"GS>"
}

bs_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"BS>"
}

ls_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"LS>"
}

dba_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"DBA>"
}

scs_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"SCS>"
}

dbu_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"DBU>"    
}

#sort in open order
GSS_name_list=[("ls_name",RMT_LS_BIN_FILE),\
            ("gs_name",RMT_GS_BIN_FILE),\
            ("bs_name",RMT_BS_BIN_FILE)]
#sort in open order
GDB_name_list=[("scs_name",RMT_SCS_BIN_FILE),\
               ("dbu_name",RMT_DBU_BIN_FILE),\
               ("dba_name",RMT_DBA_BIN_FILE)]
#sort in open order
updateDB_name_list=[("scs_name",RMT_SCS_BIN_FILE),\
               ("dbu_name",RMT_DBU_BIN_FILE)]

#for change process name may not in order
all_name_list=[("scs_name",RMT_SCS_BIN_FILE),\
               ("dbu_name",RMT_DBU_BIN_FILE),\
               ("dba_name",RMT_DBA_BIN_FILE),\
               ("ls_name",RMT_LS_BIN_FILE),\
               ("gs_name",RMT_GS_BIN_FILE),\
               ("bs_name",RMT_BS_BIN_FILE)]

run_bash_dic={"scs_name":RMT_SCS_BASH_FILE,\
              "dbu_name":RMT_DBU_BASH_FILE,\
              "dba_name":RMT_DBA_BASH_FILE,\
              "bs_name":RMT_BS_BASH_FILE,\
              "gs_name":RMT_GS_BASH_FILE,\
              "ls_name":RMT_LS_BASH_FILE
}

check_list={"scs_name":re.compile(".*ServiceConfigServer STARTUP COMPLETED!.*",re.M|re.S),\
          "dba_name":re.compile(".*DbAgent STARTUP COMPLETED!.*",re.M|re.S),\
          "bs_name":re.compile(".*BridgeServer STARTUP COMPLETED!.*",re.M|re.S),\
          "gs_name":re.compile(".*GameServer STARTUP COMPLETED!.*",re.M|re.S),\
          "ls_name":re.compile(".*LoginServer STARTUP COMPLETED!.*",re.M|re.S)
}

log_list={"gs_name":"gs.log",\
          "ls_name":"ls.log",\
          "bs_name":"bs.log",\
          "dba_name":"dba.log",\
          "dbu_name":"dbu.log",\
          "scs_name":"scs.log"}

GDB_copy_path_list=["lua","DBU","DBA","SCS"]
GSS_copy_path_list=["lua","GS","BS","LS"]


service_dic={
    "scs":True,\
    "dba":True,\
    "dbu":True,\
    "gs":False,\
    "bs":False,\
    "ls":False,\
}