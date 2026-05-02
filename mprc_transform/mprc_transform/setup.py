from setuptools import setup, find_packages

setup(
    name         = "mprc-transform",
    version      = "1.0.0",
    author       = "Arshad",
    description  = "MPRC Spectral Transform — geometric projection on Z₂₅₆",
    packages     = find_packages(),
    python_requires = ">=3.8",
    install_requires = ["numpy>=1.21"],
    extras_require   = {"test": ["pytest"]},
    classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
