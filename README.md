# Site-infra

This is the IaC repo for hosting my very barebones personal site.

Requires `uv` installed.

## Current infra

Cloudflare PagesProject to host site, with custom domain and DNS record.

## Development

### Type Checking

This project uses [ty](https://docs.astral.sh/ty/) for type checking. To run type checks locally:

```bash
# Install dependencies including dev dependencies
uv sync --all-groups

# Run type check
uv run ty check .
```

**Note:** Type checking runs automatically on pull requests as an advisory check (non-failing). Ty may timeout on complex dependencies like Pulumi, which is expected behavior.
