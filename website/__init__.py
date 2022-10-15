import time

from sqlalchemy import true

from website import create_app



def run():
    app = create_app()

    bool = True

    if bool:
        app.run(debug = True)

run()