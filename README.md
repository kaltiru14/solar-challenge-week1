# Solar Data Discovery Challenge

## Project Overview
Analysis of solar farm data from Benin, Sierra Leone, and Togo to identify high-potential regions for solar installation.

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-username/solar-challenge-week1.git
cd solar-challenge-week1
```
### 2. Set Up Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n solar-challenge python=3.9
conda activate solar-challenge
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Verify installation
```bash 
python -c "import pandas; print('Setup successful!')"
```

## Project Structure
```bash 
solar-challenge-week1/
├── .github/workflows/    # CI/CD configurations
├── data/                 # Data files (gitignored)
├── notebooks/            # Jupyter notebooks for EDA
├── src/                  # Source code
├── tests/                # Test files
├── scripts/              # Utility scripts
├── app/                  # Streamlit dashboard
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```