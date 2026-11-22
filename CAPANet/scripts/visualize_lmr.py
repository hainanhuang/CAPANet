import sys, torch, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
import os
from PIL import Image
import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))
from basicsr.archs.capanet_arch import CAPANet

def visualize_lmr_branches(
    model, lr_path, block_idx=4,
    save_path='output/lmr_branches.png'
):
    if not os.path.exists(lr_path):
        print(f"Warning: Image {lr_path} not found. Skipping.")
        return
        
    lmr = model.blocks[block_idx][0].lmr
    lmr._vis_hook = True

    img = np.array(Image.open(lr_path).convert('RGB')).astype(np.float32) / 255.0
    H, W = img.shape[:2]
    lq = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)

    with torch.no_grad():
        _ = model(lq)

    def to_energy_map(feat, H, W):
        """feat: (1, N, C) → 对 C 维取 L2 norm → (H, W) 热力图"""
        if feat is None:
            return None
        e = feat[0].norm(dim=-1).numpy()  # (N_level,)
        # N_level 对应降采样后的 token 数，需上采样到 H×W
        side_h = int(round((e.shape[0] * H / W) ** 0.5))
        side_w = int(round(e.shape[0] / side_h))
        if side_h * side_w != e.shape[0]:
            # fallback for non-square ratio
            side = int(round(e.shape[0] ** 0.5))
            e_map = e[:side*side].reshape(side, side)
        else:
            e_map = e.reshape(side_h, side_w)
            
        e_map = cv2.resize(e_map, (W, H), interpolation=cv2.INTER_LINEAR)
        return e_map

    lf_map = to_energy_map(lmr._vis_lf_out, H, W)
    mf_map = to_energy_map(lmr._vis_mf_out, H, W)
    hf_map = to_energy_map(lmr._vis_hf_out, H, W)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(img)
    axes[0].set_title('LR Input')
    axes[0].axis('off')
    for ax, feat_map, title in zip(
        axes[1:],
        [lf_map, mf_map, hf_map],
        ['LF Branch', 'MF Branch', 'HF Branch']
    ):
        if feat_map is not None:
            ax.imshow(feat_map, cmap='hot')
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'LMR branch map saved: {save_path}')
    lmr._vis_hook = False

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
        
    visualize_lmr_branches(model, '/home/featurize/data/TestDataSR/LR/LRBI/Urban100/x4/img001.png',
                           block_idx=4, save_path='output/lmr_branches_b4.png')