#!/usr/bin/env bash

function echo_block() {
    echo "----------------------------"
    echo $1
    echo "----------------------------"
}

function final_message() {
    echo_block "Run the script !"
    echo "You can now use the script by executing:"
    echo "'source .env/bin/activate; python3 analyzef1' or"
    echo "'source .env/bin/activate; python3 -m streamlit run analyzef1/Home.py'"
}

function check_installed_pip() {
   ${PYTHON} -m pip > /dev/null
   if [ $? -ne 0 ]; then
        echo_block "Installing Pip for ${PYTHON}"
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        ${PYTHON} get-pip.py
        rm get-pip.py
   fi
}

# Check which python version is installed
function check_installed_python() {
    if [ -n "${VIRTUAL_ENV}" ]; then
        echo "Please deactivate your virtual environment before running setup.sh."
        echo "You can do this by running 'deactivate'."
        exit 2
    fi

    for v in 9 8
    do
        PYTHON="python3.${v}"
        which $PYTHON
        if [ $? -eq 0 ]; then
            echo "using ${PYTHON}"
            check_installed_pip
            return
        fi
    done

    echo "No usable python found. Please make sure to have python3.8 or python3.9 ."
    exit 1
}

function updateenv() {
    echo_block "Updating your virtual env"
    if [ ! -f .env/bin/activate ]; then
        echo "Something went wrong, no virtual environment found."
        exit 1
    fi
    source .env/bin/activate
    SYS_ARCH=$(uname -m)
    echo "pip install in-progress. Please wait..."
    ${PYTHON} -m pip install --upgrade pip
    REQUIREMENTS=requirements.txt

    ${PYTHON} -m pip install --upgrade -r ${REQUIREMENTS}
    if [ $? -ne 0 ]; then
        echo "Failed installing dependencies"
        exit 1
    fi
    echo "pip install completed"
}

function install() {
    if [ -d ".env" ]; then
        echo "- Deleting your previous virtual env"
        rm -rf .env
    fi
    echo
    ${PYTHON} -m venv .env
    if [ $? -ne 0 ]; then
        echo "Could not create virtual environment. Leaving now"
        exit 1
    fi
    updateenv
    final_message
}

function update() {
    git pull
    updateenv
    final_message
}

function help() {
    echo "usage:"
    echo "	-i,--install    Install from scratch"
    echo "	-u,--update     Update requirements."
}

echo_block "Running setup for analyzef1 .. "
check_installed_python

case $* in
--install|-i)
install
;;
--update|-u)
update
;;
*)
help
;;
esac
exit 0