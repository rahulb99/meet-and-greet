import json
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


class CelebExtract(BaseModel):
    """A class representing raw celeb data extracted from external sources.

    This class follows the structure of the celebs.json file and contains
    basic information about celebs before enrichment.

    Args:
        id (str): Unique identifier for the celeb.
        urls (List[str]): List of URLs with information about the celeb.
    """

    id: str = Field(description="Unique identifier for the celeb")
    urls: List[str] = Field(
        description="List of URLs with information about the celeb"
    )

    @classmethod
    def from_json(cls, metadata_file: Path) -> list["CelebExtract"]:
        with open(metadata_file, "r") as f:
            celebs_data = json.load(f)

        return [cls(**celeb) for celeb in celebs_data]


class Celeb(BaseModel):
    """A class representing a celeb agent with memory capabilities.

    Args:
        id (str): Unique identifier for the celeb.
        name (str): Name of the celeb.
        perspective (str): Description of the celeb's theoretical views
            about AI.
        style (str): Description of the celeb's talking style.
    """

    id: str = Field(description="Unique identifier for the celeb")
    name: str = Field(description="Name of the celeb")
    perspective: str = Field(
        description="Description of the celeb's theoretical views about AI"
    )
    style: str = Field(description="Description of the celeb's talking style")

    def __str__(self) -> str:
        return f"Celeb(id={self.id}, name={self.name}, perspective={self.perspective}, style={self.style})"
