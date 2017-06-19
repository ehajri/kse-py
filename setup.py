from setuptools import setup

setup(name='kse_project',
      version='0.1.0',
      packages=['kse_project'],
      entry_points={
          'console_scripts': [
              'kse_project = kse.__main__:main'
          ]
      },
      )
