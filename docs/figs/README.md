# Figures

Figures embedded in the top-level [`README.md`](../../README.md). Export the paper's
figures as **PNG** (GitHub does not render PDF inline) and place them here with these
exact filenames:

| Filename | Paper source | Used in |
|----------|--------------|---------|
| `system_architecture.png` | `figs/system_architecture.pdf` (Fig. *System Architecture*) | README → Problem & method |
| `NATE_architecture.png`   | `figs/NATE_architecture.pdf` (Fig. *NATE Architecture*)     | README → Problem & method |
| `T-NATE_architecture.png` | `figs/T-NATE_architecture.pdf` (Fig. *T-NATE Architecture*) | README → Problem & method |

Suggested export (≈150–200 DPI keeps the README light):

```bash
# with ImageMagick / Ghostscript
magick -density 200 system_architecture.pdf -quality 90 system_architecture.png
# or with pdftoppm
pdftoppm -png -r 200 NATE_architecture.pdf NATE_architecture
```
