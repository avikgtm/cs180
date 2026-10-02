import cv2
import numpy as np
from scipy.signal import convolve2d
from skimage import io, img_as_float, img_as_ubyte

### Part 2.1: Image "Sharpening"

ALPHAS = (0.5, 1, 2, 4)


def conv_color(im, kernel):
    return np.dstack([convolve2d(im[..., c], kernel, mode="same", boundary="symm") for c in range(3)])

def save(name, im):
    io.imsave(f"../images/part2_1/{name}.jpg", img_as_ubyte(np.clip(im, 0, 1)))


if __name__ == "__main__":
    taj = img_as_float(io.imread("../data/taj.jpg"))
    dog = img_as_float(io.imread("../data/dog.jpg"))
    selfie = img_as_float(io.imread("../data/selfie_color.jpg"))

    sigma = 2
    ksize = (sigma * 6) + 1
    g = cv2.getGaussianKernel(ksize, sigma)
    G = g @ g.T

    for name, im in [("taj", taj), ("dog", dog), ("sharp", selfie)]:
        save(f"{name}_original", im)

    alpha = 1
    for name, im in [("taj", taj), ("dog", dog)]:
        blurred = conv_color(im, G)
        high = im - blurred
        sharpened = im + alpha * high
        save(f"{name}_blurred", blurred)
        save(f"{name}_high", high + 0.5)
        save(f"{name}_sharpened", sharpened)

        e = np.zeros(G.shape)
        e[ksize // 2, ksize //2] = 1
        unsharp = (1 + alpha) * e - alpha * G
        sharpened_2 = conv_color(im, unsharp)

        print(np.allclose(sharpened_2, sharpened))

    for alpha in ALPHAS:
        im = taj
        blurred = conv_color(im, G)
        high = im - blurred
        sharpened = im + alpha * high
        save(f"taj_alpha_{alpha}", sharpened)

    alpha = 4
    blurred = conv_color(selfie, G)
    high = blurred - conv_color(blurred, G)
    resharpened = blurred + alpha * high
    save("sharp_blurred", blurred)
    save("sharp_resharpened", resharpened)
