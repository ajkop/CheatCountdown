from setuptools import setup

setup(
    name='CheatCountdown',
    install_requires=['flask', 'requests'],
    version='1.1',
    packages=['countdown', 'countdown.frontend', 'countdown.exceptions', 'countdown.api_wrapper'],
    url='https://countdowncheat.com',
    license='MIT',
    author='AJ Kopczynski',
    author_email='',
    description='Little flask app to cheat at countdown, cuz im competitive scum'
)
