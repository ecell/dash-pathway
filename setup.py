import setuptools

setuptools.setup(
    name="dash-pathway",
    version="0.0.3",
    packages=setuptools.find_packages(),
    install_requires=["dash-cytoscape", "dash", "pathway2cyjs"],
)
