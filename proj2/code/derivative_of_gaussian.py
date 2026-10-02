import cv2
import numpy as np
from scipy.signal import convolve2d
from skimage import io, img_as_float, img_as_ubyte

### Part 1.3: Derivative of Gaussian (DoG) Filter

DX = np.array([[1, 0, -1]])
DY = np.array([[1], [0], [-1]])
THRESHOLD = 0.05


if __name__ == "__main__":
    im = img_as_float(io.imread("../data/cameraman.png"))[..., 0]

    sigma = 2
    ksize = (sigma * 6) + 1
    g = cv2.getGaussianKernel(ksize, sigma)
    G = g @ g.T

    # Method 1 -- blur first, then differentiate (two convolutions).
    blurred = convolve2d(im, G, mode="same")
    dx = convolve2d(blurred, DX, mode="same")
    dy = convolve2d(blurred, DY, mode="same")
    grad_mag = np.sqrt(dx ** 2 + dy ** 2)

    io.imsave("../images/part1_3/cameraman_blurred.jpg", img_as_ubyte(np.clip(blurred, 0, 1)))
    for name, x in [("dx", dx), ("dy", dy)]:
        io.imsave(f"../images/part1_3/cameraman_blur_{name}.jpg", img_as_ubyte((x - x.min()) / (x.max() - x.min())))
    io.imsave("../images/part1_3/cameraman_blur_grad_mag.jpg", img_as_ubyte(grad_mag / grad_mag.max()))
    io.imsave("../images/part1_3/cameraman_blur_edges.jpg", img_as_ubyte(grad_mag > THRESHOLD))

    # Method 2 -- derivative of Gaussian (one convolution).
    dog_x = convolve2d(G, DX, mode="full")
    dog_y = convolve2d(G, DY, mode="full")
    dx = convolve2d(im, dog_x, mode="same")
    dy = convolve2d(im, dog_y, mode="same")
    dog_grad_mag = np.sqrt(dx ** 2 + dy ** 2)
    
    print("methods match:", np.allclose(grad_mag[10:-10, 10:-10], dog_grad_mag[10:-10, 10:-10]))

    for name, f in [("x", dog_x), ("y", dog_y)]:
        f = np.kron(f, np.ones((20, 20)))
        io.imsave(f"../images/part1_3/dog_{name}.jpg", img_as_ubyte((f - f.min()) / (f.max() - f.min())))
    io.imsave("../images/part1_3/cameraman_dog_edges.jpg", img_as_ubyte(dog_grad_mag > THRESHOLD))
