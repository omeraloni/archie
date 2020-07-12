# Archie CLI

> TP-Link Archer C7 CLI
  
Wi-Fi routers tend to get stuck occasionally.  
I made this app so I can schedule a reboot using cron, and practice Poetry and some Python modules such as re, such as Click and CronTab.  

Yes, it's an overkill... 🙃  

## Prerequisites 

Install Poetry: 
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
```  

## Install
```
cd archie-cli
poetry install
poetry build
pip install dist/archie_cli-...-py3-none-any.whl
```

## Run
```
# set router login details
archie config set

# reboot
archie reboot now

# schedule a reboot for 5AM
archie reboot schedule set 05:00

# install a watchdog service (TODO) 
archie watchdog install --host=google.com --period=120

# disable watchdog (TODO)
archie watchdog disable
```

See additional options by running `archie --help`.

# TODO
- [x] Save hashed password.
- [ ] Implement watchdog service.
- [ ] Add tests.
  



