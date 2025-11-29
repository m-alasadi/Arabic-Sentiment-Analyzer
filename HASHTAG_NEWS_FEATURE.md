# 📰 Hashtag & News Analysis Feature - Implementation Complete

**Date:** November 27, 2025  
**Version:** 2.0  
**Status:** ✅ Ready for Testing

---

## 🎯 What's New

The Arabic Sentiment Analysis Dashboard now includes a **Hashtag & News Analysis** feature alongside the original Post URL Analysis mode.

### Two Analysis Modes:

1. **📱 Post URL Analysis** (Original)
   - Analyze comments from social media posts
   - Supported platforms: Facebook, Twitter/X, Instagram
   - Mock data with 15 Arabic comments

2. **🏷️ Hashtag News Analysis** (NEW)
   - Search for news articles related to a hashtag/topic
   - Analyze sentiment of news headlines
   - Predefined mock datasets for quick testing

---

## 📦 Files Updated

### 1. `requirements.txt`
**Changes:**
- ✅ Added `requests>=2.31.0` - HTTP library for web requests
- ✅ Added `beautifulsoup4>=4.12.0` - HTML/XML parsing library

**Full dependency list:**
```
transformers>=4.40.0
torch>=2.9.0
torchvision>=0.18.0
streamlit>=1.31.0
pandas>=2.1.0
openpyxl>=3.1.0
selenium>=4.15.0
requests>=2.31.0          ← NEW
beautifulsoup4>=4.12.0    ← NEW
typing-extensions>=4.9.0
numpy>=1.24.0
accelerate>=0.27.0
safetensors>=0.4.1
```

### 2. `scraper.py`
**New Methods Added:**

#### `scrape_hashtag_news(hashtag_query: str) -> List[Dict[str, Any]]`
- **Purpose:** Scrape news articles related to a hashtag/topic
- **Input:** Arabic hashtag (e.g., "بغداد" or "#بغداد")
- **Output:** List of dictionaries with `text` (headline) and `source` (URL)
- **Features:**
  - Mock data for 5 Arabic topics:
    - بغداد (Baghdad)
    - الاقتصاد (Economy)
    - التكنولوجيا (Technology)
    - الرياضة (Sports)
    - الصحة (Health)
  - Each topic has 5 realistic news headlines
  - Fallback to economy news if topic not found
  - Template for real API integration (NewsAPI, Google News, etc.)

#### `_fetch_real_news(hashtag_query: str) -> List[Dict[str, Any]]`
- **Purpose:** Template for real news fetching
- **Note:** Placeholder for production integration with:
  - NewsAPI.org
  - Google News API
  - Bing News Search API

---

### 3. `app.py` (Major Rewrite)
**New Features:**

#### Analysis Mode Selection
- **Radio button** to switch between two modes
- Horizontal layout for better UX
- Emojis for visual distinction

#### Post URL Analysis Mode (Original)
- Unchanged from v1.0
- Analyzes social media comments
- Shows sentiment distribution with charts

#### Hashtag News Analysis Mode (NEW)
- **Input:** Arabic hashtag/topic field
- **Process:**
  1. User enters hashtag (e.g., "بغداد" or "#بغداد")
  2. Scraper retrieves 5 relevant news articles
  3. SentimentAnalyzer processes each headline
  4. Results displayed in table with sentiment labels
- **Output:**
  - Headline text
  - Source URL
  - Sentiment classification (إيجابي/سلبي/محايد)
  - Confidence score

#### Enhanced UI Components
- Separate processing functions: `process_news_articles()`
- Flexible summary statistics: `create_summary_stats()` handles both modes
- Updated export function with dynamic sheet names

---

## 🎨 User Interface Changes

### Before (v1.0)
```
┌─────────────────────────────────┐
│  Post URL Analysis Only          │
│  - URL input field               │
│  - Single "Analyze" button        │
└─────────────────────────────────┘
```

