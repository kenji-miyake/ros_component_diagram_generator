from glob import glob

from setuptools import setup

package_name = "ros_component_diagram_generator"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/templates", glob("templates/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Kenji Miyake",
    maintainer_email="kenji.miyake@tier4.jp",
    description="ROS component diagram generator",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            f"launch2json={package_name}.bin.launch2json:main",
        ],
    },
)
