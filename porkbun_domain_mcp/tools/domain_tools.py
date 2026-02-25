"""Domain management MCP tools.

This module provides MCP tools for managing domains through the Porkbun API.

Tools provided:
- list_domains: List all domains in the account
- get_domain_info: Get detailed information for a domain
- get_auth_code: Get transfer authorization code (EPP code)
- renew_domain: Renew a domain registration
- get_pricing: Get domain pricing information
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from porkbun_domain_mcp.client import PorkbunDomainClient
from porkbun_domain_mcp.config import get_logger_instance
from porkbun_domain_mcp.models import Domain, PricingInfo

if TYPE_CHECKING:
    from fastmcp import FastMCP

logger = get_logger_instance("porkbun-domain-mcp.tools")


class ToolResponse(BaseModel):
    """Standardized LLM-friendly tool response."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable result message")
    data: dict[str, Any] | None = Field(
        default=None,
        description="Structured output data",
    )
    error: str | None = Field(
        default=None,
        description="Error details if operation failed",
    )
    next_steps: list[str] | None = Field(
        default=None,
        description="Suggested follow-up actions",
    )


def _domain_to_dict(domain: Domain) -> dict[str, Any]:
    """Convert Domain to dictionary for API response."""
    return {
        "domain": domain.domain,
        "status": domain.status,
        "tld": domain.tld,
        "create_date": domain.create_date,
        "expire_date": domain.expire_date,
        "whois_privacy": domain.whois_privacy,
        "auto_renew": domain.auto_renew,
        "not_local": domain.not_local,
    }


def _pricing_to_dict(pricing: PricingInfo) -> dict[str, Any]:
    """Convert PricingInfo to dictionary."""
    return {
        "tld": pricing.tld,
        "registration": pricing.registration,
        "renewal": pricing.renewal,
        "transfer": pricing.transfer,
    }


def register_domain_tools(app: "FastMCP", client: PorkbunDomainClient) -> None:
    """Register domain management tools with the FastMCP app."""

    @app.tool()
    async def list_domains() -> ToolResponse:
        """List all domains in your Porkbun account.

        Retrieves a list of all domains registered through Porkbun
        associated with the configured API credentials.

        Returns:
            ToolResponse with list of domains
        """
        logger.info("Listing domains")

        try:
            domains = await client.list_domains()

            return ToolResponse(
                success=True,
                message=f"Found {len(domains)} domains in your account",
                data={
                    "domains": [_domain_to_dict(d) for d in domains],
                    "count": len(domains),
                },
                next_steps=[
                    "Use get_domain_info for details on a specific domain",
                    "Use get_pricing to check renewal costs",
                    "Use renew_domain to extend registration",
                ],
            )

        except Exception as e:
            logger.error("Failed to list domains", error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to list domains",
                error=str(e),
                next_steps=[
                    "Verify your API credentials are valid",
                    "Check network connectivity",
                ],
            )

    @app.tool()
    async def get_domain_info(domain: str) -> ToolResponse:
        """Get detailed information for a specific domain.

        Args:
            domain: Domain name (e.g., 'example.com')

        Returns:
            ToolResponse with domain details
        """
        logger.info("Getting domain info", domain=domain)

        try:
            d = await client.get_domain_info(domain)

            return ToolResponse(
                success=True,
                message=f"Retrieved information for {domain}",
                data={
                    "domain": _domain_to_dict(d),
                },
                next_steps=[
                    "Use get_auth_code to get transfer authorization",
                    "Use renew_domain to extend registration",
                ],
            )

        except Exception as e:
            logger.error("Failed to get domain info", domain=domain, error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to get info for {domain}",
                error=str(e),
                next_steps=[
                    "Verify the domain name is correct",
                    "Ensure the domain is in your account",
                    "Use list_domains to see all your domains",
                ],
            )

    @app.tool()
    async def get_auth_code(domain: str) -> ToolResponse:
        """Get transfer authorization code (EPP code) for a domain.

        The auth code is required to transfer a domain to another registrar.
        Keep this code secure!

        Args:
            domain: Domain name (e.g., 'example.com')

        Returns:
            ToolResponse with the auth code
        """
        logger.info("Getting auth code", domain=domain)

        try:
            auth_code = await client.get_auth_code(domain)

            return ToolResponse(
                success=True,
                message=f"Retrieved auth code for {domain}",
                data={
                    "domain": domain,
                    "auth_code": auth_code,
                },
                next_steps=[
                    "Provide this code to the gaining registrar",
                    "Unlock the domain at Porkbun before transfer",
                    "Verify the admin email is correct for transfer approval",
                ],
            )

        except Exception as e:
            logger.error("Failed to get auth code", domain=domain, error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to get auth code for {domain}",
                error=str(e),
                next_steps=[
                    "Verify the domain is in your account",
                    "Check if the domain is eligible for transfer",
                ],
            )

    @app.tool()
    async def renew_domain(domain: str, years: int = 1) -> ToolResponse:
        """Renew a domain registration.

        Extends the registration period for a domain.

        Args:
            domain: Domain name (e.g., 'example.com')
            years: Number of years to renew (1-10, default: 1)

        Returns:
            ToolResponse with renewal result
        """
        logger.info("Renewing domain", domain=domain, years=years)

        try:
            result = await client.renew_domain(domain, years)

            return ToolResponse(
                success=True,
                message=f"Renewed {domain} for {years} year(s)",
                data=result,
                next_steps=[
                    "Check the new expiration date",
                    "Verify auto-renew is configured if desired",
                ],
            )

        except Exception as e:
            logger.error("Failed to renew domain", domain=domain, error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to renew {domain}",
                error=str(e),
                next_steps=[
                    "Verify the domain is in your account",
                    "Check if the domain is eligible for renewal",
                    "Ensure you have sufficient account balance",
                ],
            )

    @app.tool()
    async def get_pricing(tld: str | None = None) -> ToolResponse:
        """Get domain pricing information.

        Shows registration, renewal, and transfer pricing for TLDs.

        Args:
            tld: Optional TLD to filter by (e.g., 'com', 'net')
                 If not provided, returns pricing for all TLDs

        Returns:
            ToolResponse with pricing information
        """
        logger.info("Getting pricing", tld=tld)

        try:
            pricing = await client.get_pricing(tld)

            pricing_list = [
                {"tld": t, **_pricing_to_dict(p)}
                for t, p in pricing.items()
            ]

            return ToolResponse(
                success=True,
                message=f"Retrieved pricing for {len(pricing_list)} TLD(s)",
                data={
                    "pricing": pricing_list,
                    "count": len(pricing_list),
                },
                next_steps=[
                    "Compare prices across TLDs",
                    "Use this info to plan domain registrations",
                ],
            )

        except Exception as e:
            logger.error("Failed to get pricing", error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to get pricing information",
                error=str(e),
                next_steps=[
                    "Try again later",
                    "Check network connectivity",
                ],
            )

    logger.info("Registered 5 domain management tools")
