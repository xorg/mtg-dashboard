import setuptools


setuptools.setup(
    name='mtg-dashboard',
    version='0.0.1',
    long_description=__doc__,
    packages = ['mtg_dashboard'],
    include_package_data=True,
    zip_safe=False,
    install_requires = ['app']
)

