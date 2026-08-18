# Open-source references

This starter kit synthesizes maintained practices from the following public projects and official
guides. The implementation remains intentionally smaller than any one template and adapts ideas
rather than copying a generated project wholesale.

## Packaging and project structure

- [PyPA Sample Project](https://github.com/pypa/sampleproject) for standards-based `pyproject.toml`
  metadata and source layout.
- [Scientific Python Cookie](https://github.com/scientific-python/cookie) for PEP 735 dependency
  groups, strict pytest configuration, documentation, repository review, and modern build choices.
- [Hypermodern Python](https://github.com/cjolowicz/cookiecutter-hypermodern-python) for the unified
  approach to packaging, testing, documentation, coverage, typing, and security automation.

## Dependency management, CI, and containers

- [Astral uv GitHub Actions guide](https://github.com/astral-sh/uv/blob/main/docs/guides/integration/github.md)
  for locked synchronization, Python matrices, caching, and isolated distribution smoke tests.
- [Astral uv Docker guide](https://github.com/astral-sh/uv/blob/main/docs/guides/integration/docker.md)
  for pinned uv images, lockfile-based installs, cache mounts, non-editable environments, bytecode
  compilation, and multi-stage images.
- [Copier UV](https://github.com/pawamoy/copier-uv) for cross-platform tasks, generated API
  documentation, conventional changelogs, and repository lifecycle conventions.
- [Serious Scaffold Python](https://github.com/serious-scaffold/ss-python) for cross-platform CI,
  dev containers, long-term maintenance documentation, and distribution/container releases.

## Security and releases

- [Zizmor](https://github.com/zizmorcore/zizmor) for GitHub Actions security analysis and immutable
  dependency pins.
- [PyPA trusted publishing action](https://github.com/pypa/gh-action-pypi-publish) for the principle
  of separating unprivileged builds from privileged publication and preferring OIDC over tokens.
- [GitHub's Python build guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
  for job permissions, artifacts, and packaging workflow structure.

Revisit these upstreams periodically; toolchain and supply-chain practices evolve quickly.
