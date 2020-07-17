# Archie CLI

> TP-Link Archer C7 command line interface
  
Wi-Fi routers tend to get stuck occasionally.  
I made this app so I can schedule a reboot using cron, and practice Poetry and some Python modules such as re, Click and CronTab.  

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
archie-cli config set

# show config
archie-cli config show

# reboot
archie-cli reboot now

# schedule a reboot for 5AM
archie-cli reboot schedule set 05:00

# install a watchdog service (ping google.com every 2min over wlan0) 
archie-cli watchdog install --interface=wlan0 --host=google.com --period=2

# uninstall watchdog
archie-cli watchdog uninstall
```

See additional options by running `archie --help`.

# TODO
- [x] Save hashed password.
- [ ] Implement watchdog service.
- [ ] Add tests.
- [ ] Hanlde cron environment issues.
  



