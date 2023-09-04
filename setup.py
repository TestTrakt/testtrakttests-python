from setuptools import setup, find_packages,Command

class CleanCommand(Command):
    
    user_options = []
    
setup(
    name="testtrakt-python-tests",
    version="1.0.0",
    packages=find_packages(),
    install_requires=['pytest', 'testtrakt-core-api'],
    python_requires='>=3.6.5',
    cmdclass={'clean': CleanCommand,}
)