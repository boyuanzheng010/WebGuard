#!/bin/bash
#SBATCH --job-name=qwen2_5vl_32b
#SBATCH --partition=gpu
#SBATCH --account=PAS1576
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=4
#SBATCH --cpus-per-task=8
#SBATCH --mem=0
#SBATCH --time=72:00:00
#SBATCH --output=logs/qwen2_5vl_32b_%j.out
#SBATCH --error=logs/qwen2_5vl_32b_%j.err

# 设置环境变量
export MASTER_PORT=29500
export MASTER_ADDR=$(hostname -s)
export WORLD_SIZE=$SLURM_NTASKS
export NODE_RANK=$SLURM_NODEID
export LOCAL_RANK=$SLURM_LOCALID
export RANK=$SLURM_PROCID

# 激活conda环境
module load miniconda3
conda activate factory
cd /fs/ess/PAS1576/byzheng/projects/train_monitor/LLaMA-Factory

# 创建日志目录
mkdir -p logs

# 启动训练
srun python src/train_bash.py \
    --config examples/train_full/32b_monitor_qwen2_5vl_full_sft_eval.yaml \
    --deepspeed \
    --ddp_timeout 180000000 