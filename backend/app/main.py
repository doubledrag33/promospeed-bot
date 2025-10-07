from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api import auth, catalog, cart, favorites, optimize, pandr, admin, merchant
from app.core.config import get_settings

settings = get_settings()

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.rate_limit_per_minute}/minute"])

app = FastAPI(title="Gropt API", version="0.1.0")

app.state.limiter = limiter
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(catalog.router, prefix="/api", tags=["catalog"])
app.include_router(cart.router, prefix="/api", tags=["cart"])
app.include_router(favorites.router, prefix="/api", tags=["favorites"])
app.include_router(optimize.router, prefix="/api", tags=["optimize"])
app.include_router(pandr.router, prefix="/api", tags=["pandr"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(merchant.router, prefix="/api/merchant", tags=["merchant"])


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
