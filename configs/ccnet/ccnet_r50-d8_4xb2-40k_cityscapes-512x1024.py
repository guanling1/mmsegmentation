_base_ = [
    '../_base_/models/ccnet_r50-d8_deepglobe_5.py', '../_base_/datasets/deepGlobe.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_40k.py'
]
crop_size = (256, 256)
data_preprocessor = dict(size=crop_size)
model = dict(data_preprocessor=data_preprocessor)
