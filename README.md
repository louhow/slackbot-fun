Google Compute Instance Setup
```bash
# Enable swap space
sudo dd if=/dev/zero of=/swapfile1 bs=1024 count=1048576
sudo chmod 600 /swapfile1
sudo mkswap /swapfile1
sudo swapon /swapfile1
vi /etc/fstab # add the following: /swapfile1 swap swap defaults 0 0
sudo swapon --show # verify swap exists
sudo free -h

# Install docker
sudo apt update
sudo apt install --yes apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt update
sudo apt install --yes docker-ce
sudo usermod -aG docker $USER # make docker runnable without sudo
logout # and log back in
```

First Time Setup
```bash
cp slackbot_settings.py.default slackbot_settings.py # and update
touch core/helpers/spotify_access_token.txt
mkvirtualenv slackbot-fun
workon slackbot-fun
pip install -r requirements.txt
docker stack deploy --compose-file=docker-compose.yml slackbot
yoyo apply --database 'mysql://root:pass@localhost:14306/slackbot-db' ./migrations
```

Running after setup
```bash
workon slackbot-fun
nohup ~/.virtualenvs/slackbot-fun/bin/python run.py &
```