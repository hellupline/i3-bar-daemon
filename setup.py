from setuptools import setup, find_packages

setup(
    name='i3-status-line',
    version='0.0.1',
    description='i3 status bar data output',
    url='http://github.com/hellupline/i3-status-line',
    author_email='hellupline+i3@gmail.com',
    author='Renan Traba',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'cached-property',
        'psutil',
        # 'dbus-python',
        # 'mpris2',
        # 'pyalsaaudio',
        # 'requests',
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'i3-status-line = i3_status_line.run:main'
        ]
    },
)
