import smtplib
from email.mime.text import MIMEText

# El correo y contraseña de la cuenta emisora
correo = "************************"
password = "**********************"
# La cuenta receptora del mensaje
destino = "+++++++++++++++++++++++"
# El texto y el tema del correo
mensaje = MIMEText("Hola desde Python")
mensaje["Subject"] = "Prueba SSL"
# Conexión al servidor
servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
# Registro con la información de la cuenta emisora
servidor.login(correo, password)
# Envia el mail 
servidor.sendmail(correo, destino, mensaje.as_string())
# Abandona la conexión
servidor.quit()
# Comprueba que se haya enviado correctamente
print("Correo enviado")
