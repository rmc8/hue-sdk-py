from setuptools import setup, find_packages

setup(
    version="0.0.1",
    name="hue-sdk-py",
    description="Python client for Philips Hue",
    license="MIT",
    author="Kohei Miyashita",
    author_email="k@rmc-8.com",
    install_requires=["requests", "ColorPy", "PyYaml"],
    url="https://github.com/rmc8/hue-sdk-py",
    keywords=["Hue", "Philips", "SDK"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "hueconn = hue.conn:main",
        ],
    },
)
