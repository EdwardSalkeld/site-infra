from typing import Any
import pulumi
import pulumi_cloudflare as cloudflare

config = pulumi.Config("site")
zone = config.require_secret("zone_id")
account_id = config.require_secret("account_id")
domain_name = config.require("domain_name")


class StaticSiteConfig:
    resource_name: str = "site"
    site_name: str = "personal-site"
    build_config: dict[str, str | bool] = {
        "build_caching": False,
        "build_command": "ls -la",
        "destination_dir": "/html",
        "root_dir": "/",
    }
    repo_name: str = "site"
    domain_name: str = domain_name


def static_site(config: StaticSiteConfig):
    pages_projects = cloudflare.PagesProject(
        f"{config.resource_name}-pages-project",
        account_id=account_id,
        name=config.site_name,
        build_config=config.build_config,
        production_branch="main",
        source={
            "config": {
                "deployments_enabled": True,
                "pr_comments_enabled": True,
                "production_branch": "main",
                "production_deployments_enabled": True,
                "repo_name": config.repo_name,
                "owner": "EdwardSalkeld",
            },
            "type": "github",
        },
    )

    cloudflare.PagesDomain(
        f"{config.resource_name}-pages-domain",
        account_id=account_id,
        project_name=pages_projects.name,
        name=config.domain_name,
    )
    cloudflare.DnsRecord(
        f"{config.resource_name}-pages-dns",
        name=config.domain_name,
        proxied=True,
        ttl=1,
        type="CNAME",
        content=pages_projects.domains[0],
        zone_id=zone,
    )


# main personal site
personal = StaticSiteConfig()
personal.build_config = {
    "build_caching": True,
    "build_command": "hugo",
    "destination_dir": "/public",
    "root_dir": "/hugo-site",
}
static_site(personal)

# liff archive sub site
liff_config = StaticSiteConfig()
liff_config.resource_name = "liff"
liff_config.site_name = "liff-archive"
liff_config.repo_name = "liff-archive"
liff_config.domain_name = f"liff.{domain_name}"
liff_config.build_config = {
    "build_caching": False,
    "build_command": "hugo",
    "destination_dir": "/public",
    "root_dir": "/hugo",
}
static_site(liff_config)
