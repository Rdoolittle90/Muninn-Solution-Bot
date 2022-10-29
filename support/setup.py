def install_packages():
    from sys import executable
    from subprocess import check_call, check_output

    # process output with an API in the subprocess module:
    installed = 0
    with open("requirements.txt", "r") as fin:
        raw = fin.readlines()

    reqs = []
    for lines in raw:
        reqs.append(lines.split('==')[0])

    check_installed = check_output([executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in check_installed.split()]

    for package in reqs:
        if package not in installed_packages:
            check_call([executable, '-m', 'pip', 'install', package])
            installed += 1
            
    print(f"{installed} packges")



if __name__ == "__main__":

    consent = input("This will install the required packages\nwould you like to continue?\n[Y]es [N]o : ")
    if consent.lower() == "y" or consent.lower() == "yes":
        install_packages()
