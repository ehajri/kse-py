from setuptools import setup

setup(
    name='StockExchange',
    version='1.0',
    py_module=['stockexchange'],
    install_requires=[
        'Click',
        'SQLAlchemy',
        'PyMySQL'
    ],
    entry_points='''
        [console_scripts]
        stock=brain:cli
    '''
)
