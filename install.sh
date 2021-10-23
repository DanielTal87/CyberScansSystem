#!/bin/bash

red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

echo "${blue}At-bay - Cyber Scans System${reset}"

# ====================
# Install Dependencies
# ====================
echo "${green}Installing Requirements${reset}"
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
  echo "${green}Installing requirements succeeded${reset}"
else
  echo "${red}Installing requirements failed, please install major: $version${reset}"
  exit 1
fi

brew install redis

# =====================
# Update Scripts Access
# =====================

chmod 775 run.sh

echo "${blue}Installing Cyber Scans System finished successfully${reset}"
