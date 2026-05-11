from __future__ import annotations

import jwt
import httpx
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

security = HTTPBearer(auto_error=True)
optional_security = HTTPBearer(auto_error=False)


async def fetch_jwks() -> dict | None:
    jwks_url = f"{settings.MEDPLUM_BASE_URL}/oauth2/jwks"
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(jwks_url)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def _decode_with_local_secret(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
        options={"require": ["sub"]},
    )


def _build_user_context(payload: dict) -> dict:
    roles = payload.get("roles") or payload.get("role") or []
    if isinstance(roles, str):
        roles = [roles]
    return {
        "sub": payload["sub"],
        "roles": roles,
        "scope": payload.get("scope", ""),
        "profile": payload.get("profile"),
        "raw": payload,
    }


async def verify_medplum_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    token = credentials.credentials

    try:
        payload = _decode_with_local_secret(token)
        return _build_user_context(payload)
    except jwt.InvalidTokenError:
        pass

    jwks = await fetch_jwks()
    if not jwks:
        raise HTTPException(status_code=401, detail="Unable to verify token")

    try:
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = next(
            (
                {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                for key in jwks.get("keys", [])
                if key["kid"] == unverified_header["kid"]
            ),
            None,
        )
        if not rsa_key:
            raise HTTPException(status_code=401, detail="Signing key not found")
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key)
        options = {"verify_aud": bool(settings.MEDPLUM_CLIENT_ID)}
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.MEDPLUM_CLIENT_ID or None,
            options=options,
        )
        return _build_user_context(payload)
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Security(optional_security),
) -> dict | None:
    if credentials is None:
        return None
    return await verify_medplum_token(credentials)


def require_roles(*expected_roles: str):
    async def checker(user: dict = Security(verify_medplum_token)) -> dict:
        if not set(user.get("roles", [])) & set(expected_roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return checker
