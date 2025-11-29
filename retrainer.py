"""
Active Learning Retraining Script
Fine-tunes the Arabic sentiment model using corrections from active_learning_data.csv
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# PyTorch & Transformers
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AdamW,
    get_linear_schedule_with_warmup
)
from tqdm import tqdm


class SentimentDataset(Dataset):
    """Custom PyTorch Dataset for sentiment data."""
    
    def __init__(self, texts, labels, tokenizer, max_length=256):
        """
        Args:
            texts (List[str]): Text samples
            labels (List[str]): Sentiment labels
            tokenizer: HuggingFace tokenizer
            max_length (int): Maximum token length
        """
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Build label to ID mapping
        unique_labels = sorted(set(labels))
        self.label2id = {label: idx for idx, label in enumerate(unique_labels)}
        self.id2label = {idx: label for label, idx in self.label2id.items()}
        
        print(f"✓ Label Mapping: {self.label2id}")
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(self.label2id[label], dtype=torch.long)
        }


class SentimentRetrainer:
    """Fine-tunes sentiment model using active learning corrections."""
    
    def __init__(
        self,
        model_dir: str = "./my_final_expert_model_v3",
        output_dir: str = "./my_updated_expert_model_v4",
        learning_rate: float = 2e-5,
        epochs: int = 3,
        batch_size: int = 8,
        max_length: int = 256
    ):
        """
        Initialize retrainer.
        
        Args:
            model_dir (str): Path to original model
            output_dir (str): Where to save updated model
            learning_rate (float): Learning rate for fine-tuning
            epochs (int): Number of training epochs (1-3 recommended)
            batch_size (int): Batch size for training
            max_length (int): Max token length
        """
        self.model_dir = model_dir
        self.output_dir = output_dir
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.max_length = max_length
        
        # Device selection
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"✓ Using device: {self.device}")
        
        # Model and tokenizer (loaded on demand)
        self.model = None
        self.tokenizer = None
        self.dataset = None
        self.dataloader = None
    
    def load_model(self) -> bool:
        """Load pre-trained model and tokenizer."""
        try:
            print(f"\n📦 Loading model from: {self.model_dir}")
            
            if not os.path.exists(self.model_dir):
                print(f"❌ Model directory not found: {self.model_dir}")
                return False
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            print(f"✓ Tokenizer loaded ({len(self.tokenizer)} tokens)")
            
            # Load model
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir)
            self.model.to(self.device)
            print(f"✓ Model loaded ({self.model.config.num_labels} labels)")
            
            # Print model config
            print(f"  - Model type: {self.model.config.model_type}")
            print(f"  - Hidden size: {self.model.config.hidden_size}")
            print(f"  - Num layers: {self.model.config.num_hidden_layers}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            return False
    
    def load_training_data(self, csv_path: str = "active_learning_data.csv") -> bool:
        """Load corrections from CSV file."""
        try:
            print(f"\n📄 Loading training data from: {csv_path}")
            
            if not os.path.exists(csv_path):
                print(f"❌ Training data file not found: {csv_path}")
                return False
            
            df = pd.read_csv(csv_path)
            
            # Validate columns
            if 'text' not in df.columns or 'label' not in df.columns:
                print(f"❌ CSV must contain 'text' and 'label' columns")
                print(f"   Found columns: {df.columns.tolist()}")
                return False
            
            # Remove duplicates and empty rows
            df = df.dropna(subset=['text', 'label'])
            df = df[df['text'].str.strip() != '']
            df = df.drop_duplicates(subset=['text'], keep='first')
            
            texts = df['text'].tolist()
            labels = df['label'].tolist()
            
            print(f"✓ Loaded {len(texts)} training samples")
            print(f"  - Unique labels: {sorted(set(labels))}")
            print(f"  - Label distribution:")
            for label, count in df['label'].value_counts().items():
                print(f"    • {label}: {count}")
            
            # Create dataset
            self.dataset = SentimentDataset(
                texts, labels, self.tokenizer, self.max_length
            )
            
            # Create dataloader
            self.dataloader = DataLoader(
                self.dataset,
                batch_size=self.batch_size,
                shuffle=True
            )
            
            print(f"✓ Created dataloader ({len(self.dataloader)} batches)")
            return True
        
        except Exception as e:
            print(f"❌ Error loading training data: {str(e)}")
            return False
    
    def train(self) -> bool:
        """Run fine-tuning loop."""
        try:
            print(f"\n🚀 Starting fine-tuning ({self.epochs} epochs)")
            print(f"   Learning rate: {self.learning_rate}")
            print(f"   Batch size: {self.batch_size}")
            
            # Optimizer setup
            optimizer = AdamW(self.model.parameters(), lr=self.learning_rate)
            total_steps = len(self.dataloader) * self.epochs
            scheduler = get_linear_schedule_with_warmup(
                optimizer,
                num_warmup_steps=0,
                num_training_steps=total_steps
            )
            
            # Training loop
            for epoch in range(self.epochs):
                print(f"\n📍 Epoch {epoch + 1}/{self.epochs}")
                
                self.model.train()
                total_loss = 0.0
                total_samples = 0
                
                pbar = tqdm(self.dataloader, desc="Training", leave=True)
                
                for batch_idx, batch in enumerate(pbar):
                    # Move batch to device
                    input_ids = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    labels = batch['labels'].to(self.device)
                    
                    # Forward pass
                    outputs = self.model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=labels
                    )
                    
                    loss = outputs.loss
                    total_loss += loss.item()
                    total_samples += input_ids.size(0)
                    
                    # Backward pass
                    optimizer.zero_grad()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                    optimizer.step()
                    scheduler.step()
                    
                    # Update progress bar
                    avg_loss = total_loss / (batch_idx + 1)
                    pbar.set_postfix({'loss': f"{avg_loss:.4f}"})
                
                epoch_loss = total_loss / len(self.dataloader)
                print(f"   Loss: {epoch_loss:.4f}")
            
            print(f"\n✓ Fine-tuning complete!")
            return True
        
        except Exception as e:
            print(f"❌ Error during training: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_model(self) -> bool:
        """Save fine-tuned model."""
        try:
            print(f"\n💾 Saving model to: {self.output_dir}")
            
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Save model
            self.model.save_pretrained(self.output_dir)
            print(f"   ✓ Model weights saved")
            
            # Save tokenizer
            self.tokenizer.save_pretrained(self.output_dir)
            print(f"   ✓ Tokenizer saved")
            
            # Save label mapping
            label_mapping = self.dataset.id2label
            with open(os.path.join(self.output_dir, 'label_mapping.json'), 'w') as f:
                json.dump(label_mapping, f, indent=2, ensure_ascii=False)
            print(f"   ✓ Label mapping saved: {label_mapping}")
            
            # Create metadata
            metadata = {
                "created": datetime.now().isoformat(),
                "source_model": self.model_dir,
                "training_epochs": self.epochs,
                "learning_rate": self.learning_rate,
                "batch_size": self.batch_size,
                "max_length": self.max_length,
                "device": str(self.device),
                "training_samples": len(self.dataset) if self.dataset else 0,
                "model_type": self.model.config.model_type,
                "num_labels": self.model.config.num_labels,
                "label_mapping": label_mapping
            }
            
            with open(os.path.join(self.output_dir, 'metadata.json'), 'w') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"   ✓ Metadata saved")
            
            print(f"\n✅ Model successfully saved to: {os.path.abspath(self.output_dir)}")
            return True
        
        except Exception as e:
            print(f"❌ Error saving model: {str(e)}")
            return False
    
    def run_full_pipeline(self, csv_path: str = "active_learning_data.csv") -> bool:
        """Execute full retraining pipeline."""
        steps = [
            ("Load Model", self.load_model),
            ("Load Training Data", lambda: self.load_training_data(csv_path)),
            ("Fine-tune", self.train),
            ("Save Model", self.save_model)
        ]
        
        print("=" * 70)
        print("🤖 ACTIVE LEARNING RETRAINING PIPELINE")
        print("=" * 70)
        
        for step_name, step_func in steps:
            print(f"\n{'=' * 70}")
            print(f"Step: {step_name}")
            print("=" * 70)
            
            if not step_func():
                print(f"\n❌ Pipeline failed at step: {step_name}")
                return False
        
        print("\n" + "=" * 70)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\n📌 Next Steps:")
        print(f"   1. Update analyzer.py to load from: {self.output_dir}")
        print(f"   2. Or update app.py line ~95: model_path = '{self.output_dir}'")
        print(f"   3. Restart Streamlit: streamlit run app.py")
        print("\n")
        return True


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Fine-tune Arabic sentiment model with active learning corrections"
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="./my_final_expert_model_v3",
        help="Path to original model (default: ./my_final_expert_model_v3)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./my_updated_expert_model_v4",
        help="Output directory for fine-tuned model (default: ./my_updated_expert_model_v4)"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="active_learning_data.csv",
        help="Path to training data CSV (default: active_learning_data.csv)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs (default: 3, recommended: 1-3)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Batch size (default: 8)"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-5,
        help="Learning rate (default: 2e-5)"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=256,
        help="Max token length (default: 256)"
    )
    
    args = parser.parse_args()
    
    # Create retrainer and run pipeline
    retrainer = SentimentRetrainer(
        model_dir=args.model_dir,
        output_dir=args.output_dir,
        learning_rate=args.learning_rate,
        epochs=args.epochs,
        batch_size=args.batch_size,
        max_length=args.max_length
    )
    
    success = retrainer.run_full_pipeline(args.csv)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
