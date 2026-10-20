"""Data model for one scraped product."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    name: Optional[str]
    price: Optional[str]
    description: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
