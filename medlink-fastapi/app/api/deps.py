from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_optional_user, verify_medplum_token
from app.db.redis import get_redis
from app.db.session import get_db


async def get_current_user(payload: dict = Depends(verify_medplum_token)):
    return payload


async def get_optional_current_user(payload: dict | None = Depends(get_optional_user)):
    return payload


SessionDep = Annotated[AsyncSession, Depends(get_db)]
RedisDep = Annotated[object, Depends(get_redis)]
CurrentUserDep = Annotated[dict, Depends(get_current_user)]
OptionalUserDep = Annotated[dict | None, Depends(get_optional_current_user)]
