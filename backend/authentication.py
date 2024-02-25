"""
Questo modulo contiene utility di autenticazione.
"""
from fastapi import Depends
from fastapi.security import APIKeyHeader
from fastapi_oauth2.security import OAuth2
from social_core.backends.oauth import BaseOAuth2
from starlette.requests import Request

from backend.configuration import API_URL, AUTH_URL, TOKEN_URL
from backend.crud import quick_retrieve, quick_create
from backend.database import models
from backend.database.db import Session
from backend.dependencies import dep_dbsession


class AuthMasterOAuth2(BaseOAuth2):
    name = "AuthMaster"
    API_URL = API_URL
    AUTHORIZATION_URL = AUTH_URL
    ACCESS_TOKEN_URL = TOKEN_URL
    ACCESS_TOKEN_METHOD = "POST"
    REDIRECT_STATE = False
    DEFAULT_SCOPE = ["Profile"]
    EXTRA_DATA = [
        ("id", "id"),
        ("expires_in", "expires"),
        ("refresh_token", "refresh_token"),
    ]

    def api_url(self, path):
        api_url = self.setting("API_URL") or self.API_URL
        return "{}{}".format(api_url.rstrip("/"), path)

    def authorization_url(self):
        return self.api_url("/oauth/authorize")

    def access_token_url(self):
        return self.api_url("/oauth/token")

    def get_user_details(self, response):
        """Return user details from GitLab account"""
        return {
            "username": response.get("username") or "",
            "id": response.get("id"),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            self.api_url("/api/me"), headers={"Authorization": "Bearer " + access_token}
        )


oauth = OAuth2()
bearer = APIKeyHeader(name='Authorization', scheme_name='authorization')


def get_current_user(request: Request,  db: Session = Depends(dep_dbsession), auth=Depends(oauth), b=Depends(bearer)):
    try:
        user = quick_retrieve(db, models.User, ext_id=request.user.id)
        user.username = request.user.username
        db.commit()
    except Exception:
        user = quick_create(db, models.User(ext_id=request.user.id, username=request.user.username))
    finally:
        return user.id
