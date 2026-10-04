import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'substitutions_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yms]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Juhyun Lee',
    maintainer_email='279787542+bestbada@users.noreply.github.com',
    description='Launch substitutions and event handlers practice based on the ROS 2 documentation',
    license='CC-BY-4.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