### After (v2.0)
```
┌─────────────────────────────────┐
│  📱 Post URL | 🏷️ Hashtag News  │  ← Radio Selection
├─────────────────────────────────┤
│  Mode 1: Post URL Analysis       │
│  - URL input field               │
│  - "Analyze Comments" button     │
│                                  │
│  Mode 2: Hashtag News Analysis   │
│  - Hashtag/Topic input field     │
│  - "Analyze News" button         │
├─────────────────────────────────┤
│  Both modes: Results, Stats,     │
│  Charts, Excel Export            │
└─────────────────────────────────┘
```

---

## 📊 Mock News Data Structure

### Available Topics:

**1. بغداد (Baghdad)**
```python
{
    'text': 'بغداد تشهد أحداث سياسية مهمة في البرلمان العراقي',
    'source': 'https://news-ar.com/baghdad-politics-2025'
}
```
- 5 headlines about Baghdad politics, conferences, economy, development, security

**2. الاقتصاد (Economy)**
```python
{
    'text': 'الأسواق العربية تشهد تحسناً في الأداء الاقتصادي',
    'source': 'https://bloomberg-ar.com/markets'
}
```
- 5 headlines about Arab markets, investments, inflation, expansion

**3. التكنولوجيا (Technology)**
```python
{
    'text': 'ثورة التكنولوجيا: الذكاء الاصطناعي يغير المشهد الاقتصادي',
    'source': 'https://tech-news-ar.com/ai-2025'
}
```
- 5 headlines about AI, blockchain, digital infrastructure, cybersecurity, fintech

**4. الرياضة (Sports)**
```python
{
    'text': 'دوري الكرة العراقي يشهد منافسة قوية بين الفرق الكبرى',
    'source': 'https://sports-ar.com/iraq-league'
}
```
- 5 headlines about Iraqi league, national team, transfers, tournaments

**5. الصحة (Health)**
```python
{
    'text': 'وزارة الصحة تطلق حملة توعوية جديدة حول الأمراض المزمنة',
    'source': 'https://health-gov.iq/campaign'
}
```
- 5 headlines about health campaigns, medical research, mental health, hospitals

---

## 🧪 Testing the New Feature

### Quick Test 1: Hashtag Analysis with Mock Data
```
1. Open: http://localhost:8501
2. Select: 🏷️ Hashtag News Analysis
3. Enter: "بغداد" or "#بغداد"
4. Click: 🚀 تحليل الأخبار
5. See: 5 Baghdad news articles with sentiment analysis
6. Export: Download as Excel with Summary sheet
```

### Quick Test 2: Different Topics
Try these hashtags:
- `الاقتصاد` → Economy news
- `التكنولوجيا` → Technology news
- `الرياضة` → Sports news
- `الصحة` → Health news

### Expected Results:
- **Headlines:** Display realistic Arabic news
- **Sentiments:** Mix of positive, negative, neutral
- **Scores:** 80% - 99% confidence
- **Excel:** Two sheets (News Analysis + Summary)

---

## 🔌 Production Integration Ready

### To Connect Real News APIs:

**Option 1: NewsAPI.org**
```python
# In _fetch_real_news()
import requests
url = f'https://newsapi.org/v2/everything?q={hashtag}&language=ar'
headers = {'X-Api-Key': 'YOUR_API_KEY'}
response = requests.get(url, headers=headers)
articles = response.json()['articles']
return [{'text': a['title'], 'source': a['url']} for a in articles]
```

**Option 2: Google News RSS**
```python
# Parse Google News RSS feed
from bs4 import BeautifulSoup
url = f'https://news.google.com/rss/search?q={hashtag}&hl=ar'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'xml')
items = soup.find_all('item')
return [{'text': item.title.text, 'source': item.link.text} for item in items]
```

**Option 3: Bing News Search API**
```python
# Bing News Search
endpoint = 'https://api.bing.microsoft.com/v7.0/news/search'
params = {'q': hashtag, 'mkt': 'ar-SA'}
headers = {'Ocp-Apim-Subscription-Key': 'YOUR_KEY'}
```

