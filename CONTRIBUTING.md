# Contributing

We welcome each and every reasonable contribution to this project!
If you are unsure whether your idea is a good fit, please do not hesitate to open an issue or ask one of the maintainers on Discord.

To make sure your merge request can pass our CI and gets accepted we kindly ask you to follow the instructions below:

## Code Formatting

This project uses [pre-commit](https://github.com/pre-commit/pre-commit) to
verify compliance with formatting rules. To use:

1. Pip install `pre-commit`
2. From inside the project's root directory, run `pre-commit install`.
3. You're all done! Code will be checked automatically using git hooks.

## Testing

Please include proper unit tests for all new functionality.

We are using [Python unittest](https://docs.python.org/3/library/unittest.html) with the Django `TestCase` classes for all tests.
