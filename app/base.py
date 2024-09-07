import socketio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import config
from app.socket.base import server_sio
from app.domain.response_model import ok_response
from app.socket.socket_event_handler import handle_socket_server_events


def create_app():
    app = FastAPI(title=f'{config.app_name} API',
                  version='0.1.0',
                  openapi_url='/v1/openapi.json',
                  docs_url='/v1/docs',
                  redoc_url='/v1/redoc',
                  swagger_ui_oauth2_redirect_url='/v1/docs/oauth2-redirect')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 모든 도메인 허용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get('/health')
    async def check_health():
        return ok_response

    socket_app = socketio.ASGIApp(socketio_server=server_sio,
                                  other_asgi_app=app)
    handle_socket_server_events()
    return socket_app
