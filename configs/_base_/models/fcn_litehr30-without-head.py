# model settings
_base_ = './fcn_litehr18-without-head.py'
model = dict(
    backbone=dict(extra=dict(stages_spec=dict(num_modules=(3, 8, 3)))))
