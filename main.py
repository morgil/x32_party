import asyncio
import math
import time

from behringer_mixer import mixer_api

import color_interface
import colors


async def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--address",
        default="192.168.208.99",
        help="name/ip-address of Behringer X32 mixing desk",
        required=True,
    )

    args = parser.parse_args()

    mixer = mixer_api.create(
        "X32",
        ip=args.address,
        #  logLevel=logging.DEBUG,
    )

    await mixer.start()
    await mixer.reload()
    state = mixer.state()

    while (time.time() - mixer.last_received()) < 1:
        await asyncio.sleep(0.1)
    print(state)

    await mixer.set_value("/-stat/chfaderbank", 0)
    await mixer.set_value("/-stat/grpfaderbank", 5)

    faders = [f"/ch/{x+1}" for x in range(16)] + ["/main/st"]

    color_backup = {fader: state[f"{fader}/config_color"] for fader in faders}

    gradient = colors.rainbow

    step = 0

    try:
        while True:
            await asyncio.gather(
                *[
                    color_interface.set_color(
                        mixer,
                        faders[i],
                        gradient[step + i * gradient.channel_offset],
                    )
                    for i in range(len(faders))
                ]
                + [
                    mixer.set_value(
                        f"{faders[i]}/mix_fader",
                        round(math.sin((step + i * gradient.channel_offset) / 3) / 2 + 0.5, 2),
                    )
                    for i in range(len(faders))
                ]
                + [asyncio.sleep(gradient.delay)]
            )
            # print(mixer.state())
            step += 1
            print(".", end="")
            if step % 20 == 0:
                print()

    finally:
        await color_interface.set_colors(mixer, color_backup)
        await mixer.stop()


if __name__ == "__main__":
    asyncio.run(main())
