"""
Comprehensive test suite for configuration module.

Tests cover:
- Environment variable loading
- Configuration validation
- Default value application
- Type conversions
- Error handling
- Edge cases
"""

import os
from typing import Any
from unittest.mock import patch

import pytest

from src.config import Config


class TestConfigInitialization:
    """Test suite for Config class initialization and environment variable loading."""

    def test_config_loads_all_required_environment_variables(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config successfully loads all required environment variables."""
        # Arrange
        env_vars = {
            "API_KEY": "test_api_key_12345",
            "API_SECRET": "test_api_secret_67890",
            "TRADING_PAIRS": "EURUSD,GBPUSD,XAUUSD",
            "RISK_REWARD_RATIO": "2",
            "MAX_POSITION_SIZE": "1000",
            "STOP_LOSS_PERCENTAGE": "2.5",
        }
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # Act
        config = Config()

        # Assert
        assert config.API_KEY == "test_api_key_12345"
        assert config.API_SECRET == "test_api_secret_67890"
        assert config.TRADING_PAIRS == ["EURUSD", "GBPUSD", "XAUUSD"]
        assert config.RISK_REWARD_RATIO == 2
        assert config.MAX_POSITION_SIZE == 1000
        assert config.STOP_LOSS_PERCENTAGE == 2.5

    def test_config_applies_default_values_when_optional_vars_missing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config applies default values for optional environment variables."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")

        # Act
        config = Config()

        # Assert
        assert config.TRADING_PAIRS == ["EURUSD", "GBPUSD", "XAUUSD"]
        assert config.RISK_REWARD_RATIO == 2
        assert config.MAX_POSITION_SIZE == 1000
        assert config.STOP_LOSS_PERCENTAGE == 2.0

    def test_config_raises_value_error_when_api_key_missing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config raises ValueError when API_KEY is not set."""
        # Arrange
        monkeypatch.delenv("API_KEY", raising=False)
        monkeypatch.setenv("API_SECRET", "test_secret")

        # Act & Assert
        with pytest.raises(ValueError, match="API_KEY environment variable is required"):
            Config()

    def test_config_raises_value_error_when_api_secret_missing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config raises ValueError when API_SECRET is not set."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.delenv("API_SECRET", raising=False)

        # Act & Assert
        with pytest.raises(
            ValueError, match="API_SECRET environment variable is required"
        ):
            Config()

    def test_config_raises_value_error_when_both_credentials_missing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config raises ValueError when both API credentials are missing."""
        # Arrange
        monkeypatch.delenv("API_KEY", raising=False)
        monkeypatch.delenv("API_SECRET", raising=False)

        # Act & Assert
        with pytest.raises(ValueError, match="API_KEY environment variable is required"):
            Config()


class TestConfigTradingPairs:
    """Test suite for TRADING_PAIRS configuration."""

    def test_trading_pairs_returns_list_from_comma_separated_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that TRADING_PAIRS correctly parses comma-separated string."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("TRADING_PAIRS", "EURUSD,GBPUSD,XAUUSD")

        # Act
        config = Config()

        # Assert
        assert isinstance(config.TRADING_PAIRS, list)
        assert config.TRADING_PAIRS == ["EURUSD", "GBPUSD", "XAUUSD"]

    def test_trading_pairs_handles_whitespace_in_values(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that TRADING_PAIRS strips whitespace from values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("TRADING_PAIRS", " EURUSD , GBPUSD , XAUUSD ")

        # Act
        config = Config()

        # Assert
        assert config.TRADING_PAIRS == ["EURUSD", "GBPUSD", "XAUUSD"]

    def test_trading_pairs_handles_single_pair(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that TRADING_PAIRS handles single trading pair correctly."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("TRADING_PAIRS", "EURUSD")

        # Act
        config = Config()

        # Assert
        assert config.TRADING_PAIRS == ["EURUSD"]

    def test_trading_pairs_handles_empty_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that TRADING_PAIRS handles empty string by using default."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("TRADING_PAIRS", "")

        # Act
        config = Config()

        # Assert
        assert config.TRADING_PAIRS == ["EURUSD", "GBPUSD", "XAUUSD"]

    def test_trading_pairs_filters_empty_values(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that TRADING_PAIRS filters out empty values from comma-separated list."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("TRADING_PAIRS", "EURUSD,,GBPUSD,")

        # Act
        config = Config()

        # Assert
        assert config.TRADING_PAIRS == ["EURUSD", "GBPUSD"]


class TestConfigRiskRewardRatio:
    """Test suite for RISK_REWARD_RATIO configuration."""

    def test_risk_reward_ratio_converts_string_to_integer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that RISK_REWARD_RATIO converts string to integer."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("RISK_REWARD_RATIO", "3")

        # Act
        config = Config()

        # Assert
        assert isinstance(config.RISK_REWARD_RATIO, int)
        assert config.RISK_REWARD_RATIO == 3

    def test_risk_reward_ratio_validates_positive_integer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that RISK_REWARD_RATIO validates positive integer values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("RISK_REWARD_RATIO", "-1")

        # Act & Assert
        with pytest.raises(
            ValueError, match="RISK_REWARD_RATIO must be a positive integer"
        ):
            Config()

    def test_risk_reward_ratio_rejects_zero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that RISK_REWARD_RATIO rejects zero value."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("RISK_REWARD_RATIO", "0")

        # Act & Assert
        with pytest.raises(
            ValueError, match="RISK_REWARD_RATIO must be a positive integer"
        ):
            Config()

    def test_risk_reward_ratio_rejects_non_numeric_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that RISK_REWARD_RATIO rejects non-numeric string values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("RISK_REWARD_RATIO", "invalid")

        # Act & Assert
        with pytest.raises(ValueError, match="RISK_REWARD_RATIO must be a valid integer"):
            Config()

    def test_risk_reward_ratio_rejects_float_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that RISK_REWARD_RATIO rejects float string values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("RISK_REWARD_RATIO", "2.5")

        # Act & Assert
        with pytest.raises(ValueError, match="RISK_REWARD_RATIO must be a valid integer"):
            Config()


class TestConfigMaxPositionSize:
    """Test suite for MAX_POSITION_SIZE configuration."""

    def test_max_position_size_converts_string_to_integer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that MAX_POSITION_SIZE converts string to integer."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("MAX_POSITION_SIZE", "5000")

        # Act
        config = Config()

        # Assert
        assert isinstance(config.MAX_POSITION_SIZE, int)
        assert config.MAX_POSITION_SIZE == 5000

    def test_max_position_size_validates_positive_integer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that MAX_POSITION_SIZE validates positive integer values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("MAX_POSITION_SIZE", "-100")

        # Act & Assert
        with pytest.raises(
            ValueError, match="MAX_POSITION_SIZE must be a positive integer"
        ):
            Config()

    def test_max_position_size_rejects_zero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that MAX_POSITION_SIZE rejects zero value."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("MAX_POSITION_SIZE", "0")

        # Act & Assert
        with pytest.raises(
            ValueError, match="MAX_POSITION_SIZE must be a positive integer"
        ):
            Config()


class TestConfigStopLossPercentage:
    """Test suite for STOP_LOSS_PERCENTAGE configuration."""

    def test_stop_loss_percentage_converts_string_to_float(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that STOP_LOSS_PERCENTAGE converts string to float."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("STOP_LOSS_PERCENTAGE", "3.5")

        # Act
        config = Config()

        # Assert
        assert isinstance(config.STOP_LOSS_PERCENTAGE, float)
        assert config.STOP_LOSS_PERCENTAGE == 3.5

    def test_stop_loss_percentage_validates_positive_value(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that STOP_LOSS_PERCENTAGE validates positive values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("STOP_LOSS_PERCENTAGE", "-1.5")

        # Act & Assert
        with pytest.raises(
            ValueError, match="STOP_LOSS_PERCENTAGE must be a positive number"
        ):
            Config()

    def test_stop_loss_percentage_rejects_zero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that STOP_LOSS_PERCENTAGE rejects zero value."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("STOP_LOSS_PERCENTAGE", "0")

        # Act & Assert
        with pytest.raises(
            ValueError, match="STOP_LOSS_PERCENTAGE must be a positive number"
        ):
            Config()

    def test_stop_loss_percentage_rejects_non_numeric_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that STOP_LOSS_PERCENTAGE rejects non-numeric string values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("STOP_LOSS_PERCENTAGE", "invalid")

        # Act & Assert
        with pytest.raises(
            ValueError, match="STOP_LOSS_PERCENTAGE must be a valid number"
        ):
            Config()

    def test_stop_loss_percentage_handles_integer_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that STOP_LOSS_PERCENTAGE handles integer string values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("STOP_LOSS_PERCENTAGE", "5")

        # Act
        config = Config()

        # Assert
        assert isinstance(config.STOP_LOSS_PERCENTAGE, float)
        assert config.STOP_LOSS_PERCENTAGE == 5.0


class TestConfigEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_config_handles_empty_api_key(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config rejects empty API_KEY."""
        # Arrange
        monkeypatch.setenv("API_KEY", "")
        monkeypatch.setenv("API_SECRET", "test_secret")

        # Act & Assert
        with pytest.raises(ValueError, match="API_KEY environment variable is required"):
            Config()

    def test_config_handles_empty_api_secret(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config rejects empty API_SECRET."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "")

        # Act & Assert
        with pytest.raises(
            ValueError, match="API_SECRET environment variable is required"
        ):
            Config()

    def test_config_handles_whitespace_only_api_key(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config rejects whitespace-only API_KEY."""
        # Arrange
        monkeypatch.setenv("API_KEY", "   ")
        monkeypatch.setenv("API_SECRET", "test_secret")

        # Act & Assert
        with pytest.raises(ValueError, match="API_KEY environment variable is required"):
            Config()

    def test_config_handles_very_large_risk_reward_ratio(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config handles very large RISK_REWARD_RATIO values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("RISK_REWARD_RATIO", "1000000")

        # Act
        config = Config()

        # Assert
        assert config.RISK_REWARD_RATIO == 1000000

    def test_config_handles_very_small_stop_loss_percentage(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config handles very small STOP_LOSS_PERCENTAGE values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("STOP_LOSS_PERCENTAGE", "0.01")

        # Act
        config = Config()

        # Assert
        assert config.STOP_LOSS_PERCENTAGE == 0.01

    def test_config_handles_special_characters_in_credentials(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config handles special characters in API credentials."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key!@#$%^&*()")
        monkeypatch.setenv("API_SECRET", "test_secret_+=[]{}|;:',.<>?/")

        # Act
        config = Config()

        # Assert
        assert config.API_KEY == "test_key!@#$%^&*()"
        assert config.API_SECRET == "test_secret_+=[]{}|;:',.<>?/"


class TestConfigImmutability:
    """Test suite for configuration immutability and singleton behavior."""

    def test_config_values_are_accessible(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that all Config values are accessible after initialization."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")

        # Act
        config = Config()

        # Assert
        assert hasattr(config, "API_KEY")
        assert hasattr(config, "API_SECRET")
        assert hasattr(config, "TRADING_PAIRS")
        assert hasattr(config, "RISK_REWARD_RATIO")
        assert hasattr(config, "MAX_POSITION_SIZE")
        assert hasattr(config, "STOP_LOSS_PERCENTAGE")

    def test_config_creates_new_instance_each_time(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config creates new instance on each instantiation."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")

        # Act
        config1 = Config()
        config2 = Config()

        # Assert
        assert config1 is not config2
        assert config1.API_KEY == config2.API_KEY


class TestConfigTypeConversions:
    """Test suite for type conversion edge cases."""

    def test_config_handles_leading_zeros_in_integers(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config handles leading zeros in integer values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("RISK_REWARD_RATIO", "003")

        # Act
        config = Config()

        # Assert
        assert config.RISK_REWARD_RATIO == 3

    def test_config_handles_scientific_notation_in_float(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config handles scientific notation in float values."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        monkeypatch.setenv("STOP_LOSS_PERCENTAGE", "2.5e0")

        # Act
        config = Config()

        # Assert
        assert config.STOP_LOSS_PERCENTAGE == 2.5

    def test_config_handles_very_long_trading_pairs_list(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that Config handles very long TRADING_PAIRS list."""
        # Arrange
        monkeypatch.setenv("API_KEY", "test_key")
        monkeypatch.setenv("API_SECRET", "test_secret")
        pairs = ",".join([f"PAIR{i}" for i in range(100)])
        monkeypatch.setenv("TRADING_PAIRS", pairs)

        # Act
        config = Config()

        # Assert
        assert len(config.TRADING_PAIRS) == 100
        assert config.TRADING_PAIRS[0] == "PAIR0"
        assert config.TRADING_PAIRS[99] == "PAIR99"


@pytest.fixture
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixture to ensure clean environment for each test."""
    env_vars = [
        "API_KEY",
        "API_SECRET",
        "TRADING_PAIRS",
        "RISK_REWARD_RATIO",
        "MAX_POSITION_SIZE",
        "STOP_LOSS_PERCENTAGE",
    ]
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def valid_config_env(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Fixture providing valid configuration environment variables."""
    env_vars = {
        "API_KEY": "test_api_key",
        "API_SECRET": "test_api_secret",
        "TRADING_PAIRS": "EURUSD,GBPUSD,XAUUSD",
        "RISK_REWARD_RATIO": "2",
        "MAX_POSITION_SIZE": "1000",
        "STOP_LOSS_PERCENTAGE": "2.0",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars