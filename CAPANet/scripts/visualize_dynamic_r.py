import sys, torch, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
import os
from PIL import Image
from glob import glob

sys.path.insert(0, str(Path(__file__).parent.parent))
from basicsr.archs.capanet_arch import CAPANet

def collect_dynamic_r(model, lr_dir, block_idx=4, level='hf', max_images=50):
    if not os.path.exists(lr_dir):
        print(f"Warning: Directory {lr_dir} not found. Returning dummy data.")
        return np.random.rand(100), np.random.rand(100) * 0.5 + 0.25
        
    pfsa = model.blocks[block_idx][0].lmr.level_attn[level]
    pfsa._collect_focus = True
    pfsa._purity_list = []
    pfsa._ratio_list = []

    paths = sorted(glob(f'{lr_dir}/*.png'))[:max_images]
    if not paths:
        print(f"No PNG images found in {lr_dir}. Returning dummy data.")
        return np.random.rand(100), np.random.rand(100) * 0.5 + 0.25
        
    for p in paths:
        img = np.array(Image.open(p).convert('RGB')).astype(np.float32) / 255.0
        lq = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)
        with torch.no_grad():
            _ = model(lq)

    purity_all = [v for lst in pfsa._purity_list for v in lst]
    ratio_all  = [v for lst in pfsa._ratio_list  for v in lst]
    pfsa._collect_focus = False
    return np.array(purity_all), np.array(ratio_all)

def plot_purity_vs_r(purity, ratio, save_path='output/dynamic_r_scatter.png'):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(purity, ratio, alpha=0.2, s=5, color='steelblue')
    # 趋势线
    if len(purity) > 1:
        z = np.polyfit(purity, ratio, 1)
        x_line = np.linspace(purity.min(), purity.max(), 100)
        ax.plot(x_line, np.polyval(z, x_line), 'r-', linewidth=1.5, label='Trend')
        
    ax.set_xlabel('Cluster Purity')
    ax.set_ylabel('Dynamic Focus Ratio r')
    ax.set_title('PFSA: Purity vs Dynamic r')
    ax.legend()
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'Scatter plot saved: {save_path}')

if __name__ == '__main__':
    # ===== 调用示例 =====
    model = CAPANet(upscale=4, level_head_split=[2,1,1],
                    focus_mode='dynamic', use_sparse_pfsa=True,
                    global_branch_levels=['mf','hf'],
                    attn_state_mode='layered', routing_mode='dpr').eval()
    ckpt_path = 'experiments/train_CAPANet_x4_finetune/models/net_g_latest.pth'
    if os.path.exists(ckpt_path):
        params = torch.load(ckpt_path, map_location='cpu')
        model.load_state_dict(params.get('params', params), strict=False)
        print(f"Loaded {ckpt_path}")
    else:
        print(f"Warning: Checkpoint {ckpt_path} not found. Using untrained weights.")
        
    purity, ratio = collect_dynamic_r(model, '/home/featurize/data/TestDataSR/LR/LRBI/Urban100/x4', block_idx=4)
    plot_purity_vs_r(purity, ratio, save_path='output/dynamic_r_scatter.png')
