import codecs
import os
import re
import sys

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read(filepath):
    return codecs.open(filepath, "r", "utf-8").read()


def get_entity(package, entity):
    """
    eg, get_entity('spectator', 'version') returns `__version__` value in
    `__init__.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    find = "__%s__ = ['\"]([^'\"]+)['\"]" % entity
    return re.search(find, init_py).group(1)


def get_version():
    return get_entity("spectator", "version")


def get_license():
    return get_entity("spectator", "license")


def get_author():
    return get_entity("spectator", "author")


def get_author_email():
    return get_entity("spectator", "author_email")


# Do `python setup.py tag` to tag with the current version number.
if sys.argv[-1] == "tag":
    os.system("git tag -a %s -m 'version %s'" % (get_version(), get_version()))
    os.system("git push --tags")
    sys.exit()

# Do `python setup.py publish` to send current version to PyPI.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")
    os.system("twine upload dist/django-spectator-%s.tar.gz" % (get_version()))
    sys.exit()

# Do `python setup.py testpublish` to send current version to Test PyPI.
if sys.argv[-1] == "testpublish":
    os.system("python setup.py sdist")
    os.system(
        "twine upload --repository-url https://test.pypi.org/legacy/ dist/django-spectator-%s.tar.gz"  # noqa: E501
        % (get_version())
    )
    sys.exit()

dev_require = [
    "django-debug-toolbar>=2.0,<5.0",
    "flake8>=4.0,<7.0",
    "black",
    "pre-commit",
    "python-dotenv",
    "unittest-parametrize",
]
tests_require = dev_require + [
    "factory-boy>=2.12.0,<4.0",
    "freezegun>=0.3.12,<2.0",
    "coverage[toml]",
]

setup(
    name="django-spectator",
    version=get_version(),
    packages=["spectator"],
    install_requires=[
        "django-imagekit>=4.0,<4.2",
        "hashids>=1.2.0,<1.4",
        "piexif>=1.1.3,<2.0",
        "pillow>=8.0.0,<10.0",
    ],
    dependency_links=[],
    tests_require=tests_require,
    extras_require={"dev": dev_require + ["Django>=4.0,<=4.3"], "test": tests_require},
    include_package_data=True,
    license=get_license(),
    description="A Django app to track book reading, movie viewing, "
    "gig going, play watching, etc.",
    long_description=read(os.path.join(os.path.dirname(__file__), "README.md")),
    long_description_content_type="text/markdown",
    url="https://github.com/philgyford/django-spectator",
    author=get_author(),
    author_email=get_author_email(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords="",
    project_urls={
        "Blog posts": "https://www.gyford.com/phil/writing/tags/django-spectator/",
        "Bug Reports": "https://github.com/philgyford/django-spectator/issues",
        "Documentation": (
            "https://github.com/philgyford/django-spectator/blob/master/README.md"
        ),
        "Source": "https://github.com/philgyford/django-spectator",
    },
)
