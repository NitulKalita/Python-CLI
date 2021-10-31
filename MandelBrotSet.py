from PIL import Image
from tqdm import tqdm
import math


W, H = 200, 200
ITER = 255
FRAMES = 100


def get_palette(max_iter):
    palette = [
        (
            int(255 * math.sin(i / 50.0 + 1.0) ** 2),
            int(255 * math.sin(i / 50.0 + 0.5) ** 2),
            int(255 * math.sin(i / 50.0 + 1.7) ** 2)
        ) for i in range(max_iter - 1)
    ]
    palette.append((0, 0, 0))
    return palette


def mandelbrot(w, h, palette, x1=-2, y1=-1, x2=1, y2=1):
    img = Image.new('RGB', (w, h))

    dx = x2 - x1
    dy = y2 - y1
    iters = len(palette)

    n = 0
    for px in range(w):
        for py in range(h):
            x = px / w * dx + x1
            y = py / h * dy + y1
            c = x + 1j * y
            z = 0j
            for n in range(iters):
                z = z ** 2 + c
                if (z * z.conjugate()).real > 4.0:
                    break
            img.putpixel((px, py), palette[n])
    return img


def main():
    x, y, r = 0, 0, 5
    x_tar, y_tar, r_tar = -0.74529, 0.113075, 1.5e-6

    palette = get_palette(ITER)

    frames = []
    for _ in tqdm(range(FRAMES)):
        frames.append(mandelbrot(W, H, palette, x - r, y - r, x + r, y + r))
        x += (x_tar - x) * 0.1
        y += (y_tar - y) * 0.1
        r += (r_tar - r) * 0.1

    frames[0].save('mandelbrot.gif', save_all=True, append_images=frames[1:], duration=60, loop=0)


if __name__ == '__main__':
    main()