# GhostFace — Blackpine Cybersecurity

Research-stage privacy project. No protection engine or public service is implemented. No efficacy claims have been validated.

## Development
Python 3.11+; install pinned development dependencies for local image utility tests.

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Read [specification](docs/spec.json), [requirements](docs/requirements.csv), [threat model](docs/threat-model.md), [research register](docs/research-register.md), [licensing gate](docs/licensing-register.md) and [handoff](docs/HANDOFF.md). Do not commit personal images, model weights or credentials. Public repository does not imply a third-party redistribution license.

See [local image utilities](docs/image-utilities.md). These remove metadata and check fidelity; they do not protect against AI cloning.
