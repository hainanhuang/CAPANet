import matplotlib.pyplot as plt
import numpy as np
import os

# 格式: {方法名: (Params/K, FLOPs/G, Urban100-PSNR)}
models = {
    'Bicubic':       (0,     0,      23.14),
    'IMDN':          (715,   58.5,   26.04),
    'RFDN':          (534,   23.9,   26.61),
    'CATANet':       (535,   55.2,   26.95),
    'PFT-light':     (560,   50.3,   26.87),
    'SwinIR-light':  (930,   89.7,   26.47),
    'CAPANet':       (617,   59.8,   26.98),
}

def plot_pareto(models_dict, dataset_name="Urban100"):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, x_key, x_label in [
        (axes[0], 0, 'Params (K)'),
        (axes[1], 1, 'FLOPs (G)'),
    ]:
        for name, vals in models_dict.items():
            x, psnr = vals[x_key], vals[2]
            # 跳过 bicubic 如果是 params 和 flops
            if name == 'Bicubic' and x == 0:
                continue
                
            color = 'tomato' if name == 'CAPANet' else 'steelblue'
            marker = '*' if name == 'CAPANet' else 'o'
            size   = 200 if name == 'CAPANet' else 60
            ax.scatter(x, psnr, color=color, marker=marker, s=size, zorder=3)
            ax.annotate(name, (x, psnr), textcoords='offset points',
                        xytext=(5, 3), fontsize=8)
        ax.set_xlabel(x_label)
        ax.set_ylabel(f'PSNR (dB) on {dataset_name} x4')
        ax.set_title(f'PSNR vs {x_label}')
        ax.grid(True, linestyle='--', alpha=0.4)

    plt.tight_layout()
    save_path = f'output/pareto_{dataset_name.lower()}.png'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f'Pareto plot saved: {save_path}')

if __name__ == '__main__':
    plot_pareto(models, "Urban100")
