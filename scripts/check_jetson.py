#!/usr/bin/env python3
"""Print a read-only Jetson/ROS software inventory. No ROS node or robot I/O.

Uses only the Python standard library; compatible with Python 3.8 (Foxy).
"""
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess


def read_file(path):
    try:
        return Path(path).read_text(encoding="utf-8").strip("\x00\n ")
    except (OSError, UnicodeError):
        return None


def installed_package(name):
    if not shutil.which("dpkg-query"):
        return None
    try:
        result = subprocess.run(
            ["dpkg-query", "--show", "--showformat=${Status}\t${Version}", name],
            capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    status, separator, version = result.stdout.strip().partition("\t")
    if not separator or status != "install ok installed":
        return None
    return version


def report():
    release = {}
    for line in (read_file("/etc/os-release") or "").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            release[key] = value.strip('"')
    try:
        setups = sorted(str(path) for path in Path("/opt/ros").glob("*/setup.bash"))
    except OSError:
        setups = []
    try:
        rclpy_available = importlib.util.find_spec("rclpy") is not None
    except (ImportError, ValueError):
        rclpy_available = False
    return {
        "host_system": platform.system(),
        "architecture": platform.machine(),
        "kernel": platform.release(),
        "jetson_model": read_file("/proc/device-tree/model"),
        "os": {key: release.get(key) for key in ("PRETTY_NAME", "VERSION_ID")},
        "installed_ros_setup_files": setups,
        "active_shell": {key: os.environ.get(key) for key in
                         ("ROS_VERSION", "ROS_DISTRO", "RMW_IMPLEMENTATION", "ROS_DOMAIN_ID")},
        "python": platform.python_version(),
        "rclpy_available_in_this_python": rclpy_available,
        "ros2_cli_on_path": shutil.which("ros2"),
        "installed_nvidia_packages": {name: installed_package(name) for name in
                                      ("nvidia-jetpack", "nvidia-l4t-core")},
        "nv_tegra_release": read_file("/etc/nv_tegra_release"),
        "lab_workspace_setups": {name: (Path.home() / name).is_file() for name in
                                  ("cyclonedds_ws/install/setup.bash", "go2_ws/install/setup.bash")},
        "notes": ["Run on the Jetson; null means absent or not readable.",
                  "ROS setup files show installed environments, not the active one.",
                  "No robot firmware query or motion command was performed."]
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
