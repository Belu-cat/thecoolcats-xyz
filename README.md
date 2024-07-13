# thecoolcats-xyz
This is the source code for my personal website, available at https://thecoolcats.xyz. This guide assumes that you are on Linux.

## Deployment
First, clone this repository
```git clone https://github.com/Belu-cat/thecoolcats-xyz```

Then, set up the virtual enviorment
```
python3 -m venv .venv
. .venv/bin/activate
```

Now, install the requirements
```
pip install -r requirements.txt
```

Run the initial setup script. This script downloads the files in /cta and /cdn-main. It will ask you if you wish to create `start.sh`
```
python3 initsetup.py
```

Now, run the (newly created) `start.sh`
```
chmod +x start.sh
./start.sh
```

or run the server in a development environment
```
flask --app thecoolcats-xyz run
```