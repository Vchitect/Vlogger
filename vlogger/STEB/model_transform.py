import torch
# import argparse
# from omegaconf import OmegaConf
# from models import get_models
# import sys
# import os
# from PIL import Image
# from copy import deepcopy


def tca_transform_model(model):
    for down_block in model.down_blocks:
        try:
            for attention in down_block.attentions:
                attention.transformer_blocks[0].tca_transform()
                attention.transformer_blocks[0].tca_transform()
        except:
            continue
    for attention in model.mid_block.attentions:
        attention.transformer_blocks[0].tca_transform()
        attention.transformer_blocks[0].tca_transform()
    for up_block in model.up_blocks:
        try:
            for attention in up_block.attentions:
                attention.transformer_blocks[0].tca_transform()
                attention.transformer_blocks[0].tca_transform()
        except:
            continue
    return model


class ImageProjModel(torch.nn.Module):
    """Projection Model"""
    def __init__(self, cross_attention_dim=1024, clip_embeddings_dim=1024, clip_extra_context_tokens=4):
        super().__init__()
        
        self.cross_attention_dim = cross_attention_dim
        self.clip_extra_context_tokens = clip_extra_context_tokens
        self.proj = torch.nn.Linear(clip_embeddings_dim, self.clip_extra_context_tokens * cross_attention_dim)
        self.norm = torch.nn.LayerNorm(cross_attention_dim)
        
    def forward(self, image_embeds):
        embeds = image_embeds
        clip_extra_context_tokens = self.proj(embeds).reshape(-1, self.clip_extra_context_tokens, self.cross_attention_dim)
        clip_extra_context_tokens = self.norm(clip_extra_context_tokens)
        return clip_extra_context_tokens
    

def ip_transform_model(model):
    model.image_proj_model = ImageProjModel(cross_attention_dim=768, clip_embeddings_dim=1024,
                                            clip_extra_context_tokens=4).to(model.device)
    for down_block in model.down_blocks:
        try:
            for attention in down_block.attentions:
                attention.transformer_blocks[0].attn2.ip_transform()
                attention.transformer_blocks[0].attn2.ip_transform()
        except:
            continue
    for attention in model.mid_block.attentions:
        attention.transformer_blocks[0].attn2.ip_transform()
        attention.transformer_blocks[0].attn2.ip_transform()
    for up_block in model.up_blocks:
        try:
            for attention in up_block.attentions:
                attention.transformer_blocks[0].attn2.ip_transform()
                attention.transformer_blocks[0].attn2.ip_transform()
        except:
            continue
    return model


def ip_scale_set(model, scale):
    for down_block in model.down_blocks:
        try:
            for attention in down_block.attentions:
                attention.transformer_blocks[0].attn2.set_scale(scale)
                attention.transformer_blocks[0].attn2.set_scale(scale)
        except:
            continue
    for attention in model.mid_block.attentions:
        attention.transformer_blocks[0].attn2.set_scale(scale)
        attention.transformer_blocks[0].attn2.set_scale(scale)
    for up_block in model.up_blocks:
        try:
            for attention in up_block.attentions:
                attention.transformer_blocks[0].attn2.set_scale(scale)
                attention.transformer_blocks[0].attn2.set_scale(scale)
        except:
            continue
    return model


def ip_train_set(model):
    model.requires_grad_(False)
    model.image_proj_model.requires_grad_(True)
    for down_block in model.down_blocks:
        try:
            for attention in down_block.attentions:
                attention.transformer_blocks[0].attn2.ip_train_set()
                attention.transformer_blocks[0].attn2.ip_train_set()
        except:
            continue
    for attention in model.mid_block.attentions:
        attention.transformer_blocks[0].attn2.ip_train_set()
        attention.transformer_blocks[0].attn2.ip_train_set()
    for up_block in model.up_blocks:
        try:
            for attention in up_block.attentions:
                attention.transformer_blocks[0].attn2.ip_train_set()
                attention.transformer_blocks[0].attn2.ip_train_set()
        except:
            continue
    return model
