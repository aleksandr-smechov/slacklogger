import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="slacklogger",
    version="1.0.0",
    description="Application-level event tracking with Slack",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Aleks Smechov",
    author_email="aleks@smechov.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["slacklogger"],
    include_package_data=True,
    install_requires=["pytz", "requests"],
)
