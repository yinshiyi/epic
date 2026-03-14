# sudo apt update
# sudo apt install -y chromium-browser
# sudo apt install -y chromium
# pip install playwright
sudo rm /etc/apt/sources.list.d/yarn.list
sudo apt update
playwright install-deps
playwright install chromium
