"""Offline parser and software-inventory checks; never connect to a robot."""
import contextlib
import io
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import go2_walk
from scripts import check_jetson


class VelocityArguments(unittest.TestCase):
    def test_first_checkout_has_bounded_cruise_and_default_ramps(self):
        args = go2_walk.arguments(['--vel', '0.5', '--time', '1'])
        self.assertEqual((args.vx, args.duration, args.ramp_up, args.ramp_down),
                         (0.5, 1.0, 1.0, 1.0))
        self.assertEqual(args.record_mode, 'none')

    def test_invalid_motion_parameters_are_rejected_before_ros(self):
        for values in (['--vel', '0'], ['--vel', 'nan'], ['--vel', '1.1'],
                       ['--time', '31'], ['--vy', '.21'], ['--yaw-rate', '.51']):
            with self.subTest(values=values), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    go2_walk.arguments(values)
                self.assertEqual(error.exception.code, 2)

    def test_explicit_stop_accepts_zero_forward_velocity(self):
        args = go2_walk.arguments(['--stop', '--vel', '0'])
        self.assertTrue(args.stop)
        self.assertEqual(args.vx, 0)


class JetsonInventory(unittest.TestCase):
    def test_only_installed_package_versions_are_reported(self):
        with patch.object(check_jetson.shutil, 'which', return_value='/usr/bin/dpkg-query'):
            for text, expected in [('install ok installed\t5.1.1-b56', '5.1.1-b56'),
                                   ('deinstall ok config-files\t5.1.1-b56', None)]:
                with self.subTest(text=text), patch.object(check_jetson.subprocess, 'run',
                     return_value=SimpleNamespace(returncode=0, stdout=text)) as command:
                    self.assertEqual(check_jetson.installed_package('nvidia-jetpack'), expected)
                    self.assertEqual(command.call_args[0][0][0], 'dpkg-query')

    def test_missing_package_manager_does_not_run_a_command(self):
        with patch.object(check_jetson.shutil, 'which', return_value=None), \
             patch.object(check_jetson.subprocess, 'run') as command:
            self.assertIsNone(check_jetson.installed_package('nvidia-jetpack'))
            command.assert_not_called()

    def test_installed_ros_and_active_ros_are_distinct(self):
        files = {'/etc/os-release': 'PRETTY_NAME="Ubuntu 20.04"\nVERSION_ID="20.04"',
                 '/proc/device-tree/model': 'NVIDIA Jetson Orin NX',
                 '/etc/nv_tegra_release': '# R35, REVISION: 3.1'}
        with patch.object(check_jetson, 'read_file', side_effect=lambda p: files.get(p)), \
             patch.object(Path, 'glob', return_value=[Path('/opt/ros/foxy/setup.bash'), Path('/opt/ros/noetic/setup.bash')]), \
             patch.object(Path, 'home', return_value=Path('/home/unitree')), \
             patch.dict(check_jetson.os.environ, {'ROS_DISTRO': 'noetic', 'ROS_VERSION': '1'}, clear=True), \
             patch.object(check_jetson, 'installed_package', return_value=None), \
             patch.object(check_jetson.shutil, 'which', return_value=None), \
             patch.object(check_jetson.importlib.util, 'find_spec', return_value=None):
            data = check_jetson.report()
        self.assertEqual(data['active_shell']['ROS_DISTRO'], 'noetic')
        self.assertEqual(len(data['installed_ros_setup_files']), 2)
        self.assertIsNone(data['installed_nvidia_packages']['nvidia-jetpack'])
        self.assertIn('R35', data['nv_tegra_release'])
        self.assertEqual(data['os']['VERSION_ID'], '20.04')
        self.assertNotIn('jetpack_version_guessed', data)


if __name__ == '__main__':
    unittest.main()
