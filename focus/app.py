
from pydantic import BaseModel
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles


class Mount(BaseModel):
    path: str
    dpath: str
    name: str


def add_view(app: FastAPI, router: APIRouter) -> None:
    app.include_router(router)


def add_views(app: FastAPI, routers: list[APIRouter]) -> None:
    for route in routers:
        add_view(app, route)


def add_mount(app: FastAPI, path: str, static: StaticFiles, name: str) -> None:
    app.mount(path, static, name=name)


def add_mounts(app: FastAPI, mounts: list[Mount]) -> None:
    for mnt in mounts:
        add_mount(app, mnt.path, StaticFiles(directory=mnt.dpath), mnt.name)


def create_app(mounts: list[Mount], routers: list[APIRouter]) -> FastAPI:
    app = FastAPI()
    add_mounts(app, mounts)
    add_views(app, routers)
    return app
