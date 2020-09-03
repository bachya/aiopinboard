"""Run an example script to quickly test the guardian."""
import asyncio
import logging

from aiopinboard import Client
from aiopinboard.errors import GuardianError

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    async with Client("172.16.11.208") as guardian:
        try:
            wifi_status_response = await guardian.wifi.status()
            _LOGGER.info("wifi_status command response: %s", wifi_status_response)

            # wifi_reset_response = await guardian.wifi.reset()
            # _LOGGER.info("wifi_reset command response: %s", wifi_reset_response)

            # wifi_configure_response = await guardian.wifi.configure(
            #     "<SSID>", "<PASSWORD>"
            # )
            # _LOGGER.info("wifi_configure command response: %s", wifi_configure_response)

            # wifi_enable_ap_response = await guardian.wifi.enable_ap()
            # _LOGGER.info("wifi_enable_ap command response: %s", wifi_enable_ap_response)

            # wifi_disable_ap_response = await guardian.wifi.disable_ap()
            # _LOGGER.info(
            #     "wifi_disable_ap command response: %s", wifi_disable_ap_response
            # )
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
