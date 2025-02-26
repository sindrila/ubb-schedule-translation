#!/bin/bash

GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

echo -e "${YELLOW}🔧 Setting up the Python environment...${RESET}"

# Step 1: Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${GREEN}📂 Creating virtual environment...${RESET}"
    python3 -m venv venv
else
    echo -e "${GREEN}✅ Virtual environment already exists.${RESET}"
fi

# Step 2: Activate the virtual environment
echo -e "${YELLOW}🚀 Activating virtual environment...${RESET}"
source venv/bin/activate

# Step 3: Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${RESET}"
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Run the script
echo -e "${YELLOW}🏃 Running database checker...${RESET}"
python main.py

# Step 5: Deactivate virtual environment after script exits
deactivate
echo -e "${GREEN}✅ Finished! Virtual environment deactivated.${RESET}"
