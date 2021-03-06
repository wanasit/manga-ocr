from comic_ocr import Rectangle
from comic_ocr.models.localization.localization_utils import divine_rect_into_overlapping_tiles, align_line_horizontal
from comic_ocr.typing import Size


def test_align_line_horizontal_on_good_align():
    x = Rectangle.of_size(size=(55, 15), at=(520, 690))
    y = Rectangle.of_size(size=(12, 15), at=(580, 690))
    assert align_line_horizontal(x, y)
    assert align_line_horizontal(y, x)


def test_align_line_horizontal_on_overlap_horizontal():
    x = Rectangle.of_size(size=(61, 15), at=(521, 690))
    y = Rectangle.of_size(size=(12, 16), at=(580, 689))
    assert align_line_horizontal(x, y)
    assert align_line_horizontal(y, x)


def test_divine_rect_into_overlapping_tiles():
    tiles = divine_rect_into_overlapping_tiles(
        rect=Size.of(100, 100), tile_size=Size.of(50, 50), min_overlap_x=10, min_overlap_y=10)

    assert list(tiles) == [
        Rectangle.of_size((50, 50), at=(0, 0)),
        Rectangle.of_size((50, 50), at=(25, 0)),
        Rectangle.of_size((50, 50), at=(50, 0)),
        Rectangle.of_size((50, 50), at=(0, 25)),
        Rectangle.of_size((50, 50), at=(25, 25)),
        Rectangle.of_size((50, 50), at=(50, 25)),
        Rectangle.of_size((50, 50), at=(0, 50)),
        Rectangle.of_size((50, 50), at=(25, 50)),
        Rectangle.of_size((50, 50), at=(50, 50)),
    ]


def test_divine_rect_into_overlapping_tiles_large():
    tiles = divine_rect_into_overlapping_tiles(
        rect=Size.of(100, 100), tile_size=Size.of(100, 100), min_overlap_x=10, min_overlap_y=10)
    assert list(tiles) == [Rectangle.of_size((100, 100))]

    tiles = divine_rect_into_overlapping_tiles(
        rect=Size.of(100, 100), tile_size=Size.of(120, 120), min_overlap_x=10, min_overlap_y=10)
    assert list(tiles) == [Rectangle.of_size((120, 120), at=(0, 0))]


def test_divine_rect_into_overlapping_tiles_real_cases():
    tiles = divine_rect_into_overlapping_tiles(
        rect=Size.of(750, 1000), tile_size=Size.of(750, 750), min_overlap_x=750 // 4, min_overlap_y=750 // 4)
    assert list(tiles) == [(0, 0, 750, 750), (0, 250, 750, 1000)]

    tiles = divine_rect_into_overlapping_tiles(
        rect=Size.of(750, 1500), tile_size=Size.of(750, 750), min_overlap_x=750 // 4, min_overlap_y=750 // 4)
    assert list(tiles) == [(0, 0, 750, 750), (0, 375, 750, 1125), (0, 750, 750, 1500)]
