import sys, torch, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
import os
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent))
from basicsr.archs.capanet_arch import CAPANet

def visualize_attention_heatmap(
    model, lr_path,
    block_idx=4,       # 选中间层效果更明显
    level='hf',        # 'hf' / 'mf' / 'lf'
    query_group=10,    # 第几个 group window
    query_token=4,     # group 内第几个 token
    save_path='output/attn_heatmap.png',
):
    if not os.path.exists(lr_path):
        print(f"Warning: Image {lr_path} not found. Skipping.")
        return
        
    # 启用钩子
    pfsa = model.blocks[block_idx][0].lmr.level_attn[level]
    pfsa._vis_hook = True

    img = np.array(Image.open(lr_path).convert('RGB')).astype(np.float32) / 255.0
    lq = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)
    with torch.no_grad():
        _ = model(lq)

    # attn_dense / attn_local: (B, num_groups, heads, gs, ws)
    attn_dense = pfsa._vis_attn_dense[0]   # (G, H, gs, ws)
    attn_sparse = pfsa._vis_attn_local[0]  # (G, H, gs, ws)

    # 取指定 group 和 token，对所有 head 做平均
    dense_row = attn_dense[query_group, :, query_token, :].mean(0).numpy()   # (ws,)
    sparse_row = attn_sparse[query_group, :, query_token, :].mean(0).numpy() # (ws,)

    fig, axes = plt.subplots(1, 2, figsize=(10, 3))
    axes[0].bar(range(len(dense_row)), dense_row, color='steelblue', alpha=0.7)
    axes[0].set_title(f'Dense Attention (Block {block_idx}, {level})')
    axes[0].set_xlabel('Key token index')
    axes[1].bar(range(len(sparse_row)), sparse_row, color='tomato', alpha=0.7)
    axes[1].set_title(f'PFSA Sparse Attention (Block {block_idx}, {level})')
    axes[1].set_xlabel('Key token index')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f'Attention heatmap saved: {save_path}')
    pfsa._vis_hook = False

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
        
    visualize_attention_heatmap(model, '/home/featurize/data/TestDataSR/LR/LRBI/Urban100/x4/img001.png',
                                block_idx=4, level='hf', save_path='output/attn_hf_b4.png')
