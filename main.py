import paramiko
import tkinter as tk
import webbrowser
import os

host=''
port=22
username=''
privatekey=r''
container=''
website=''
localpath=r''

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=username, key_filename=privatekey)

window = tk.Tk()
window.title(container)
window.geometry('400x200')

l_var = tk.StringVar()
b_var = tk.StringVar()

in_status, out_status, err_status = ssh.exec_command('docker ps --filter name="'+ container + '" --format {{.Status}}')
status = out_status.read().decode()

def update():
	global l_var, b_var
	in_status, out_status, err_status = ssh.exec_command('docker ps --filter name="'+ container + '" --format {{.Status}}')
	status = out_status.read().decode()
	if status is '':
		l_var.set(container + ' has been stopped')
		b_var.set('Start ' + container)
		window.after(20000, update)
	else:
		l_var.set(container + ' is ' + status.lower())
		b_var.set('Stop ' + container)
		window.after(10000, update)

if status is '':
	l_var.set(container + ' is NOT running')
	b_var.set('Start ' + container)
	window.after(20000, update)
else:
	l_var.set(container + ' is ' + status.lower())
	b_var.set('Stop ' + container)
	window.after(10000, update)

l = tk.Label(window, textvariable=l_var, font=('Arial', 12), width=30, height=2)
l.pack()

def webconsole():
	if website != '':
		os.system('"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" --app=' + website)

def localfolder():
	if localpath != '':
		os.system('explorer.exe ' + localpath)

def start_stop():
	global l_var, b_var
	in_status, out_status, err_status = ssh.exec_command('docker ps --filter name="'+ container + '" --format {{.Status}}')
	status = out_status.read().decode()
	if status is '':
		ssh.exec_command('docker start ' + container)
		l_var.set(container + ' has been started')
		b_var.set('Stop ' + container)
		webconsole()
		localfolder()
		window.after(11000, update)
	else:
		ssh.exec_command('docker stop ' + container)
		l_var.set(container + ' has been stopped')
		b_var.set('Start ' + container)
		window.after(20000, update)

b = tk.Button(window, textvariable=b_var, font=('Arial', 12), width=25, height=1, command=start_stop)
b.pack()

b1 = tk.Button(window, text='Open web console (if any)', font=('Arial', 12), width=25, height=1, command=webconsole)
b2 = tk.Button(window, text='Open local folder path (if any)', font=('Arial', 12), width=25, height=1, command=localfolder)
b1.pack()
b2.pack()

window.mainloop()

ssh.close()
