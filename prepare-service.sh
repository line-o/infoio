sudo cp ./infoschild.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/infoschild.service
sudo systemctl daemon-reload
sudo systemctl enable infoschild.service