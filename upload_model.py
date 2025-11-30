#!/usr/bin/env python
"""
Upload Arabic Sentiment Model to Hugging Face Hub (flexible CLI)

Usage examples:
  # Use HF token in env and custom repo id
  $env:HF_TOKEN="<your_token>"
  python .\upload_model.py --repo-id m-alasadi/Arabic-Sentiment-Model

  # Or login with huggingface-cli and run without HF_TOKEN
  huggingface-cli login
  python .\upload_model.py --repo-id m-alasadi/Arabic-Sentiment-Model

Notes:
 - The script will look for `HF_TOKEN` in the environment. If not found,
   it relies on your local huggingface-cli login session.
 - The default local model folder is `./my_final_expert_model_v3`.
"""

import os
import sys
import argparse
from huggingface_hub import HfApi, Repository


def upload_folder(local_model_path: str, repo_id: str, token: str | None = None, private: bool = False):
    if not os.path.exists(local_model_path):
        raise FileNotFoundError(f"Model not found: {local_model_path}")

    api = HfApi()

    print(f"⏳ Uploading {local_model_path} -> {repo_id} (private={private})")

    # If a token is provided, pass it to the API methods
    try:
        api.upload_folder(
            folder_path=local_model_path,
            repo_id=repo_id,
            repo_type="model",
            token=token,
            path_in_repo="",
            create_pr=False,
            repo_type_hf="model",
            private=private
        )
    except TypeError:
        # Older huggingface_hub may not accept 'private' or 'token' named args in upload_folder
        # Fall back to a simpler call and rely on login/session
        api.upload_folder(folder_path=local_model_path, repo_id=repo_id)


def main():
    parser = argparse.ArgumentParser(description="Upload local model folder to Hugging Face Hub")
    parser.add_argument("--local-path", default="./my_final_expert_model_v3", help="Local model folder path")
    parser.add_argument("--repo-id", required=True, help="Target repo id (e.g. username/repo-name)")
    parser.add_argument("--private", action="store_true", help="Create the model repo as private")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")

    try:
        upload_folder(local_model_path=args.local_path, repo_id=args.repo_id, token=token, private=args.private)
        print("\n✅ Upload successful!")
        print(f"Model URL: https://huggingface.co/{args.repo_id}")
    except Exception as e:
        print("\n❌ Upload failed:")
        print(str(e))
        print("\nTips:")
        print(" - Ensure you have internet access.")
        print(" - Either set HF_TOKEN environment variable or run 'huggingface-cli login' before running this script.")
        print(" - Ensure the local path is correct and contains model files (pytorch_model.bin or model.safetensors, config.json, tokenizer files).")
        sys.exit(1)


if __name__ == "__main__":
    main()
