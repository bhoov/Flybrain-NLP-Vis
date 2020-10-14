from setuptools import setup, find_packages

requires = []

setup(
    name="flybrain",
    description="Visualize synapses for context embedding NLP as attentions",
    package_dir={"":"backend"},
    packages=find_packages("backend"),
    license="Apache",
    author="Ben Hoover, Dima Krotov, Leopold Grinberg",
    include_package_data=True,
    install_requires=requires
)