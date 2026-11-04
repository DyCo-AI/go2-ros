# Public demo media

| File | Purpose | Export |
| --- | --- | --- |
| `go2-jetson-ethernet.jpg` | Go2 EDU with Ethernet plugged into its Jetson dock | 960 px wide JPEG; metadata stripped |
| `go2-velocity-demo.gif` | Short lab motion example | 320 px wide, 8 fps, 64-color palette, original timing, looped; no audio |
| `go2-controller.jpg` | Remote button reference | Existing lab-provided photo |

Original files stay local. These visuals do not record a complete stop test,
software inventory, requested velocity, or firmware version. Do not infer those
values from the image or GIF. The read-only inventory and actual trial notes
are the evidence for those fields.

FFmpeg filter for the GIF:

```text
fps=8,scale=320:-2:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4
```

Photo filter: `scale=960:-2:flags=lanczos`, JPEG quality 4. Both exports remove
source metadata. The source video is not uploaded to Git.

Published export checksums:

```json
{
  "go2-controller.jpg": {
    "bytes": 714280,
    "sha256": "89c287cb0e84ce0c553f3a56f2c74f238c610a0281946032eb23a818b78ca015"
  },
  "go2-jetson-ethernet.jpg": {
    "bytes": 163583,
    "sha256": "4d82e0d273cf16f5e77d35fbbcf63fcf2661f4b0d8091f4f706bafa96e0dbaad"
  },
  "go2-velocity-demo.gif": {
    "bytes": 1932676,
    "sha256": "53a30171987ae78ba177acb10fce3d813d682d9cc64a78514f127e886d99d5b1"
  }
}
```
