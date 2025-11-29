"""
Arabic Sentiment Analysis Module
Handles sentiment classification for Arabic text using a local transformer model.
"""

import os
from typing import Dict, Any
from transformers import pipeline


class SentimentAnalyzer:
    """
    Sentiment analyzer for Arabic text using local transformer models.
    
    This class loads a pre-trained Arabic sentiment model and provides
    methods to analyze text sentiment with multilingual label support.
    """
    
    def __init__(self, model_path: str = "./my_updated_expert_model_v4"):
        """
        Initialize the SentimentAnalyzer with a local model.
        
        Args:
            model_path (str): Path to the local model directory.
                             Defaults to fine-tuned model v4.
                             Falls back to v3 if v4 not found.
            
        Raises:
            FileNotFoundError: If neither model path exists.
            Exception: If model loading fails.
        """
        # Auto-fallback logic: try v4 first, then v3
        if not os.path.exists(model_path) and model_path == "./my_updated_expert_model_v4":
            fallback_path = "./my_final_expert_model_v3"
            if os.path.exists(fallback_path):
                print(f"⚠️  Model v4 not found. Falling back to v3: {fallback_path}")
                model_path = fallback_path
        
        self.model_path = model_path
        self.model = None
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
        Load the sentiment analysis model from the local path.
        
        Raises:
            FileNotFoundError: If the model path doesn't exist.
            Exception: If model initialization fails.
        """
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model path not found: {self.model_path}. "
                f"Please ensure the model directory exists at the specified location. "
                f"Run: python retrainer.py"
            )
        
        try:
            self.model = pipeline(
                "text-classification",
                model=self.model_path,
                device=-1  # Use CPU; set device=0 for GPU
            )
            model_version = "v4 (Fine-tuned)" if "v4" in self.model_path else "v3 (Base)"
            print(f"✓ Model loaded successfully from {self.model_path} [{model_version}]")
        except Exception as e:
            raise Exception(f"Failed to load model from {self.model_path}: {str(e)}")
    
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
