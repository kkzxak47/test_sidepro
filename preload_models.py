from diffusers import AmusedPipeline
import torch


pipe = AmusedPipeline.from_pretrained("amused/amused-256", torch_dtype=torch.float32)

