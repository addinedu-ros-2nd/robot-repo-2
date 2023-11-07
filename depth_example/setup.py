from setuptools import find_packages, setup

package_name = 'depth_example'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sechan',
    maintainer_email='my7868@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "basic_tracking = depth_example.basic_tracking:main",
            "basic_distance = depth_example.basic_distance:main",
            "yolov8_box_tracking = depth_example.yolov8_box_tracking:main",
            "yolov8_seg_tracking = depth_example.yolov8_seg_tracking:main",
            "open3d_viewer = depth_example.open3d_viewer:main",
            "open3d_test = depth_example.open3d_test:main",
        ],
    },
)
