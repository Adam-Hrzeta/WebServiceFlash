from werkzeug.security import generate_password_hash

# Cambia "1234" por la contraseña que desees
password_plana = "fostin1234?"
password_segura = generate_password_hash(password_plana)
print("Contraseña encriptada:", password_segura)
