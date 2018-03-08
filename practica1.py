#!/usr/bin/python3

"""
Practica1: Ejercicio de acortamiento de URLS como diccionario

Juan Ureña García-Gasco
j.urenag@alumnos.urjc.es

(Universidad Rey Juan Carlos)
"""

import webapp
import socket
from urllib.parse import unquote

url_short={}
url_long={}

#To Do deberia mostrar toda la biblioteca, no volver a si mismo

#form action siempre devulve a barra, y en el caso de que me pasen una url buena ya pondre yo que tengo que mandar a otra pagina
FORMULARIO= """
<form action="" method="POST"> 
URL que quiere guardar:<br>
<input type="text" name="URL" value=><br>
<input type="submit" value="Enviar">
</form>
"""


data=open("data_url")

urls_code=data.read().split()
print (urls_code)

class practica1(webapp.webApp):

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        
        method=request.split()[0]
        resource=request.split()[1]

        return method, resource, request
        #Cambiar nombre variable 
    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """
        method, resource, request=parsedRequest
        text=""
        if method=="GET":
            if resource=="/":
                code="200 OK"
        
                for keys, values in url_short.items():
                    text=text+"["+keys+"]:("+values+")</br>"
                answer=("<html><body><h1>DICCIONARIO URLs</h1>"+FORMULARIO+"Actualmente las URLs acortadas son:</br>"+ text + "</body></html>")
                
            elif resource in url_short:
                code="302 Found \r\nLocation: "+url_short[resource]
                text=resource +"   "+ url_short[resource]
                answer=("<html><body><h1></h1></body></html>")
            else:
                code="404 NOT FOUND"
                answer=("<html><h1>PROBLEMA</h1></html>")
        elif method=="POST":
            body=request.split('\r\n\r\n',1)[1]
            url=body.split('=')[1]
            print(url)
            url=unquote(unquote(url))
            print(url)
            if not (url.startswith('http://') or url.startswith('https://')):
                url="http://"+url
            if not (url in url_long):
                pos="/"+str(len(url_short))
                url_short[pos] =url
                url_long[url] =pos
                code="200 OK"
                answer=("<html><body><h1>La URL se ha guardado correctamente</h1><a href="+url+">URL Original</a> </br><a href=http://localhost:1234"+pos+">URL corta</a></body></html>")
            else: 
#hay que hacer esta parte de mostrar donde esta url corta
                print("Hay que mandar el codigo y demas") 
                code="200 OK"
                answer=("<html><body><h1>La URL ya estaba en la lista</h1></body></html>")
            

        return (code, answer)
#Revisar si quitar.
    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = recvSocket.recv(2048).decode('utf-8')
            print(request)
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print('Answering back...')
            recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n", 'utf-8'))
            recvSocket.close()
            
if __name__ == "__main__":
    testWebApp = practica1("localhost", 1234)
