import urllib3
import subprocess
import time
# disable InsecureRequestWarning if your are working without certificate verification
# see https://urllib3.readthedocs.org/en/latest/security.html
# be sure to use a recent enough urllib3 version if this fails
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

	#subprocess.call(["vcgencmd measure_temp"])
	#pa = subprocess.Popen("",stdout=subprocess.PIPE, shell=True)
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
	time.sleep(30)

