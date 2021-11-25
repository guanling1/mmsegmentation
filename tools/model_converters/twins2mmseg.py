# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import os.path as osp
from collections import OrderedDict

import mmcv
import torch
from mmcv.runner import CheckpointLoader


def convert_vit(args, ckpt):

    new_ckpt = OrderedDict()

    for k, v in list(ckpt.items()):
        new_v = v
        if k.startswith('head'):
            continue
        elif k.startswith('backbone.patch_embeds'):
            if 'proj.' in k:
                new_k = k.replace('proj.', 'projection.')
            else:
                new_k = k
        elif k.startswith('backbone.blocks'):
            # Union
            if 'attn.q.' in k:
                new_k = k.replace('q.', 'attn.in_proj_')
                new_v = torch.cat([v, ckpt[k.replace('attn.q.', 'attn.kv.')]],
                                  dim=0)
            elif 'mlp.fc1' in k:
                new_k = k.replace('mlp.fc1', 'ffn.layers.0.0')
            elif 'mlp.fc2' in k:
                new_k = k.replace('mlp.fc2', 'ffn.layers.1')

            # Only pcpvt
            if args.model == 'pcpvt':
                if 'attn.proj.' in k:
                    new_k = k.replace('proj.', 'attn.out_proj.')
                else:
                    new_k = k

            # Only svt
            if args.model == 'svt':
                if 'attn.proj.' in k:
                    k_lst = k.split('.')
                    if int(k_lst[3]) % 2 == 1:
                        new_k = k.replace('proj.', 'attn.out_proj.')
                    else:
                        new_k = k
                else:
                    new_k = k
        elif k.startswith('backbone.pos_block'):
            if 'proj.0.' in k:
                new_k = k.replace('proj.0.', 'proj.')
            else:
                new_k = k
        else:
            new_k = k
        if 'attn.kv.' not in k:
            new_ckpt[new_k] = new_v
    return new_ckpt


def main():
    parser = argparse.ArgumentParser(
        description='Convert keys in timm pretrained vit models to '
        'MMSegmentation style.')
    parser.add_argument('src', help='src model path or url')
    # The dst path must be a full path of the new checkpoint.
    parser.add_argument('dst', help='save path')
    parser.add_argument('model', help='model: pcpvt or svt')
    args = parser.parse_args()

    checkpoint = CheckpointLoader.load_checkpoint(args.src, map_location='cpu')

    state_dict = checkpoint
    if 'state_dict' in checkpoint:
        # timm checkpoint
        state_dict = checkpoint['state_dict']
    else:
        state_dict = checkpoint

    weight = convert_vit(args, state_dict)

    checkpoint['state_dict'] = weight
    mmcv.mkdir_or_exist(osp.dirname(args.dst))
    torch.save(checkpoint, args.dst)


if __name__ == '__main__':
    main()
