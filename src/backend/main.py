from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.backend.routers import conversation_agent, optimization, research_agent


def create_app() -> FastAPI:
    app = FastAPI(
        title="Make Money AI",
        version="0.0.1",
        description="AI for making finance portfolio",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # TODO: This should be actual frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok"}
    
    app.include_router(conversation_agent.router)
    app.include_router(optimization.router)
    app.include_router(research_agent.router)

    return app

app = create_app()