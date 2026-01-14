
import uvicorn

from focus import SERVER_HOST, SERVER_PORT, LOG_LEVEL
from focus.app import create_app

from focus.routes import init_routes, router


if __name__ == "__main__":
    init_routes()
    app = create_app(mounts=[], routers=[router])
    uvicorn.run(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level=LOG_LEVEL,
    )
