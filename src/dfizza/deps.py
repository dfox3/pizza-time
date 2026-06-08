from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.db_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
