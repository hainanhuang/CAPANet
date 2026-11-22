import subprocess, sys, os
from pathlib import Path

# 将当前工作目录设为项目根目录 (CAPANet)
project_root = Path(__file__).parent.parent
os.chdir(project_root)

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

scripts = [
    'scripts/make_visual_comparison.py',
    'scripts/visualize_dpr.py',
    'scripts/visualize_attention.py',
    'scripts/visualize_lmr.py',
    'scripts/visualize_dynamic_r.py',
    'scripts/plot_pareto.py',
    'scripts/calculate_complexity.py'
]

print("=== CAPANet 自动绘图与指标生成脚本 ===")
print("请确保已安装所需依赖：pip install matplotlib seaborn einops tqdm fvcore opencv-python")
print("=====================================\n")

for s in scripts:
    print(f'\n>>> Running {s} ...')
    result = subprocess.run([sys.executable, s], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f'[ERROR] {s} failed:\n{result.stderr}')
        
print("\nAll visualizations finished. Results are saved in 'output/' directory.")
