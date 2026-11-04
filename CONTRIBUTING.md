# Maintaining the starter

Keep the README runnable from a fresh Windows terminal and label every block
as Windows PowerShell or Jetson SSH. Keep credentials and full recordings out
of Git. Record the actual Jetson/ROS/JetPack inventory rather than assuming a
factory image. Noetic is ROS 1; the supplied motion example is ROS 2.

For changes, check Python 3.8 syntax, `go2_walk.py --help`, CLI limits, and the
read-only inventory. Motion changes require a supervised robot checkout with
firmware, interfaces, requested command, observed response, and stop outcome.
Offline tests do not qualify physical motion. Preserve existing logs and do
not use command-inclusive bag playback on a live robot connection.

Run offline checks without ROS or a robot:

```bash
python3 -m unittest discover -s tests -v
```

GitHub Actions runs these checks with Python 3.8 and 3.11.

Documentation ownership belongs to the DyCo-AI Lab; development credit and Git
authorship are retained for Sriram Krishnamoorthy and future contributors.
