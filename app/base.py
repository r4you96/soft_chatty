import socketio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import config
from app.core.mongo import mongo
from app.router import channel_router, messaging_user_router
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

    app.include_router(router=channel_router.router,
                       prefix='/v1/channels',
                       tags=['Channel'])

    app.include_router(router=messaging_user_router.router,
                       prefix='/v1/messaging_users',
                       tags=['MessagingUser'])

    @app.get('/health')
    async def check_health():
        return ok_response

    @app.on_event("startup")
    async def handle_startup():
        await mongo.connect()

    @app.on_event("shutdown")
    async def handle_shutdown():
        await mongo.close()

    socket_app = socketio.ASGIApp(socketio_server=server_sio,
                                  other_asgi_app=app)
    handle_socket_server_events()
    return socket_app
