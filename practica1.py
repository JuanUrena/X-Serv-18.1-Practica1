#!/usr/bin/python3

"""
Practica1: Ejercicio de acortamiento de URLS como diccionario

Juan Ureña García-Gasco
j.urenag@alumnos.urjc.es

(Universidad Rey Juan Carlos)
"""

import webapp
import socket

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
                    text=text+"["+keys+"] -> ("+values+")</br>"
                answer=("<html><body><h1>DICCIONARIO URLs</h1>"+FORMULARIO+"Actualmente las URLs acorttadas son:</br>"+ text + "</body></html>")
                
            elif resource in url_short:
                code="200 OK"
                text=resource +"   "+ url_short[resource]
                answer=("<html><body><h1>REDIRECCIONO</h1></br>"+text+"</body></html>")
            else:
                code="404 NOT FOUND"
                answer=("<html><h1>PROBLEMA</h1></html>")
        elif method=="POST":
            body=request.split('\r\n\r\n',1)[1]
            url_short["/"+str(len(url_short))] =body.split('=')[1]
            url_long[body.split('=')[1]] =len(url_long)
            code="200 OK"
            answer=("<html><h1>AÑADIDO</h1></html>")   

        return (code, answer)

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
