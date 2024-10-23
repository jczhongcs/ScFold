import math
import torch.nn as nn
import torch
import itertools
import torch.nn.functional as F
# from mmcv.cnn.bricks import ConvModule

"TransXNet: Learning Both Global and Local Dynamics with a Dual Dynamic Token Mixer for Visual Recognition"


class OSRAttention(nn.Module):  ### OSRA
    def __init__(self, dim,
                 num_heads=8,
                 qk_scale=None,
                 attn_drop=0,
                 sr_ratio=2,):
        super().__init__()

        assert dim % num_heads == 0, f"dim {dim} should be divided by num_heads {num_heads}."
        self.dim = dim
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = qk_scale or head_dim ** -0.5
        self.sr_ratio = sr_ratio
        self.q = nn.Conv2d(dim, dim, kernel_size=1)
        self.kv = nn.Conv2d(dim, dim*2, kernel_size=1)
        self.attn_drop = nn.Dropout(attn_drop)
        if sr_ratio > 1:
            self.sr = nn.Sequential(
                nn.Conv2d(dim, dim,kernel_size=sr_ratio+3,stride=sr_ratio,padding=(sr_ratio+3)//2,groups=dim,bias=False),
                nn.BatchNorm2d(dim),
                nn.ReLU(),
                # ConvModule(dim, dim,
                #            kernel_size=sr_ratio+3,
                #            stride=sr_ratio,
                #            padding=(sr_ratio+3)//2,
                #            groups=dim,
                #            bias=False,
                #            norm_cfg=dict(type='BN2d'),
                #            act_cfg=dict(type='GELU')),
                # ConvModule(dim, dim,
                #            kernel_size=1,
                #            groups=dim,
                #            bias=False,
                #            norm_cfg=dict(type='BN2d'),
                #            act_cfg=None,),)
                nn.Conv2d(dim, dim, kernel_size=1, groups=dim, bias=False),
                nn.BatchNorm2d(dim),)
        else:
            self.sr = nn.Identity()
        self.local_conv = nn.Conv2d(dim, dim, kernel_size=3, padding=1, groups=dim)

    def forward(self, x, relative_pos_enc=None):
        b, c = x.shape
        x = x.reshape(b,c,1,1)
        B, C, H, W = x.shape
        q = self.q(x).reshape(B, self.num_heads, C//self.num_heads, -1).transpose(-1, -2)

        # 通过OSR操作得到k/v表示
        kv = self.sr(x)
        kv = self.local_conv(kv) + kv
        k, v = torch.chunk(self.kv(kv), chunks=2, dim=1)

        k = k.reshape(B, self.num_heads, C//self.num_heads, -1)
        v = v.reshape(B, self.num_heads, C//self.num_heads, -1).transpose(-1, -2)

        attn = (q @ k) * self.scale

        # 为注意力矩阵添加位置编码
        if relative_pos_enc is not None:
            if attn.shape[2:] != relative_pos_enc.shape[2:]:
                relative_pos_enc = F.interpolate(relative_pos_enc, size=attn.shape[2:],
                                                 mode='bicubic', align_corners=False)
            attn = attn + relative_pos_enc

        attn = torch.softmax(attn, dim=-1)
        attn = self.attn_drop(attn)
        x = (attn @ v).transpose(-1, -2)
        return x.reshape(B, C)


if __name__ == '__main__':
    # (B,C,H,W)
    x = torch.randn(500, 128)

    Model = OSRAttention(dim=128)

    out = Model(x)

    print(out.shape)