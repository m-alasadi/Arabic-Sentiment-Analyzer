# 🤖 Active Learning Retraining Script Guide

**Script Name:** `retrainer.py`  
**Purpose:** Fine-tune the Arabic sentiment model using corrections collected in `active_learning_data.csv`  
**Status:** ✅ Ready to use

---

## Quick Start

### Prerequisites
Ensure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Basic Command (Recommended)

```powershell
python retrainer.py
```

This will:
1. Load the model from `./my_final_expert_model_v3`
2. Load corrections from `active_learning_data.csv`
3. Fine-tune for **3 epochs** (default)
4. Save the updated model to `./my_updated_expert_model_v4`

---

## Advanced Usage

### Custom Parameters

```powershell
python retrainer.py `
  --model-dir "./my_final_expert_model_v3" `
  --output-dir "./my_updated_expert_model_v4" `
  --csv "active_learning_data.csv" `
  --epochs 2 `
  --batch-size 8 `
  --learning-rate 2e-5 `
  --max-length 256
```

### Parameter Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--model-dir` | `./my_final_expert_model_v3` | Path to original pre-trained model |
| `--output-dir` | `./my_updated_expert_model_v4` | Where to save fine-tuned model |
| `--csv` | `active_learning_data.csv` | Training data file with corrections |
| `--epochs` | `3` | Number of training epochs (recommended: 1-3) |
| `--batch-size` | `8` | Batch size (8-16 for GPU, 2-4 for CPU) |
| `--learning-rate` | `2e-5` | Learning rate (typical: 1e-5 to 5e-5) |
| `--max-length` | `256` | Maximum token length for texts |

---

## Workflow: From Feedback to Deployment

### Step 1: Collect Feedback via Streamlit App
```powershell
streamlit run app.py
```
- Analyze comments/news
- Scroll to "✍️ Manual Correction & Active Learning Feedback"
- Select misclassified entries and correct them
- Click "💾 Save Correction to Training Data"
- Corrections auto-saved to `active_learning_data.csv`

### Step 2: Review Collected Corrections (Optional)
```powershell
# View first 10 corrections
Get-Content .\active_learning_data.csv | Select-Object -First 10

# Or in PowerShell:
Import-Csv .\active_learning_data.csv | Format-Table -AutoSize
```

### Step 3: Run Fine-tuning Script
```powershell
python retrainer.py
```

**Expected Output:**
```
======================================================================
🤖 ACTIVE LEARNING RETRAINING PIPELINE
======================================================================

======================================================================
Step: Load Model
======================================================================
✓ Using device: cuda (or cpu)
✓ Tokenizer loaded (30522 tokens)
✓ Model loaded (3 labels)
  - Model type: bert
  - Hidden size: 768
  - Num layers: 12

======================================================================
Step: Load Training Data
======================================================================
✓ Loaded 25 training samples
  - Unique labels: ['إيجابي', 'محايد', 'سلبي']
  - Label distribution:
    • إيجابي: 12
    • سلبي: 8
    • محايد: 5

✓ Created dataloader (4 batches)

======================================================================
Step: Fine-tune
======================================================================
🚀 Starting fine-tuning (3 epochs)
   Learning rate: 2e-05
   Batch size: 8

📍 Epoch 1/3
Training: 100%|████████| 4/4 [00:15<00:00, 3.82s/batch]
   Loss: 0.8234

📍 Epoch 2/3
Training: 100%|████████| 4/4 [00:14<00:00, 3.51s/batch]
   Loss: 0.5821

📍 Epoch 3/3
Training: 100%|████████| 4/4 [00:13<00:00, 3.25s/batch]
   Loss: 0.3147

✓ Fine-tuning complete!

======================================================================
Step: Save Model
======================================================================
💾 Saving model to: ./my_updated_expert_model_v4
   ✓ Model weights saved
   ✓ Tokenizer saved
   ✓ Label mapping saved: {0: 'محايد', 1: 'سلبي', 2: 'إيجابي'}
   ✓ Metadata saved

✅ Model successfully saved to: C:\...\my_updated_expert_model_v4

======================================================================
✅ PIPELINE COMPLETED SUCCESSFULLY!
======================================================================

📌 Next Steps:
   1. Update analyzer.py to load from: ./my_updated_expert_model_v4
   2. Or update app.py line ~95: model_path = './my_updated_expert_model_v4'
   3. Restart Streamlit: streamlit run app.py
```

### Step 4: Deploy Updated Model
**Option A:** Update `analyzer.py` (default model path)
```python
# analyzer.py, line ~30
def __init__(self, model_path: str = "./my_updated_expert_model_v4"):
    # ... rest of code
```

**Option B:** Update `app.py` (inline override)
```python
# app.py, line ~95
model_path = "./my_updated_expert_model_v4"
```

### Step 5: Restart App with New Model
```powershell
streamlit run app.py
```

Now the app uses the fine-tuned model with improved accuracy from your corrections!

---

## Output Files

After running `retrainer.py`, the `./my_updated_expert_model_v4` directory contains:

```
my_updated_expert_model_v4/
├── config.json                 # Model configuration
├── model.safetensors           # Fine-tuned weights (safe format)
├── tokenizer.json              # Tokenizer vocab
├── tokenizer_config.json       # Tokenizer config
├── special_tokens_map.json     # Special tokens
├── vocab.txt                   # Vocabulary
├── label_mapping.json          # Label ID mappings (NEW)
└── metadata.json               # Training metadata (NEW)
```

### Label Mapping Example (label_mapping.json)
```json
{
  "0": "محايد",
  "1": "سلبي",
  "2": "إيجابي"
}
```

