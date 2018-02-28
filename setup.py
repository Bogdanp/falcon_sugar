import os

from setuptools import Extension, setup


def path_to(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


with open(path_to("falcon_sugar", "__init__.py"), "r") as f:
    version_marker = "__version__ = "
    for line in f:
        if line.startswith(version_marker):
            _, version = line.split(version_marker)
            version = version.strip().strip('"')
            break
    else:
        raise RuntimeError("Version marker not found.")


try:
    from Cython.Distutils import build_ext

    cmdclass = {"build_ext": build_ext}
    ext_modules = [Extension("falcon_sugar.resource", [path_to("falcon_sugar", "resource.py")])]
except ImportError:
    cmdclass = {}
    ext_modules = []


setup(
    name="falcon_sugar",
    version=version,
    description="A little sugar for Falcon.",
    long_description="Visit https://github.com/Bogdanp/falcon_sugar for more information.",
    packages=["falcon_sugar"],
    install_requires=["falcon>=1.4,<2"],
    python_requires=">=3.5",
    extras_require={"marshmallow": ["marshmallow==3.0.0b7"]},
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
