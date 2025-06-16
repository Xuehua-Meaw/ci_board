from dataclasses import dataclass
from typing import Any, Union

@dataclass
class BMPData:
    success: bool
    data: Union[bytes, Any]
    size: tuple[int, int]
    bit_count: int
    timestamp: str