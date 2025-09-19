"""
Settings and configuration management.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class Settings:
    """
    Central configuration management for the application.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize settings from config dict, file, or environment variables.
        
        Args:
            config: Optional configuration dictionary
        """
        self._config = {}
        
        # Load configuration in order of precedence:
        # 1. Default values
        # 2. Config file
        # 3. Environment variables
        # 4. Passed config parameter
        
        self._load_defaults()
        self._load_config_file()
        self._load_environment_variables()
        
        if config:
            self._config.update(config)
            
        self._validate_config()
        
    def _load_defaults(self):
        """Load default configuration values."""
        self._config = {
            "claude": {
                "api_key": None,
                "model": "claude-3-sonnet",
                "max_tokens": 4000,
                "temperature": 0.1
            },
            "codex": {
                "api_key": None,
                "model": "code-davinci-002",
                "max_tokens": 2000,
                "temperature": 0.1
            },
            "templates": {
                "directory": "templates/",
                "default_language": "python"
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "output": {
                "directory": "output/",
                "overwrite": False
            }
        }
        
    def _load_config_file(self):
        """Load configuration from YAML file."""
        config_paths = [
            "config/config.yaml",
            "config.yaml",
            os.path.expanduser("~/.codex-claude-crosstalk/config.yaml")
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        file_config = yaml.safe_load(f)
                        if file_config:
                            self._merge_config(self._config, file_config)
                            logger.info(f"Loaded configuration from {config_path}")
                            break
                except Exception as e:
                    logger.warning(f"Failed to load config from {config_path}: {e}")
                    
    def _load_environment_variables(self):
        """Load configuration from environment variables."""
        env_mappings = {
            "CLAUDE_API_KEY": ("claude", "api_key"),
            "CLAUDE_MODEL": ("claude", "model"),
            "OPENAI_API_KEY": ("codex", "api_key"),
            "CODEX_MODEL": ("codex", "model"),
            "TEMPLATES_DIR": ("templates", "directory"),
            "OUTPUT_DIR": ("output", "directory"),
            "LOG_LEVEL": ("logging", "level")
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                if section not in self._config:
                    self._config[section] = {}
                self._config[section][key] = value
                logger.debug(f"Set {section}.{key} from environment variable {env_var}")
                
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Recursively merge configuration dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
                
    def _validate_config(self):
        """Validate the configuration."""
        # Check for required API keys in production mode
        if not self._config["claude"]["api_key"]:
            logger.warning("No Claude API key configured - will run in simulation mode")
            
        if not self._config["codex"]["api_key"]:
            logger.warning("No OpenAI API key configured - will run in simulation mode")
            
        # Ensure directories exist
        os.makedirs(self._config["templates"]["directory"], exist_ok=True)
        os.makedirs(self._config["output"]["directory"], exist_ok=True)
        
    @property
    def claude_config(self) -> Dict[str, Any]:
        """Get Claude configuration."""
        return self._config["claude"]
        
    @property
    def codex_config(self) -> Dict[str, Any]:
        """Get Codex configuration."""
        return self._config["codex"]
        
    @property
    def templates_config(self) -> Dict[str, Any]:
        """Get templates configuration."""
        return self._config["templates"]
        
    @property
    def logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self._config["logging"]
        
    @property
    def output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self._config["output"]
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'claude.model')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'claude.model')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        
    def to_dict(self) -> Dict[str, Any]:
        """Return the configuration as a dictionary."""
        return self._config.copy()
        
    def save_to_file(self, file_path: str):
        """
        Save the current configuration to a YAML file.
        
        Args:
            file_path: Path to save the configuration file
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                yaml.dump(self._config, f, default_flow_style=False)
            logger.info(f"Configuration saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration to {file_path}: {e}")
            raise