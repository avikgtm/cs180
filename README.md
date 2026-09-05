# CS180 Project 0

Live site: https://avikgtm.github.io/cs180/

## Photos

Real photos are in place (converted from iPhone HEIC via macOS `sips`,
resized to 1600px wide for the web):

| Slot | File |
|---|---|
| Part 1, photo 1–3 (close / mid / far portrait) | `images/part1/photo1.jpg` ... `photo3.jpg` |
| Part 2, photo 1–2 (building far-zoomed / close-no-zoom) | `images/part2/photo1.jpg`, `photo2.jpg` |
| Part 3, GIF (3-frame dolly zoom) | `images/part3/dolly-zoom.gif` |

To swap in a different photo, replace the file at the same path (keep the
name and extension) and update the `<figcaption>` text in `index.html` to
match.

## Local preview

Open `index.html` directly in a browser, or run a tiny local server:

```
python3 -m http.server 8000
```

then visit `http://localhost:8000`.
