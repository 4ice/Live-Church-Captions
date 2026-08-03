#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -d ".venv" ]]; then
  echo "No .venv found. Run the setup script for this operating system first."
  exit 1
fi

source .venv/bin/activate
python -m pip install --upgrade "pip==26.1.2" "setuptools<82" wheel
python -m pip install "ctranslate2>=4.4,<5" "transformers<5" "sentencepiece>=0.2.1,<0.3" safetensors "OpenCC==1.4.1"

python - <<'PY'
import hashlib
from pathlib import Path
from huggingface_hub import hf_hub_download
from ctranslate2.converters import TransformersConverter

model_name = "alirezamsh/small100"
revision = "8ab680e26a596d2e3d2d2d17ae0f68df1037328c"
tokenizer_sha256 = "73c8d2405e9c588582434c9f91327127faf133b9f915b203ed07ba4cd0ca9c92"
output_dir = Path("data/models/small100-ct2-int8")
output_dir.parent.mkdir(parents=True, exist_ok=True)

print(f"Downloading {model_name} tokenizer/model metadata into the local cache...")
tokenizer_file = Path(hf_hub_download(model_name, "tokenization_small100.py", revision=revision))
if hashlib.sha256(tokenizer_file.read_bytes()).hexdigest() != tokenizer_sha256:
    raise RuntimeError("Pinned SMaLL-100 tokenizer failed its integrity check.")

print(f"Converting {model_name} to CTranslate2 INT8 at {output_dir}...")
converter = TransformersConverter(model_name, revision=revision, trust_remote_code=False)
converter.convert(output_dir=str(output_dir), quantization="int8", force=True)
print("Fast Core / CTranslate2 INT8 model is installed. Enable Fast Core from the operator Languages page.")
PY
