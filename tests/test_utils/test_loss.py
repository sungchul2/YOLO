import sys
from pathlib import Path

import pytest
import torch
from hydra import compose, initialize

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from yolo.utils.loss import YOLOLoss


@pytest.fixture
def cfg():
    with initialize(config_path="../../yolo/config", version_base=None):
        cfg = compose(config_name="config")
    return cfg


@pytest.fixture
def loss_function(cfg) -> YOLOLoss:
    return YOLOLoss(cfg)


@pytest.fixture
def data():
    [[torch.zeros]]
    targets = torch.zeros(20, 6, device=torch.device("cuda"))
    predicts = [
        [torch.zeros(1, 144, 80 // i, 80 // i, device=torch.device("cuda")) for i in [1, 2, 4]] for _ in range(2)
    ]
    return predicts, targets


def test_yolo_loss(loss_function, data):
    predicts, targets = data
    loss_iou, loss_dfl, loss_cls = loss_function(predicts, targets)
    assert torch.isnan(loss_iou)
    assert torch.isnan(loss_dfl)
    assert torch.isinf(loss_cls)
