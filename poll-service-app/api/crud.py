from typing import Sequence

from sqlalchemy import select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Poll, Option, Vote
from core.schemas.poll import PollCreate
from core.schemas.vote import VoteCreate
from core.schemas.poll_result import PollResult, ChoiceResult

from fastapi import HTTPException


async def get_all_polls(session: AsyncSession) -> Sequence[Poll]:
    """
    Asynchronously retrieves all polls from the database.

    This function executes a SELECT statement to fetch all instances of the
    Poll model, ordered by their ID. It returns a sequence of Poll objects.

    Parameters:
    session (AsyncSession): The database session used to execute the query.

    Returns:
    Sequence[Poll]: A sequence containing all Poll objects retrieved from the database.
    """
    stmt = select(Poll).order_by(Poll.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_poll(
    session: AsyncSession,
    poll_create: PollCreate,
):
    """
    Asynchronously creates a new poll in the database.

    This function takes a PollCreate object, extracts the necessary data,
    and constructs a Poll instance along with its associated options.
    The poll is then added to the session, committed to the database,
    and refreshed to ensure it has the latest state.

    Parameters:
    session (AsyncSession): The database session used to execute the transaction.
    poll_create (PollCreate): An object containing the data needed to create the poll,
                              including title, description, and options.

    Returns:
    Poll: The newly created Poll object with its options.
    """
    poll_data = poll_create.model_dump()
    poll = Poll(title=poll_data["title"], description=poll_data.get("description"))
    options = [Option(**option) for option in poll_data["options"]]
    poll.options.extend(options)
    session.add(poll)
    await session.commit()
    await session.refresh(poll)
    return poll


async def submit_vote(
    session: AsyncSession,
    vote_create: VoteCreate,
) -> Vote:
    """
    Asynchronously submits a new vote to the database.

    This function takes a VoteCreate object(poll_id, choice_id),
    checks for a poll and a response option, and creates an entry in the database.

    Parameters:
    session (AsyncSession): The database session used to execute the transaction.
    vote_create (VoteCreate(poll_id, choice_id)): An object containing the data needed to create the vote.

    Returns:
    Vote: The newly created Vote object.
    """
    poll_id = vote_create.poll_id
    await poll_id_exists_check(session, poll_id)

    choice_id = vote_create.choice_id
    await option_id_exists_check(session, choice_id)

    vote = Vote(poll_id=poll_id, choice_id=choice_id)
    session.add(vote)
    await session.commit()
    await session.refresh(vote)
    return vote


async def get_poll_results(
    session: AsyncSession,
    poll_id: int,
):
    """
    Asynchronously retrieves the results of a specific poll.

    This function executes a query to count the number of votes for each option
    in the specified poll. It returns a PollResult object containing the poll ID
    and a list of ChoiceResult objects, each representing the vote count for an option.

    Parameters:
    session (AsyncSession): The database session used to execute the query.
    poll_id (int): The ID of the poll for which to retrieve the results.

    Returns:
    PollResult: An object containing the poll ID and a list of choice results,
                each including the option ID and the corresponding vote count.
    """
    await poll_id_exists_check(session, poll_id)
    stmt = (
        select(
            Option.id.label("option_id"), func.count(Vote.choice_id).label("vote_count")
        )
        .join(
            Vote,
            Vote.choice_id == Option.id,
            isouter=True,
        )
        .filter(Option.poll_id == poll_id)
        .group_by(Option.id)
        .order_by(Option.id)
    )
    result = await session.execute(stmt)
    choice_results = [
        ChoiceResult(option_id=option_id, vote_count=vote_count)
        for option_id, vote_count in result.all()
    ]
    poll_result = PollResult(poll_id=poll_id, result=choice_results)
    return poll_result


async def poll_id_exists_check(session: AsyncSession, poll_id: int):
    """Checks if a poll exists by its ID."""
    poll_exists = await session.execute(select(exists().where(Poll.id == poll_id)))
    if not poll_exists.scalar():
        raise HTTPException(status_code=404, detail="Poll not found")


async def option_id_exists_check(session: AsyncSession, option_id: int):
    """Checks if an option exists by its ID."""
    option_exists = await session.execute(
        select(exists().where(Option.id == option_id))
    )
    if not option_exists.scalar():
        raise HTTPException(status_code=404, detail="Option not found")
