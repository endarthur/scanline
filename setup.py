from setuptools import setup

setup(
    name="scanline",
    version="0.2.1",
    py_modules = ['scanline'],
    entry_points={
        'console_scripts': [
            'scanline = scanline:main',
        ]
    },
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["numpy"],

    # metadata for upload to PyPI
    author="Arthur Endlein",
    author_email="endarthur@gmail.com",
    description="Script for extraction of attitudes from 3d models using meshlab's point picking tool",
    license="MIT",
    keywords="geology attitudes meshlab",
    url="https://github.com/endarthur/scanline",
    dowload_url= "https://github.com/endarthur/scanline/archive/0.2.1.tar.gz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
