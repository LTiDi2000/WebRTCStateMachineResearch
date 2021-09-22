import frida, sys
import time
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)
def banner():
	print("""

██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                           		Frida      
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
	print('[*] Running script:')
	script.load()
	if (sys.argv[1] == "start"):
		device.resume(pid)
	input()
