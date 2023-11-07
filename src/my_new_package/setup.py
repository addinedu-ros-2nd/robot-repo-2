from setuptools import find_packages, setup

package_name = 'my_new_package'

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
        'my_new_package': ['*'],
    },
    install_requires=['setuptools',
                      ],
    zip_safe=True,
    maintainer='jin',
    maintainer_email='jin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher=my_new_package.publisher_node:main',
            'basic.py=my_new_package.basic:main',
            'FaceID2.py=my_new_package.FaceID2:main',
            'minibot=my_new_package.minibot:main',
            'roboarm=my_new_package.roboarm:main',
            'mvpbasic.py=my_new_package.mvpbasic:main',
            'prefaceid=my_new_package.prefaceid:main',
        ],
    },
)
