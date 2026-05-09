from setuptools import setup, find_packages

setup(
    name="minimessage-rich",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
    ],
    author="LGRY",
    description="A Rich extension for parsing Minecraft's MiniMessage format",
    python_requires=">=3.7",
)
