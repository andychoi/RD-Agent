import sys
from pathlib import Path
from typing import Optional

from pydantic_settings import SettingsConfigDict

from rdagent.components.coder.CoSTEER.config import CoSTEERSettings
from rdagent.utils.env import Env, LocalConf, LocalEnv


class FactorCoSTEERSettings(CoSTEERSettings):
    model_config = SettingsConfigDict(env_prefix="FACTOR_CoSTEER_")

    data_folder: str = "git_ignore_folder/factor_implementation_source_data"
    """Path to the folder containing financial data (default is fundamental data in Qlib)"""

    data_folder_debug: str = "git_ignore_folder/factor_implementation_source_data_debug"
    """Path to the folder containing partial financial data (for debugging)"""

    simple_background: bool = False
    """Whether to use simple background information for code feedback"""

    file_based_execution_timeout: int = 3600
    """Timeout in seconds for each factor implementation execution"""

    select_method: str = "random"
    """Method for the selection of factors implementation"""

    python_bin: str = "python"
    """Path to the Python binary"""


def get_factor_env(
    conf_type: Optional[str] = None,
    extra_volumes: dict = {},
    running_timeout_period: int = 600,
    enable_cache: Optional[bool] = None,
) -> Env:
    conf = FactorCoSTEERSettings()
    if hasattr(conf, "python_bin"):
        # Source installs commonly run in a venv rather than Conda. Use the
        # active interpreter directly so generated factor code executes in the
        # same tested Python environment as RD-Agent.
        env = LocalEnv(
            conf=LocalConf(
                bin_path=str(Path(sys.executable).parent),
                default_entry="python main.py",
            )
        )
    env.conf.extra_volumes = extra_volumes.copy()
    # macOS does not provide GNU `timeout`; LocalEnv's wrapper would fail before
    # Python starts. CoSTEER retains its own file execution timeout.
    env.conf.running_timeout_period = None
    if enable_cache is not None:
        env.conf.enable_cache = enable_cache
    env.prepare()
    return env


FACTOR_COSTEER_SETTINGS = FactorCoSTEERSettings()
