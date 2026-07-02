"""Secure secrets management using environment variables and vaults."""

import os
from typing import Optional
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class SecretsManager:
    """Secure secrets management."""
    
    @staticmethod
    def get_secret(
        key: str,
        default: Optional[str] = None,
        required: bool = False
    ) -> Optional[str]:
        """Get secret from environment variables."""
        value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"Required secret {key} not found")
        
        if not value:
            logger.warning(f"Secret {key} not found, using default")
        
        return value
    
    @staticmethod
    def validate_secrets() -> bool:
        """Validate that all required secrets are set."""
        required_secrets = [
            "DATABASE_URL",
            "JWT_SECRET",
            "SECRET_KEY",
        ]
        
        missing = []
        for secret in required_secrets:
            if not os.getenv(secret):
                missing.append(secret)
        
        if missing:
            logger.error(f"Missing required secrets: {', '.join(missing)}")
            return False
        
        return True
    
    @staticmethod
    def encrypt_value(value: str, key: str) -> str:
        """Encrypt a value using Fernet encryption."""
        cipher = Fernet(key.encode())
        return cipher.encrypt(value.encode()).decode()
    
    @staticmethod
    def decrypt_value(encrypted: str, key: str) -> str:
        """Decrypt a value using Fernet decryption."""
        cipher = Fernet(key.encode())
        return cipher.decrypt(encrypted.encode()).decode()


class VaultManager:
    """Manager for external vault services (HashiCorp Vault, AWS Secrets Manager, etc)."""
    
    @staticmethod
    def get_from_vault(secret_path: str) -> Optional[dict]:
        """Get secret from HashiCorp Vault."""
        import hvac
        
        try:
            vault_addr = os.getenv("VAULT_ADDR", "http://localhost:8200")
            vault_token = os.getenv("VAULT_TOKEN")
            
            if not vault_token:
                logger.warning("VAULT_TOKEN not set, skipping vault lookup")
                return None
            
            client = hvac.Client(url=vault_addr, token=vault_token)
            secret = client.secrets.kv.v2.read_secret_version(path=secret_path)
            return secret["data"]["data"]
        except Exception as e:
            logger.error(f"Failed to retrieve secret from vault: {str(e)}")
            return None
    
    @staticmethod
    def get_from_aws_secrets(
        secret_name: str,
        region_name: str = "us-east-1"
    ) -> Optional[dict]:
        """Get secret from AWS Secrets Manager."""
        try:
            import boto3
            import json
            
            client = boto3.client("secretsmanager", region_name=region_name)
            response = client.get_secret_value(SecretId=secret_name)
            
            if "SecretString" in response:
                return json.loads(response["SecretString"])
            else:
                logger.error("Secret is binary, not JSON")
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve secret from AWS: {str(e)}")
            return None
