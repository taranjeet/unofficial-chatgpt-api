# ChatGPT api

- It uses playwright and chromium to open browser and parse html.
- It is an unoffical api for development purpose only.

# How to install

- Make sure that python and virual environment is installed.

- Create a new virtual environment

```python
# one time
virtualenv -p $(which python3) pyenv

# everytime you want to run the server
source pyenv/bin/activate
```

- Now install the requirements

```
pip install -r requirements.txt
```

- If you are installing playwright for the first time, it will ask you to run this command for one time only.

```
playwright install
```

👉 The installation can also be done with:

```sh
source install.sh
```

- Now run the server

```sh
python server.py
```

Runnning the server will open a browser window. You need to login to your account the first time you run the server.

👉 A script has been to run the server : `run.sh`.

- The server runs at port `5001`. If you want to change, you can change it in server.py

# Api Documentation

- There is a single end point only. It is available at `/chat`

```sh
curl -XGET http://localhost:5001/chat?q=Write%20a%20python%20program%20to%20reverse%20a%20list
```

# Credit

- All the credit for this script goes to [Daniel Gross's whatsapp gpt](https://github.com/danielgross/whatsapp-gpt) package. I have just taken the script as an individual file and added documentation for how to install and run it.

- Modified by [Raphaël MANSUY](https://www.github.com/raphaelmansuy) to improve the waiting algorithm and to add a script to install and run the server.
