# Wheelchair Interface Remapper
Copyright 2024-2026 Joel Goh

This product is licensed under the Apache License, Version 2.0 (the "License").
You may obtain a copy of the License in the LICENSE file in this repository or
at http://www.apache.org/licenses/LICENSE-2.0.

## Acknowledgments

This software was originally developed as part of the National Science Foundation 
(NSF) Convergence Accelerator Track H project "Mobility Independence through 
Accelerated Wheelchair Intelligence" (NSF SP0076554) with input from a wide range 
of stakeholders.

## Third-Party Components

This project depends on, and in some cases bundles, third-party software. Those
components remain under their own licenses, reproduced or referenced below. This
NOTICE is informational and does not modify the Apache License governing this
project's own source.

Bundled code (included in this repository):

  * ROS 2 test templates — files under ros_remapper/test/ (test_copyright.py,
    test_flake8.py, test_pep257.py)
    Copyright 2015-2017 Open Source Robotics Foundation, Inc.
    Licensed under the Apache License, Version 2.0.

  * Create React App scaffolding — files generated under
    web-server/wdi-reconfigurer/ (e.g. public/index.html, src/index.js,
    src/reportWebVitals.js, src/setupTests.js, configuration in package.json)
    Copyright (c) 2013-present Meta Platforms, Inc. and affiliates.
    Licensed under the MIT License.

Python runtime dependencies (not bundled; installed separately):

  * python-evdev          — BSD (Revised) License
  * Flask                 — BSD 3-Clause License
  * Flask-CORS            — MIT License
  * pytest (tests only)   — MIT License

ROS 2 dependencies (not bundled; provided by a ROS 2 distribution):

  * rclpy, std_msgs, sensor_msgs, geometry_msgs, builtin_interfaces,
    ament_* and rosidl_* packages — Apache License, Version 2.0.

JavaScript / web dependencies (not bundled; installed via npm):

  * react, react-dom            — MIT License
  * react-router-dom            — MIT License
  * react-scripts               — MIT License
  * @testing-library/* packages — MIT License
  * web-vitals                  — Apache License, Version 2.0

External dependency (NOT included):

  * luci_messages — Required by the ROS 2 nodes in ros_remapper/. This package
    is available at https://github.com/lucimobility/luci-ros2-sdk.

License identifiers above reflect each project's published license at the time
of writing. Consult each dependency's own distribution for the authoritative
license text and version-specific details.
