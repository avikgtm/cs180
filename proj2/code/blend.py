import numpy as np
from skimage import io, img_as_float, img_as_ubyte, transform

from stacks import gaussian_stack, laplacian_stack, blur, LEVELS, SIGMA

### Part 2.4: Multiresolution Blending


def save(name, im):
    io.imsave(f"../images/part2_4/{name}.jpg", img_as_ubyte(np.clip(im, 0, 1)))

def show(im):
    # Rescales a Laplacian level (small, has negative values) to [0, 1] for display.
    return (im - im.min()) / (im.max() - im.min())

def step_mask(shape):
    # 1 on the left half, 0 on the right half -- the vertical seam for the oraple.
    mask = np.zeros(shape)
    mask[:, : shape[1] // 2] = 1
    return mask

def load_mask(path, shape):
    # For irregular masks: a black-and-white image, white = take image A. Returns 3 channels.
    m = img_as_float(io.imread(path))
    m = m[..., 0] if m.ndim == 3 else m
    return np.dstack([m] * shape[2])

def blend(a, b, mask, levels, sigma):
    la = laplacian_stack(gaussian_stack(a, levels, sigma))
    lb = laplacian_stack(gaussian_stack(b, levels, sigma))
    gm = gaussian_stack(mask, levels, sigma)
    output = 0
    for i in range(levels):
        output += gm[i] * la[i] + (1 - gm[i]) * lb[i]
    return output


if __name__ == "__main__":
    apple = img_as_float(io.imread("../data/apple.jpeg"))
    orange = img_as_float(io.imread("../data/orange.jpeg"))
    mask = step_mask(apple.shape)

    save("apple", apple)
    save("orange", orange)

    oraple = blend(apple, orange, mask, LEVELS, SIGMA)
    save("oraple", oraple)

    la = laplacian_stack(gaussian_stack(apple, LEVELS, SIGMA))
    lb = laplacian_stack(gaussian_stack(orange, LEVELS, SIGMA))
    gm = gaussian_stack(mask, LEVELS, SIGMA)
    apple_levels = [gm[i] * la[i] for i in range(LEVELS)]
    orange_levels = [(1 - gm[i]) * lb[i] for i in range(LEVELS)]
    for i in (0, 2, 4):
        save(f"fig_apple_{i}", show(apple_levels[i]))
        save(f"fig_orange_{i}", show(orange_levels[i]))
        save(f"fig_blend_{i}", show(apple_levels[i] + orange_levels[i]))
    save("fig_apple_full", sum(apple_levels))
    save("fig_orange_full", sum(orange_levels))
    save("fig_blend_full", oraple)

    ship = img_as_float(io.imread("../data/aerial-view-cruise-ship.jpg"))
    ship = transform.rescale(ship, 0.8, channel_axis=-1, anti_aliasing=True)
    pad = (720 - ship.shape[0]) // 2
    ship = np.pad(ship, ((pad, 720 - ship.shape[0] - pad), (pad, 720 - ship.shape[1] - pad), (0, 0)), mode="reflect")
    glass = img_as_float(io.imread("../data/cup-with-water.jpg"))
    glass = transform.resize(glass[20:3820, 570:4370], (720, 720), anti_aliasing=True)
    yy, xx = np.mgrid[:720, :720]
    circle = np.dstack([(np.hypot(xx - 360, yy - 360) < 255).astype(float)] * 3)

    ship_glass = blend(ship, glass, circle, LEVELS, SIGMA)
    save("blend2_a", ship)
    save("blend2_b", glass)
    save("blend2_mask", circle)
    save("blend2", ship_glass)

    sand = transform.resize(img_as_float(io.imread("../data/sand.jpg")), (600, 800), anti_aliasing=True)
    snow = img_as_float(io.imread("../data/snow.jpg"))
    snow = transform.resize(snow[:, 333:5666], (600, 800), anti_aliasing=True)  # crop 3:2 to 4:3 to match sand
    line = blur(step_mask(sand.shape), 40)  # pre-softened: the two scenes differ, so a hard seam shows

    sand_snow = blend(sand, snow, line, LEVELS, SIGMA)
    save("blend3_a", sand)
    save("blend3_b", snow)
    save("blend3_mask", line)
    save("blend3", sand_snow)
