-------------------------------------------------------------------------------------------------------------
local require = require
-------------------------------------------------------------------------------------------------------------
module "dti_fixed_config"
-------------------------------------------------------------------------------------------------------------
d_ms = require "ms"
-------------------------------------------------------------------------------------------------------------
d_ms.d_dti_config.configtable.listen_ip 		= d_ms.d_config.dti_ip  	            -- ������ַ
d_ms.d_dti_config.configtable.listen_port		= d_ms.d_config.dti_listen_port  		-- �����˿�
d_ms.d_dti_config.configtable.telnet_port		= d_ms.d_config.dti_telnet_port			-- telnet�˿�
d_ms.d_dti_config.configtable.http_ip			= d_ms.d_config.dti_http_ip
d_ms.d_dti_config.configtable.http_port			= d_ms.d_config.dti_http_port			-- http�˿