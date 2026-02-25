"""Porkbun API client for domain management.

This module provides an async HTTP client for interacting with the Porkbun Domain API.

API Documentation: https://porkbun.com/api/json/v3/documentation
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from .config import PorkbunDomainSettings, get_logger_instance, get_settings
from .models import (
    AuthCodeResponse,
    Domain,
    DomainsResponse,
    PorkbunError,
    PricingInfo,
    PricingResponse,
)

logger = get_logger_instance("porkbun-domain-mcp.client")


class PorkbunDomainClient:
    """Async HTTP client for Porkbun Domain API.

    Provides methods for managing domains through the Porkbun API.
    All operations require authentication via API key and secret key.

    Attributes:
        settings: Configuration settings
        client: HTTPX async client
    """

    def __init__(self, settings: PorkbunDomainSettings | None = None) -> None:
        """Initialize the Porkbun domain client."""
        self.settings = settings or get_settings()
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "PorkbunDomainClient":
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            config = self.settings.http_client_config()
            self._client = httpx.AsyncClient(**config)
            logger.debug(
                "HTTP client initialized",
                base_url=config["base_url"],
                timeout=self.settings.timeout,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.debug("HTTP client closed")

    async def _request(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated request to the Porkbun API."""
        client = await self._ensure_client()

        # Merge authentication payload with request payload
        full_payload = {**self.settings.auth_payload()}
        if payload:
            full_payload.update(payload)

        # Retry logic with exponential backoff
        last_error: Exception | None = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                response = await client.request(
                    method,
                    endpoint,
                    json=full_payload,
                )
                response.raise_for_status()

                data = response.json()

                # Check Porkbun API status
                if data.get("status", "").upper() != "SUCCESS":
                    message = data.get("message", "Unknown API error")
                    raise PorkbunError(
                        message=message,
                        status=response.status_code,
                        details=data,
                    )

                logger.debug(
                    "API request successful",
                    endpoint=endpoint,
                    attempt=attempt + 1,
                )
                return data

            except httpx.HTTPStatusError as e:
                last_error = e
                logger.warning(
                    "API request failed",
                    endpoint=endpoint,
                    status_code=e.response.status_code,
                    attempt=attempt + 1,
                )
                if attempt < self.settings.max_retries:
                    await asyncio.sleep(0.5 * (2**attempt))
                else:
                    raise PorkbunError(
                        message=f"HTTP {e.response.status_code}: {e.response.text}",
                        status=e.response.status_code,
                    ) from e

            except httpx.RequestError as e:
                last_error = e
                logger.warning(
                    "API request error",
                    endpoint=endpoint,
                    error=str(e),
                    attempt=attempt + 1,
                )
                if attempt < self.settings.max_retries:
                    await asyncio.sleep(0.5 * (2**attempt))
                else:
                    raise PorkbunError(
                        message=f"Request failed: {e}",
                    ) from e

        raise PorkbunError(
            message=f"Request failed after {self.settings.max_retries} retries",
        ) from last_error

    # =========================================================================
    # Domain Operations
    # =========================================================================

    async def list_domains(self) -> list[Domain]:
        """Retrieve all domains in the account.

        Returns:
            List of domains
        """
        logger.debug("Listing domains")

        data = await self._request("POST", "/domain/list/all")

        response = DomainsResponse(**data)
        return response.domains

    async def get_domain_info(self, domain: str) -> Domain:
        """Get detailed information for a domain.

        Args:
            domain: Domain name

        Returns:
            Domain information
        """
        logger.debug("Getting domain info", domain=domain)

        # Porkbun doesn't have a direct domain info endpoint
        # We need to list all and find the specific one
        domains = await self.list_domains()

        for d in domains:
            if d.domain == domain:
                return d

        raise PorkbunError(
            message=f"Domain {domain} not found in account",
            status=404,
        )

    async def get_auth_code(self, domain: str) -> str:
        """Get transfer authorization code (EPP code) for a domain.

        Args:
            domain: Domain name

        Returns:
            Authorization code
        """
        logger.debug("Getting auth code", domain=domain)

        data = await self._request("POST", f"/domain/getAuthCode/{domain}")

        response = AuthCodeResponse(**data)
        return response.auth_code or ""

    async def renew_domain(self, domain: str, years: int = 1) -> dict[str, Any]:
        """Renew a domain.

        Args:
            domain: Domain name
            years: Number of years to renew (1-10)

        Returns:
            Renewal result
        """
        logger.debug("Renewing domain", domain=domain, years=years)

        payload = {"years": years}

        data = await self._request(
            "POST",
            f"/domain/renew/{domain}",
            payload,
        )

        return {
            "domain": domain,
            "years": years,
            "success": True,
            "message": data.get("message", "Domain renewed successfully"),
        }

    async def get_pricing(self, tld: str | None = None) -> dict[str, PricingInfo]:
        """Get domain pricing information.

        Note: This endpoint doesn't require authentication.

        Args:
            tld: Optional TLD to filter by

        Returns:
            Pricing information by TLD
        """
        logger.debug("Getting pricing", tld=tld)

        # Pricing endpoint doesn't require auth
        client = await self._ensure_client()

        # Use minimal auth payload for public endpoint
        response = await client.post(
            "/pricing/get",
            json=self.settings.auth_payload(),
        )
        response.raise_for_status()
        data = response.json()

        if data.get("status", "").upper() != "SUCCESS":
            raise PorkbunError(
                message=data.get("message", "Failed to get pricing"),
            )

        pricing_response = PricingResponse(**data)

        if tld:
            if tld in pricing_response.pricing:
                return {tld: pricing_response.pricing[tld]}
            return {}

        return pricing_response.pricing


__all__ = ["PorkbunDomainClient"]
