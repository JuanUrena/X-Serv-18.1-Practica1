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
import os.path

url_short={}
url_long={}



FORMULARIO= """
<form action="" method="POST"> 
URL que quiere guardar:<br>
<input type="text" name="URL" value=><br>
<input type="submit" value="Enviar">
</form>
"""


if (os.path.isfile("data_url")):
    data=open("data_url")
else:
    data=open("data_url", "w")
    data.close()
    data=open("data_url")
   
urls_code=data.read().split()
data.close()
#print (urls_code)
    
#moverlo al if name main 
for url in urls_code:
    key=url.split(":",1)[0]
    value=url.split(":",1)[1]
    url_short[key] =value
    url_long[value] =key

class practica1(webapp.webApp):

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        if (request):
            method=request.split()[0]
            resource=request.split()[1]
        else:
            method=None
            resource=None
            request=None
   
        return method, resource, request
        
        
        
        
    def dict_to_string(self, dictionary):
        text=""
        for keys, values in dictionary.items():
            text=text+"["+keys+"]:("+values+")</br>"
        return text
        
        
#si me pasan url en blanco, comprobar.    
#Cambiar nombre variable 
    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """
        method, resource, request=parsedRequest
        text=""
        answer=""
        code="200 OK"
        if method=="GET":
            if resource=="/":
                code="200 OK"
                text=self.dict_to_string(url_short) 
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
            
            if (url):
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
                    data=open("data_url", "a")
                    data.write(pos+":"+url+"\n")
                    data.close()
                else: 
                    print("La url ya estaba guardada") 
                    code="200 OK"
                    answer=("<html><body><h1>La URL ya estaba en la lista, su direccion es:</h1><a href="+url_long[url]+">http://localhost:1234"+url_long[url]+"</a> </body></html>")
            else: 
                code="200 OK"
                answer=("<html><h1>Rosu hermano quieres casarte conmigo <3 </h1></html>")
            

        return (code, answer)

            
if __name__ == "__main__":
    testWebApp = practica1("localhost", 1234)
