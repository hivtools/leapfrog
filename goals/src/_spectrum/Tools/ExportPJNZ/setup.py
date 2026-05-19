from setuptools import find_packages, setup


subpackages = find_packages(where=".")

packages = ["Tools.ExportPJNZ"]
package_dir = {
    "Tools.ExportPJNZ": ".",
}

for package_name in subpackages:
    full_name = f"Tools.ExportPJNZ.{package_name}"
    packages.append(full_name)
    package_dir[full_name] = package_name.replace(".", "/")


setup(
    packages=packages,
    package_dir=package_dir,
    include_package_data=True,
)
