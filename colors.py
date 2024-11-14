import dataclasses


color_list = ["OFF", "RD", "GN", "YE", "BL", "MG", "CY", "WH", "OFFi", "RDi", "GNi", "YEi", "BLi", "MGi", "CYi", "WHi"]


@dataclasses.dataclass
class Gradient:
    """Basic color gradient."""

    colors: list[str]
    channel_offset: int
    delay: float

    def __getitem__(self, item: int):
        return color_list.index(self.colors[item % len(self.colors)])


rainbow = Gradient(
    colors=["RD", "YE", "GN", "CY", "BL", "MG"],
    channel_offset=-1,
    delay=0.1,
)

reverse_rainbow = Gradient(
    colors=["RD", "YE", "GN", "CY", "BL", "MG"],
    channel_offset=1,
    delay=0.1,
)
