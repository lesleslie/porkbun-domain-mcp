"""Pydantic models for Porkbun Domain API request/response validation.

This module defines all the data models used for interacting with the
Porkbun Domain API, including domain listings, registration, and transfers.

API Documentation: https://porkbun.com/api/json/v3/documentation
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class DomainStatus(str, Enum):
    """Domain status values."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    TRANSFER_PENDING = "TRANSFER PENDING"
    WHOIS_PENDING = "WHOIS PENDING"


class WhoisPrivacy(str, Enum):
    """WHOIS privacy status."""

    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    NOT_ELIGIBLE = "NOT ELIGIBLE"


class Domain(BaseModel):
    """A domain from Porkbun API.

    Attributes:
        domain: Domain name
        status: Domain status
        tld: Top-level domain
        create_date: Registration date
        expire_date: Expiration date
        whois_privacy: WHOIS privacy status
        auto_renew: Auto-renew enabled
        not_local: Whether domain is not managed at Porkbun
    """

    domain: str = Field(description="Domain name")
    status: str = Field(description="Domain status")
    tld: str = Field(description="Top-level domain")
    create_date: str | None = Field(default=None, description="Registration date")
    expire_date: str | None = Field(default=None, description="Expiration date")
    whois_privacy: str | None = Field(default=None, description="WHOIS privacy status")
    auto_renew: bool | None = Field(default=None, description="Auto-renew enabled")
    not_local: bool | None = Field(default=None, description="Not managed at Porkbun")


class DomainInfo(BaseModel):
    """Detailed domain information.

    Attributes:
        domain: Domain name
        status: Domain status
        nameservers: List of nameservers
        security: Security features (DNSSEC, etc.)
        whois_privacy: WHOIS privacy status
        auto_renew: Auto-renew enabled
    """

    domain: str = Field(description="Domain name")
    status: str = Field(description="Domain status")
    nameservers: list[str] = Field(
        default_factory=list,
        description="List of nameservers",
    )
    security: dict[str, Any] | None = Field(
        default=None,
        description="Security features",
    )
    whois_privacy: str | None = Field(default=None, description="WHOIS privacy status")
    auto_renew: bool | None = Field(default=None, description="Auto-renew enabled")


class AuthCode(BaseModel):
    """Domain transfer authorization code (EPP code).

    Attributes:
        domain: Domain name
        auth_code: Transfer authorization code
    """

    domain: str = Field(description="Domain name")
    auth_code: str = Field(description="Transfer authorization code (EPP code)")


class RenewalResult(BaseModel):
    """Result of a domain renewal.

    Attributes:
        domain: Domain name
        years: Number of years renewed
        new_expire_date: New expiration date
        success: Whether renewal was successful
    """

    domain: str = Field(description="Domain name")
    years: int = Field(description="Number of years renewed")
    new_expire_date: str | None = Field(
        default=None,
        description="New expiration date",
    )
    success: bool = Field(description="Whether renewal was successful")


class PricingInfo(BaseModel):
    """Domain pricing information.

    Attributes:
        tld: Top-level domain
        registration: Registration price
        renewal: Renewal price
        transfer: Transfer price
    """

    tld: str = Field(description="Top-level domain")
    registration: str | None = Field(default=None, description="Registration price")
    renewal: str | None = Field(default=None, description="Renewal price")
    transfer: str | None = Field(default=None, description="Transfer price")


class PorkbunResponse(BaseModel):
    """Base response from Porkbun API."""

    status: str = Field(description="Response status: SUCCESS or ERROR")
    message: str | None = Field(
        default=None,
        description="Error message when status is ERROR",
    )

    @property
    def success(self) -> bool:
        """Check if the response indicates success."""
        return self.status.upper() == "SUCCESS"


class DomainsResponse(PorkbunResponse):
    """Response containing domain list."""

    domains: list[Domain] = Field(
        default_factory=list,
        description="List of domains",
    )


class PricingResponse(PorkbunResponse):
    """Response containing pricing information."""

    pricing: dict[str, PricingInfo] = Field(
        default_factory=dict,
        description="Pricing by TLD",
    )


class AuthCodeResponse(PorkbunResponse):
    """Response containing auth code."""

    auth_code: str | None = Field(
        default=None,
        description="Transfer authorization code",
    )


class PorkbunError(Exception):
    """Exception raised for Porkbun API errors."""

    def __init__(
        self,
        message: str,
        status: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        result: dict[str, Any] = {
            "error": self.message,
            "status": self.status,
        }
        if self.details:
            result["details"] = self.details
        return result


__all__ = [
    "DomainStatus",
    "WhoisPrivacy",
    "Domain",
    "DomainInfo",
    "AuthCode",
    "RenewalResult",
    "PricingInfo",
    "PorkbunResponse",
    "DomainsResponse",
    "PricingResponse",
    "AuthCodeResponse",
    "PorkbunError",
]
