from setuptools import setup

setup(
    name="vdifheader",
    version="0.1",
    description="A simple library for parsing and validating the format and values of VDIF headers in radio telescope data files.",
    author="Mars Buttfield-Addison",
    author_email="hello@themartianlife.com",
    packages=["vdifheader"],
    license="GPLv3+",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
