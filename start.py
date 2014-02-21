# -*- coding:GBK -*-
from module.menu.menu import *
from module.menu.item import *
from bins import *
import sys

reload(sys)
sys.setdefaultencoding('GBK')
"""
def service_select():
	flag=False
	while not flag:
		areas_str=raw_input("请按照顺序选择服务 'SCS','DBA','LS','GS','BS' 以逗号','分割或者输入'all'\n"\).strip().lower()
		services=[]
		if services_str=="all":
			#directly put all area in 
			services.extend(service_dic.keys())
			flag=True
		else:
			temp_flag=True
			for name_string in services_str.split(","):
				if not service_dic.has_key(name_string):
					print("Unkonwn area name %s"%name_string)
					temp_flag=False
				else:
					services.append(name_string)
			if temp_flag:
				flag=True
	if flag:
		return services
"""

def area_select():
	flag=False
	while not flag:
		sorted_keys = copy.copy(nick_id_dic.keys())
		sorted_keys.sort()
		str_sorted_keys = str(sorted_keys).replace("'","")
		str_sorted_keys = str(str_sorted_keys).replace(" ","")
		areas_str=raw_input("please select areas sperate with ',' or type all\n area names:%s \n"%(str_sorted_keys)).strip()
		areas_ids=[]
		if areas_str=="all":
			#directly put all area in 
			areas_ids.extend(area_configs.keys())
			flag=True
		else:
			temp_flag=True
			for name_string in areas_str.split(","):
				if not nick_id_dic.has_key(name_string):
					print("Unkonwn area name %s"%name_string)
					temp_flag=False
				else:
					areas_ids.append(nick_id_dic[name_string])
			if temp_flag:
				flag=True
				
			#elif num_string.find("-")!=-1:
				#nums=num_string.split("-")
				#if len(nums)!=2 or not nums[0].isdigit() or not nums[1].isdigit():
					#print("[%s] wrong format"%num_string)
					#continue
				#start=int(nums[0])
				#end=int(nums[1])
				#if start>=end:
					#print("[%s] wrong format"%num_string)
				#for area_id in range(start,end+1):
					#ids.append(area_id)
			#else:
				#print("[%s] wrong format"%num_string)
				#continue
			#temp_flag=True
			#for area_id in ids:
				#if not area_configs.has_key(area_id):
					#print("Failed hasn't config file for area [%d]"% area_id)
					#temp_flag=False
			#if not temp_flag:
				#continue
			#for area_id in ids:
				#areas_ids.append(area_id)
			#flag=True
			
	areas_ids.sort()
	while flag and True:
		y_or_n=raw_input("process will operate on area %s are you sure?y/n\n"%(str(areas_ids)))
		y_or_n=y_or_n.lower()
		if y_or_n=="y":
			return areas_ids
		elif y_or_n=="n":
			return False
		
def service_select():
	flag=False
	while not flag:
		areas_str=raw_input("please select service to open sperate with ',' :%s \n"%(nick_id_dic.keys())).strip()
		areas_ids=[]
		if areas_str=="all":
			#directly put all area in 
			areas_ids.extend(area_configs.keys())
			flag=True
		else:
			temp_flag=True
			for name_string in areas_str.split(","):
				if not nick_id_dic.has_key(name_string):
					print("Unkonwn area name %s"%name_string)
					temp_flag=False
				else:
					areas_ids.append(nick_id_dic[name_string])
			if temp_flag:
				flag=True	
		
def path_select(op_str,is_abs_path):
	print(op_str)
	while True:
		if is_abs_path:
			path_str=raw_input("please enter an absolute path begin with '/' example:[/test/abc]\n").strip()	
		else:
			path_str=raw_input("please enter an relative path not begin with '/' example:[test/abc]\n").strip()
		#tricky judgement 
		if is_abs_path != path_str.startswith("/"):
			print("[%s]format error:\n"%path_str)
		else:
			return path_str
			
def true_false_select(op_string):
	while True:
		y_or_n=raw_input(op_string)
		y_or_n=y_or_n.lower()
		if y_or_n=="y":
			return True
		elif y_or_n=="n":
			return False
def is_gdb_select():
	while True:
		gdb_or_gss=raw_input("want to upload to GS or GDB?gs/gdb\n").lower()
		if gdb_or_gss=="gs":
			return False
			
		elif gdb_or_gss=="gdb":
			return True
	
			
def bin_backup_areas():
	#return false indicate he want to back to menu
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP
	result=backup_areas(area_ids,time.strftime("%m%d_%H%M%S"))
	if not result:
		return Menu.ERROR_STEP
	return Menu.SUC_STEP
	
