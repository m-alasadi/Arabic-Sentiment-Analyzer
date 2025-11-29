"""
Arabic Sentiment Analysis Dashboard
Streamlit-based web application for analyzing sentiment of Arabic social media comments and news.
"""

import sys
import os
import traceback
import warnings
from datetime import datetime
from typing import List, Dict, Any
import io

# Suppress warnings
warnings.filterwarnings('ignore')

# Import Streamlit first
try:
    import streamlit as st
except ImportError as e:
    print(f"ERROR: Streamlit not installed. Run: pip install streamlit")
    sys.exit(1)

# Import data processing libraries
try:
    import pandas as pd
except ImportError as e:
    st.error("ERROR: pandas not installed. Run: pip install pandas")
    st.stop()

# Import local modules
try:
    from analyzer import SentimentAnalyzer
    from scraper import fetch_api_comments, scrape_hashtag_news
except ImportError as e:
    st.error(f"ERROR: Failed to import local modules. {str(e)}")
    st.stop()

# Configure Streamlit page (MUST be first Streamlit call)
try:
    st.set_page_config(
        page_title="Arabic Sentiment Analysis Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    print(f"ERROR: Failed to configure Streamlit page: {str(e)}")
    sys.exit(1)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
    }
    .stDataFrame {
        width: 100%;
    }
    .metric-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_analyzer() -> SentimentAnalyzer:
    """Load the sentiment analyzer model (cached for performance)."""
    try:
        model_path = "./my_final_expert_model_v3"
        
        # Verify model path exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model directory not found at: {os.path.abspath(model_path)}\n"
                f"Current working directory: {os.getcwd()}"
            )
        
        # Load the model
        analyzer = SentimentAnalyzer(model_path=model_path)
        return analyzer
        
    except FileNotFoundError as e:
        st.error(f"❌ Model Error: {str(e)}")
        st.stop()
    except ImportError as e:
        st.error(f"❌ Import Error - Missing dependency: {str(e)}")
        st.error("Run: pip install -r requirements.txt")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")
        st.error(traceback.format_exc())
        st.stop()


def process_comments(comments: List[Any], analyzer: SentimentAnalyzer) -> List[Dict[str, Any]]:
    """
    Process comments and analyze their sentiment.
    
    Args:
        comments (List[Any]): List of comments (strings or dicts with 'text' key).
        analyzer (SentimentAnalyzer): Sentiment analyzer instance.
        
    Returns:
        List[Dict[str, Any]]: List of analysis results with comments and sentiments.
    """
    if not comments:
        st.error("❌ No comments to process")
        return []
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, comment in enumerate(comments):
        try:
            # Handle both string and dict formats
            if isinstance(comment, dict):
                clean_comment = comment.get('text', '').strip()
                source = comment.get('source', 'Unknown')
            else:
                clean_comment = comment.strip() if isinstance(comment, str) else str(comment).strip()
                source = 'Unknown'
            
            if not clean_comment:
                continue
            
            # Analyze sentiment
            sentiment = analyzer.analyze_text(clean_comment)
            
            results.append({
                "التعليق (Comment)": clean_comment,
                "المصدر (Source)": source,
                "التصنيف (Label)": sentiment['label'],
                "الثقة (Score)": sentiment['score'],
            })
            
            # Update progress
            progress = (idx + 1) / len(comments)
            progress_bar.progress(progress)
            status_text.text(f"معالجة التعليقات... {idx + 1}/{len(comments)}")
        
        except Exception as e:
            st.warning(f"⚠ Error processing comment #{idx + 1}: {str(e)}")
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    return results


