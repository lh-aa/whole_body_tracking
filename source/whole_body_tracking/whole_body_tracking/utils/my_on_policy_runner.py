import os

from rsl_rl.env import VecEnv
from rsl_rl.runners.on_policy_runner import OnPolicyRunner

from isaaclab_rl.rsl_rl import export_policy_as_onnx

from whole_body_tracking.utils.exporter import attach_onnx_metadata, export_motion_policy_as_onnx


class MyOnPolicyRunner(OnPolicyRunner):
    def save(self, path: str, infos=None):
        """Save the model and training information."""
        super().save(path, infos)
        # Always export ONNX locally without wandb dependency
        policy_path = path.split("model")[0]
        filename = policy_path.split("/")[-2] + ".onnx"
        export_policy_as_onnx(self.alg.policy, normalizer=self.obs_normalizer, path=policy_path, filename=filename)
        # Attach minimal metadata (no wandb run path)
        try:
            attach_onnx_metadata(self.env.unwrapped, "none", path=policy_path, filename=filename)
        except Exception:
            pass


class MotionOnPolicyRunner(OnPolicyRunner):
    def __init__(
        self, env: VecEnv, train_cfg: dict, log_dir: str | None = None, device="cpu", registry_name: str = None
    ):
        super().__init__(env, train_cfg, log_dir, device)
        self.registry_name = registry_name

    def save(self, path: str, infos=None):
        """Save the model and training information."""
        super().save(path, infos)
        # Always export ONNX locally without wandb dependency
        policy_path = path.split("model")[0]
        filename = policy_path.split("/")[-2] + ".onnx"
        export_motion_policy_as_onnx(
            self.env.unwrapped, self.alg.policy, normalizer=self.obs_normalizer, path=policy_path, filename=filename
        )
        # Attach minimal metadata (no wandb run path)
        try:
            attach_onnx_metadata(self.env.unwrapped, "none", path=policy_path, filename=filename)
        except Exception:
            pass
        # Do not link/use wandb artifacts
        self.registry_name = None
