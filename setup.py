from setuptools import setup

setup(
    name='i3-status-line',
    version='0.0.1',
    description='i3 status bar data output',
    url='http://github.com/hellupline/i3-status-line',
    author_email='hellupline+i3@gmail.com',
    author='Renan Traba',
    license='MIT',
    packages=['i3_status_line'],
    install_requires=[
        'gevent',
        'cached-property',
        'psutil',
        'dbus-python',
        'mpris2',
        'pyalsaaudio',
        'requests',
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'i3-status-line = i3_status_line.main:main'
        ]
    },
)
