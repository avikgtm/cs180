import time

import numpy as np
from scipy.signal import convolve2d
from skimage import io, img_as_float, img_as_ubyte

### Part 1.1: Convolutions from Scratch

BOX_9 = np.ones((9, 9)) / 81.0
DX = np.array([[1, 0, -1]])
DY = np.array([[1], [0], [-1]])


def conv_four_loops(im, kernel):
    flip_kernel = kernel[::-1, ::-1]

    kh, kw = kernel.shape
    h, w = im.shape

    pad_top = kh // 2
    pad_bottom = (kh - 1) - pad_top
    pad_left = kw // 2
    pad_right = (kw - 1) - pad_left

    padded = np.zeros(((h + pad_top + pad_bottom), (w + pad_left + pad_right)))
    padded[pad_top:pad_top + h, pad_left:pad_left + w] = im
    output = np.zeros(im.shape)

    for i in range(h):
        for j in range(w):
            total = 0
            for u in range(kh):
                for v in range(kw):
                    total += padded[i+u, j+v] * flip_kernel[u, v]
            output[i, j] = total

    return output

def conv_two_loops(im, kernel):
    flip_kernel = kernel[::-1, ::-1]
    
    kh, kw = kernel.shape
    h, w = im.shape

    pad_top = kh // 2
    pad_bottom = (kh - 1) - pad_top
    pad_left = kw // 2
    pad_right = (kw - 1) - pad_left

    padded = np.zeros(((h + pad_top + pad_bottom), (w + pad_left + pad_right)))
    padded[pad_top:pad_top + h, pad_left:pad_left + w] = im

    output = np.zeros(im.shape)

    for i in range(h):
        for j in range(w):
            output[i, j] = np.sum(padded[i:i + kh, j:j + kw] * flip_kernel)

    return output


if __name__ == "__main__":
    selfie = io.imread("../data/selfie.jpg")
    selfie = img_as_float(selfie)

    results = {}
    for name, k in [("box", BOX_9), ("dx", DX), ("dy", DY)]:
        start = time.perf_counter()
        expected = convolve2d(selfie, k, mode="same")
        print(f"{name} convolve2d: {time.perf_counter() - start:.3f}s")
        for fn in (conv_four_loops, conv_two_loops):
            start = time.perf_counter()
            results[name] = fn(selfie, k)
            print(f"{name} {fn.__name__}: {time.perf_counter() - start:.3f}s, matches scipy: {np.allclose(results[name], expected)}")

    io.imsave("../images/part1_1/selfie_gray.jpg", img_as_ubyte(selfie))
    io.imsave("../images/part1_1/selfie_box.jpg", img_as_ubyte(np.clip(results["box"], 0, 1)))
    for name in ("dx", "dy"):
        x = results[name]
        io.imsave(f"../images/part1_1/selfie_{name}.jpg", img_as_ubyte((x - x.min()) / (x.max() - x.min())))
