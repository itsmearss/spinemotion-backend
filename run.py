from app import create_app, socketio
from app.config import Config
import subprocess

app = create_app(Config)

if __name__ == '__main__':
    subprocess.Popen(["streamlit", "run", "streamlit.py"])
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)