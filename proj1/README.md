# CS180 Project 1 — Colorizing the Prokudin-Gorskii Photo Collection

## Layout

| Path | Contents |
|---|---|
| `code/colorize_skel.py` | Official starter code, fetched verbatim from the course site |
| `code/align.py` | Your implementation (single-scale + pyramid alignment) — not yet written |
| `data/` | Raw `.jpg`/`.tif` plates (gitignored — never commit these, some are 50–100MB+) |
| `images/` | Small JPEG outputs referenced by `index.html` for the write-up |
| `index.html` | Project write-up (uses the shared `../css/style.css` theme) |

## Getting the data

Download the data zip from the assignment page and extract into `data/`:
https://cal-cs180.github.io/fa26/hw/proj1/index.html

`data/` is gitignored, so nothing there will be committed.

## Starter code note

`code/colorize_skel.py` is the official fa24 skeleton (the fa26 assignment page
links to the same file). It uses `np.floor(...).astype(np.int)` — `np.int` was
removed in NumPy ≥ 1.24, so that line will need to become `.astype(int)` before
it will actually run on a current environment.

## requirements

```
numpy
scikit-image
```

## Filling in the write-up

`index.html` has `TODO` placeholders in four spots:
1. Offsets table for `cathedral.jpg` / `monastery.jpg` (Part 1)
2. Result thumbnails + offsets table for every provided `.tif` example (Part 2)
3. Three self-selected images from the Library of Congress collection (Part 3)
4. Failure discussion and any bells & whistles (final section)

Drop result JPEGs into `images/` and swap the placeholder `src`/`alt`/captions
to match.
