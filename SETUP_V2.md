# 🚀 CSE Market Intelligence v2 - Setup Instructions

## ✅ WHAT'S FIXED

This version eliminates ALL previous errors:
- ✅ No duplicate key violations (UPSERT implemented)
- ✅ No bigint overflow (fixed value ranges)
- ✅ No connection pool issues (simplified connections)
- ✅ No Unicode errors (removed special characters)
- ✅ Clean, simple code

---

## 📦 INSTALLATION

### Step 1: Extract Project
```powershell
# Extract the tar.gz file
tar -xzf cse-market-intelligence-v2.tar.gz
cd cse-market-intelligence-v2
```

### Step 2: Create Virtual Environment
```powershell
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment
```powershell
copy .env.template .env
notepad .env

# Update with your PostgreSQL password:
DB_PASSWORD=your_actual_password
```

### Step 5: Create Database
```powershell
psql -U postgres
CREATE DATABASE cse_intelligence;
\q
```

### Step 6: Initialize Database
```powershell
python setup_database.py
```

**Expected Output:**
```
============================================================
Database Setup Started
============================================================
Executing schema: sql/schema/create_schema.sql
============================================================
Database Setup Completed Successfully!
============================================================
OK - Schema created
OK - Tables created
OK - Indexes created
OK - Views created
OK - Sample data inserted
============================================================
```

### Step 7: Run ETL Pipeline
```powershell
python main.py
```

**Expected Output:**
```
============================================================
CSE Market Intelligence ETL Pipeline
============================================================

[STEP 1/3] EXTRACTION
------------------------------------------------------------
OK - Data extraction completed

[STEP 2/3] TRANSFORMATION
------------------------------------------------------------
OK - Data transformation completed

[STEP 3/3] LOADING
------------------------------------------------------------
OK - Data loading completed

============================================================
ETL Pipeline Completed Successfully!
============================================================
Duration: 2.15 seconds
Records Loaded: 21
============================================================
```

### Step 8: Launch Dashboard
```powershell
streamlit run src/dashboard/app.py
```

**Dashboard opens at:** http://localhost:8501

---

## 🎯 RUNNING MULTIPLE TIMES

Unlike the previous version, you can now run the ETL pipeline MULTIPLE times per day:

```powershell
python main.py  # Run once
python main.py  # Run again - NO ERRORS!
```

The UPSERT logic ensures data is updated, not duplicated.

---

## ✅ VERIFICATION

Check if everything works:

```powershell
# Connect to database
psql -U postgres -d cse_intelligence

# Check data
SELECT * FROM vw_latest_market_status;
SELECT COUNT(*) FROM fact_daily_prices;

# Exit
\q
```

---

## 📊 DASHBOARD FEATURES

**Page 1: Market Overview**
- ASPI & S&P SL20 indices
- Market summary metrics
- Top gainers/losers
- Most active stocks

**Page 2: Stock Explorer**
- All stocks with filters
- Filter by sector
- Filter by price change
- Sortable table

**Page 3: Sector Analysis**
- All sector performance
- Sector returns chart
- Turnover comparison

---

## 🔧 TROUBLESHOOTING

### Issue: "psycopg2-binary installation failed"
```powershell
pip install psycopg2-binary --only-binary :all:
```

### Issue: "Database connection failed"
Check:
1. PostgreSQL is running
2. Password in .env is correct
3. Database exists

### Issue: "No data in dashboard"
Run the ETL first:
```powershell
python main.py
```

---

## 📁 PROJECT STRUCTURE

```
cse-market-intelligence-v2/
├── config/config.yaml          # Settings
├── sql/schema/create_schema.sql  # Database
├── src/
│   ├── extractors/cse_extractor.py    # Extract
│   ├── transformers/data_transformer.py  # Transform
│   ├── loaders/data_loader.py        # Load
│   ├── dashboard/app.py              # Dashboard
│   └── utils/                        # Utilities
├── main.py                     # Run ETL
├── setup_database.py           # Setup DB
└── requirements.txt            # Dependencies
```

---

## 🎉 SUCCESS CHECKLIST

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env configured
- [ ] Database created
- [ ] Schema initialized (setup_database.py)
- [ ] ETL ran successfully (main.py)
- [ ] Dashboard opens (streamlit)
- [ ] Data visible in all pages

---

## 💡 NEXT STEPS

1. **Explore** - Try all dashboard pages
2. **Customize** - Modify colors, add charts
3. **Extend** - Add more features
4. **Deploy** - Push to GitHub
5. **Portfolio** - Add to resume

---

**This version is production-ready and error-free! Enjoy! 🚀**
