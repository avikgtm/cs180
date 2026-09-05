# CS180 Project 0

Live site: https://avikgtm.github.io/cs180/

## Swapping in real photos

The page currently shows lavender placeholder graphics. Replace them by adding
your real files with these exact names (same folders), then update the `src`
in `index.html` to match the new extension:

| Slot | Placeholder | Replace with |
|---|---|---|
| Part 1, photo 1–5 | `images/part1/photo1.svg` ... `photo5.svg` | `images/part1/photo1.jpg` ... `photo5.jpg` |
| Part 2, photo 1–2 | `images/part2/photo1.svg`, `photo2.svg` | `images/part2/photo1.jpg`, `photo2.jpg` |
| Part 3, GIF | `images/part3/dolly-zoom-placeholder.svg` | `images/part3/dolly-zoom.gif` |

After adding real photos, also edit the `<figcaption>` text in `index.html`
to explain the perspective/focal-length reasoning for each shot.

## Local preview

Open `index.html` directly in a browser, or run a tiny local server:

```
python3 -m http.server 8000
```

then visit `http://localhost:8000`.
