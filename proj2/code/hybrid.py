import cv2
import numpy as np
from scipy.signal import convolve2d
from skimage import io, img_as_float, img_as_ubyte, color

from align_image_code import align_images

### Part 2.2: Hybrid Images


def gaussian(sigma):
    ksize = int(sigma * 3) * 2 + 1
    g = cv2.getGaussianKernel(ksize, sigma)
    return g @ g.T

def blur(im, sigma):
    return convolve2d(im, gaussian(sigma), mode="same", boundary="symm")

def save(name, im):
    io.imsave(f"../images/part2_2/{name}.jpg", img_as_ubyte(np.clip(im, 0, 1)))

def save_fft(name, im):
    f = np.log(np.abs(np.fft.fftshift(np.fft.fft2(im))) + 1e-8)
    save(name, (f - f.min()) / (f.max() - f.min()))

def hybrid_image(im1, im2, sigma1, sigma2):
    low = blur(im1, sigma1)
    high = im2 - blur(im2, sigma2)
    return low, high, low + high


if __name__ == "__main__":
    derek = img_as_float(io.imread("../data/DerekPicture.jpg"))
    nutmeg = img_as_float(io.imread("../data/nutmeg.jpg"))
    save("derek_original", derek)
    save("nutmeg_original", nutmeg)

    nutmeg_aligned, derek_aligned = align_images(nutmeg, derek)

    derek_gray = color.rgb2gray(derek_aligned)
    nutmeg_gray = color.rgb2gray(nutmeg_aligned)
    save("derek_aligned", color.rgb2gray(derek_aligned))
    save("nutmeg_aligned", color.rgb2gray(nutmeg_aligned))

    sigma1 = 10
    sigma2 = 4

    low, high, hybrid_im = hybrid_image(derek_gray, nutmeg_gray, sigma1, sigma2)
    save("derek_low", low)
    save("nutmeg_high", high + 0.5)
    save("derek_nutmeg", hybrid_im)

    for name, im in [("im1", derek_gray), ("im2", nutmeg_gray), ("low", low), ("high", high), ("hybrid", hybrid_im)]:
        save_fft(f"fft_{name}", im)


    dog = img_as_float(io.imread("../data/IMG_0827.jpg"))
    me = color.rgb2gray(img_as_float(io.imread("../data/selfie_color.jpg")))

    dog_aligned, me_aligned = align_images(dog, me)

    low, high, hybrid_im = hybrid_image(me_aligned, dog_aligned, 6, 3)
    save("hybrid2_im1", me_aligned)
    save("hybrid2_im2", dog_aligned)
    save("hybrid2", hybrid_im)

    mochi = img_as_float(io.imread("../data/mochi.jpg"))
    ashley = img_as_float(io.imread("../data/ashley.jpg"))

    mochi_aligned, ashley_aligned = align_images(mochi, ashley)

    low, high, hybrid_im = hybrid_image(ashley_aligned, mochi_aligned, 6, 2)
    save("hybrid3_im1", ashley_aligned)
    save("hybrid3_im2", mochi_aligned)
    save("hybrid3", hybrid_im)
