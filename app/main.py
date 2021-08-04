from dataclasses import asdict

import uvicorn
from fastapi import FastAPI

from app.database.conn import mongo
from app.common.config import conf
from app.routes import index, provider, user, inventory

def create_app():
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    mongo.init_app(app, **conf_dict)
    app.include_router(index.router)
    app.include_router(provider.router)
    app.include_router(user.router)
    app.include_router(inventory.router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=conf().PROJ_RELOAD)