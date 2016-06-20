import sys
import os
import subprocess  
base_dir = ''
if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('usag: python info.py num_weibo|num_user|weibo|user')
	arg = sys.argv[1]
	path = '%s../data/' % (base_dir)
	if arg == 'num_weibo':
		shellcommand = 'wc -l %sweibos'%path
  		result= subprocess.getstatusoutput(shellcommand)  
		output= result[1]
		output = output.split(' ')[0].strip()
		sys.exit(output)
	if arg == 'num_user':
		shellcommand = 'wc -l %sseen'%path
  		result= subprocess.getstatusoutput(shellcommand)  
		output= result[1]
		output = output.split(' ')[0].strip()
		sys.exit(output)
	if arg == 'weibo':
		shellcommand = 'tail -n 5 %sweibos'%path
  		result= subprocess.getstatusoutput(shellcommand)  
		output= result[1]
		sys.exit(output)
	if arg == 'user':
		shellcommand = 'tail -n 5 %susers'%path
  		result= subprocess.getstatusoutput(shellcommand)  
		output= result[1]
		sys.exit(output)
		
