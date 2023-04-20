from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import yagmail
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"]="./static/images"

@app.route("/")
def inicio():
    return render_template("formulario.html")

@app.route("/enviarCorreo", methods=["POST"])
def envarCorreo():
    try:
        destinatario = request.form["correoDestinatario"]
        remitente = request.form["correoRemitente"]
        asunto = request.form["txtAsunto"]
        textoMensaje = request.form["txtMensaje"]
        
        archivo = request.files["fileAnexo"]
        nombreArchivo = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreArchivo))
        
        correo = yagmail.SMTP("juansebt.0610@gmail.com",
                              open("password.txt").read(),
                              encoding="utf-8")
        
        correo.send(to=destinatario, subject=asunto, contents=textoMensaje, attachments=app.config["UPLOAD_FOLDER"]+"/"+nombreArchivo)
        
        mensaje = f"Correo enviado"
        
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"]+"/"+nombreArchivo))
        
    except Exception as error:
        mensaje = error
    return render_template("formulario.html",mensaje=mensaje)

#iniciar el servidor web
if __name__=='__main__':
    app.run(host="0.0.0.0",port=3000,debug=True)