def process_news_articles(articles: List[Dict[str, Any]], analyzer: SentimentAnalyzer) -> List[Dict[str, Any]]:
    """
    Process news articles and analyze their sentiment.
    
    Args:
        articles (List[Dict[str, Any]]): List of article dicts with 'text' and 'source'.
        analyzer (SentimentAnalyzer): Sentiment analyzer instance.
        
    Returns:
        List[Dict[str, Any]]: List of analysis results with articles and sentiments.
    """
    if not articles:
        st.error("❌ No articles to process")
        return []
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, article in enumerate(articles):
        try:
            # Extract text and source
            text = article.get('text', '').strip() if isinstance(article.get('text'), str) else ''
            source = article.get('source', '').strip() if isinstance(article.get('source'), str) else ''
            
            if not text:
                continue
            
            # Analyze sentiment
            sentiment = analyzer.analyze_text(text)
            
            results.append({
                "الخبر (Headline)": text,
                "المصدر (Source)": source,
                "التصنيف (Label)": sentiment['label'],
                "الثقة (Score)": sentiment['score'],
            })
            
            # Update progress
            progress = (idx + 1) / len(articles)
            progress_bar.progress(progress)
            status_text.text(f"معالجة الأخبار... {idx + 1}/{len(articles)}")
        
        except Exception as e:
            st.warning(f"⚠ Error processing article #{idx + 1}: {str(e)}")
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    return results


