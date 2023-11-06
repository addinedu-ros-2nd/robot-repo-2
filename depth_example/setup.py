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
            "detect = depth_example.detect:main",
            "distance = depth_example.distance:main",
            "Streaming_for_loop_with_tracking = depth_example.Streaming_for_loop_with_tracking:main",
        ],
    },
)
