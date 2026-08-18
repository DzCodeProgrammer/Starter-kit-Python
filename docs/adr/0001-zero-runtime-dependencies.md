# ADR 0001: Keep the foundation free of runtime dependencies

- Status: accepted
- Date: 2026-08-18

## Context

This repository must be reusable for command-line tools, workers, services, and libraries.
Choosing a framework or configuration/logging package in the base layer would impose upgrade,
security, and compatibility costs on every derived project.

## Decision

The starter implements its foundational CLI, configuration, logging, context propagation, and
diagnostics with the Python standard library. Third-party tools are isolated in PEP 735 development
dependency groups and do not appear in built wheel metadata as runtime requirements.

## Consequences

The installed package remains small and has a minimal supply-chain surface. Derived applications
may add frameworks deliberately. Some conveniences require more local code, which is accepted as
long as it remains typed, tested, and narrowly scoped.
