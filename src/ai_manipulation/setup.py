from setuptools import find_packages, setup

package_name = 'ai_manipulation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + "/utils/models/", ["common.py"]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sechan',
    maintainer_email='sechan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'make_my_model = ai_manipulation.make_my_model:main',
            'run_my_model = ai_manipulation.run_my_model:main',
        ],
    },
)
