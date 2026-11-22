import sys, torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from basicsr.archs.capanet_arch import CAPANet

try:
    from fvcore.nn import FlopCountAnalysis, flop_count_table
except ImportError:
    print("fvcore not found. Please install via: pip install fvcore")
    sys.exit(1)

def calculate_complexity(upscale=4, resolution=(256, 256)):
    model = CAPANet(upscale=upscale, level_head_split=[2,1,1],
                    focus_mode='dynamic', use_sparse_pfsa=True,
                    global_branch_levels=['mf','hf'],
                    attn_state_mode='layered', routing_mode='dpr').eval()
    
    # 统计参数量
    num_params = sum(p.numel() for p in model.parameters())
    print(f"CAPANet x{upscale} Parameters: {num_params / 1e3:.3f} K")
    
    # 统计 FLOPs (MACs)
    # 输入为 1 x 3 x H x W
    dummy_input = torch.randn(1, 3, resolution[0], resolution[1])
    
    flops = FlopCountAnalysis(model, dummy_input)
    macs = flops.total()
    print(f"CAPANet x{upscale} FLOPs (MACs) at {resolution[0]}x{resolution[1]}: {macs / 1e9:.3f} G")
    
    print("\nDetailed Flop Count Table:")
    print(flop_count_table(flops))

if __name__ == '__main__':
    print("Calculating complexity for x2...")
    calculate_complexity(upscale=2)
    print("\n" + "="*50 + "\n")
    print("Calculating complexity for x3...")
    calculate_complexity(upscale=3)
    print("\n" + "="*50 + "\n")
    print("Calculating complexity for x4...")
    calculate_complexity(upscale=4)
