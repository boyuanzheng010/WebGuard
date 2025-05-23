#!/bin/bash

# 设置环境变量
export MASTER_ADDR=c0804
export MASTER_PORT=29500
export WORLD_SIZE=8  # 2个节点 * 4个GPU
export FORCE_TORCHRUN=1

# 在第一个节点上启动训练
ssh c0804 "module load miniconda3 && conda activate factory && cd /fs/ess/PAS1576/byzheng/projects/train_monitor/LLaMA-Factory && export NODE_RANK=0 && llamafactory-cli train examples/train_full/32b_monitor_qwen2_5vl_full_sft_eval.yaml" &

# 在第二个节点上启动训练
ssh c0806 "module load miniconda3 && conda activate factory && cd /fs/ess/PAS1576/byzheng/projects/train_monitor/LLaMA-Factory && export NODE_RANK=1 && llamafactory-cli train examples/train_full/32b_monitor_qwen2_5vl_full_sft_eval.yaml" &

# 等待所有后台进程完成
wait 