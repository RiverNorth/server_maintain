-------------------------------------------------------------------------------------------------------------
-- Project: MobileGame
-- Modle  : BS
-- Title  : 网关服务器可配置数据
-- Author : robencle
-------------------------------------------------------------------------------------------------------------
-- History:
--          2012.09.15----Create
----------------------------------------------------------------------------------------------------------
local require = require
----------------------------------------------------------------------------------------------------------
module "bs_fixed_config"
----------------------------------------------------------------------------------------------------------
local d_ms = require "ms"
----------------------------------------------------------------------------------------------------------
d_ms.d_bs_config.configtable.area    		 	= d_ms.d_config.current_area_id
d_ms.d_bs_config.configtable.server_ip			= d_ms.d_config.gs_ip
d_ms.d_bs_config.configtable.server_port		= d_ms.d_config.gs_listen_port
d_ms.d_bs_config.configtable.listen_ip			= d_ms.d_config.bs_ip
d_ms.d_bs_config.configtable.listen_port		= d_ms.d_config.bs_listen_port
d_ms.d_bs_config.configtable.telnet_ip			= d_ms.d_config.bs_telnet_ip
d_ms.d_bs_config.configtable.telnet_port		= d_ms.d_config.bs_telnet_port
d_ms.d_bs_config.configtable.stat_msg			= true
d_ms.d_bs_config.configtable.stat_interval		= 60000
----------------------------------------------------------------------------------------------------------
