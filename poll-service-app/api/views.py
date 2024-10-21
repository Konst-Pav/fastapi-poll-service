from typing import Annotated

from core.models import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import get_all_polls
from api import crud

from core.schemas.poll import PollCreate
from core.schemas.vote import VoteCreate

router = APIRouter(
    tags=["Polls"],
)


@router.get("/")
async def get_polls(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    polls = await get_all_polls(session=session)
    return polls


@router.post("/create-poll/", response_model=PollCreate)
async def create_poll(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    poll_create: PollCreate,
):
    poll = await crud.create_poll(session=session, poll_create=poll_create)
    return poll


@router.post("/poll/")
async def submit_vote(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    vote_create: VoteCreate,
):
    vote = await crud.submit_vote(session=session, vote_create=vote_create)
    return "Voted"
