import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

version_contents = {}
with open(os.path.join(here, "ten99policy", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

setup(
    name="ten99policy",
    version=version_contents["VERSION"],
    description="Python bindings for the ten99policy API",
    long_description_content_type="text/x-rst",
    author="Ray Ventura",
    author_email="support@1099policy.com",
    url="https://github.com/1099policy/1099policy-client-python",
    license="MIT",
    keywords="ten99policy api insurance",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    project_urls={
        "Bug Tracker": "https://github.com/1099policy/1099policy-client-python/issues",
        "Documentation": "https://1099policy.com/docs/api/?lang=python",
        "Source Code": "https://github.com/1099policy/1099policy-client-python",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
