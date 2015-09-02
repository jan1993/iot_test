import urllib3
import subprocess
import time
import os
import glob
# disable InsecureRequestWarning if your are working without certificate verification
# see https://urllib3.readthedocs.org/en/latest/security.html
# be sure to use a recent enough urllib3 version if this fails

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
	
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c

while True:
	
	try:
		urllib3.disable_warnings()
	except:
		#print('urllib3.disable_warnings() failed - get a recent enough urllib3 version to avoid potential InsecureRequestWarning warnings! Can and will continue though.')
		print ''
	print '---- ---- ---- ---- ---- ---- ----'
	# use with or without proxy
	http = urllib3.PoolManager()
	# http = urllib3.proxy_from_url('http://proxy_host:proxy_port')

	# interaction for a specific Device instance - replace 1 with your specific Device ID
	url = 'https://iotmmsd059251trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/e203e513-4ba4-4544-b7a3-6bed7faa52d6'

	headers = urllib3.util.make_headers()

	#magic
	pTemp = subprocess.Popen("vcgencmd measure_temp",stdout=subprocess.PIPE, shell=True)
	(cpuTemp,err) = pTemp.communicate()
	cpuTemp = cpuTemp[5:-3]

	timestamp = int(time.time())
	# use with authentication
	# please insert correct OAuth token
	headers['Authorization'] = 'Bearer ' + '56e7d5215dbede9951faef46ecf73275'
	headers['Content-Type'] = 'application/json;charset=utf-8'

	# send message of Message Type 1 and the corresponding payload layout that you defined in the IoT Services Cockpit
	body='{"mode":"async", "messageType":"ee71d66528cc09922871", "messages":[{"sensor":"cpuTemp", "value":'+cpuTemp+', "timestamp":'+str(timestamp)+'}]}'
	print body

	r = http.urlopen('POST', url, body=body, headers=headers)

	print(r.status)
	print(r.data)

	body='{"mode":"async", "messageType":"ee71d66528cc09922871", "messages":[{"sensor":"roomTemp", "value":'+read_temp()+', "timestamp":'+str(timestamp)+'}]}'
	r = http.urlopen('POST', url, body=body, headers=headers)


	time.sleep(30)
