# Optional ROS 2 recording

[Back to the starter](../README.md). Run these commands on the Jetson after
loading the ROS 2 environment and completing the approved motion checkout.
Recording is off by default.

## 9. Choose whether to record

There are three mutually exclusive recording flags:

| Option | What happens |
| --- | --- |
| No recording flag | No recording; default |
| `--no-record` | Explicitly choose no recording |
| `--record-states` | Record robot states, control requests/responses, and available visualization topics |
| `--record-all` | Record all discoverable supported ROS topics, including active camera/LiDAR streams |

Examples, run in the **SSH terminal**:

```bash
# Default: no recording.
python3 go2_walk.py --vel 0.5 --time 5

# Same behavior, explicitly selected.
python3 go2_walk.py --vel 0.5 --time 5 --no-record

# Robot states and commands.
python3 go2_walk.py --vel 0.5 --time 5 --record-states

# All supported active ROS topics.
python3 go2_walk.py --vel 0.5 --time 5 --record-all

# Choose a recording parent folder.
python3 go2_walk.py --vel 0.5 --time 5 --record-states --log-dir ~/go2_data
```

Recording starts before movement and stays active through stopping and stance
settling. No separate rosbag terminal is needed. When recording is requested,
a recorder startup failure prevents walking, and a recorder failure during
walking triggers stopping.

`--record-states` includes full high/low-frequency Unitree body and motor state,
IMU, battery, joystick, service status, available odometry, and Sport API
requests/responses. It also requests `/joint_states`, `/tf`, `/tf_static`,
`/robot_description`, and other standard visualization topics if published.
It excludes camera video and LiDAR point clouds.

`--record-all` can include raw and processed copies of camera/LiDAR streams and
other traffic, so files can be much larger. It does not turn sensors on.
Unavailable message types may be skipped. Unitree's encoded camera streams
may need decoding before a viewer can show the images.

## 10. Find and inspect recordings

Each recorded run creates a unique timestamped folder under:

```text
/home/unitree/go2_ws/logs/
```

The automatically generated name includes a timestamp and random suffix.
Existing recordings are not overwritten. No-record runs create no recording
folder. The exact run path is printed in the terminal.

| File or folder | Purpose |
| --- | --- |
| `bag/metadata.yaml` and `bag/*.db3` | The ROS 2 bag |
| `run.json` | Arguments, start/end times, message counts, and result |
| `recorder.log` | Recorder output and skipped-topic diagnostics |
| `go2_walk.py` | Copy of the script used for this run |
| `message_definitions/` | Available installed Unitree/common message definitions |
| `qos_overrides.yaml` | Recorder subscription settings |

Use the exact folder name printed by the script in place of `RUN_FOLDER`:

```bash
ros2 bag info ~/go2_ws/logs/RUN_FOLDER/bag
cat ~/go2_ws/logs/RUN_FOLDER/run.json
```

`recording_verified: true` means the recorder closed with metadata and nonzero
message counts on core body/motor state and Sport request/response topics.
It does not prove that every optional stream was present or every sample was
captured. Check the per-topic counts and `recorder.log` for actual coverage.
`motion_exit_code` separately reports the motion-script result.

To copy the whole run to Windows, use **Windows PowerShell**:

```powershell
scp -r unitree@192.168.123.18:/home/unitree/go2_ws/logs/RUN_FOLDER "$env:USERPROFILE\Downloads\"
```

Keep the complete run folder. It preserves the metadata and message-definition
snapshot needed for later analysis. The snapshot covers common packages, not
necessarily every custom type captured by `--record-all`; retain the ROS
workspace and Unitree source ZIP too.

