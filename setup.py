from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="smartsort",
    version="1.0.0",
    author="VIDHYA",
    description="An automated file organizer that sorts files by type, watches folders, and supports undo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VIDHYA/smartsort",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "smartsort=smartsort.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
)
