import pulumi
import pulumi_cloudflare as cloudflare

config = pulumi.Config("site")
zone = config.require_secret("zone_id")
account_id = config.require_secret("account_id")
domain_name = config.require("domain_name")


def static_site():
    pages_projects = cloudflare.PagesProject(
        "site-pages-project",
        account_id=account_id,
        name="personal-site",
        build_config={
            "build_caching": False,
            "build_command": "ls -la",
            "destination_dir": "/html",
            "root_dir": "/",
        },
        production_branch="main",
        source={
            "config": {
                "deployments_enabled": True,
                "pr_comments_enabled": True,
                "production_branch": "main",
                "production_deployments_enabled": True,
                "repo_name": "site",
                "owner": "EdwardSalkeld",
            },
            "type": "github",
        },
    )

    cloudflare.PagesDomain(
        "site-pages-domain",
        account_id=account_id,
        project_name=pages_projects.name,
        name=domain_name,
    )
    cloudflare.DnsRecord(
        "site-pages-dns",
        name=domain_name,
        proxied=True,
        ttl=1,
        type="CNAME",
        content=pages_projects.domains[0],
        zone_id=zone,
    )


static_site()
