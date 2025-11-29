# 🎯 EXACT COMMAND SEQUENCE - Copy & Paste into Terminal

## For First-Time Setup (Complete Clean Install)

Copy and paste each block into PowerShell one at a time:

### Block 1: Navigate and Clean
```powershell
cd "c:\Users\alasa\OneDrive\Documents\GitHub\Arabic-Sentiment-Analyzer"
Get-Location
```

**Wait for response showing directory path**

---

### Block 2: Upgrade Python Tools
```powershell
python -m pip install --upgrade pip setuptools wheel
```

**Wait for completion (2-3 minutes)**

---

### Block 3: Install All Dependencies
```powershell
pip install -r requirements.txt --upgrade
```

**Wait for all packages to complete (5-10 minutes on first run)**

---

### Block 4: Verify Installation
```powershell
python verify.py
```

**Should show all ✓ checkmarks. If any ❌, run Block 3 again**

---

### Block 5: Launch Streamlit Application
```powershell
$env:PYTHONUNBUFFERED=1; python -u -m streamlit run app.py --client.showErrorDetails=true
```

**CRITICAL: Look for:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## Expected Output Timeline

| Action | Time | Expected Output |
|--------|------|-----------------|
| Block 1 | < 1s | Path to directory |
| Block 2 | 1-2 min | "Successfully installed pip" |
| Block 3 | 5-10 min | Multiple packages installing |
| Block 4 | 10-30 sec | Verification checkmarks |
| Block 5 | 20-60 sec | Local URL appears |

---

## Once You See "Local URL: http://localhost:8501"

1. **Open your browser**
2. **Go to:** `http://localhost:8501`
3. **You should see:**
   - Title: "📊 لوحة تحليل المشاعر العربية"
   - Sidebar with "Use Mock Data" checkbox
   - Text input for "Post URL"
   - "Analyze Comments" button

---

## Testing the App (First Run)

1. ✅ Leave "Use Mock Data (Testing)" **checked**
2. ✅ Leave "Post URL" **empty**
3. ✅ Click **"🚀 تحليل التعليقات (Analyze Comments)"**
4. ✅ Wait 10-30 seconds for model to load
5. ✅ See table with 15 Arabic comments and their sentiments
6. ✅ Click **"⬇️ تحميل النتائج"** to download Excel

---

## If Local URL Doesn't Appear

### Troubleshoot with these exact commands (one at a time):

```powershell
# Check Python installation
python --version

# Check pip installation
pip --version

# Check Streamlit specifically
pip show streamlit

# Check if Streamlit can import
python -c "import streamlit as st; print(f'Streamlit {st.__version__}')"

# Run verification script
python verify.py

# Try launching with verbose errors
$env:PYTHONUNBUFFERED=1; python -m streamlit run app.py --logger.level=debug
```

---

## If You Get a PORT ERROR

```powershell
# Use port 8502 instead
python -u -m streamlit run app.py --server.port=8502

# Then open: http://localhost:8502
```

---

## Windows Firewall Issue (Rare)

If Windows Firewall blocks the port:
```powershell
# Allow Python through firewall (run as Administrator)
netsh advfirewall firewall add rule name="Python" dir=in action=allow program="C:\Users\alasa\AppData\Local\Programs\Python\Python311\python.exe"
```

---

## To Stop the App

Press `Ctrl+C` in the PowerShell terminal

---

## To Relaunch (After Stopping)

```powershell
python -u -m streamlit run app.py
```

---

## Quick Reference: All Files Created

✅ `analyzer.py` - Sentiment analysis engine
✅ `scraper.py` - Comment scraper with mock data
✅ `app.py` - Streamlit dashboard (REWRITTEN for robustness)
✅ `requirements.txt` - All dependencies
✅ `verify.py` - Diagnostic verification script
✅ `SETUP_GUIDE.md` - Detailed troubleshooting guide
✅ `QUICK_START.md` - This file

---

## Support Checklist

- [ ] Python 3.8+ installed
- [ ] requirements.txt installed
- [ ] Model directory exists with files
- [ ] verify.py shows all ✓
- [ ] Local URL appears in terminal
- [ ] Browser opens to http://localhost:8501
- [ ] "Use Mock Data" is checked
- [ ] "Analyze" button shows results
- [ ] Excel download button works

---

**Generated:** November 26, 2025
**Version:** 1.0 - Ready for Production
