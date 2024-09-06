from fastapi import FastAPI

from app.domain.response_model import ok_response


def create_app():
    app = FastAPI(title='Soft Chatty API',
                  version='0.1.0',
                  openapi_url='/v1/openapi.json',
                  docs_url='/v1/docs',
                  redoc_url='/v1/redoc',
                  swagger_ui_oauth2_redirect_url='/v1/docs/oauth2-redirect')

    @app.get('/health')
    async def check_health():
        return ok_response

    return app
