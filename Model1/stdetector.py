import frida
import sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

def banner():
	print("""
   .dMMMb dMMMMMMP .aMMMb dMMMMMMP dMMMMMP dMMMMMMMMb  .aMMMb  .aMMMb  dMP dMP dMP dMMMMb  dMMMMMP 
  dMP" VP   dMP   dMP"dMP   dMP   dMP     dMP"dMP"dMP dMP"dMP dMP"VMP dMP dMP amr dMP dMP dMP      
  VMMMb    dMP   dMMMMMP   dMP   dMMMP   dMP dMP dMP dMMMMMP dMP     dMMMMMP dMP dMP dMP dMMMP     
dP .dMP   dMP   dMP dMP   dMP   dMP     dMP dMP dMP dMP dMP dMP.aMP dMP dMP dMP dMP dMP dMP        
VMMMP"   dMP   dMP dMP   dMP   dMMMMMP dMP dMP dMP dMP dMP  VMMMP" dMP dMP dMP dMP dMP dMMMMMP     
                                                                                                   
    dMMMMb  dMMMMMP dMMMMMMP dMMMMMP .aMMMb dMMMMMMP .aMMMb  dMMMMb                                
   dMP VMP dMP        dMP   dMP     dMP"VMP   dMP   dMP"dMP dMP.dMP                                
  dMP dMP dMMMP      dMP   dMMMP   dMP       dMP   dMP dMP dMMMMK"                                 
 dMP.aMP dMP        dMP   dMP     dMP.aMP   dMP   dMP.aMP dMP"AMF                                  
dMMMMP" dMMMMMP    dMP   dMMMMMP  VMMMP"   dMP    VMMMP" dMP dMP                                   
                                           							DVD Team      
	""")


if __name__ == "__main__":
	banner()
	if (len(sys.argv) < 5):
		print("python {} start|hook <device> <application name> file.js".format(sys.argv[0]))
		sys.exit(0)
	devices = frida.enumerate_devices()
	device = 0
	for item in devices:
		print(item.name)
		if sys.argv[2] == item.name:
			device = item

	if device != 0:
		print("device: ", device)
	else:
		print("Double check your input device")
		sys.exit(0)

	if (sys.argv[1] == "start"):
		pid = device.spawn([sys.argv[3]])
		process = device.attach(pid)
	elif(sys.argv[1] == "hook"):
		process = device.attach(sys.argv[3])
	else:
		print("python {} start|hook <device> <application name> file.js".format(sys.argv[0]))
		sys.exit(0)

	jscode = ""
	for i in range(4, len(sys.argv)):
		with open(sys.argv[i], "r") as f:
			jscode += f.read()
	script = process.create_script(jscode)
	script.on('message', on_message)
	print('[*] Running DETECTOR:')
	script.load()
	if (sys.argv[1] == "start"):
		device.resume(pid)
	input()