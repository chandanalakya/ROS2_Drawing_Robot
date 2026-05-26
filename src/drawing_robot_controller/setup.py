from setuptools import setup

package_name = 'drawing_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Controller for XY drawing robot',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
    	     'draw_controller = drawing_robot_controller.draw_controller:main',
             'image_draw_controller = drawing_robot_controller.image_draw_controller:main',
],
    },
)
