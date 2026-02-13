# 📈 CSE Market Intelligence Dashboard v2

**Redesigned, simplified, and error-free version**

## Quick Start

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env with your PostgreSQL password

# Create database
psql -U postgres -c "CREATE DATABASE cse_intelligence;"

# Initialize schema
python setup_database.py
```

### 2. Run ETL
```bash
python main.py
```

### 3. Launch Dashboard
```bash
streamlit run src/dashboard/app.py
```

## Features

✅ Automated ETL pipeline  
✅ UPSERT logic (no duplicate errors)  
✅ Fixed value ranges (no overflow)  
✅ Simple & clean code  
✅ Interactive dashboard  
✅ Error-free execution  

## Project Structure

```
cse-market-intelligence-v2/
├── config/                 # Configuration
├── data/                   # Data directories
├── logs/                   # Application logs
├── sql/schema/             # Database schema
├── src/
│   ├── extractors/         # Data extraction
│   ├── transformers/       # Data transformation
│   ├── loaders/            # Data loading
│   ├── dashboard/          # Streamlit app
│   └── utils/              # Utilities
├── main.py                 # ETL orchestrator
├── setup_database.py       # Database setup
└── requirements.txt        # Dependencies
```

## Tech Stack

- Python 3.8+
- PostgreSQL 12+
- Streamlit
- pandas
- SQLAlchemy

## Notes

This version uses mock data for demonstration. For production, update the extractor with real CSE scraping logic.

---

**Portfolio Project | Data Engineering**
