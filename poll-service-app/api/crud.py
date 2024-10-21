from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Poll, Option
from core.schemas.poll import PollCreate
from core.schemas.vote import VoteCreate

from fastapi import HTTPException, status


async def get_all_polls(session: AsyncSession) -> Sequence[Poll]:
    stmt = select(Poll).order_by(Poll.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_poll(
    session: AsyncSession,
    poll_create: PollCreate,
):
    poll_data = poll_create.model_dump()
    poll = Poll(title=poll_data["title"], description=poll_data.get("description"))
    options = [Option(**option) for option in poll_data["options"]]
    poll.options.extend(options)
    session.add(poll)
    await session.commit()
    await session.refresh(poll)
    return poll


async def return_poll(session: AsyncSession) -> Poll:
    stmt = select(Poll).where(Poll.id == 4)
    poll_result = await session.scalars(stmt)
    poll = poll_result.one()
    return poll


def submit_vote(session: AsyncSession, vote_create: VoteCreate):
    return None
