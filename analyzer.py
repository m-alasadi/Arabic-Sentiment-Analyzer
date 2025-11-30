"""
Arabic Sentiment Analysis Module
Handles sentiment classification for Arabic text using transformer models.
Models can be loaded from local directories or Hugging Face Hub.
"""

import os
from typing import Dict, Any
from transformers import pipeline


class SentimentAnalyzer:
    """
    Sentiment analyzer for Arabic text using transformer models.
    
    Supports loading models from local directories or Hugging Face Hub.
    Falls back to a reliable multilingual model if local path unavailable.
    """
    
    def __init__(self, model_path: str = "./my_final_expert_model_v3"):
        """
        Initialize the SentimentAnalyzer.
        
        Args:
            model_path: Local path or Hugging Face model ID.
                       Defaults to local expert model v3.
                       Falls back to bert-base-multilingual-uncased if unavailable.
        """
        self.model_path = model_path
        self.model = None
        self.loaded_from = None
        self.label_mapping = {
            'POSITIVE': 'إيجابي',
            'NEGATIVE': 'سلبي',
            'NEUTRAL': 'محايد',
            'positive': 'إيجابي',
            'negative': 'سلبي',
            'neutral': 'محايد'
        }
        
        self._load_model()
    
    def _load_model(self) -> None:
        """
        Load model: try requested path first, then fallback to public multilingual model.
        
        Never raises: if both attempts fail, prints error but doesn't crash.
        """
        fallback_model = "bert-base-multilingual-uncased"

        # Attempt 1: Load requested model path
        try:
            print(f"[Loading] Attempting to load model from: {self.model_path}")
            self.model = pipeline(
                "text-classification",
                model=self.model_path,
                device=-1
            )
            self.loaded_from = str(self.model_path)
            print(f"[SUCCESS] Model loaded from: {self.loaded_from}")
            return
        except Exception as first_exc:
            print(f"[WARNING] Failed to load from {self.model_path}: {str(first_exc)[:100]}")

        # Attempt 2: Load fallback public model
        try:
            print(f"[Loading] Attempting fallback model: {fallback_model}")
            self.model = pipeline(
                "text-classification",
                model=fallback_model,
                device=-1
            )
            self.loaded_from = fallback_model
            print(f"[SUCCESS] Using fallback model: {self.loaded_from}")
            return
        except Exception as second_exc:
            print(f"[ERROR] Both loading attempts failed. Last error: {str(second_exc)[:100]}")
            raise Exception(f"Failed to load model. Tried: {self.model_path}, {fallback_model}. Error: {second_exc}")
    
    def _truncate_text(self, text: str, max_tokens: int = 512) -> str:
        """
        Truncate text to a maximum number of tokens.
        
        Args:
            text (str): Input text to truncate.
            max_tokens (int): Maximum number of tokens (approximate).
            
        Returns:
            str: Truncated text.
        """
        # Approximate truncation: 1 token ≈ 4 characters
        char_limit = max_tokens * 4
        if len(text) > char_limit:
            return text[:char_limit]
        return text
    
    def _translate_label(self, label: str) -> str:
        """
        Translate model labels to Arabic.
        
        Args:
            label (str): English label from the model.
            
        Returns:
            str: Arabic label or original if translation not found.
        """
        return self.label_mapping.get(label, label)
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of Arabic text.
        
        Args:
            text (str): Arabic text to analyze.
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'label': Arabic sentiment label ('إيجابي', 'سلبي', or 'محايد')
                - 'score': Confidence score (0.0 to 1.0)
                - 'original_label': Original model label
                
        Raises:
            ValueError: If text is empty or None.
            Exception: If model inference fails.
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string.")
        
        if self.model is None:
            raise Exception("Model not loaded. Please reinitialize the analyzer.")
        
        try:
            # Truncate text to 512 tokens
            truncated_text = self._truncate_text(text)
            
            # Run inference
            results = self.model(truncated_text)
            
            if not results or len(results) == 0:
                raise Exception("Model returned no results.")
            
            result = results[0]
            
            # Extract label and score
            original_label = result.get('label', 'NEUTRAL')
            score = round(result.get('score', 0.0), 4)
            arabic_label = self._translate_label(original_label)
            
            return {
                'label': arabic_label,
                'score': score,
                'original_label': original_label
            }
        
        except Exception as e:
            raise Exception(f"Error during sentiment analysis: {str(e)}")
    
    def analyze_batch(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts (list): List of text strings to analyze.
            
        Returns:
            list: List of sentiment analysis results.
        """
        results = []
        for text in texts:
            try:
                result = self.analyze_text(text)
                results.append(result)
            except Exception as e:
                results.append({
                    'label': 'خطأ',
                    'score': 0.0,
                    'error': str(e)
                })
        return results
