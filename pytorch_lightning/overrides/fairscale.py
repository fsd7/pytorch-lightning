# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import operator

import torch.nn as nn

import pytorch_lightning as pl
from pytorch_lightning.overrides.base import _LightningModuleWrapperBase, unwrap_lightning_module
from pytorch_lightning.utilities import _module_available
from pytorch_lightning.utilities.imports import _compare_version, _IS_WINDOWS

_FAIRSCALE_AVAILABLE = not _IS_WINDOWS and _module_available("fairscale.nn")
_FAIRSCALE_OSS_FP16_BROADCAST_AVAILABLE = _FAIRSCALE_AVAILABLE and _compare_version("fairscale", operator.ge, "0.3.3")
_FAIRSCALE_FULLY_SHARDED_AVAILABLE = _FAIRSCALE_AVAILABLE and _compare_version("fairscale", operator.ge, "0.3.4")

if _FAIRSCALE_AVAILABLE:
    from fairscale.nn.data_parallel.sharded_ddp import ShardedDataParallel

    class LightningShardedDataParallel(_LightningModuleWrapperBase):
        # Just do this for later docstrings
        pass

    def unwrap_lightning_module_sharded(wrapped_model: nn.Module) -> "pl.LightningModule":
        model = wrapped_model
        if isinstance(model, ShardedDataParallel):
            model = model.module

        return unwrap_lightning_module(model)

else:
    LightningShardedDataParallel = ...  # type: ignore[assignment,misc]
    unwrap_lightning_module_sharded = ...  # type: ignore[assignment]
