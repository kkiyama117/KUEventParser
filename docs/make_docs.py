def main():
    """docs作成.

    setup.py に移行したので,廃止します.

    """
    import subprocess

    import warnings

    warnings.warn(PendingDeprecationWarning)
    warnings.warn("deprecated", DeprecationWarning)
    cmd_pre = "pip install sphinx sphinx-rtd-theme"
    cmd_api = "sphinx-apidoc -f -o ./source ../src"
    cmd_doc = "sphinx-build -b html ./source ./build"

    for cmd in [cmd_pre, cmd_api, cmd_doc]:
        result = subprocess.check_output(cmd, universal_newlines=True,
                                         shell=True)
        print(result)


if __name__ == "__main__":
    main()
