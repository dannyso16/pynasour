from setuptools import find_packages, setup  # type: ignore

setup(
    name='pynasour',
    version="1.1.1",
    description='chrome dino clone in python 3',
    description_content_type='',
    license='MIT License',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dannyso16/pynasour',
    author='dannyso16',
    packages=find_packages(),
    python_requires='>=3.6.8',
    include_package_data=True,
    package_data={'': ['assets/*']},
    install_requires=['pyxel==1.1.8'],
    entry_points={
        'console_scripts': [
            'pynasour=pynasour.main:main'
        ]
    }
)
