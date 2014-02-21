-------------------------------------------------------------------------------------------------------------
local require = require
-------------------------------------------------------------------------------------------------------------
module "dbu_fixed_config"
-------------------------------------------------------------------------------------------------------------
d_ms = require "ms"
-------------------------------------------------------------------------------------------------------------
-- 1 表示更新 0 表示不更新
d_ms.d_dbu_config.configtable.is_update_Game	= 1									-- 是否更新Game
d_ms.d_dbu_config.configtable.is_update_Log	= 1									-- 是否更新Game_log

d_ms.d_dbu_config.configtable.listen_ip 		= d_ms.d_config.dbu_ip  	            -- 监听地址
d_ms.d_dbu_config.configtable.listen_port		= d_ms.d_config.dbu_listen_port  		-- 监听端口
d_ms.d_dbu_config.configtable.telnet_port		= d_ms.d_config.dbu_telnet_port		-- telnet端口

d_ms.d_dbu_config.configtable.exec_bak 			= false		-- 是否执行备份和优化 默认打开
d_ms.d_dbu_config.configtable.exec_optimize 	= false		-- 是否执行优化 默认打开
d_ms.d_dbu_config.configtable.dba_password      = "5-,o}$#tO5x\\,iIvd\\&\\v"
d_ms.d_dbu_config.configtable.bak_command 		= "mysqldump --default-character-set=UTF-8 --opt -R --flush-logs -umysqlbak -p%s -h127.0.0.1 -P3306 %s>d:/home/backup/%s"				-- 备份的命令配置, 备份存放的文件夹必须存在
d_ms.d_dbu_config.configtable.optimize_sql 		= "OPTIMIZE TABLE %s.player;"

-- 游戏数据库MYSQL配置
d_ms.d_dbu_config.configtable.db_game_dsn     = d_ms.d_config.game_db_ip
d_ms.d_dbu_config.configtable.db_game_port    = d_ms.d_config.game_db_port
d_ms.d_dbu_config.configtable.db_game_user    = "mgdb3201"
d_ms.d_dbu_config.configtable.db_game_pswd    = "pUzg.\"$}Rk$\"v\\pUzg.\\[}B?-Zt\"5-,o#PVC#~Tv#lu"
d_ms.d_dbu_config.configtable.db_game_db      = d_ms.d_config.game_db_name
d_ms.d_dbu_config.configtable.db_game_cs	  = d_ms.d_config.game_db_cs

d_ms.d_dbu_config.configtable.db_gamelog_dsn	= d_ms.d_config.log_db_ip
d_ms.d_dbu_config.configtable.db_gamelog_port	= d_ms.d_config.log_db_port
d_ms.d_dbu_config.configtable.db_gamelog_user	= "mgdb3201"
d_ms.d_dbu_config.configtable.db_gamelog_pswd	= "pUzg.\"$}Rk$\"v\\pUzg.\\[}B?-Zt\"5-,o#PVC#~Tv#lu"
d_ms.d_dbu_config.configtable.db_gamelog_db		= d_ms.d_config.log_db_name
d_ms.d_dbu_config.configtable.db_gamelog_cs		= d_ms.d_config.log_db_cs
-------------------------------------------------------------------------------------------------------------
