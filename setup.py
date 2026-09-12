"""Setuptools entry point; project metadata lives in pyproject.toml."""

from setuptools import find_packages, setup


if __name__ == "__main__":
    setup(
        package_dir={"": "src"},
        packages=find_packages(where="src"),
    )


# from setuptools import setup, find_packages

# setup(
#     name='vcs',
#     version='0.1',
#     packages=find_packages() + ['utils'],
#     package_dir={'utils': 'utils'},
#     entry_points={
#         'console_scripts': [
#             'vcs = vcs.cli:main',
#         ],
#     },
#     python_requires='>=3.10',
# )

