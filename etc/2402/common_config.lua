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
game_db_name = "mobile_game2402"                                -- ��Ϸ���ݿ������
game_db_cs = "UTF-8"                                            -- ��Ϸ���ݿ��ַ���

log_db_ip = "127.0.0.1"                                 -- ��־���ݿ��IP
log_db_port = 3306                                      -- ��־���ݿ�Ķ˿�
log_db_name = "mobile_game_log2402"                             -- ��־���ݿ������
log_db_cs = "UTF-8"                                                     -- ��־���ݿ��ַ���

dba_ip = "192.168.201.37"                               -- DBA��������IP
dba_listen_port = 9032                                  -- DBA�������ķ���˿�
dba_telnet_port = 9932                                  -- DBA��������telnet�˿�

dbu_ip = "192.168.201.37"                               -- DBU��������IP
dbu_listen_port = 9022                                  -- DBU�������ķ���˿�
dbu_telnet_port = 9922                                  -- DBU��������telnet�˿�


scs_ip = "192.168.201.37"                               -- SCS��������IP
scs_listen_port = 9012                          -- SCS�������ķ���˿�
scs_telnet_port = 9912                                          -- SCS��������telnet�˿�

ls_ip_for_gs                    = "192.168.201.4"               -- LS������ΪGS�ṩ��IP
ls_port_for_gs                  = 9042                          -- LS������ΪGS�ṩ�ķ���˿�
ls_ip_for_client                = "123.103.63.59"               -- LS������ΪClient�ṩ��IP
ls_port_for_client              = 9052                          -- LS������ΪClient�ṩ�ķ���˿�
ls_ip_for_telnet        = "192.168.201.4"               -- LS������ΪTelnet�ṩ��IP
ls_port_for_telnet              = 9952                          -- LS������ΪTelnet�ṩ�ķ���˿�

gs_ip = "192.168.201.4"                                         -- GS��������IP
gs_listen_port = 9062                                   -- GS�������ķ���˿�
gs_telnet_port = 9962                                   -- GS��������telnet�˿�
gs_http_ip = "192.168.201.4"                                            -- GS��������http IP
gs_http_port = 8082                                    -- GS��������http�˿�

bs_ip = "123.103.63.59"                                                 -- BS��������IP
bs_listen_port = 9072                                           -- BS�������ķ���˿�
bs_telnet_ip = "192.168.201.4"                                  -- BS��������telnetIP
bs_telnet_port = 9972                                   -- BS��������telnet�˿�

send_alive_tick                         = 3000          -- ������Ϣ���ͼ��(���ͼ������ҪС�ڼ����)
check_alive_tick                        = 15000         -- ������Ϣ�����
check_alive_count                       = 5                             -- ����������γ�����ŶϿ�����

low_netspeed_check_tick         = 30000                 -- �������ӳٿͻ�����GS������ʱ��
normal_netspeed_check_tick      = 60000                 -- �������ӳٿͻ�����GS������ʱ��
max_no_msg_duration                     = 300000                -- ��������ͻ��˱������ӵ��ʱ��

open_public_log_db                            = true             -- �Ƿ���������־�⣨�ֶβ�����false��true��

public_log_db_ip = "192.168.201.38"                                             -- ������־���ݿ��IP
public_log_db_port = 3306                                                  -- ������־���ݿ�Ķ˿�
public_log_db_name = "jgb_public_log"                                    -- ������־���ݿ������
public_log_db_cs = "UTF-8"                                                   -- ������־���ݿ��ַ���

-------------------------------------------------------------------------------------------------
current_min_version     = 1             -- ��С�汾��
current_max_version     = 500          -- ���汾��
current_area_id         = 159         -- ��ǰ����

register_account   = true  -- �Ƿ����˺�ע�Ṧ��(�ǹٷ�����������Ϊfalse)
activate_account   = true  -- �Ƿ����˺ż����(�ǹٷ�����������Ϊfalse)

current_gift_type       = 4           ----������ͣ�1-oppo/VIVO��2-PP��
server_name        = "��׿���-�����ʥ-2402"   -------����telnet������ʱ��ʾ���������ƣ���άͬ�¸��ݷ������������ã�
current_area_type       = 1         ---IOS�ٷ�ƽ̨Ϊ2����IOS�ٷ���IOSԽ������׿��Ϊ1

current_output_type                = 2       -- ������Ԫ���������� (1-oppo/vivo/vivo_a/IOSԽ��(sy_p91_i/pp_i/tb_i),2-IOS�ٷ�)
