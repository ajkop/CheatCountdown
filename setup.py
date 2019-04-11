from setuptools import setup

setup(
    name='countdown',
    install_requires=['pyenchant', 'requests', 'flask'],
    version='1.0',
    packages=['countdown', 'countdown.frontend', 'countdown.exceptions', 'countdown.api_wrapper'],
    url='http://countdowncheat.com',
    license='MIT',
    author='AJ Kopczynski',
    author_email='',
    description='Little flask app to cheat at countdown'
)