### Training Metadata Example (metadata.json)
```json
{
  "created": "2025-11-28T14:35:22.123456",
  "source_model": "./my_final_expert_model_v3",
  "training_epochs": 3,
  "learning_rate": 2e-5,
  "batch_size": 8,
  "max_length": 256,
  "device": "cuda",
  "training_samples": 25,
  "model_type": "bert",
  "num_labels": 3,
  "label_mapping": {"0": "محايد", "1": "سلبي", "2": "إيجابي"}
}
```

---

## Common Scenarios

### Scenario 1: Fresh Start (Few Corrections)
```powershell
# Minimum training (1 epoch to avoid overfitting on small dataset)
python retrainer.py --epochs 1
```

### Scenario 2: Many Corrections (50+ samples)
```powershell
# Standard fine-tuning (3 epochs)
python retrainer.py --epochs 3
```

### Scenario 3: GPU with Large Batch
```powershell
# Optimize for GPU acceleration
python retrainer.py --batch-size 16 --epochs 3
```

### Scenario 4: CPU-Only (Slower but works)
```powershell
# Reduce batch size for CPU
python retrainer.py --batch-size 4 --epochs 2
```

### Scenario 5: Custom Model Path
```powershell
# If you want different source/output directories
python retrainer.py `
  --model-dir "./my_final_expert_model_v3" `
  --output-dir "./my_production_model_v4" `
  --csv "my_custom_corrections.csv"
```

---

## Troubleshooting

### Error: "active_learning_data.csv not found"
**Solution:** Ensure you've collected at least one correction via the Streamlit app:
1. Run `streamlit run app.py`
2. Analyze comments
3. Scroll to "Manual Correction & Active Learning Feedback"
4. Click "Save Correction to Training Data"
5. Run `retrainer.py` again

### Error: "Model directory not found: ./my_final_expert_model_v3"
**Solution:** Verify model exists:
```powershell
# Check if model dir exists
Test-Path "./my_final_expert_model_v3"

# List its contents
Get-ChildItem "./my_final_expert_model_v3"
```

### Error: "CUDA out of memory"
**Solution:** Reduce batch size:
```powershell
python retrainer.py --batch-size 4
```

### Error: "No module named 'transformers'"
**Solution:** Install dependencies:
```powershell
pip install -r requirements.txt
```

### Slow Training on CPU
**Solution:** This is expected. Training 3 epochs on CPU may take 5-10 minutes. To speed up:
```powershell
# Reduce epochs or batch size
python retrainer.py --epochs 1 --batch-size 2
```

---

## Performance Tips

### For Faster Training
1. **Use GPU** (if available): Script auto-detects CUDA
2. **Increase batch size** (if memory allows):
   ```powershell
   python retrainer.py --batch-size 16
   ```
3. **Reduce epochs** (if dataset is small):
   ```powershell
   python retrainer.py --epochs 1
   ```

### For Better Accuracy
1. **Collect more corrections** (50+ samples recommended)
2. **Balanced labels** (equal distribution of positive/negative/neutral)
3. **Use 3 epochs** for better convergence:
   ```powershell
   python retrainer.py --epochs 3
   ```

### For Preventing Overfitting
1. **Keep learning rate low** (default 2e-5 is good):
   ```powershell
   python retrainer.py --learning-rate 1e-5
   ```
2. **Don't over-train** on small datasets:
   ```powershell
   python retrainer.py --epochs 1  # For <20 samples
   ```
3. **Use gradient clipping** (already built-in)

---

## Script Architecture

### Key Classes

**SentimentDataset**
- Converts CSV data to PyTorch tensors
- Handles tokenization and padding
- Manages label encoding

**SentimentRetrainer**
- Orchestrates the fine-tuning pipeline
- Handles model loading/saving
- Manages training loop
- Implements error handling and logging

### Pipeline Steps

1. **Load Model** → Loads pre-trained model + tokenizer
2. **Load Training Data** → Reads CSV, validates, tokenizes
3. **Fine-tune** → Runs training loop with Adam optimizer
4. **Save Model** → Saves weights, tokenizer, metadata

---

## Integration with Existing Code

### Update analyzer.py
To make the app automatically use the new model:

```python
# analyzer.py line ~30
def __init__(self, model_path: str = "./my_updated_expert_model_v4"):
    self.model_path = model_path
    # ... rest unchanged
```

### Or Keep Both Models
Keep using v3 for production, load v4 for testing:

```python
# app.py
# For production
# model_path = "./my_final_expert_model_v3"

# For testing updated model
model_path = "./my_updated_expert_model_v4"
```

---

## Data Format Reference

### active_learning_data.csv Format
```csv
text,label
"هذا منتج رائع جداً!",إيجابي
"تجربة سيئة جداً مع الخدمة",سلبي
"المنتج عادي، لا بأس به",محايد
```

### Custom Label Example
```csv
text,label
"النص هنا",custom_label_1
```

The script auto-maps any labels in the CSV file.

---

## Next Steps After Fine-tuning

1. **Test the updated model** using the Streamlit app
2. **Collect more feedback** if accuracy is still not satisfactory
3. **Iterate:** More corrections → Retrain → Evaluate
4. **Archive old model** if satisfied with v4
5. **Version control:** Commit updated model to git (or .gitignore for size)

---

## Support & Questions

- **Slow training?** Use `--epochs 1` for quick testing
- **Out of memory?** Reduce `--batch-size` to 2-4
- **Model not improving?** Ensure corrections are high-quality and labels are consistent
- **Script crashes?** Check Python version (3.8+) and library versions

---

**Last Updated:** November 28, 2025  
**Script Version:** 1.0  
**Python:** 3.8+  
**Status:** Production Ready ✅
