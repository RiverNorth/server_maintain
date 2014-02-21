-------------------------------------------------------------------------------------------------------------
local require = require
-------------------------------------------------------------------------------------------------------------
module "ls_fixed_config"
-------------------------------------------------------------------------------------------------------------
d_ms = require "ms"
-------------------------------------------------------------------------------------------------------------
p_t = d_ms.d_common_def.platform_type
-------------------------------------------------------------------------------------------------------------
d_ms.d_ls_config.configtable.current_min_version    = d_ms.d_config.current_min_version  	-- 当前最小版本号
d_ms.d_ls_config.configtable.current_max_version    = d_ms.d_config.current_max_version  	-- 当前最大版本号
-------------------------------------------------------------------------------------------------------------
d_ms.d_ls_config.configtable.area					= d_ms.d_config.current_area_id			-- 区号
d_ms.d_ls_config.configtable.ip_for_gs				= d_ms.d_config.ls_ip_for_gs			-- 监听地址0(GS)
d_ms.d_ls_config.configtable.port_for_gs			= d_ms.d_config.ls_port_for_gs			-- 监听端口0(GS)
d_ms.d_ls_config.configtable.ip_for_client			= d_ms.d_config.ls_ip_for_client		-- 监听地址1(Client)
d_ms.d_ls_config.configtable.port_for_client		= d_ms.d_config.ls_port_for_client		-- 监听端口1(Client)
d_ms.d_ls_config.configtable.telnet_ip          	= d_ms.d_config.ls_ip_for_telnet		-- telnet地址
d_ms.d_ls_config.configtable.telnet_port			= d_ms.d_config.ls_port_for_telnet		-- telnet端口
d_ms.d_ls_config.configtable.dba_server_ip			= d_ms.d_config.dba_ip		            -- DBA服务器地址
d_ms.d_ls_config.configtable.dba_server_port		= d_ms.d_config.dba_listen_port  		-- DBA服务器端口
d_ms.d_ls_config.configtable.for_inter_ios			= false  								-- 允许公司内部人员用IOS登录第三方服务器
d_ms.d_ls_config.configtable.start_listen			= true  								-- 是否启动后直接监听
d_ms.d_ls_config.configtable.platform_list			=										-- 允许在本区登录的第三方平台账号
{
  [p_t.sy_pgy_i]   = true ,
  [p_t.tb_i]   = true ,
  [p_t.pp_i]   = true ,
  [p_t.sy_p91_i]   = true ,
  [p_t.uc_i]   = true ,	
  [p_t.dj_i]   = true ,	
  [p_t.p91_i]                     = true,
  [p_t.ky_i]                      = true,

}


