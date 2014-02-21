----------------------------------------------------------------------------------------------------------
local require = require
----------------------------------------------------------------------------------------------------------
module "gs_fixed_config"
----------------------------------------------------------------------------------------------------------
d_ms = require "ms"
----------------------------------------------------------------------------------------------------------
d_ms.d_gs_config.configtable.area    		 = d_ms.d_config.current_area_id      -- 区号
d_ms.d_gs_config.configtable.port            = d_ms.d_config.gs_listen_port  	  -- 监听端口
d_ms.d_gs_config.configtable.telnet_port     = d_ms.d_config.gs_telnet_port	      -- telnet端口
d_ms.d_gs_config.configtable.ip              = d_ms.d_config.gs_ip                -- 客户端监听IP
d_ms.d_gs_config.configtable.ls_server_ip    = d_ms.d_config.ls_ip_for_gs         -- LS服务器地址
d_ms.d_gs_config.configtable.ls_server_port  = d_ms.d_config.ls_port_for_gs       -- LS服务器端口
d_ms.d_gs_config.configtable.dba_server_ip   = d_ms.d_config.dba_ip 	          -- DB服务器地址
d_ms.d_gs_config.configtable.dba_server_port = d_ms.d_config.dba_listen_port	  -- DB服务器端口
d_ms.d_gs_config.configtable.http_ip         = d_ms.d_config.gs_http_ip		      -- HTTP服务器地址
d_ms.d_gs_config.configtable.http_port       = d_ms.d_config.gs_http_port	      -- HTTP服务器端口
d_ms.d_gs_config.configtable.auto_listen     = true                               -- 自动启动监听

d_ms.d_gs_config.configtable.gs_status_for_login = {							  -- 服务器状态配置
    disconnect		= -1,			-- 断开（这个不要修改）
    idle			= 0,			-- 空闲 (客户端可正常登录游戏)
    normal			= 2500,			-- 正常 (超过该值，需要考虑开新区)
    busy			= 3000,			-- 繁忙 (达到该值，无法接受新的登录)
}

d_ms.d_gs_config.configtable.option_config = {									  -- 客户端其他选项列表
	collector		= true,
	achievement		= true,
	Bulletin		= true,
	message			= true,
	chat			= true,
	setting			= true,
	service			= true,
	relogin			= true,
	gift_card		= true,
	forum			= true,
	item_fly		= false,
}