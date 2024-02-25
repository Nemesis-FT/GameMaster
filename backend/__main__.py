import os

import bcrypt
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, APIKeyHeader
from fastapi_oauth2.claims import Claims
from fastapi_oauth2.security import OAuth2
from starlette.requests import Request

from backend.authentication import AuthMasterOAuth2, oauth, bearer
from backend.crud import quick_retrieve, quick_create
from backend.database import models
from backend.database.db import Session, engine
from fastapi_oauth2.middleware import OAuth2Middleware, Auth, User
from fastapi_oauth2.config import OAuth2Config, OAuth2Client
from fastapi_oauth2.router import router as OAuth2Router

from backend.configuration import setting_required
from backend.errors import *
from backend.handlers import *
from backend.configuration import JWT_KEY, OAUTH2_CLIENT, OAUTH2_SECRET
from backend.routers.api.v1.users.router import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(OAuth2Middleware, config=OAuth2Config(
    allow_http=True,
    jwt_secret=JWT_KEY,
    clients=[
        OAuth2Client(
            backend=AuthMasterOAuth2,
            client_id=OAUTH2_CLIENT,
            client_secret=OAUTH2_SECRET,
            redirect_uri="http://127.0.0.1:8001/login_callback",
            scope=["Profile"],
            claims=Claims(username=lambda u: u.username, email=lambda u: u.email, id=lambda u: u.id)
        )
    ]
))


@app.get("/login_callback")
async def login_callback(request: Request, auth=Depends(oauth), b=Depends(bearer)):
    # Attempt to find user in database, and update its data. If it's the first login for the user, create a new profile.
    with Session(future=True) as db:
        try:
            user = quick_retrieve(db, models.User, ext_id=request.user.id)
            user.username = request.user.username
            db.commit()
        except Exception:
            user = quick_create(db, models.User(ext_id=request.user.id, username=request.user.username))
        finally:
            return {"token": auth,
                    "user": user.username}


# On authmaster, set redirect_uri to http://127.0.0.1:8001/oauth2/AuthMaster/token!

app.add_exception_handler(AcmedeliverException, handle_acme_error)
app.add_exception_handler(sqlalchemy.exc.NoResultFound, handle_sqlalchemy_not_found)
app.add_exception_handler(sqlalchemy.exc.MultipleResultsFound, handle_sqlalchemy_multiple_results)

app.include_router(OAuth2Router)
app.include_router(user_router)

if __name__ == "__main__":
    # Configurazione dati collegamento
    BIND_IP = setting_required("BIND_IP")
    BIND_PORT = setting_required("BIND_PORT")
    # Avvia il server uvicorn
    uvicorn.run(app, host=BIND_IP, port=int(BIND_PORT), debug=True)
