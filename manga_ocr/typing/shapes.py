from __future__ import annotations

from typing import Tuple, Union, List


class Point(tuple):
    """
    A tuple of [x, y] with helper functions
    """

    def __new__(cls, point: Tuple[int, int]):
        return tuple.__new__(Point, point)

    @staticmethod
    def of(x: int, y: int) -> Point:
        return Point((x, y))

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[0]


class Size(tuple):
    """
    A tuple of [w, h] with helper functions
    """

    def __new__(cls, size: Tuple[int, int]):
        return tuple.__new__(Size, size)

    @staticmethod
    def of(w: int, h: int) -> Size:
        return Size((w, h))

    @property
    def width(self) -> int:
        return self[0]

    @property
    def height(self) -> int:
        return self[1]


class Rectangle(tuple):
    """
    A tuple of [x0, y0, x1, y1] with helper functions to manipulate the shape.
    It is compatible with Pillow function that require rectangle or box.
    e.g. draw.rectangle(rect) or image.crop(rect)
    """

    def __new__(cls, rect: RectangleLike):
        return tuple.__new__(Rectangle, rect)

    @staticmethod
    def of_xywh(x: int, y: int, w: int, h: int) -> Rectangle:
        return Rectangle([x, y, x + w, y + h])

    @staticmethod
    def of_size(size: Tuple[int, int], at: Tuple[int, int] = (0, 0)) -> Rectangle:
        return Rectangle([at[0], at[1], at[0] + size[0], at[1] + size[1]])

    @staticmethod
    def of_tl_br(tl: Tuple[int, int], br: Tuple[int, int] = (0, 0)) -> Rectangle:
        return Rectangle([tl[0], tl[1], br[0], br[1]])

    @property
    def box(self) -> Tuple[int, int, int, int]:
        return self.left, self.top, self.right, self.bottom

    @property
    def left(self) -> int:
        return self[0]

    @property
    def top(self) -> int:
        return self[1]

    @property
    def right(self) -> int:
        return self[2]

    @property
    def bottom(self) -> int:
        return self[3]

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def size(self) -> Size:
        return Size((self.width, self.height))

    @property
    def center(self) -> Point:
        return Point(((self.left + self.right) // 2, (self.top + self.bottom) // 2))

    @property
    def tl(self) -> Point:
        return Point((self[0], self[1]))

    @property
    def br(self) -> Point:
        return Point((self[2], self[3]))

    def expand(self, unit: Union[int, Tuple]) -> Rectangle:
        unit_x = unit if isinstance(unit, int) else unit[0]
        unit_y = unit if isinstance(unit, int) else unit[1]
        return Rectangle((self[0] - unit_x, self[1] - unit_y, self[2] + unit_x, self[3] + unit_y))

    def is_overlap(self, rect: RectangleLike) -> bool:
        overlap_x = self.left < rect[0] < self.right or \
                    rect[0] < self.left < rect[2]
        overlap_y = self.top < rect[1] < self.bottom or \
                    rect[1] < self.top < rect[3]
        return overlap_x and overlap_y

    def __contains__(self, item):
        if isinstance(item, tuple) or isinstance(item, list):

            if len(item) == 2:  # rect contains point
                x, y = item
                return (self.left <= x <= self.right) and (self.top <= y <= self.bottom)

            if len(item) == 4:  # rect contains rect
                x1, y1, x2, y2 = item
                return (self.left <= x1 <= x2 <= self.right) and (self.top <= y1 <= y2 <= self.bottom)

        return tuple.__contains__(self, item)


RectangleLike = Union[
    Tuple[int, int, int, int],
    List[int],
    Rectangle
]
