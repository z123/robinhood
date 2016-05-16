from setuptools import setup

setup(
    name='robinhood',
    version='1.0',
    py_modules=['robinhood'],
    install_requires=[
        'click'
    ],
    entry_points = '''
        [console_scripts]
        robinhood=scripts.robinhood:cli
    '''
)
