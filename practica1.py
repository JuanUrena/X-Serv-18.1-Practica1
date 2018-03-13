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
import sys

url_short = {}
url_long = {}

FORMULARIO = """
<form action=""method="POST">
URL que quiere guardar:<br>
<input type="text" name="URL" value=><br>
<input type="submit" value="Enviar">
</form>
"""
Text = "data_url"


class practica1(webapp.webApp):

    # Procesado de la petición
    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        if (request):
            method = request.split()[0]
            resource = request.split()[1]
        else:
            method = None
            resource = None
            request = None
        return method, resource, request

    # Pasamos la informacion en un diccionario a un String
    def dict_to_string(self, dictionary):
        text = ""
        for keys, values in dictionary.items():
            text += "[" + keys + "]:(" + values + ")</br>"
        return text

    # Obtenemos de la peticion la direccion URL en el cuerpo
    def request_to_url(self, request):
        body = request.split('\r\n\r\n', 1)[1]
        return body.split('=')[1]

    # Añadimos comienzo a la URL si es necesario
    def process_url(self, url):
        url = unquote(unquote(url))
        if not (url.startswith('http://') or url.startswith('https://')):
            url = "http://" + url
        return url

    # Añadimos entrada al diccionario
    def add_to_dict(self, key, value, dic):
        dic[key] = value
        return dic

    # Generamos respuesta http
    def process_answer(self, head, body):
        answer = "<html><body><h1>" + head + "</h1>"
        answer = answer + body + "</body></html>"
        return answer

    # Añadimos entrada l archivo
    def add_to_file(self, archive, text):
        data = open(archive, "a")
        data.write(text)
        data.close()

    # Procesamos la petición
    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """
        method, resource, request = parsedRequest

        global url_short
        global url_long
        global data
        text = ""
        answer = ""
        code = "200 OK"

        if method == "GET":
            # Solicitud
            if (resource == "/"):
                # Página principal de adiccion de URL
                code = "200 OK"
                text = FORMULARIO + "Actualmente las URLs acortadas son:</br>"
                text += self.dict_to_string(url_short)
                answer = self.process_answer("ACORTADOR URLs", text)
            elif resource in url_short:
                # Redirección a una página del diccionario
                code = "302 Found \r\nLocation:" + url_short[resource]
                answer = self.process_answer("", "")
            else:
                # Recurso no encontrado
                code = "404 NOT FOUND"
                text = "No se ha encontrado el recurso"
                answer = self.process_answer(code, text)
        elif method == "POST":
            # Adiccion
            url = self.request_to_url(request)
            if (url):
                # Compruebo si esta vacio el String
                url = self.process_url(url)
                if not (url in url_long):
                    # Si no está en mi diccionario añado url
                    pos = "/" + str(len(url_short))
                    url_short = self.add_to_dict(pos, url, url_short)
                    url_long = self.add_to_dict(url, pos, url_long)
                    code = "200 OK"
                    text = "<a href=" + url + ">" + url + "</a></br>"
                    text += "<a href=" + pos + ">"
                    text += "http://localhost:1234" + pos + "</a>"
                    answer = self.process_answer("URL guardada", text)
                    self.add_to_file(Text, pos + "," + url + "\n")
                else:
                    # La url ya estaba en el diccionario
                    code = "200 OK"
                    text = "<a href=" + url_long[url] + ">"
                    text += "http://localhost:1234" + url_long[url] + "</a>"
                    answer = self.process_answer("URL repetida", text)
            else:
                # La url esta vacia
                code = "200 OK"
                answer = self.process_answer("Error", "Valor no valido")
        else:
            # Si no es ni post ni get
            code = "404 NOT FOUND"
            answer = self.process_answer(code, "Peticion no encontrada")
        return (code, answer)

if __name__ == "__main__":
    try:

        # Lectura del archivo exterior
        if (os.path.isfile(Text)):
            data = open(Text)
        else:
            data = open(Text, "w")
            data.close()
            data = open(Text)

        urls_code = data.read().split()
        data.close()

        # Creacion de diccionarios
        for url in urls_code:
            key = url.split(",", 1)[0]
            value = url.split(",", 1)[1]
            url_short[key] = value
            url_long[value] = key
    except IndexError:
        print("Error de lectura, pueden faltar datos")
    except:
        sys.exit("Ha ocurrido un ERROR. Reinicie el Server.")

    try:
        testWebApp = practica1("localhost", 1234)
    except KeyboardInterrupt:
        print("\nEl Server ha sido apagado")
    except:
        print("Ha ocurrido un ERROR. Reinicie el Server.")
