import uvicorn
from app import app
from app.utils.config import Config

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    )
