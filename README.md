# Job Scheduler

## Development
Setup the pre-commit hooks for automated Python formatting.

```bash
pip install yapf
wget -O ../.git/hooks/pre-commit https://raw.githubusercontent.com/google/yapf/main/plugins/pre-commit.sh
chmod +x ../.git/hooks/pre-commit
```