from distutils.core import setup


with open('README.txt') as file:
    long_description = file.read()
with open('CHANGES.txt') as file:
    long_description += file.read()

setup(
    name="quantity",
    version="0.7.3",
    author="Michael Amrhein",
    author_email="michael@adrhinum.de",
    url="https://pypi.python.org/pypi/quantity",
    description="Unit-safe computations with quantities",
    long_description=long_description,
    packages=['quantity'],
    requires=["decimalfp(>=0.9.11)"],
    install_requires=["decimalfp>=0.9.11"],
    license='BSD',
    keywords='quantity unit',
    platforms='all',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
