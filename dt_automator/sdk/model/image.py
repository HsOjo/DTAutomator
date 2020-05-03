from io import BytesIO
from typing import List

from PIL.Image import new as img_new, Image

from dt_automator.base.model import BaseModel
from dt_automator.maker.model import MakerFeatureModel
from dt_automator.utils import list_math


class ImageModel(BaseModel):
    def __init__(self):
        self.w = 0
        self.h = 0
        self.pxs = []  # type: List[int]

    def load_image(self, img: Image, x=0, y=0, w=None, h=None):
        if w is None:
            w = img.width - x
        if h is None:
            h = img.height - y

        pxs = []
        for py in range(h):
            py = y + py
            for px in range(w):
                px = x + px
                pixel = img.getpixel((px, py))  # type: List[int]
                for v in pixel:
                    pxs.append(v)

        self.pxs, self.w, self.h = pxs, w, h

    def dump_image(self, x=0, y=0, w=None, h=None, hook_pixel=None, hook_save=None, format='png'):
        if w is None:
            w = self.w
        if h is None:
            h = self.h
        if w <= 0 or h <= 0:
            return None

        img = img_new('RGBA', (w, h))
        for oy in range(h):
            for ox in range(w):
                pixel = self.pixel(x + ox, y + oy)
                if hook_pixel is not None:
                    pixel = hook_pixel(pixel)
                img.putpixel((ox, oy), pixel)
        if hook_save is not None:
            img = hook_save(img)
        with BytesIO() as io:
            img.save(io, format)
            io.seek(0)
            data = io.read()
        return data

    def dump_text_image(self, color=None, rect=None, px_distance=0, text_border=2, separate_chars=False):
        if color is None:
            color = self.most_acc_text_color
        if isinstance(color, list):
            color = tuple(color)
        if rect is None:
            rect = self.text_rect(color, px_distance, text_border)

        def hook_pixel(c):
            if c == color or (px_distance > 0 and sum(list_math.abs_(list_math.reduce(c, color))) < px_distance):
                return 0, 0, 0, 255
            else:
                return 255, 255, 255, 255

        def hook_save(img: Image):
            w, h = img.width, img.height
            img = img.convert('1')

            if separate_chars:
                sx, ex = -1, -1
                chrs_rect = []  # type: List[tuple]
                for x in range(w):
                    for y in range(h):
                        if img.getpixel((x, y)) == 0 and x != w - 1:
                            if sx == -1:
                                sx = x
                            break
                        elif (y == h - 1 or x == w - 1) and ex == -1 and sx != -1:
                            ex = x
                            chrs_rect.append((sx, 0, ex - sx, h))
                            sx, ex = -1, -1
                            break
                sum_w = sum([rect[2] for rect in chrs_rect])
                chrs_num = len(chrs_rect)
                if chrs_num >= 2:
                    avg_w = sum_w / chrs_num
                    for i in range(chrs_num - 1, 0, -1):
                        px, py, pw, ph = chrs_rect[i]
                        x, y, w, h = chrs_rect[i - 1]
                        if px - x - w >= avg_w * 0.5:
                            chrs_rect.insert(i, (None, None, avg_w * 0.5, None))

                sum_w = sum([rect[2] for rect in chrs_rect])
                avg_w = sum_w / chrs_num
                chr_distance = avg_w * 0.8
                new_img = img_new('1', (int(sum_w * 2 + chr_distance * (chrs_num - 1)), int(h * 2)), 255)
                ox = 0
                for chr_rect in chrs_rect:
                    if chr_rect[0] is None:
                        ox += chr_rect[2] + chr_distance
                        continue

                    x, y, w, h = chr_rect
                    new_img.paste(img.crop((x, y, x + w, y + h)), (int(sum_w * 0.5 + ox), int(h * 0.5)))
                    ox += w + chr_distance
            else:
                new_img = img_new('1', (w * 2, h * 2), 255)
                new_img.paste(img, (int(w * 0.5), int(h * 0.5)))

            return new_img

        return self.dump_image(*rect, hook_pixel=hook_pixel, hook_save=hook_save, format='png')

    def pixel(self, x, y):
        index = (y * self.w + x) * 4
        [r, g, b, a] = self.pxs[index:index + 4]
        return r, g, b, a

    def compare(self, img: Image, mode, x=0, y=0, w=None, h=None, detect_weight=MakerFeatureModel.DETECT_WEIGHT_MAX):
        d_value = 0
        d_value_max = 0
        dw = MakerFeatureModel.DETECT_WEIGHT_MAX + 1 - detect_weight
        pixel_d_max = 255 * 4
        for py in range(h):
            if py % dw == 0:
                oy = y + py
                for px in range(w):
                    if px % dw == 0:
                        ox = x + px
                        if 0 <= ox < img.width and 0 <= oy < img.height:
                            pixel = img.getpixel((ox, oy))
                        else:
                            pixel = None
                        pixel_self = self.pixel(px, py)
                        if mode == MakerFeatureModel.MODE_DIFFERENCE:
                            d_value_max += 1
                            if pixel is not None:
                                for i in range(4):
                                    if pixel[i] != pixel_self[i]:
                                        d_value += 1
                                        break
                            else:
                                d_value += 1
                        elif mode == MakerFeatureModel.MODE_DISTANCE:
                            d_value_max += 1
                            if pixel is not None:
                                d_values = list_math.reduce(pixel, pixel_self)
                                d_values = list_math.abs_(d_values)
                                d_value += sum(d_values) / pixel_d_max
                            else:
                                d_value += 1

        if d_value_max == 0:
            return 0, 0

        return d_value, d_value_max

    @property
    def most_acc_text_color(self):
        colors = []
        colors_count = {}
        colors_diff = {}
        colors_border = {}

        for y in range(self.h):
            for x in range(self.w):
                c = self.pixel(x, y)
                if x == 0 or x == self.w - 1 or y == 0 or y == self.h - 1:
                    if c in colors_border:
                        colors_border[c] += 1
                    else:
                        colors_border[c] = 0
                if c in colors_count:
                    colors_count[c] += 1
                else:
                    colors.append(c)
                    colors_count[c] = 0
                    colors_diff[c] = 0
        colors_count_sorted = [color for color, _ in sorted(colors_count.items(), key=lambda x: x[1], reverse=True)]
        for color in colors_count_sorted[:10]:
            for color_compare in colors:
                if color == color_compare or (
                        color in colors_border and colors_border[color] > (self.w + self.h) * 1.5):
                    continue
                colors_diff[color] += sum(list_math.reduce(color, color_compare))
        colors_diff_sorted = [color for color, _ in sorted(colors_diff.items(), key=lambda x: x[1], reverse=True)]
        colors = sorted(colors, key=lambda x: colors_count_sorted.index(x) + colors_diff_sorted.index(x))
        return colors[0]

    def text_rect(self, color=None, px_distance=0, text_border=2):
        if color is None:
            color = self.most_acc_text_color
        if isinstance(color, list):
            color = tuple(color)
        l, b = self.w, 0
        r, t = 0, self.h
        for y in range(self.h):
            for x in range(self.w):
                c = self.pixel(x, y)
                if c == color or (px_distance > 0 and sum(list_math.abs_(list_math.reduce(c, color))) < px_distance):
                    if x < l:
                        l = x
                    if x > r:
                        r = x
                    if y < t:
                        t = y
                    if y > b:
                        b = y
        result = [l, t, r - l, b - t]
        if text_border > 0:
            result = list_math.add(result, [-text_border, -text_border, text_border * 2, text_border * 2])
        return result