def create_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create summary statistics from analysis results.
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment analysis results.
        
    Returns:
        Dict[str, Any]: Summary statistics.
    """
    # Determine which label column is being used
    label_column = None
    if "التصنيف (Label)" in df.columns:
        label_column = "التصنيف (Label)"
    elif "Label" in df.columns:
        label_column = "Label"
    
    if label_column is None:
        return {"total_items": len(df), "label_counts": {}, "avg_score": 0}
    
    # Determine which score column is being used
    score_column = None
    if "الثقة (Score)" in df.columns:
        score_column = "الثقة (Score)"
    elif "Score" in df.columns:
        score_column = "Score"
    
    label_counts = df[label_column].value_counts()
    avg_score = df[score_column].mean() if score_column else 0
    
    return {
        "total_items": len(df),
        "label_counts": label_counts.to_dict(),
        "avg_score": round(avg_score, 4),
        "max_score": df[score_column].max() if score_column else 0,
        "min_score": df[score_column].min() if score_column else 0
    }


def export_to_excel(df: pd.DataFrame, sheet_name: str = "Analysis Results") -> bytes:
    """
    Export analysis results to Excel format.
    
    Args:
        df (pd.DataFrame): DataFrame with analysis results.
        sheet_name (str): Name of the main data sheet.
        
    Returns:
        bytes: Excel file as bytes.
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write data sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Write summary sheet
        summary_stats = create_summary_stats(df)
        summary_df = pd.DataFrame({
            'الإحصائية': [
                'إجمالي العناصر',
                'متوسط الثقة',
                'أقصى ثقة',
                'أدنى ثقة',
                'وقت التصدير'
            ],
            'القيمة': [
                summary_stats['total_items'],
                f"{summary_stats['avg_score']:.2%}",
                f"{summary_stats['max_score']:.2%}",
                f"{summary_stats['min_score']:.2%}",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
        })
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    return output.getvalue()


def save_active_learning_entry(text: str, label: str, filepath: str = "active_learning_data.csv") -> tuple[bool, str]:
    """Append a corrected (text, label) pair to a CSV file for active learning.

    Returns (success: bool, message: str)
    """
    try:
        row = {"text": text, "label": label}
        abs_path = os.path.join(os.getcwd(), filepath)

        if os.path.exists(abs_path):
            try:
                existing = pd.read_csv(abs_path)
            except Exception:
                # If file exists but cannot be read as CSV, overwrite with new
                existing = pd.DataFrame()

            new_df = pd.DataFrame([row])
            if not existing.empty:
                combined = pd.concat([existing, new_df], ignore_index=True)
            else:
                combined = new_df
            combined.to_csv(abs_path, index=False)
        else:
            pd.DataFrame([row]).to_csv(abs_path, index=False)

        return True, f"Saved to {abs_path}"
    except Exception as e:
        return False, str(e)


def main():
    """Main application function."""
    try:
        # Header
        st.markdown("<h1 class='main-header'>📊 لوحة تحليل المشاعر العربية</h1>", unsafe_allow_html=True)
        st.markdown("<h3 class='main-header'>Arabic Sentiment Analysis Dashboard</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Sidebar configuration
        st.sidebar.header("⚙️ الإعدادات (Settings)")
        
        use_mock_data = st.sidebar.checkbox(
            "استخدام البيانات الوهمية (Use Mock Data - Testing)",
            value=True,
            help="استخدم البيانات الوهمية للاختبار السريع"
        )
        
        # Load analyzer
        analyzer = load_analyzer()
        
        # Analysis mode selection
        st.subheader("🔄 نمط التحليل (Analysis Mode)")
        analysis_mode = st.radio(
            "اختر نمط التحليل:",
            options=["📱 Post URL Analysis", "🏷️ Hashtag News Analysis"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if analysis_mode == "📱 Post URL Analysis":
            # Original Post URL Analysis Mode
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📱 مصدر البيانات (Data Source)")
                post_url = st.text_input(
                    "رابط المنشور (Post URL)",
                    placeholder="https://www.facebook.com/post/123456789",
                    help="أدخل رابط المنشور من وسائل التواصل الاجتماعي"
                )
            
            with col2:
                st.subheader("🔧 الخيارات (Options)")
                st.write(f"**الوضع (Mode):** {'🧪 اختبار (Testing)' if use_mock_data else '🔴 مباشر (Live)'}")
            
            # Analyze button for Post URL mode
            if st.button("🚀 تحليل التعليقات (Analyze Comments)", type="primary", use_container_width=True):
                
                with st.spinner("جاري جلب التعليقات من API... (Fetching comments from API)"):
                    try:
                        # Fetch comments from the stable API
                        if use_mock_data:
                            st.info("🧪 Using local mock data for testing")
                            api_data = fetch_api_comments()
                            comments_dict = api_data
                        else:
                            st.info("🌐 Fetching from external API")
                            api_data = fetch_api_comments()
                            comments_dict = api_data
                        
                        if not comments_dict:
                            st.error("❌ فشل جلب التعليقات (Failed to fetch comments)")
                            st.stop()
                        
                        st.success(f"✓ تم جلب {len(comments_dict)} تعليق بنجاح")
                        
                        # Process comments
                        st.subheader("📈 نتائج التحليل (Analysis Results)")
                        results = process_comments(comments_dict, analyzer)
                        
                        if not results:
                            st.error("❌ فشل معالجة التعليقات (Failed to process comments)")
                            st.stop()
                        
                        # Create DataFrame
                        df = pd.DataFrame(results)
                        
                        # Display results
                        st.dataframe(df, use_container_width=True, height=400)

                        # ----------------------
                        # Manual Correction & Active Learning Feedback
                        # ----------------------
                        st.subheader("✍️ Manual Correction & Active Learning Feedback")
                        if not df.empty:
                            # Determine text column (comments vs news)
                            if "التعليق (Comment)" in df.columns:
                                text_col = "التعليق (Comment)"
                            elif "الخبر (Headline)" in df.columns:
                                text_col = "الخبر (Headline)"
                            else:
                                text_col = df.columns[0]

                            idx_options = df.index.tolist()
                            def _fmt(i):
                                txt = str(df.loc[i, text_col])
                                preview = txt[:80] + ("..." if len(txt) > 80 else "")
                                return f"{i} - {preview}"

                            selected_idx = st.selectbox(
                                "اختر السطر لتصحيحه (Select row to correct)",
                                options=idx_options,
                                format_func=_fmt
                            )

                            original_text = str(df.loc[selected_idx, text_col])
                            st.text_area("النص الأصلي (Original Text)", value=original_text, height=120)

                            label_options = ["إيجابي", "سلبي", "محايد", "Positive", "Negative", "Neutral"]
                            corrected_label = st.selectbox("التسمية الصحيحة (Select correct label)", options=label_options)
                            custom_label = st.text_input("أو أدخل تسمية مخصصة (Or enter custom label)", value="")
                            final_label = custom_label.strip() if custom_label.strip() else corrected_label

                            if st.button("💾 Save Correction to Training Data", key=f"save_correction_comments_{selected_idx}"):
                                ok, msg = save_active_learning_entry(original_text, final_label)
                                if ok:
                                    st.success(f"✅ تم حفظ التصحيح: {final_label}")
                                else:
                                    st.error(f"❌ فشل حفظ التصحيح: {msg}")
                        else:
                            st.info("ℹ️ لا توجد بيانات للعرض أو التصحيح في الوقت الحالي (No data to correct)")
                        
                        # Summary statistics
                        st.subheader("📊 الإحصائيات (Summary Statistics)")
                        stats = create_summary_stats(df)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(
                                "إجمالي التعليقات",
                                stats['total_items']
                            )
                        
                        with col2:
                            st.metric(
                                "متوسط الثقة",
                                f"{stats['avg_score']:.2%}"
                            )
                        
                        with col3:
                            st.metric(
                                "أقصى ثقة",
                                f"{stats['max_score']:.2%}"
                            )
                        
                        with col4:
                            st.metric(
                                "أدنى ثقة",
                                f"{stats['min_score']:.2%}"
                            )
                        
                        # Sentiment distribution
                        st.subheader("🎯 توزيع المشاعر (Sentiment Distribution)")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            sentiment_counts = df["التصنيف (Label)"].value_counts()
                            st.bar_chart(sentiment_counts)
                        
                        with col2:
                            # Summary table
                            fig_data = {
                                'التصنيف': sentiment_counts.index,
                                'العدد': sentiment_counts.values
                            }
                            fig_df = pd.DataFrame(fig_data)
                            st.write(fig_df)
                        
                        # Export to Excel
                        st.subheader("💾 التصدير (Export)")
                        
                        excel_data = export_to_excel(df, sheet_name="Comments Analysis")
                        st.download_button(
                            label="⬇️ تحميل النتائج (Download Results as Excel)",
                            data=excel_data,
                            file_name=f"comments_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"❌ خطأ في المعالجة: {str(e)}")
                        st.error("Error Details:")
                        st.code(traceback.format_exc())
        
        else:  # Hashtag News Analysis Mode
            st.subheader("🏷️ تحليل أخبار الهاشتاغ (Hashtag News Analysis)")
            
            # Show available topics
            st.info("📚 **الموضوعات المتاحة (Available Topics):**\n\n"
                    "🇮🇶 **بغداد** (Baghdad) | 💰 **الاقتصاد** (Economy) | 🖥️ **التكنولوجيا** (Technology) | "
                    "⚽ **الرياضة** (Sports) | 🏥 **الصحة** (Health)")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                hashtag_query = st.text_input(
                    "أدخل الهاشتاغ أو الموضوع (Enter Hashtag/Topic)",
                    placeholder="بغداد / الاقتصاد / التكنولوجيا",
                    help="مثال: #بغداد أو بغداد (الهاشتاغ اختياري)"
                )
            
            with col2:
                st.write(f"**الوضع (Mode):** 🧪 Mock Data")
            
            # Analyze button for Hashtag mode
            if st.button("🚀 تحليل الأخبار (Analyze News)", type="primary", use_container_width=True):
                
                if not hashtag_query or not hashtag_query.strip():
                    st.error("❌ يرجى إدخال هاشتاغ أو موضوع (Please enter a hashtag)")
                    st.warning("💡 جرب أحد الموضوعات المتاحة أعلاه")
                else:
                    with st.spinner("جاري جلب الأخبار ذات الصلة... (Fetching news)"):
                        try:
                            # Fetch news articles for hashtag
                            articles = scrape_hashtag_news(hashtag_query.strip())
                            
                            if not articles or len(articles) == 0:
                                st.error(f"❌ لم يتم العثور على أخبار للموضوع: {hashtag_query}")
                                st.error("⚠️ الرجاء جرب أحد الموضوعات التالية:\n"
                                        "• بغداد\n"
                                        "• الاقتصاد\n"
                                        "• التكنولوجيا\n"
                                        "• الرياضة\n"
                                        "• الصحة")
                                st.stop()
                            
                            st.success(f"✓ تم جلب {len(articles)} خبر عن: {hashtag_query}")
                            
                            # Process articles
                            st.subheader("📰 نتائج التحليل (Analysis Results)")
                            results = process_news_articles(articles, analyzer)
                            
                            if not results:
                                st.error("❌ فشل معالجة الأخبار (Failed to process articles)")
                                st.stop()
                            
                            # Create DataFrame
                            df = pd.DataFrame(results)
                            
                            # Display results
                            st.dataframe(df, use_container_width=True, height=400)

                            # ----------------------
                            # Manual Correction & Active Learning Feedback
                            # ----------------------
                            st.subheader("✍️ Manual Correction & Active Learning Feedback")
                            if not df.empty:
                                # Determine text column (comments vs news)
                                if "التعليق (Comment)" in df.columns:
                                    text_col = "التعليق (Comment)"
                                elif "الخبر (Headline)" in df.columns:
                                    text_col = "الخبر (Headline)"
                                else:
                                    text_col = df.columns[0]

                                idx_options = df.index.tolist()
                                def _fmt(i):
                                    txt = str(df.loc[i, text_col])
                                    preview = txt[:80] + ("..." if len(txt) > 80 else "")
                                    return f"{i} - {preview}"

                                selected_idx = st.selectbox(
                                    "اختر السطر لتصحيحه (Select row to correct)",
                                    options=idx_options,
                                    format_func=_fmt
                                )

                                original_text = str(df.loc[selected_idx, text_col])
                                st.text_area("النص الأصلي (Original Text)", value=original_text, height=120)

                                label_options = ["إيجابي", "سلبي", "محايد", "Positive", "Negative", "Neutral"]
                                corrected_label = st.selectbox("التسمية الصحيحة (Select correct label)", options=label_options)
                                custom_label = st.text_input("أو أدخل تسمية مخصصة (Or enter custom label)", value="")
                                final_label = custom_label.strip() if custom_label.strip() else corrected_label

                                if st.button("💾 Save Correction to Training Data", key=f"save_correction_news_{selected_idx}"):
                                    ok, msg = save_active_learning_entry(original_text, final_label)
                                    if ok:
                                        st.success(f"✅ تم حفظ التصحيح: {final_label}")
                                    else:
                                        st.error(f"❌ فشل حفظ التصحيح: {msg}")
                            else:
                                st.info("ℹ️ لا توجد بيانات للعرض أو التصحيح في الوقت الحالي (No data to correct)")
                            
                            # Summary statistics
                            st.subheader("📊 الإحصائيات (Summary Statistics)")
                            stats = create_summary_stats(df)
                            
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric(
                                    "إجمالي الأخبار",
                                    stats['total_items']
                                )
                            
                            with col2:
                                st.metric(
                                    "متوسط الثقة",
                                    f"{stats['avg_score']:.2%}"
                                )
                            
                            with col3:
                                st.metric(
                                    "أقصى ثقة",
                                    f"{stats['max_score']:.2%}"
                                )
                            
                            with col4:
                                st.metric(
                                    "أدنى ثقة",
                                    f"{stats['min_score']:.2%}"
                                )
                            
                            # Sentiment distribution
                            st.subheader("🎯 توزيع المشاعر (Sentiment Distribution)")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                sentiment_counts = df["التصنيف (Label)"].value_counts()
                                st.bar_chart(sentiment_counts)
                            
                            with col2:
                                # Summary table
                                fig_data = {
                                    'التصنيف': sentiment_counts.index,
                                    'العدد': sentiment_counts.values
                                }
                                fig_df = pd.DataFrame(fig_data)
                                st.write(fig_df)
                            
                            # Export to Excel
                            st.subheader("💾 التصدير (Export)")
                            
                            excel_data = export_to_excel(df, sheet_name="News Analysis")
                            st.download_button(
                                label="⬇️ تحميل النتائج (Download Results as Excel)",
                                data=excel_data,
                                file_name=f"news_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                            
                        except Exception as e:
                            st.error(f"❌ خطأ في المعالجة: {str(e)}")
                            st.error("Error Details:")
                            st.code(traceback.format_exc())
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: gray; font-size: 0.8rem;'>
            <p>Arabic Sentiment Analysis Dashboard v2.0</p>
            <p>مع دعم تحليل أخبار الهاشتاغ | With Hashtag News Analysis Support</p>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Critical Application Error: {str(e)}")
        st.error(traceback.format_exc())
        st.stop()


if __name__ == "__main__":
    main()
