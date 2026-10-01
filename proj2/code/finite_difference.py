import numpy as np
from scipy.signal import convolve2d
from skimage import io, img_as_float, img_as_ubyte

### Part 1.2: Finite Difference Operator

DX = np.array([[1, 0, -1]])
DY = np.array([[1], [0], [-1]])


if __name__ == "__main__":
    im = img_as_float(io.imread("../data/cameraman.png"))[..., 0]

    dx = convolve2d(im, DX, mode="same")
    dy = convolve2d(im, DY, mode="same")
    grad_mag = np.sqrt(dx ** 2 + dy ** 2)

    threshold = 0.25
    edges = grad_mag > threshold

    for name, x in [("dx", dx), ("dy", dy)]:
        io.imsave(f"../images/part1_2/cameraman_{name}.jpg", img_as_ubyte((x - x.min()) / (x.max() - x.min())))
    io.imsave("../images/part1_2/cameraman_grad_mag.jpg", img_as_ubyte(grad_mag / grad_mag.max()))
    io.imsave("../images/part1_2/cameraman_edges.jpg", img_as_ubyte(edges))