def bin_piliangshangchuan():
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP
	local_path=path_select("please enter an local file to upload",True)
	remote_path=path_select("please enter an remote server path to upload",False)
	is_gdb=is_gdb_select()
	t_or_f=true_false_select("are sure want to upload %s to %s on area%s\n"%(local_path,remote_path,str(area_ids)))
	result=False
	if t_or_f==False:
		return Menu.BACK_STEP
	else:
		result=piliangshangchuan(local_path,area_ids,remote_path,is_gdb)
	
	if not result:
		return Menu.ERROR_STEP
	else:
		return Menu.SUC_STEP

def bin_shangchuanfenqu():
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP
	local_path=False
	while True:
		local_path=path_select("please enter an local zip file to upload and unpack",True)
		if not local_path.endswith(".zip"):
			print("local file must be a zip file\n")
			continue
		break
	t_or_f=true_false_select("are sure want to upload %s to GDM on area%s\n"%(local_path,area_ids))
	result=False	
	if t_or_f==False:
		return Menu.BACK_STEP
	else:
		result=shangchuanfenqu(local_path,area_ids)
	
	if not result:
		return Menu.ERROR_STEP
	else:
		return Menu.SUC_STEP	
	
def bin_gengxinfenqu():
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP
	result=gengxinfenqu(area_ids)
	if not result:
		return Menu.ERROR_STEP
	else:
		return Menu.SUC_STEP		

def bin_guanbifenqu():
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP
	t_or_f=true_false_select("are sure want to shutdown server on area%s\n"%(area_ids))
	result=True	
	if t_or_f==False:
		return Menu.BACK_STEP
	else:
		for area_id in area_ids:
			print("----------begin shutdown server on area[%d]----------"%area_id)
			for service_name,cmd_pairs in shutdown_cmd_dic:
				t_result = shutdown_service(area_id, service_name, cmd_pairs)
				if t_result == False:
					result = False
					break
	
	if not result:
		return Menu.ERROR_STEP
	else:
		return Menu.SUC_STEP		
		
def bin_kaiqifenqu():
	flag=True
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP	
	for area_id in area_ids:
		#start GDB service
		result=startup_server1([area_id],True)
		if not result:
			continue
		#start GS service
		result1=startup_server1([area_id],False)
		if not result or not result1:
			flag=False	
	if not flag:
		return Menu.ERROR_STEP	
	return Menu.SUC_STEP

def bin_gengxinshujuku():
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP	
	result=gengxinshujuku(area_ids)
	if not result:
		return Menu.ERROR_STEP
	else:
		return Menu.SUC_STEP	
	
def bin_rejiazai():
	area_ids=area_select()
	if area_ids==False:
		return Menu.BACK_STEP
	cmd=raw_input("please type a cmd to execute:\n")
	result=rejiazai(area_ids,cmd)
	if not result:
		return Menu.ERROR_STEP
	else:
		return Menu.SUC_STEP	
	
def bin_kaiqifuwu():
	pass
	
def bin_exit():
	sys.exit(0)

def testcase1():
	f=open("/tmp/asdf.log","w")
	sys.stdout=f
	main_menu=Menu()
	item1=Item("BeiFen fenqu",bin_backup_areas)
	item2=Item("PiLiangChuanWenJian",bin_piliangshangchuan)
	item3=Item("ShangChuanFenQu",bin_shangchuanfenqu)
	item4=Item("GuanBiFenqu",bin_guanbifenqu)
	item5=Item("KaiQiFenqu",bin_kaiqifenqu)
	item6=Item("Exit",bin_exit)
	main_menu.register_item(item1)
	main_menu.register_item(item2)
	main_menu.register_item(item3)
	main_menu.register_item(item4)
	main_menu.register_item(item5)
	main_menu.register_item(item6)
	main_menu.display()

def main():
	main_menu=Menu()
	item1=Item("备份分区",bin_backup_areas)
	item2=Item("批量传文件",bin_piliangshangchuan)
	item3=Item("上传分区",bin_shangchuanfenqu)
	item4=Item("更新分区",bin_gengxinfenqu)
	item5=Item("关闭分区",bin_guanbifenqu)
	item6=Item("开启分区",bin_kaiqifenqu)
	item7=Item("更新数据库",bin_gengxinshujuku)
	item8=Item("热加载",bin_rejiazai)
	item9=Item("Exit",bin_exit)
	main_menu.register_item(item1)
	main_menu.register_item(item2)
	main_menu.register_item(item3)
	main_menu.register_item(item4)
	main_menu.register_item(item5)
	main_menu.register_item(item6)
	main_menu.register_item(item7)
	main_menu.register_item(item8)
	main_menu.register_item(item9)
	main_menu.display()
	
if __name__ == '__main__':
	main()	