from behringer_mixer.mixer_types import MixerTypeBase


colored_entities = {
    "ch": [x for x in range(1, 32)],
    "auxin": [x for x in range(1, 8)],
    "fxrtn": [x for x in range(1, 8)],
    "bus": [x for x in range(1, 16)],
    "mtx": [x for x in range(1, 6)],
    "dca": [x for x in range(1, 8)],
    "main": ["st", "m"],
}


async def set_color(x32: MixerTypeBase, channel: str, color: int) -> None:
    """Set a specific color."""
    await x32.set_value(f"{channel}/config_color", color)


async def set_colors(x32: MixerTypeBase, channel_colors: dict[str, int]) -> None:
    """Set a lot of colors."""
    for channel, color in channel_colors.items():
        await set_color(x32, channel, color)