---

## 📋 Function Reference

### New in scraper.py

```python
def scrape_hashtag_news(hashtag_query: str) -> List[Dict[str, Any]]
    """
    Args:
        hashtag_query: String like "بغداد" or "#بغداد"
    
    Returns:
        List of dicts with 'text' and 'source' keys
    
    Topics supported:
        - بغداد, الاقتصاد, التكنولوجيا, الرياضة, الصحة
    """
```

### New in app.py

```python
def process_news_articles(articles, analyzer) -> List[Dict[str, Any]]
    """Process news articles with sentiment analysis"""

def create_summary_stats(df: pd.DataFrame) -> Dict[str, Any]
    """Enhanced to handle both comment and news DataFrames"""
```

---

## 🚀 Launch Instructions

### Start the App:
```powershell
python -u -m streamlit run app.py
```

### Access:
- Local: `http://localhost:8501`
- Network: `http://192.168.168.131:8501`

### Switch Modes:
Use the radio button at the top: **📱 Post URL Analysis** or **🏷️ Hashtag News Analysis**

---

## 📊 Excel Export Features

### Hashtag News Analysis Export:
**Sheet 1: "News Analysis"**
| الخبر (Headline) | المصدر (Source) | التصنيف (Label) | الثقة (Score) |
|---|---|---|---|
| بغداد تشهد أحداث سياسية... | https://news-ar.com/... | إيجابي | 0.89 |
| مؤتمر دولي كبير يعقد... | https://aljazeera.net/... | محايد | 0.76 |
| ... | ... | ... | ... |

**Sheet 2: "Summary"**
| الإحصائية | القيمة |
|---|---|
| إجمالي العناصر | 5 |
| متوسط الثقة | 87.34% |
| أقصى ثقة | 98.93% |
| أدنى ثقة | 75.22% |
| وقت التصدير | 2025-11-27 10:35:22 |

---

## ✨ Key Improvements Over v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Analysis Modes | 1 (Post URL) | 2 (Post URL + Hashtag News) |
| Input Types | URLs only | URLs + Hashtags |
| Mock Data Topics | 1 (Comments) | 6 (Comments + 5 News Topics) |
| Export Sheets | Dynamic | Dynamic with mode-specific naming |
| UI Modes | Single | Radio-selectable dual mode |
| API Ready | No | Yes (template included) |

---

## 🔍 Debugging Tips

### If hashtag not found:
- Falls back to economy (الاقتصاد) news
- Check the terminal for "No match" message

### If sentiment scores are extreme:
- Normal behavior (0.76 - 0.99 range typical)
- Some headlines very positive/negative in language

### To add custom topics:
- Edit `mock_news_data` dict in `scraper.py`
- Add new key: `'your_topic': [...]`
- Format: `{'text': 'Arabic headline', 'source': 'URL'}`

---

## 📞 Support & Enhancement Path

### Next Steps (Optional):
1. Connect real NewsAPI.org account
2. Add more Arabic news sources
3. Implement caching for news results
4. Add date filtering for news articles
5. Create trending topics dashboard

### Known Limitations (v2.0):
- Real scraping not implemented (mock only)
- No real-time news updates
- Fixed set of mock topics
- No search analytics

---

## ✅ Verification Checklist

- [x] `requirements.txt` updated with requests & beautifulsoup4
- [x] `scraper.py` has `scrape_hashtag_news()` method
- [x] `scraper.py` includes mock data for 5 Arabic topics
- [x] `app.py` has radio button for mode selection
- [x] `app.py` displays hashtag input when news mode selected
- [x] `process_news_articles()` function works correctly
- [x] Sentiment analysis applied to news headlines
- [x] Excel export includes news results
- [x] No syntax errors in any file
- [x] Feature ready for immediate testing

---

**All tasks complete. The app is updated and ready to use with both analysis modes! 🎉**

Try it now: `http://localhost:8501`

Select the 🏷️ **Hashtag News Analysis** tab and enter "بغداد" to test!
