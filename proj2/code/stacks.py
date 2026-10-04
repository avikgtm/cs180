import cv2
import numpy as np
from scipy.signal import convolve2d, fftconvolve
from skimage import io, img_as_float, img_as_ubyte

### Part 2.3: Gaussian and Laplacian Stacks

LEVELS = 5
SIGMA = 2


def gaussian(sigma):
    ksize = int(sigma * 3) * 2 + 1
    g = cv2.getGaussianKernel(ksize, sigma)
    return g @ g.T

def blur(im, sigma):
    # Same result as convolve2d(..., mode="same", boundary="symm"), but via FFT so the large kernels
    # at high levels (sigma up to 32) stay fast.
    G = gaussian(sigma)
    p = G.shape[0] // 2
    padded = np.pad(im, ((p, p), (p, p), (0, 0)), mode="symmetric")
    return np.dstack([fftconvolve(padded[..., c], G, mode="valid") for c in range(im.shape[2])])

def save_stack(name, stack):
    # Saves every level side by side. Each level is rescaled to [0, 1] on its own so the
    # Laplacian levels (which are small and have negative values) are visible.
    levels = [(im - im.min()) / (im.max() - im.min()) for im in stack]
    io.imsave(f"../images/part2_3/{name}.jpg", img_as_ubyte(np.hstack(levels)))

def gaussian_stack(im, levels, sigma):
    l = [im]
    for level in range(1, levels):
        l.append(blur(l[level - 1], sigma * 2 ** level))
    return l

def laplacian_stack(g_stack):
    l = []
    for i in range(len(g_stack) - 1):
        l.append(g_stack[i] - g_stack[i + 1])
    l.append(g_stack[-1])
    return l


if __name__ == "__main__":
    apple = img_as_float(io.imread("../data/apple.jpeg"))
    orange = img_as_float(io.imread("../data/orange.jpeg"))

    for name, im in [("apple", apple), ("orange", orange)]:
        g_stack = gaussian_stack(im, LEVELS, SIGMA)
        l_stack = laplacian_stack(g_stack)
        save_stack(f"{name}_gaussian", g_stack)
        save_stack(f"{name}_laplacian", l_stack)
        print(np.allclose(sum(l_stack), im))
