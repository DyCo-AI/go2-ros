# Public demo media

| File | Purpose | Export |
| --- | --- | --- |
| `go2-jetson-ethernet.png` | Annotated Go2 EDU photo showing the Jetson Ethernet connector and cable to the host PC | 1200 px wide PNG, source metadata removed |
| `go2-velocity-demo.gif` | Short lab motion example | 320 px wide, 8 fps, 64-color palette, looped; no audio |
| `go2-controller.jpg` | Remote button reference | Existing lab-provided photo |

Original media remains local. The PNG annotation was supplied by the maintainer;
the published export keeps the same filename. The motion GIF is unchanged.

FFmpeg filter for the GIF:

```text
fps=8,scale=320:-2:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4
```

Annotated image export: `scale=1200:-2:flags=lanczos`, PNG compression level 9,
`-map_metadata -1`. Published export checksums:

```json
{
  "go2-controller.jpg": {
    "bytes": 714280,
    "sha256": "89c287cb0e84ce0c553f3a56f2c74f238c610a0281946032eb23a818b78ca015"
  },
  "go2-jetson-ethernet.png": {
    "bytes": 1503573,
    "sha256": "bb766dc0976c10e48c84f8bc19ddd67f5c26961abc2b5a4b1eb0f7bf76f963e5"
  },
  "go2-velocity-demo.gif": {
    "bytes": 1932676,
    "sha256": "53a30171987ae78ba177acb10fce3d813d682d9cc64a78514f127e886d99d5b1"
  }
}
```
