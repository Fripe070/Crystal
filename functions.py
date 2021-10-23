import os


def getcogs(cogdir: str = None):
    COGS = []  # Makes a empty list named "COGS"

    # If the "cogdir" variable is empty deafult it to "cogs"
    if cogdir is None:
        cogdir = "cogs"
    # If it starts with "cogs" then pass, this could be the case if the user inputs: "cogs/example.py"
    elif cogdir.startswith("cogs"):
        pass
    # If both tests fail set , this could be the case if the user inputs: "cogs/example.py"
    else:
        cogdir = f"cogs/{cogdir}"

    cogdir = cogdir.replace(".", "/")  # Replaces "." with "/"
    cogdir = cogdir.replace("\\", "/")  # Replaces "\" with "/"

    if os.path.isfile(f"{cogdir}.py"):  # If the path provided is a file (aka not a directory)
        return [cogdir.replace("\\", ".").replace("/", ".")]  # Replaces "\" and "/" with "." and returns the file

    for path, subdirs, files in os.walk(cogdir):  # For evcerything in the "dir" directory
        for filename in files:  # For all files in that directory
            if filename.endswith(".py"):  # Makes sure the file is actualy a python file
                # Adds the file to the list named "COGS"
                COGS.append(
                    (os.path.join(path, filename)
                     # Replaces "\" and "/" with "."
                     ).replace("\\", ".").replace("/", ".")[:-3])

    # If there are
    return COGS if COGS != [] else None
