# 🚀 Arabic Sentiment Analysis Dashboard - Setup & Deployment Guide

## Quick Diagnosis: Common Streamlit Startup Issues

### ❌ Problem: No "Local URL" in terminal when running `streamlit run app.py`

**Causes:**
1. Missing dependencies (transformers, torch, streamlit, pandas, openpyxl)
2. Python environment not properly configured
3. Port conflict (default: 8501)
4. Buffered output preventing display

**Solutions:**

---

## ✅ Complete Installation & Launch Sequence

### Step 1: Clean Install & Environment Setup

Run these commands **in order** in your VS Code PowerShell terminal:

```powershell
# Step 1: Navigate to project directory
cd "c:\Users\alasa\OneDrive\Documents\GitHub\Arabic-Sentiment-Analyzer"

# Step 2: Verify you're in correct directory
Get-Location
# Output should show: ...Arabic-Sentiment-Analyzer

# Step 3: Check if you have a Python venv (optional but recommended)
# If you want to create one:
python -m venv venv
.\venv\Scripts\Activate.ps1

# Step 4: Upgrade pip to latest version
python -m pip install --upgrade pip

# Step 5: Install ALL dependencies from requirements.txt
pip install -r requirements.txt

# Step 6: Verify torch installation (critical for transformers)
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

# Step 7: Verify transformers installation
python -c "import transformers; print(f'Transformers version: {transformers.__version__}')"

# Step 8: Launch Streamlit with unbuffered output
python -u -m streamlit run app.py --client.showErrorDetails=true --logger.level=debug
```

### Step 2: Access the Application

After running the commands above, you should see output like:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Open in browser:** `http://localhost:8501`

---

## 🔧 Troubleshooting - What to Check

### Issue 1: ModuleNotFoundError for 'streamlit'
```
Solution: pip install streamlit==1.31.1
```

### Issue 2: ModuleNotFoundError for 'transformers'
```
Solution: pip install transformers==4.36.2
```

### Issue 3: ModuleNotFoundError for 'torch'
```
Solution: pip install torch==2.1.2 torchvision==0.16.2
```

### Issue 4: Port 8501 already in use
```powershell
# Use different port:
streamlit run app.py --server.port=8502
```

### Issue 5: Model not found (FileNotFoundError)
```
Ensure ./my_final_expert_model_v3 directory exists in:
c:\Users\alasa\OneDrive\Documents\GitHub\Arabic-Sentiment-Analyzer\
```

### Issue 6: Still no URL appearing?
```powershell
# Try with verbose logging:
$env:PYTHONUNBUFFERED=1
python -m streamlit run app.py --logger.level=debug --client.showErrorDetails=true
```

---

## 📋 Complete Dependency List (requirements.txt)

```
transformers==4.36.2
torch==2.1.2
torchvision==0.16.2
streamlit==1.31.1
pandas==2.1.4
openpyxl==3.11.0
selenium==4.15.2
typing-extensions==4.9.0
numpy==1.24.3
accelerate==0.27.0
safetensors==0.4.1
```

---

## ✨ Features Available in the Dashboard

- ✅ **Mock Data Testing**: 15 pre-loaded Arabic comments for immediate testing
- ✅ **Sentiment Analysis**: Positive, Negative, Neutral classification in Arabic
- ✅ **Real-time Progress**: Visual progress bar during analysis
- ✅ **Beautiful UI**: Bilingual interface (Arabic & English)
- ✅ **Data Export**: Download results as Excel file
- ✅ **Summary Statistics**: Total comments, average confidence, min/max scores
- ✅ **Sentiment Distribution**: Bar chart visualization

---

## 🎯 First Run Checklist

- [ ] All 3 Python files created (analyzer.py, scraper.py, app.py)
- [ ] requirements.txt installed successfully
- [ ] Model directory exists: ./my_final_expert_model_v3
- [ ] Model contains: config.json, model.safetensors, tokenizer.json, etc.
- [ ] Terminal shows "Local URL: http://localhost:8501"
- [ ] Browser opens to dashboard successfully
- [ ] Click "Analyze Comments" button with "Use Mock Data" checked
- [ ] See results table with 15 Arabic comments and sentiments
- [ ] Excel export button works and downloads file

---

## 📞 If You Still Have Issues

1. **Check Python Version:** `python --version` (Should be 3.8+)
2. **Check pip version:** `pip --version` (upgrade with: `python -m pip install --upgrade pip`)
3. **Check installed packages:** `pip list | findstr streamlit`
4. **Verify model path:** Test with `Test-Path ".\my_final_expert_model_v3"`
5. **Check file permissions:** Ensure all .py files are readable

---

## 🚀 One-Line Quick Start (After Setup)

```powershell
cd "c:\Users\alasa\OneDrive\Documents\GitHub\Arabic-Sentiment-Analyzer"; python -u -m streamlit run app.py
```

---

## 💡 Pro Tips

1. **Faster Startup**: First run takes longer due to model loading. Subsequent runs are cached.
2. **Mock Data is Pre-Loaded**: Click "Analyze Comments" immediately - no URL needed when "Use Mock Data" is checked
3. **Monitor Console**: Check the PowerShell terminal for detailed error messages
4. **Clear Cache**: If you modify the model, run: `streamlit cache clear`

---

Generated: November 26, 2025
Version: 1.0
