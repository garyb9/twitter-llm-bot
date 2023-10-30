from setuptools import setup
import setuptools_scm

setup(
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    include_package_data=True
)