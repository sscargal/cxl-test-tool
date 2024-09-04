import utils.tools as tools
import os

# start: below are rasdaemon related
def install_rasdaemon(url="https://github.com/moking/rasdaemon-clone", branch="scrub_control", dire="~/rasdaemon"):
    cmd="install rasdaemon..."
    print(cmd)

    if tools.path_exist_on_vm(dire):
        choice=input("%s exists, delete it before git clone (Y/N): "%dire)
        if choice and choice.lower() == "y":
            cmd="rm -rf %s"%dire
            tools.execute_on_vm(cmd, echo=True)
            cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
            tools.execute_on_vm(cmd, echo=True)
    else:
            cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
            tools.execute_on_vm(cmd, echo=True)

    cmd="cd %s; bash ./run-me.sh ; ls rasdaemon -lh"%(dire)
    tools.execute_on_vm(cmd, echo=True)
    cmd="rasdaemon"
    tools.execute_on_vm(cmd, echo=True)


def install_mce_inject(url="https://git.kernel.org/pub/scm/utils/cpu/mce/mce-inject.git",
                   branch="master", dire="~/mce-inject"):

    cmd="install mce inject"
    print(cmd)
    if tools.path_exist_on_vm(dire):
        choice=input("%s exists, delete it before git clone (Y/N): "%dire)
        if choice and choice.lower() == "y":
            cmd="rm -rf %s"%dire
            tools.execute_on_vm(cmd, echo=True)
            cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
            tools.execute_on_vm(cmd, echo=True)
    else:
            cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
            tools.execute_on_vm(cmd, echo=True)

    if tools.package_installed_on_vm("flex"):
        tools.install_packages_on_vm("flex")

    cmd="cd %s; make"%dire
    tools.execute_on_vm(cmd, echo=True)


def install_mce_test(url="https://git.kernel.org/pub/scm/linux/kernel/git/gong.chen/mce-test.git", branch="master", dire="~/mce-test"): 
    cmd="install mce test"
    print(cmd)

    if tools.path_exist_on_vm(dire):
        choice=input("%s exists, delete it before git clone (Y/N): "%dire)
        if choice and choice.lower() == "y":
            cmd="rm -rf %s"%dire
            tools.execute_on_vm(cmd, echo=True)
            cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
            tools.execute_on_vm(cmd, echo=True)
    else:
        cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
        tools.execute_on_vm(cmd, echo=True)

    cmd="cd %s; make"%dire
    tools.execute_on_vm(cmd, echo=True)


def install_aer_inject(url="https://git.kernel.org/pub/scm/linux/kernel/git/gong.chen/aer-inject.git", branch="master", dire="~/aer-inject"):
    cmd="install aer inject"
    print(cmd)

    if tools.path_exist_on_vm(dire):
        choice=input("%s exists, delete it before git clone (Y/N): "%dire)
        if choice and choice.lower() == "y":
            cmd="rm -rf %s"%dire
            tools.execute_on_vm(cmd, echo=True)
            cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
            tools.execute_on_vm(cmd, echo=True)
    else:
        cmd="git clone -b %s --single-branch %s %s"%(branch, url, dire)
        tools.execute_on_vm(cmd, echo=True)

    cmd="cd %s; make"%dire
    tools.execute_on_vm(cmd, echo=True)


def install_ras_tools():
    install_rasdaemon();
    install_mce_inject()
    install_mce_test()
    install_mce_test()


def inject_aer(file, aer_tool_path="~/aer-inject"):
    print("Job: inject aer")
    if not os.path.exists(file):
        print("EINJ config file not found!")
        print("Example files can be found in einj-examples under the tool directory")
        return

    tools.copy_to_remote(src=file, dst="/tmp/aer.input")
    cmd="dmesg -C"
    tools.execute_on_vm(cmd, echo=True)
    cmd="cd %s; ./aer-inject /tmp/aer.input"%aer_tool_path
    tools.execute_on_vm(cmd, echo=True)
    cmd="dmesg"
    tools.execute_on_vm(cmd, echo=True)
