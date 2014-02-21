----------------------------------------------------------------------------------------------------------
local require = require
----------------------------------------------------------------------------------------------------------
module "gs_fixed_config"
----------------------------------------------------------------------------------------------------------
d_ms = require "ms"
----------------------------------------------------------------------------------------------------------
d_ms.d_gs_config.configtable.area    		 = d_ms.d_config.current_area_id      -- ����
d_ms.d_gs_config.configtable.port            = d_ms.d_config.gs_listen_port  	  -- �����˿�
d_ms.d_gs_config.configtable.telnet_port     = d_ms.d_config.gs_telnet_port	      -- telnet�˿�
d_ms.d_gs_config.configtable.ip              = d_ms.d_config.gs_ip                -- �ͻ��˼���IP
d_ms.d_gs_config.configtable.ls_server_ip    = d_ms.d_config.ls_ip_for_gs         -- LS��������ַ
d_ms.d_gs_config.configtable.ls_server_port  = d_ms.d_config.ls_port_for_gs       -- LS�������˿�
d_ms.d_gs_config.configtable.dba_server_ip   = d_ms.d_config.dba_ip 	          -- DB��������ַ
d_ms.d_gs_config.configtable.dba_server_port = d_ms.d_config.dba_listen_port	  -- DB�������˿�
d_ms.d_gs_config.configtable.http_ip         = d_ms.d_config.gs_http_ip		      -- HTTP��������ַ
d_ms.d_gs_config.configtable.http_port       = d_ms.d_config.gs_http_port	      -- HTTP�������˿�
d_ms.d_gs_config.configtable.auto_listen     = true                               -- �Զ���������

d_ms.d_gs_config.configtable.gs_status_for_login = {							  -- ������״̬����
    disconnect		= -1,			-- �Ͽ��������Ҫ�޸ģ�
    idle			= 0,			-- ���� (�ͻ��˿�������¼��Ϸ)
    normal			= 2500,			-- ���� (������ֵ����Ҫ���ǿ�����)
    busy			= 3000,			-- ��æ (�ﵽ��ֵ���޷������µĵ�¼)
}

d_ms.d_gs_config.configtable.option_config = {									  -- �ͻ�������ѡ���б�
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