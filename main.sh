#! /usr/bin/env bash
#SBATCH -N 1
#SBATCH --time=4-00:00:00
#SBATCH --job-name=CS671_Geet
#SBATCH --ntasks-per-node=16
#SBATCH --error=error.txt
#SBATCH --output=out.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=b20056@students.iitmandi.ac.in

module load DL-Conda_3.7
cd $SLURM_SUBMIT_DIR

nvidia-smi > nv.txt

source /home/geetanjali.scee.iitmandi/miniconda3/bin/activate cs671

CUDA_VISIBLE_DEVICES=0 python3 run.py &> out.txt