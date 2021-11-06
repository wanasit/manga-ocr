from dataclasses import dataclass, field
from typing import List, Optional

from PIL import Image, ImageDraw, ImageFont

from manga_ocr.generator.manga_generator import TextArea
from manga_ocr.types import Rectangle
from manga_ocr.types.images import Color, Drawable, to_draw


@dataclass
class TextBubble(TextArea):
    bubble_padding: int = field(default=3, repr=False)
    bubble_fill_color: Color = field(default='#ffffff', repr=False)
    bubble_outline_width: int = field(default=1, repr=False)
    bubble_outline_color: Color = field(default='#000000', repr=False)

    def draw_background(self, image: Drawable):
        draw = to_draw(image)
        inner_rect = self.get_text_rect()
        outer_rect = inner_rect.expand(self.bubble_outline_width + self.bubble_padding)
        draw.ellipse(
            _ellipse_bounding_box(outer_rect),
            fill=self.bubble_fill_color,
            outline=self.bubble_outline_color,
            width=self.bubble_outline_width
        )


def _ellipse_bounding_box(inner_rect: Rectangle):
    inner_tl, inner_br = inner_rect.tl, inner_rect.br
    inner_w, inner_h = inner_br[0] - inner_tl[0], inner_br[1] - inner_tl[1]
    diff_x, diff_y = (2 ** 0.5 - 1) * inner_w / 2, (2 ** 0.5 - 1) * inner_h / 2
    return (inner_tl[0] - diff_x, inner_tl[1] - diff_y), (inner_br[0] + diff_x, inner_br[1] + diff_y)
