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
        
    def request_to_url(self, request):
        body=request.split('\r\n\r\n',1)[1]
        return body.split('=')[1]
        
    def process_url(self, url):
        url=unquote(unquote(url))
        if not (url.startswith('http://') or url.startswith('https://')):
                    url="http://"+url
        return url
        
    def add_to_dict(self, key, value, dic):
        dic[key] =value
        return dic
        
    def process_answer(self, head, body):
        answer="<html><body><h1>" + head + "</h1>"
        answer=answer + body + "</body></html>"
        return answer
    
    def add_to_file(self, archive, text):
        data=open(archive, "a")
        data.write(text)
        data.close()
          
    #crear funcion que genere el mensaje http
    #tratar errores si el fichero se lee mal o similar.     
    
#Cambiar nombre variable 
    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """
        method, resource, request=parsedRequest
        global url_short
        global url_long
        global FORMULARIO
        global data
        text=""
        answer=""
        code="200 OK"
        if method=="GET":
            print ("aqui")
            if (resource=="/"):
                code="200 OK"
                text=FORMULARIO+"Actualmente las URLs acortadas son:</br>"+ self.dict_to_string(url_short)
                answer=self.process_answer("ACORTADOR URLs", text)
            elif resource in url_short:
                print ("REDIRECCIONO")
                code="302 Found \r\nLocation:"+ url_short[resource]
                print(code)
                answer=self.process_answer("", "")
            else:
                code="404 NOT FOUND"
                answer=self.process_answer("404 NOT FOUND", "No se ha encontrado el recurso")
        elif method=="POST":
            url=self.request_to_url(request)
            if (url):
                url=self.process_url(url)
                if not (url in url_long):
                    pos="/"+str(len(url_short))
                    #url_short[pos] =url
                    url_short=self.add_to_dict(pos, url, url_short)
                    url_long=self.add_to_dict(url, pos, url_long)
                    #url_long[url] =pos
                    code="200 OK"
                    text="<a href="+url+">"+url+"</a></br><a href="+pos+">http://localhost:1234"+pos+"</a>"
                    answer=self.process_answer("La URL se ha guardado correctamente", text)
                    data=self.add_to_file("data_url", pos+":"+url+"\n")
                else: 
                    print("La url ya estaba guardada") 
                    code="200 OK"
                    text="<a href="+url_long[url]+">http://localhost:1234"+url_long[url]+"</a>"
                    answer=self.process_answer("La URL ya estaba en la lista", text)
            else: 
                code="200 OK"
                answer=self.answer("Error", "Parece que el valor introducido no es valido")
        return (code, answer)

            
if __name__ == "__main__":
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
    testWebApp = practica1("localhost", 1234)
    
