from setuptools import find_packages, setup

package_name = 'my_talker_listener_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={
        'my_talker_listener_package': ['*'],
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jin',
    maintainer_email='jin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'testtalk = my_talker_listener_package.talker:main',
            'testlistener = my_talker_listener_package.listener:main',
            'testimport = my_talker_listener_package.testimport:main',
            'talk = my_talker_listener_package.talker_node:main',
            'listen = my_talker_listener_package.listener_node:main',
            'prefaceid=my_talker_listener_package.prefaceid:main',
        ],
    },
)
