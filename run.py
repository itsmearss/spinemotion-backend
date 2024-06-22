from app import create_app, socketio
from app.config import Config

app = create_app(Config)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=5000)