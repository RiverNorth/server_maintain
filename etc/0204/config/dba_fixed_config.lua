-------------------------------------------------------------------------------------------------------------
local require = require
-------------------------------------------------------------------------------------------------------------
module "dba_fixed_config"
-------------------------------------------------------------------------------------------------------------
d_ms = require "ms"
-------------------------------------------------------------------------------------------------------------
d_ms.d_dba_config.configtable.listen_ip 		= d_ms.d_config.dba_ip  	            -- ¼àÌýµØÖ·
d_ms.d_dba_config.configtable.listen_port		= d_ms.d_config.dba_listen_port  		-- ¼àÌý¶Ë¿Ú
d_ms.d_dba_config.configtable.telnet_port		= d_ms.d_config.dba_telnet_port		-- telnet¶Ë¿Ú

d_ms.d_dba_config.configtable.db_game_dsn        = d_ms.d_config.game_db_ip
d_ms.d_dba_config.configtable.db_game_port       = d_ms.d_config.game_db_port
d_ms.d_dba_config.configtable.db_game_user       = "mgdb0204"
d_ms.d_dba_config.configtable.db_game_pswd       = "pUzg.\"$}Rk$\"v\\pUzg.\\[}B?-Zt\"5-,o#PVC#~Tv#lu"
d_ms.d_dba_config.configtable.db_game_db         = d_ms.d_config.game_db_name
d_ms.d_dba_config.configtable.db_game_cs		 = d_ms.d_config.game_db_cs

d_ms.d_dba_config.configtable.db_gamelog_dsn	= d_ms.d_config.log_db_ip
d_ms.d_dba_config.configtable.db_gamelog_port	= d_ms.d_config.log_db_port
d_ms.d_dba_config.configtable.db_gamelog_user	= "mgdb0204"
d_ms.d_dba_config.configtable.db_gamelog_pswd	= "pUzg.\"$}Rk$\"v\\pUzg.\\[}B?-Zt\"5-,o#PVC#~Tv#lu"
d_ms.d_dba_config.configtable.db_gamelog_db		= d_ms.d_config.log_db_name
d_ms.d_dba_config.configtable.db_gamelog_cs		= d_ms.d_config.log_db_cs

d_ms.d_dba_config.configtable.db_public_gamelog_dsn             = d_ms.d_config.public_log_db_ip
d_ms.d_dba_config.configtable.db_public_gamelog_port    = d_ms.d_config.public_log_db_port
d_ms.d_dba_config.configtable.db_public_gamelog_user    = "mgdbpublic"
d_ms.d_dba_config.configtable.db_public_gamelog_pswd    = "v\"[}&}tO5x#vkPVC}&\\[#o}PVC\"&}v"
d_ms.d_dba_config.configtable.db_public_gamelog_db              = d_ms.d_config.public_log_db_name
d_ms.d_dba_config.configtable.db_public_gamelog_cs              = d_ms.d_config.public_log_db_cs
