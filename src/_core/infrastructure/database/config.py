from typing import Any

from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_recycle: int = 3600
    pool_pre_ping: bool = True
    connect_args: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_env(cls, env: str) -> "DatabaseConfig":
        """Create configuration based on environment."""
        if env == "prod":
            return cls(
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_recycle=3600,
                pool_pre_ping=True,
                connect_args={
                    "timeout": 10,
                    "connect_timeout": 10,
                    "command_timeout": 30,
                    "server_settings": {
                        "statement_timeout": "30000",
                        "idle_in_transaction_session_timeout": "300000",
                        "application_name": "server_api",
                    },
                },
            )

        # Default (local/dev) configuration
        return cls(echo=True, pool_size=5, max_overflow=10, pool_pre_ping=True)
