# 🎯 Arabic Sentiment Analysis Dashboard - User Guide

## Launch the App

```powershell
python -u -m streamlit run app.py
```

**Wait for this output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.168.131:8501
```

---

## What You'll See

### Step 1: Dashboard Opens

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│           📊 لوحة تحليل المشاعر العربية              │
│    Arabic Sentiment Analysis Dashboard                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  ⚙️ الإعدادات (Settings)                              │
│  ☑ استخدام البيانات الوهمية (Use Mock Data)         │
│     (Checked by default)                              │
├─────────────────────────────────────────────────────────┤
│  📱 مصدر البيانات (Data Source)                      │
│  ┌─────────────────────────────────────────┐          │
│  │ رابط المنشور (Post URL)                │          │
│  │ https://www.facebook.com/post/...       │          │
│  └─────────────────────────────────────────┘          │
│                                                         │
│  🔧 الخيارات (Options)                               │
│  Mode: 🧪 اختبار (Testing)                           │
│                                                         │
│  [🚀 تحليل التعليقات (Analyze Comments)]             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Step 2: First Run Setup

**What to do:**
1. ✅ Leave "Use Mock Data (Testing)" **CHECKED**
2. ✅ Leave "Post URL" **EMPTY**
3. ✅ Click **"🚀 تحليل التعليقات"** button

**Wait message appears:**
```
✓ تم تحميل 15 تعليق وهمي للاختبار
(Loaded 15 test comments)

[Progress bar: ████████████████████ 100%]
معالجة التعليقات... 15/15
```

---

### Step 3: Analysis Results Display

**After 15-30 seconds, you'll see:**

```
📈 نتائج التحليل (Analysis Results)

┌─────────────────────────────────────────────────────────┐
│ التعليق (Comment)    │ التصنيف │ الثقة  │ Original   │
├─────────────────────────────────────────────────────────┤
│ المنتج رائع جداً     │ إيجابي  │ 0.96  │ POSITIVE   │
│ خدمة ممتازة وسريعة  │ إيجابي  │ 0.94  │ POSITIVE   │
│ تجربة سيئة جداً      │ سلبي    │ 0.91  │ NEGATIVE   │
│ عادي، لا بأس به     │ محايد   │ 0.87  │ NEUTRAL    │
│ [... 11 more rows ...]                                 │
└─────────────────────────────────────────────────────────┘
```

---

### Step 4: Summary Statistics

```
📊 الإحصائيات (Summary Statistics)

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ إجمالي       │ متوسط الثقة  │ أقصى ثقة    │ أدنى ثقة    │
│ التعليقات    │              │              │              │
├──────────────┼──────────────┼──────────────┼──────────────┤
│     15       │   93.67%     │   99.43%     │   81.22%     │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

### Step 5: Sentiment Distribution Chart

```
🎯 توزيع المشاعر (Sentiment Distribution)

   │                              
   │  ███ إيجابي (Positive)
 5 ├─ ███
   │  ███
   │  ███ ███ سلبي (Negative)
 3 ├─ ███ ███
   │  ███ ███ ███ محايد (Neutral)
 1 ├─ ███ ███ ███
   │
   └─────────────────────────
     Positive Negative Neutral

Summary Table:
  التصنيف      العدد
  إيجابي       5
  سلبي         5
  محايد        5
```

---

### Step 6: Download Results

```
💾 التصدير (Export)

[⬇️ تحميل النتائج (Download Results as Excel)]

File downloaded: sentiment_analysis_20251127_100533.xlsx
```

**Excel file contains:**
- **Sheet 1: "Analysis Results"** - All 15 comments with sentiments
- **Sheet 2: "Summary"** - Statistics and export timestamp

---

## Testing Scenarios

### Scenario 1: Quick Test (What You Just Did ✅)
- Time: ~2 minutes
- Result: See all 15 mock comments analyzed
- Use case: Verify installation works

### Scenario 2: Live Social Media (When Ready)
- Uncheck "Use Mock Data"
- Enter real Facebook/Twitter URL
- Click "Analyze"
- **Note:** Requires Selenium WebDriver setup

---

## Sample Data Included

The app comes with 15 realistic Arabic comments:

**Positive (إيجابي) - 5 comments:**
- "المنتج رائع جداً، استمتعت به كثيراً"
- "خدمة ممتازة وسريعة جداً"
- "جودة عالية جداً، ممتاز"
- "أفضل من المنتجات الأخرى"
- "ممتاز جداً وأنصح الجميع به"

**Negative (سلبي) - 5 comments:**
- "تجربة سيئة جداً، لا أنصح به"
- "منتج رديء وخيب آمالي"
- "سيء جداً، لم أعجب به على الإطلاق"
- "الخدمة سيئة والموظفون غير مهتمين"
- "أسوأ عملية شراء قمت بها"

**Neutral (محايد) - 5 comments:**
- "عادي، لا بأس به"
- "المنتج متوسط الجودة"
- "لا أستطيع إعطاء تقييم محدد"
- "مقبول لكن يحتاج تحسينات"
- "المنتج طبيعي وعادي"

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `R` | Rerun the app |
| `C` | Clear cache |
| `Ctrl+C` (Terminal) | Stop the app |

---

## Common Questions

### Q: Why does the first run take longer?
**A:** The app loads the 436 MB ML model from disk on first run. Subsequent runs are much faster (cached in memory).

### Q: Can I use it with real social media links?
**A:** Yes, but you need to:
1. Install ChromeDriver for Selenium
2. Uncheck "Use Mock Data"
3. Enter a valid Facebook/Twitter URL

### Q: How do I export the data?
**A:** Click the blue "⬇️ تحميل النتائج" button. The Excel file downloads automatically.

### Q: Can I add my own comments?
**A:** Currently, the app analyzes comments from URLs or mock data. To add custom comments, modify `scraper.py` `_get_mock_data()` method.

---

## What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit dashboard - **Run this file** |
| `analyzer.py` | Loads model and analyzes text sentiment |
| `scraper.py` | Gets comments from social media or mock data |
| `verify.py` | Checks if everything is installed correctly |
| `requirements.txt` | Lists all Python packages needed |

---

## Next Steps After Testing

1. ✅ Verify mock data analysis works (you're here)
2. ⏭️ Optionally: Set up real social media scraping
3. ⏭️ Optionally: Deploy to cloud (Streamlit Cloud, Docker, etc.)
4. ⏭️ Optionally: Integrate with your backend systems

---

## Get Help

If you encounter issues:

1. **Verify installation:** Run `python verify.py`
2. **Check logs:** Look at terminal output for error messages
3. **Read guides:**
   - `SETUP_GUIDE.md` - Detailed troubleshooting
   - `QUICK_START.md` - Command reference
   - `DEPLOYMENT_COMPLETE.md` - Full status report

---

**Enjoy your Arabic Sentiment Analysis Dashboard! 🎉**

For questions or issues, refer to the documentation files or check the terminal console for detailed error messages.

Generated: November 27, 2025
