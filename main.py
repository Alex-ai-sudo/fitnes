from app import create_app
from app.database import global_init
from Config import Config

app = create_app()

if __name__ == '__main__':
    global_init(Config.DB)
    app.run(port=Config.PORT, debug=Config.DEBUG)