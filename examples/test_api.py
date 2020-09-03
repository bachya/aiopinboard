"""Run an example script to quickly test the guardian."""
import asyncio
import logging

from aiopinboard import API
from aiopinboard.errors import RequestError

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    api = API("<PINBOARD_API_TOKEN>")

    try:
        last_change_dt = await api.async_get_last_change_datetime()
        _LOGGER.info(last_change_dt)
    except RequestError as err:
        _LOGGER.info(err)


asyncio.run(main())
