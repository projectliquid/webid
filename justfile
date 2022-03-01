_default:
  @just --list --unsorted

# To create a development environment
dev:
  python3 -m venv .venv
  .venv/bin/python3 -m pip install --require-hashes -r dev-requirements.txt
  .venv/bin/python3 -m pip install --require-hashes -r requirements.txt

# To update the development requirements file
update-dev-requirements:
  .venv/bin/pip-compile --generate-hashes --allow-unsafe --output-file=dev-requirements.txt dev-requirements.in

# To update the runtime requirements file
update-requirements:
  .venv/bin/pip-compile --generate-hashes --allow-unsafe --output-file=requirements.txt requirements.in