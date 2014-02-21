-------------------------------------------------------------------------------------------------------------
local require = require
-------------------------------------------------------------------------------------------------------------
module "dbp_fixed_config"
-------------------------------------------------------------------------------------------------------------
d_ms = require "ms"
-------------------------------------------------------------------------------------------------------------
d_ms.d_dbp_config.configtable.listen_ip				= d_ms.d_config.dbu_ip  	            -- ¼àÌýµØÖ·
d_ms.d_dbp_config.configtable.listen_port			= d_ms.d_config.dbu_listen_port  		-- ¼àÌý¶Ë¿Ú
d_ms.d_dbp_config.configtable.telnet_port			= d_ms.d_config.dbu_telnet_port			-- telnet¶Ë¿Ú

-- ÓÎÏ·Êý¾Ý¿âMYSQLÅäÖÃ
d_ms.d_dbp_config.configtable.db_game_dsn			= d_ms.d_config.game_db_ip
d_ms.d_dbp_config.configtable.db_game_port			= d_ms.d_config.game_db_port
d_ms.d_dbp_config.configtable.db_game_db			= d_ms.d_config.game_db_name
d_ms.d_dbp_config.configtable.db_game_user			= "root"
d_ms.d_dbp_config.configtable.db_game_pswd			= "5-,o}$#tO5x\\,iIvd\\&\\v"
-------------------------------------------------------------------------------------------------------------