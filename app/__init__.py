from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.index import router as api_router
from app.utils.config import Config

def create_app() -> FastAPI:
    app = FastAPI(title="Akash Network API Proxy")
    
    # 配置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(api_router)
    
    return app

app = create_app()
