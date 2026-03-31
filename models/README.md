# Models Directory

This directory stores AI/ML model files used by DAVID CIS.
**Model files are NOT included in the repository** (too large for Git).
Download them manually using the instructions below.

---

## Required: LLM Brain (Mixtral GGUF)

DAVID uses a local LLM that runs **100% offline** — no OpenAI API needed.

| Model | Size | RAM Required | Download |
|-------|------|-------------|----------|
| `mixtral.gguf` | ~26 GB | 16 GB+ RAM | [HuggingFace](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF) |
| `mistral-7b.gguf` | ~4 GB | 8 GB RAM | [HuggingFace](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF) |

### Download Command

```bash
# Install huggingface_hub
pip install huggingface_hub

# Download Mistral 7B (recommended for most machines)
python -c "
from huggingface_hub import hf_hub_download
hf_hub_download(
    repo_id='TheBloke/Mistral-7B-Instruct-v0.2-GGUF',
    filename='mistral-7b-instruct-v0.2.Q4_K_M.gguf',
    local_dir='models/',
    local_dir_use_symlinks=False
)
print('Downloaded!')
"
```

Then update `.env`:
```env
LLM_MODEL_PATH=models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
LLM_MODEL_TYPE=mistral
```

### Running WITHOUT a Model

DAVID works **without any LLM model** — it uses an offline stub that:
- Returns helpful responses explaining what the AI would say
- Still runs all scan/analysis tools normally
- Shows the HuggingFace download link in the GUI

To use stub mode, simply leave `LLM_MODEL_PATH` pointing to a non-existent file or leave it empty.

---

## Optional: ML Models (Auto-Downloaded)

These are smaller models downloaded automatically on first run:

| File | Size | Purpose | Auto-Download |
|------|------|---------|---------------|
| `lstm_ids.pt` | ~2 MB | Network anomaly detection | ✅ Yes |
| `dqn_phishing.pt` | ~1 MB | Phishing URL classifier | ✅ Yes |
| `ner_cyber.bin` | ~400 MB | CyNER entity extraction | ✅ Yes |

---

## Recommended Hardware

| Setup | Min RAM | LLM Recommendation |
|-------|---------|--------------------|
| Laptop (8 GB RAM) | 8 GB | Mistral-7B Q4_K_M (4 GB) |
| Desktop (16 GB RAM) | 16 GB | Mistral-7B Q8 or Mixtral Q2 |
| Server (32 GB+ RAM) | 32 GB | Mixtral-8x7B Q4 (full quality) |
