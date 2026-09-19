from dataclasses import dataclass


@dataclass
class Scene:

    duration: float

    text: str

    background: tuple = (
        10,
        10,
        20
    )

    font_size: int = 80