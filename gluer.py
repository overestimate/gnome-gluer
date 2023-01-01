# gluer - basic launcher icon generator for gluon.
# (c) 2022- overestimate. MIT license.
#
# if you want to add another format (shell script, windows icon, macOS .app)
# feel free to make a fork and add it. was designed to be extended but i only
# made what i needed to use and put that out. have fun.

# script-wide vars.
import os
import sys
DEBUG: bool = True
MODES: list[str] = [  # a list of valid generator modes.
    "gnome"
]


# nabbed from chestnut, MIT license but not out yet
RESET: str = "\033[0m"
LOG_PREFIX: str = "[\033[38;2;20;72;220mgluer\033[0m]"


def debug(*args: list, sep: str = " ") -> None:
    if not DEBUG:
        return
    print(
        f"{LOG_PREFIX}\033;32m debug: {sep.join([str(a) for a in args])}\033[0m")


def warn(*args: list, sep: str = " ") -> None:
    print(
        f"{LOG_PREFIX}\033[31;33m warn: {sep.join([str(a) for a in args])}\033[0m")


def error(*args: list, sep: str = " ") -> None:
    print(
        f"{LOG_PREFIX}\033[31;91m error: {sep.join([str(a) for a in args])}\033[0m")


def info(*args: list, sep: str = " ") -> None:
    print(
        f"{LOG_PREFIX}\033[31;90m info: {sep.join([str(a) for a in args])}\033[0m")


def print_valid_modes(
) -> None: info(f"valid modes are: {' | '.join([m for m in MODES])}")


if len(sys.argv) < 2:
    error("pass a mode!")
    print_valid_modes()
    exit(1)

# mode validation
if sys.argv[1] not in MODES:
    error(f"invalid mode - {sys.argv[1]}")
    print_valid_modes()
    exit(2)

# gets an icon and saves to a path, returning said path. returns None if something failed.


def get_icon(url: str) -> str | None:
    # portable enough, if you're running a non-POSIX-path-compliant windows version you'll have more isuses than just this.
    if not os.path.exists("./icons"):
        os.mkdir("./icons")
    favicon_url = f"https://www.google.com/s2/favicons?sz=256&domain_url={url}"

    import re
    domain = re.match(
        '(https:?\/\/)[a-zA-Z0-9\-\_\.]*', url).group().split("//")[1]

    if os.path.exists(f"./icons/{domain}.png"): return f"./icons/{domain}.png"
    import requests

    response = requests.get(favicon_url)
    with open(f"./icons/{domain}.png", 'wb') as f:
        f.write(response.content)
    return f"./icons/{domain}.png"


def create_node(name: str, url: str):
    name_safe = name.replace(' ', '_')
    print(name)
    print(name_safe)
    if not os.path.exists(f"./{name_safe}_gluer"):
        os.mkdir(f"./{name_safe}_gluer")
    with open(f"./{name_safe}_gluer/index.js", 'w') as f:
        # trims whitespace and adds a line feed.
        def trim_and_lf(i: str) -> str: return i.strip() + "\n"
        f.write(trim_and_lf(f"const URL_TO_LOAD = '{url}';                    ") +
                trim_and_lf("import * as Gluon from '@gluon-framework/gluon';") +
                trim_and_lf("Gluon.open(URL_TO_LOAD);                        ")
                )
    with open(f"./{name_safe}_gluer/package.json", 'w') as f:
        data = {
            "name": "gluon_template_application",
            "version": "1.0.0",
            "description": "Minimal gluon wrapper used with gluer.",
            "main": "index.js",
            "author": "overestimate",
            "license": "MIT",
            "type": "module"
        }
        f.write(str(data).replace("'", '"'))  # lmao
    with open(f"./{name_safe}_gluer/install.sh", 'w') as f:
        data = (
            trim_and_lf('#!/usr/bin/bash                            ') +
            trim_and_lf('APP_PATH="$( dirname -- "$0"; )"         ') +
            trim_and_lf('cp -R "$APP_PATH" "$HOME/.local/bin"') +
            trim_and_lf(f'cp "{name_safe}_gluer.desktop" "$HOME/.local/share/applications"')
        )
        f.write(data)
    import shutil
    shutil.copyfile(get_icon(url), f"./{name_safe}_gluer/icon.png")
# generate a GNOME icon file. out is the output filename. if out is None,
# auto-generate a filename using the scheme {NAME}_gluer.desktop


def gen_linux_gnome(name: str, url: str) -> None:
    name_safe = name.replace(' ', '_')
    home = os.environ["HOME"]
    create_node(name, url)
    # trims whitespace and adds a line feed.
    def trim_and_lf(i: str) -> str: return i.strip() + "\n"
    # some odd padding, used only here in source code. each line
    # has a newline appended using the previously defined function.
    template = trim_and_lf("[Desktop Entry]")
    template += trim_and_lf(f"Name={name}")
    template += trim_and_lf("Type=Application")
    template += trim_and_lf("Exec=/usr/bin/node {home}/.local/bin/{name_safe}_gluer/index.js")
    template += trim_and_lf(f"Icon={home}/.local/bin/{name_safe}_gluer/icon.png")
    template += trim_and_lf(f"Path={home}/.local/bin/{name_safe}_gluer")

    out = f"{name}_gluer.desktop"
    with open(out, 'w') as f:
        f.write(template)
    import shutil
    shutil.copyfile(out, f"{home}/.local/applications/{name_safe}_gluer.desktop")

if len(sys.argv[2:]) % 2 != 0:
    error("pass in an url and a name!")
    exit(2)

for i in range(2, len(sys.argv[2:])+2, 2):
    url = sys.argv[i]
    name = sys.argv[i+1]
    gen_linux_gnome(name, url)
