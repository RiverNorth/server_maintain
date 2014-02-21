-------------------------------------------------------------------------------------------------------------
-- Project: MobileGame
-- Modle  : common
-- Title  : ���������ļ������з��������õ���Ϣ
-- Author : robencle
-------------------------------------------------------------------------------------------------------------
-- History:
--          2012.11.05----Create
-------------------------------------------------------------------------------------------------------------
module "common.common_config"
-------------------------------------------------------------------------------------------------------------
role_top_level = 99                                                     -- ������ߵȼ�
cortege_top_level = 200                                         -- Ӷ����ߵȼ�
in_service = true                                                       -- �Ƿ�������
game_db_ip = "127.0.0.1"                                -- ��Ϸ���ݿ��IP
game_db_port = 3306                                     -- ��Ϸ���ݿ�Ķ˿�
game_db_name = "mobile_game2305"                                -- ��Ϸ���ݿ������
game_db_cs = "UTF-8"                                            -- ��Ϸ���ݿ��ַ���

log_db_ip = "127.0.0.1"                                 -- ��־���ݿ��IP
log_db_port = 3306                                      -- ��־���ݿ�Ķ˿�
log_db_name = "mobile_game_log2305"                             -- ��־���ݿ������
log_db_cs = "UTF-8"                                                     -- ��־���ݿ��ַ���

dba_ip = "192.168.201.27"                               -- DBA��������IP
dba_listen_port = 9035                                  -- DBA�������ķ���˿�
dba_telnet_port = 9935                                  -- DBA��������telnet�˿�

dbu_ip = "192.168.201.27"                               -- DBU��������IP
dbu_listen_port = 9025                                  -- DBU�������ķ���˿�
dbu_telnet_port = 9925                                  -- DBU��������telnet�˿�


scs_ip = "192.168.201.27"                               -- SCS��������IP
scs_listen_port = 9015                          -- SCS�������ķ���˿�
scs_telnet_port = 9915                                          -- SCS��������telnet�˿�

ls_ip_for_gs                    = "192.168.201.3"               -- LS������ΪGS�ṩ��IP
ls_port_for_gs                  = 9045                          -- LS������ΪGS�ṩ�ķ���˿�
ls_ip_for_client                = "123.103.63.58"               -- LS������ΪClient�ṩ��IP
ls_port_for_client              = 9055                          -- LS������ΪClient�ṩ�ķ���˿�
ls_ip_for_telnet        = "192.168.201.3"               -- LS������ΪTelnet�ṩ��IP
ls_port_for_telnet              = 9955                          -- LS������ΪTelnet�ṩ�ķ���˿�

gs_ip = "192.168.201.3"                                         -- GS��������IP
gs_listen_port = 9065                                   -- GS�������ķ���˿�
gs_telnet_port = 9965                                   -- GS��������telnet�˿�
gs_http_ip = "192.168.201.3"                                            -- GS��������http IP
gs_http_port = 8085                                    -- GS��������http�˿�

bs_ip = "123.103.63.58"                                                 -- BS��������IP
bs_listen_port = 9075                                           -- BS�������ķ���˿�
bs_telnet_ip = "192.168.201.3"                                  -- BS��������telnetIP
bs_telnet_port = 9975                                   -- BS��������telnet�˿�

send_alive_tick                         = 3000          -- ������Ϣ���ͼ��(���ͼ������ҪС�ڼ����)
check_alive_tick                        = 15000         -- ������Ϣ�����
check_alive_count                       = 5                             -- ����������γ�����ŶϿ�����

low_netspeed_check_tick         = 30000                 -- �������ӳٿͻ�����GS������ʱ��
normal_netspeed_check_tick      = 60000                 -- �������ӳٿͻ�����GS������ʱ��
max_no_msg_duration                     = 300000                -- ��������ͻ��˱������ӵ��ʱ��

open_public_log_db            = true                -- �Ƿ���������־�⣨�ֶβ�����false��true��

public_log_db_ip = "192.168.201.38"                      -- ������־���ݿ��IP
public_log_db_port = 3306                           -- ������־���ݿ�Ķ˿�
public_log_db_name = "jgb_public_log"                   -- ������־���ݿ������
public_log_db_cs = "UTF-8"                          -- ������־���ݿ��ַ���

-------------------------------------------------------------------------------------------------
current_min_version     = 1             -- ��С�汾��
current_max_version     = 500          -- ���汾��
current_area_id         = 165         -- ��ǰ����

register_account   = false  -- �Ƿ����˺�ע�Ṧ��(�ǹٷ�����������Ϊfalse)
activate_account   = false  -- �Ƿ����˺ż����(�ǹٷ�����������Ϊfalse)


current_gift_type       = 1           ----������ͣ�1-oppo/VIVO��2-PP��
server_name        = "oppo17-������-2305"   -------����telnet������ʱ��ʾ���������ƣ���άͬ�¸��ݷ������������ã�

current_area_type            =  1                -- �����������ͣ����ֳ�ֵ���VIP�ȼ�1-��׿��Խ��IOS---2-IOS�ٷ���

current_output_type         = 1       -- ������Ԫ���������� (1-oppo/vivo/vivo_a/IOSԽ��(sy_p91_i/pp_i/tb_i),2-IOS�ٷ�)
