-------------------------------------------------------------------------------------------------------------
local require = require
-------------------------------------------------------------------------------------------------------------
module "dbu_fixed_config"
-------------------------------------------------------------------------------------------------------------
d_ms = require "ms"
-------------------------------------------------------------------------------------------------------------
-- 1 ��ʾ���� 0 ��ʾ������
d_ms.d_dbu_config.configtable.is_update_Game	= 1									-- �Ƿ����Game
d_ms.d_dbu_config.configtable.is_update_Log	= 1									-- �Ƿ����Game_log

d_ms.d_dbu_config.configtable.listen_ip 		= d_ms.d_config.dbu_ip  	            -- ������ַ
d_ms.d_dbu_config.configtable.listen_port		= d_ms.d_config.dbu_listen_port  		-- �����˿�
d_ms.d_dbu_config.configtable.telnet_port		= d_ms.d_config.dbu_telnet_port		-- telnet�˿�

d_ms.d_dbu_config.configtable.exec_bak 			= false		-- �Ƿ�ִ�б��ݺ��Ż� Ĭ�ϴ�
d_ms.d_dbu_config.configtable.exec_optimize 	= false		-- �Ƿ�ִ���Ż� Ĭ�ϴ�
d_ms.d_dbu_config.configtable.dba_password      = "5-,o}$#tO5x\\,iIvd\\&\\v"
d_ms.d_dbu_config.configtable.bak_command 		= "mysqldump --default-character-set=UTF-8 --opt -R --flush-logs -umysqlbak -p%s -h127.0.0.1 -P3306 %s>d:/home/backup/%s"				-- ���ݵ���������, ���ݴ�ŵ��ļ��б������
d_ms.d_dbu_config.configtable.optimize_sql 		= "OPTIMIZE TABLE %s.player;"

-- ��Ϸ���ݿ�MYSQL����
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
