# Identify the Jetson, ROS, and JetPack

Run these checks in the **Jetson SSH terminal**, not Windows PowerShell.
The SSH address in this lab is `unitree@192.168.123.18`: `unitree` names a Linux
account; the machine is the Go2's Jetson expansion computer.

## What is established and what still needs measurement

| Item | Status for this starter |
| --- | --- |
| Robot target | Go2 EDU with onboard Jetson expansion dock |
| Board model | Previously documented as Orin NX; confirm the actual module with the report |
| Ubuntu | Existing lab notes: 20.04; recheck this unit |
| Motion-script ROS target | ROS 2 Foxy (`rclpy`, `unitree_go`, `unitree_api`) |
| DDS | Existing lab notes: CycloneDDS 0.10.2 on `eth0` |
| ROS 1 Noetic installed? | Not yet inventoried; inspect `/opt/ros` rather than assume |
| Exact JetPack / Jetson Linux (L4T) | Not yet captured from this unit; do not infer from Ubuntu alone |
| Robot firmware | Record the version reported by the robot/app during checkout; this inventory does not query robot firmware |

The [official Unitree ROS 2 repository](https://github.com/unitreerobotics/unitree_ros2)
lists Ubuntu 20.04/Foxy and Ubuntu 22.04/Humble as tested combinations. That is
upstream compatibility information, not evidence that either image is installed
on this lab robot. This starter's environment commands preserve the Foxy baseline.

## Collect a read-only report

After copying `scripts/check_jetson.py` as described in the README:

```bash
cd ~/go2_ws/scripts
python3 check_jetson.py
# Optional local report; keep it out of Git until reviewed.
python3 check_jetson.py > ~/go2_ws/jetson-software.json
```

The script reads system files, package versions, installed ROS setup paths, and
the current shell environment. It does not create a ROS node, contact the robot,
install packages, change network settings, or send motion commands. Run it again
after sourcing Foxy to show the active ROS environment separately from installed
distributions. Both the script and motion example support Python 3.8 syntax.

You can also inspect the essential evidence manually:

```bash
cat /etc/os-release
cat /proc/device-tree/model; printf '\n'
ls /opt/ros
printf 'ROS_VERSION=%s ROS_DISTRO=%s\n' "$ROS_VERSION" "$ROS_DISTRO"
dpkg-query --show nvidia-jetpack nvidia-l4t-core
cat /etc/nv_tegra_release
```

Missing packages/files are useful observations, not reasons to install or flash
anything immediately. `apt-cache` shows available package metadata; it does not
prove a version is installed. Prefer `dpkg-query` and installed-package status.

## Foxy versus Noetic

| Distribution | ROS generation | What it means here |
| --- | --- | --- |
| Foxy | ROS 2 | The existing script uses this environment and the `ros2` CLI |
| Noetic | ROS 1 | A different API (`rospy`/catkin); this script does not run on Noetic alone |
| Humble or another ROS 2 image | ROS 2 | Needs a separate environment/interface qualification; do not source nonexistent Foxy paths |

Both Foxy and Noetic targeted Ubuntu 20.04, so an image may contain either or
both. We have not verified a vendor image-selection option for this particular
unit. Installed directories and the active shell are different facts: sourcing
Foxy selects Foxy in that shell; it does not uninstall Noetic. Start a clean SSH
session rather than mixing both environments. Foxy and Noetic are now upstream
end-of-life; retain the approved robot image and plan migrations separately.
See [ROS 2 Foxy documentation](https://docs.ros.org/en/foxy/Installation.html)
and [ROS 1 target platforms](https://reps.openrobotics.org/rep-0003/).

## JetPack versus L4T

JetPack is NVIDIA's software bundle; Jetson Linux/L4T identifies the underlying
board software release. If the installed `nvidia-jetpack` metapackage is absent,
retain the `nvidia-l4t-core` version and `/etc/nv_tegra_release` contents and
cross-reference the [NVIDIA JetPack archive](https://developer.nvidia.com/embedded/jetpack-archive).
Do not guess an exact JetPack release from the robot model or Ubuntu version.
NVIDIA documents this [L4T-based identification method](https://forums.developer.nvidia.com/t/what-version-of-the-jetson-sdk-am-i-running/111200).

## Complete the lab inventory

Add a reviewed report in the lab's approved inventory location with the date,
robot assignment, module, Ubuntu, installed and active ROS, JetPack/L4T evidence,
firmware, workspace revisions, DDS interface, and checkout result. Keep credentials
out. The exact JetPack field remains unverified until that report is collected.
