-------------------------------------------------------------------------------------------------------------
-- Project: MobileGame
-- Modle  : common
-- Title  : 公共配置文件，所有服务器公用的信息
-- Author : robencle
-------------------------------------------------------------------------------------------------------------
-- History:
--          2012.11.05----Create
-------------------------------------------------------------------------------------------------------------
module "common.common_config"
-------------------------------------------------------------------------------------------------------------
role_top_level = 99                                                     -- 主角最高等级
cortege_top_level = 200                                         -- 佣兵最高等级
in_service = true                                                       -- 是否开启服务
game_db_ip = "127.0.0.1"                                -- 游戏数据库的IP
game_db_port = 3306                                     -- 游戏数据库的端口
game_db_name = "mobile_game2402"                                -- 游戏数据库的名称
game_db_cs = "UTF-8"                                            -- 游戏数据库字符集

log_db_ip = "127.0.0.1"                                 -- 日志数据库的IP
log_db_port = 3306                                      -- 日志数据库的端口
log_db_name = "mobile_game_log2402"                             -- 日志数据库的名称
log_db_cs = "UTF-8"                                                     -- 日志数据库字符集

dba_ip = "192.168.201.37"                               -- DBA服务器的IP
dba_listen_port = 9032                                  -- DBA服务器的服务端口
dba_telnet_port = 9932                                  -- DBA服务器的telnet端口

dbu_ip = "192.168.201.37"                               -- DBU服务器的IP
dbu_listen_port = 9022                                  -- DBU服务器的服务端口
dbu_telnet_port = 9922                                  -- DBU服务器的telnet端口


scs_ip = "192.168.201.37"                               -- SCS服务器的IP
scs_listen_port = 9012                          -- SCS服务器的服务端口
scs_telnet_port = 9912                                          -- SCS服务器的telnet端口

ls_ip_for_gs                    = "192.168.201.4"               -- LS服务器为GS提供的IP
ls_port_for_gs                  = 9042                          -- LS服务器为GS提供的服务端口
ls_ip_for_client                = "123.103.63.59"               -- LS服务器为Client提供的IP
ls_port_for_client              = 9052                          -- LS服务器为Client提供的服务端口
ls_ip_for_telnet        = "192.168.201.4"               -- LS服务器为Telnet提供的IP
ls_port_for_telnet              = 9952                          -- LS服务器为Telnet提供的服务端口

gs_ip = "192.168.201.4"                                         -- GS服务器的IP
gs_listen_port = 9062                                   -- GS服务器的服务端口
gs_telnet_port = 9962                                   -- GS服务器的telnet端口
gs_http_ip = "192.168.201.4"                                            -- GS服务器的http IP
gs_http_port = 8082                                    -- GS服务器的http端口

bs_ip = "123.103.63.59"                                                 -- BS服务器的IP
bs_listen_port = 9072                                           -- BS服务器的服务端口
bs_telnet_ip = "192.168.201.4"                                  -- BS服务器的telnetIP
bs_telnet_port = 9972                                   -- BS服务器的telnet端口

send_alive_tick                         = 3000          -- 心跳消息发送间隔(发送间隔必须要小于检查间隔)
check_alive_tick                        = 15000         -- 心跳消息检查间隔
check_alive_count                       = 5                             -- 心跳连续多次超出后才断开连接

low_netspeed_check_tick         = 30000                 -- 低网络延迟客户端与GS的心跳时间
normal_netspeed_check_tick      = 60000                 -- 非网络延迟客户端与GS的心跳时间
max_no_msg_duration                     = 300000                -- 服务器与客户端保持连接的最长时间

open_public_log_db                            = true             -- 是否开启公用日志库（字段参数：false、true）

public_log_db_ip = "192.168.201.38"                                             -- 公用日志数据库的IP
public_log_db_port = 3306                                                  -- 公用日志数据库的端口
public_log_db_name = "jgb_public_log"                                    -- 公用日志数据库的名称
public_log_db_cs = "UTF-8"                                                   -- 公用日志数据库字符集

-------------------------------------------------------------------------------------------------
current_min_version     = 1             -- 最小版本号
current_max_version     = 500          -- 最大版本号
current_area_id         = 159         -- 当前区号

register_account   = true  -- 是否开启账号注册功能(非官方服务器必须为false)
activate_account   = true  -- 是否开启账号激活功能(非官方服务器必须为false)

current_gift_type       = 4           ----礼包类型（1-oppo/VIVO，2-PP）
server_name        = "安卓混合-齐天大圣-2402"   -------用于telnet服务器时显示服务器名称（运维同事根据服务器名称配置）
current_area_type       = 1         ---IOS官方平台为2，非IOS官方（IOS越狱、安卓）为1

current_output_type                = 2       -- 分渠道元宝产出类型 (1-oppo/vivo/vivo_a/IOS越狱(sy_p91_i/pp_i/tb_i),2-IOS官方)
