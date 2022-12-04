#/usr/bin/env/ bash 


# one time
virtualenv -p $(which python3) pyenv

# everytime you want to run the server
source pyenv/bin/activate

pip install -r requirements.txt

playwright install
