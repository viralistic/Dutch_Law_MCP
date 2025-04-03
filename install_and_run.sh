#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing Dutch Legal Assistant...${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

# Make the CLI script executable
chmod +x src/legal_cli.py

echo -e "${GREEN}Installation complete!${NC}"
echo -e "\nYou can now use the legal assistant in two ways:"
echo -e "1. Basic usage: ${BLUE}./src/legal_cli.py 'Your legal situation here'${NC}"
echo -e "2. With detailed information: ${BLUE}./src/legal_cli.py -v 'Your legal situation here'${NC}"
echo -e "\nExample:"
echo -e "${BLUE}./src/legal_cli.py 'Ik word gediscrimineerd op mijn werk vanwege mijn leeftijd'${NC}" 