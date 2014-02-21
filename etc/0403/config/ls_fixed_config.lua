-------------------------------------------------------------------------------------------------------------
local require = require
-------------------------------------------------------------------------------------------------------------
module "ls_fixed_config"
-------------------------------------------------------------------------------------------------------------
d_ms = require "ms"
-------------------------------------------------------------------------------------------------------------
p_t = d_ms.d_common_def.platform_type
-------------------------------------------------------------------------------------------------------------
d_ms.d_ls_config.configtable.current_min_version    = d_ms.d_config.current_min_version  	-- ��ǰ��С�汾��
d_ms.d_ls_config.configtable.current_max_version    = d_ms.d_config.current_max_version  	-- ��ǰ���汾��
-------------------------------------------------------------------------------------------------------------
d_ms.d_ls_config.configtable.area					= d_ms.d_config.current_area_id			-- ����
d_ms.d_ls_config.configtable.ip_for_gs				= d_ms.d_config.ls_ip_for_gs			-- ������ַ0(GS)
d_ms.d_ls_config.configtable.port_for_gs			= d_ms.d_config.ls_port_for_gs			-- �����˿�0(GS)
d_ms.d_ls_config.configtable.ip_for_client			= d_ms.d_config.ls_ip_for_client		-- ������ַ1(Client)
d_ms.d_ls_config.configtable.port_for_client		= d_ms.d_config.ls_port_for_client		-- �����˿�1(Client)
d_ms.d_ls_config.configtable.telnet_ip          	= d_ms.d_config.ls_ip_for_telnet		-- telnet��ַ
d_ms.d_ls_config.configtable.telnet_port			= d_ms.d_config.ls_port_for_telnet		-- telnet�˿�
d_ms.d_ls_config.configtable.dba_server_ip			= d_ms.d_config.dba_ip		            -- DBA��������ַ
d_ms.d_ls_config.configtable.dba_server_port		= d_ms.d_config.dba_listen_port  		-- DBA�������˿�
d_ms.d_ls_config.configtable.for_inter_ios			= false  								-- ����˾�ڲ���Ա��IOS��¼������������
d_ms.d_ls_config.configtable.start_listen			= true  								-- �Ƿ�������ֱ�Ӽ���
d_ms.d_ls_config.configtable.platform_list			=										-- �����ڱ�����¼�ĵ�����ƽ̨�˺�
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


