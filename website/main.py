
import time

from website import create_app



app = create_app()

#only when you run the main.py script directly, will __name =='main'
if __name__ == '__main__':
    app.run(debug = True)