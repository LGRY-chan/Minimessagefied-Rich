from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="minimessage-rich",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
    ],
    author="LGRY",
    author_email="your-email@example.com",  # Placeholder
    description="A Rich extension for parsing Minecraft's MiniMessage format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LGRY/Minimessagefied-Rich",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
