# ROS Testing Py
This is demo package for ROS2 testing in Python

## Runing the tests
Build your package with colcon.
```sh
colcon build --packages-select ros_testing_py
'''

Run tests with colcon
```sh
colcon test --packages-select ros_testing_py
```

You can pass additional paremeters to pytest with **--pytest-args** flag.
```sh
colcon test --pytest-with-coverage --pytest-args "-m \"unit\"" --packages-select ros_testing_py
```

Results are stored in files. To check test detils for this package us comand.
```sh
colcon test-result --test-result-base build/ros_testing_py/ --verbose
```

## Runing test with pytest

You can also run tests with pytest. To do thet you need to source your workspace.

```sh
source install/setup/bash
```

Go to package directory.

```sh
cd src/ros_testing_py
```

Run pytest

```sh
pytest-3
```
