#!/bin/bash
module load miniconda3
conda activate factory
cd /fs/ess/PAS1576/byzheng/projects/train_monitor/LLaMA-Factory
llamafactory-cli train examples/train_full/32b_monitor_qwen2_5vl_full_sft_eval.yaml