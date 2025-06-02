# run.py
from app import create_app

app = create_app()

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True) #VALOR 0.0.0.0 PORQUE SE ESTABLECE EN LA IP QUE SE ESTE UTILIZANDO EL SERVIDOR, PUERTO 5000 PORQUE ES EL PUERTO POR DEFECTO DE FLASK

