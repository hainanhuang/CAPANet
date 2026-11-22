import sys, torch, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
import os
from PIL import Image
from einops import rearrange

sys.path.insert(0, str(Path(__file__).parent.parent))
from basicsr.archs.capanet_arch import CAPANet
from basicsr.utils.img_util import img2tensor

def load_model(ckpt_path, upscale=4):
    model = CAPANet(
        upscale=upscale,
        level_head_split=[2, 1, 1],
        focus_mode='dynamic',
        use_sparse_pfsa=True,
        global_branch_levels=['mf', 'hf'],
        attn_state_mode='layered',
        routing_mode='dpr',
    ).eval()
    if os.path.exists(ckpt_path):
        ckpt = torch.load(ckpt_path, map_location='cpu')
        params = ckpt.get('params', ckpt)
        model.load_state_dict(params, strict=False)
        print(f"Loaded {ckpt_path}")
    else:
        print(f"Warning: Checkpoint {ckpt_path} not found. Using untrained weights for demonstration.")
    return model

def visualize_dpr_routing(model, lr_path, block_idx=0, save_path='output/dpr_routing.png'):
    if not os.path.exists(lr_path):
        print(f"Warning: Image {lr_path} not found. Skipping.")
        return
        
    # 在目标 block 上启用钩子
    target_block = model.blocks[block_idx][0]  # CAPABlock
    target_block._vis_hook = True

    # 读取 LR 图像
    img = np.array(Image.open(lr_path).convert('RGB')).astype(np.float32) / 255.0
    lq = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)

    with torch.no_grad():
        _ = model(lq)

    H_lr, W_lr = lq.shape[2], lq.shape[3]
    labels = target_block._vis_orig_labels[0]  # (H*W,)
    scores = target_block._vis_x_scores
    
    # 直接用 orig_labels 重塑为图像
    label_map = labels.numpy().reshape(H_lr, W_lr)  # (H_lr, W_lr)

    K = int(labels.max().item()) + 1
    # 给每个 prototype 分配不同颜色
    cmap = plt.get_cmap('tab20', K)
    color_map = cmap(label_map / max(K - 1, 1))[:, :, :3]  # (H, W, 3)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(img)
    axes[0].set_title('LR Input')
    axes[0].axis('off')
    axes[1].imshow(color_map)
    axes[1].set_title(f'DPR Prototype Map (Block {block_idx})')
    axes[1].axis('off')
    # 叠加
    overlay = 0.5 * img + 0.5 * color_map
    axes[2].imshow(overlay.clip(0, 1))
    axes[2].set_title('Overlay')
    axes[2].axis('off')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"DPR routing saved: {save_path}")
    target_block._vis_hook = False

if __name__ == '__main__':
    # ===== 调用示例 =====
    model = load_model('experiments/train_CAPANet_x4_finetune/models/net_g_latest.pth')
    visualize_dpr_routing(model, '/home/featurize/data/TestDataSR/LR/LRBI/Urban100/x4/img001.png',
                          block_idx=0, save_path='output/dpr_routing_block0.png')
    visualize_dpr_routing(model, '/home/featurize/data/TestDataSR/LR/LRBI/Urban100/x4/img001.png',
                          block_idx=7, save_path='output/dpr_routing_block7.png')
