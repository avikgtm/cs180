import numpy as np
import cv2 as cv

### All code is found in this .py file! Simply run colorize() on the image's filepath and 
### set the output filepath and you're good to go!

def ncc(im1, im2):
    mc1 = im1 - np.mean(im1)
    mc2 = im2 - np.mean(im2)
    return np.sum(mc1 * mc2) / (np.linalg.norm(mc1) * np.linalg.norm(mc2))

def align(im, ref, window=15):
    crop_im = crop_border(im)
    crop_ref = crop_border(ref)
    best_ncc = -np.inf
    dx, dy = 0, 0
    for x in range(-window, window+1):
        x_roll = np.roll(crop_im, x, axis=1)
        for y in range(-window, window+1):
            curr_ncc = ncc(np.roll(x_roll, y, axis=0), crop_ref)
            if curr_ncc > best_ncc:
                best_ncc = curr_ncc
                dx = x
                dy = y
    return (dy, dx)

def crop_border(im, pct=10):
    crop_y = int(round(im.shape[0] * (pct/100.0)))
    crop_x = int(round(im.shape[1] * (pct/100.0)))
    return im[crop_y:im.shape[0] - crop_y, crop_x:im.shape[1] - crop_x]

def pyramid_align(im, ref, levels=3, window=15):
    if levels == 0 or im.shape[0] < 100 or im.shape[1] < 100:
        return align(im, ref, window)
    down_im = cv.pyrDown(im)
    down_ref = cv.pyrDown(ref)
    pyr_align = pyramid_align(down_im, down_ref, levels - 1, window)
    al = (pyr_align[0]*2, pyr_align[1]*2)
    alim = np.roll(np.roll(im, al[0], axis=0), al[1], axis=1)
    residual = align(alim, ref, 8)
    return (al[0] + residual[0], al[1] + residual[1])


def colorize(imname, fname):
    # read in the image as grayscale (the glass plate scan is stacked grayscale)
    im = cv.imread(imname, cv.IMREAD_GRAYSCALE)

    # convert to float in [0,1] (might want to do this later on to save memory)
    im = im.astype(np.float32) / 255.0

    # compute the height of each part (just 1/3 of total)
    height = int(np.floor(im.shape[0] / 3.0))

    # separate color channels
    b = im[:height]
    g = im[height: 2*height]
    r = im[2*height: 3*height]

    # align the images
    # functions that might be useful for aligning the images include:
    # np.roll, np.sum, cv2.resize (for multiscale)
    if im.shape[1] < 1500:
        ag = align(g, b)
        ar = align(r, b)
    else:
        ag = pyramid_align(g, b)
        ar = pyramid_align(r, b)

    # realign based on the optimal shift
    ag = np.roll(np.roll(g, ag[0], axis=0), ag[1], axis=1)
    ar = np.roll(np.roll(r, ar[0], axis=0), ar[1], axis=1)

    # create a color image
    im_out = np.dstack([ar, ag, b])

    # prepare for OpenCV saving/display (expects BGR uint8)
    out_uint8 = np.clip(im_out * 255.0, 0, 255).astype(np.uint8)
    out_bgr = cv.cvtColor(out_uint8, cv.COLOR_RGB2BGR)

    # save the image
    cv.imwrite(fname, out_bgr)


if __name__ == "__main__":
    colorize("../data/cathedral.jpg", "../images/cathedral-result.jpg")
    colorize("../data/monastery.jpg", "../images/monastery-result.jpg")
    colorize("../data/tobolsk.jpg", "../images/tobolsk-result.jpg")
    colorize("../data/church.tif", "../images/church-result.jpg")
    colorize("../data/emir.tif", "../images/emir-result.jpg")
    colorize("../data/harvesters.tif", "../images/harvesters-result.jpg")
    colorize("../data/icon.tif", "../images/icon-result.jpg")
    colorize("../data/ilemselga.tif", "../images/ilemselga-result.jpg")
    colorize("../data/melons.tif", "../images/melons-result.jpg")
    colorize("../data/religous_painting.tif", "../images/religous_painting-result.jpg")
    colorize("../data/self_portrait.tif", "../images/self_portrait-result.jpg")
    colorize("../data/siren.tif", "../images/siren-result.jpg")
    colorize("../data/three_generations.tif", "../images/three_generations-result.jpg")
    colorize("../data/wharf.tif", "../images/wharf-result.jpg")
    colorize("../data/mosque.tif", "../images/mosque-result.jpg")
    colorize("../data/woman.tif", "../images/woman-result.jpg")
    colorize("../data/napoleon.tif", "../images/napoleon-result.jpg")
