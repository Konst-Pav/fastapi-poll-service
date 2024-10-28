from typing import Annotated

from core.models import db_helper
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import get_all_polls
from api import crud

from core.schemas.poll import PollCreate, PollRead
from core.schemas.vote import VoteCreate
from core.schemas.poll_result import PollResult

router = APIRouter(
    tags=["Polls"],
)


@router.get("/")
async def get_polls(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    polls = await get_all_polls(session=session)
    return polls


@router.post("/create-poll/", response_model=PollRead)
async def create_poll(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    poll_create: PollCreate,
):
    poll = await crud.create_poll(session=session, poll_create=poll_create)
    return poll


@router.post("/poll/", response_model=VoteCreate)
async def submit_vote(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    vote_create: VoteCreate,
):
    vote = await crud.submit_vote(session=session, vote_create=vote_create)
    return vote


@router.get("/get-result/{poll_id}", response_model=PollResult)
async def get_result(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    poll_id: int,
) -> PollResult:
    result = await crud.get_poll_results(session=session, poll_id=poll_id)
    return result
