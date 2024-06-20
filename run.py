from app import create_app, socketio
from app.config import Config

app = create_app(Config)

if __name__ == '__main__':
    socketio.run(app, host='194.31.53.102', debug=True, port=21096)