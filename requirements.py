import subprocess


def install_requirements(requirements_file):
    with open(requirements_file, "r") as f:
        packages = f.readlines()
    failed_packages = []
    for package in packages:
        package = package.strip()
        try:
            subprocess.run(["pip", "install", package], check=True)
        except subprocess.CalledProcessError as e:
            failed_packages.append(package)
    return failed_packages


failed = install_requirements("requirements.txt")

if failed:
    print(f"The following packages failed to install: {', '.join(failed)}")
else:
    print("All packages were successfully installed")
