
import time

from sqlalchemy import true

from src import create_app

#from src import run

app = create_app()

# #only when you run the main.py script directly, will __name =='main'
# if __name__ == '__main__':
#     app.run(debug = True)

# def run():
#     app = create_app()

#     bool = True

#     if bool:
#         app.run(debug = True)


#run()