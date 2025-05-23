#!/bin/bash
#SBATCH --job-name=qwen32b_sft
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:4
#SBATCH --partition=gpu
#SBATCH --account=PAS1576 
#SBATCH --output=logs/qwen32b_sft_%j.log
#SBATCH --error=logs/qwen32b_sft_%j.err

# 设置环境变量
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500
export WORLD_SIZE=$(($SLURM_NNODES * $SLURM_NTASKS_PER_NODE))
export NODE_RANK=$SLURM_NODEID
export FORCE_TORCHRUN=1

# 激活您的conda环境（如果需要）
module load miniconda3
conda activate factory
cd /fs/ess/PAS1576/byzheng/projects/train_monitor/LLaMA-Factory

# 启动训练
srun python -m torch.distributed.launch \
    --nproc_per_node=4 \
    --nnodes=$SLURM_NNODES \
    --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR \
    --master_port=$MASTER_PORT \
    src/train.py examples/train_full/multi_node_32b_monitor_qwen2_5vl_full_sft_eval.yaml