import asyncio
from functools import wraps

import click

from philoagents.application.conversation_service.generate_response import (
    get_streaming_response,
)
from philoagents.domain.celeb_factory import CelebFactory


def async_command(f):
    """Decorator to run an async click command."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "--celeb-id",
    type=str,
    required=True,
    help="ID of the celeb to call.",
)
@click.option(
    "--query",
    type=str,
    required=True,
    help="Query to call the agent with.",
)
@async_command
async def main(celeb_id: str, query: str) -> None:
    """CLI command to query a celeb.

    Args:
        celeb_id: ID of the celeb to call.
        query: Query to call the agent with.
    """

    celeb_factory = CelebFactory()
    celeb = celeb_factory.get_celeb(celeb_id)

    print(
        f"\033[32mCalling agent with celeb_id: `{celeb_id}` and query: `{query}`\033[0m"
    )
    print("\033[32mResponse:\033[0m")
    print("\033[32m--------------------------------\033[0m")
    async for chunk in get_streaming_response(
        messages=query,
        celeb_id=celeb_id,
        celeb_name=celeb.name,
        celeb_perspective=celeb.perspective,
        celeb_style=celeb.style,
        celeb_context="",
    ):
        print(f"\033[32m{chunk}\033[0m", end="", flush=True)
    print("\033[32m--------------------------------\033[0m")


if __name__ == "__main__":
    main()
