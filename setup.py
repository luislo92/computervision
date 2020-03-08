from setuptools import setup

setup(
    name='app',
    packages=['vision'],
    include_package_data=True,
    install_requires=[
        'flask', 'cs50', 'werkzeug', 'google', 'pandas'
    ],
)