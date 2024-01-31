# Guardrails Validator Template
Template repository that hosts a sample validator to be used within GuardrailsHub.

## How to create a Guardrails Validator
- On the top right of the page, click "Use this template", select "create a new repository"  and set a name for the package.
- Modify the class in [validator/main.py](validator/main.py) with source code for the new validator
    - Make sure that the class still inherits from `Validator` and has the `register_validator` annotation.
    - Set the `name` in the `register_validator` to the name of the repo and set the appropriate data type.
- Change [validator/__init__.py](validator/__init__.py) to your new Validator classname instead of RegexMatch
- Locally test the validator with the test instructions below

* Note: This package uses a pyproject.toml file, on first run, run `pip install .` to pull down and install all dependencies

### Testing and using your validator
- Open [test/test-validator.py](test/test-validator.py) to test your new validator 
- Import your new validator and modify `ValidatorTestObject` accordingly
- Modify the TEST_OUTPUT and TEST_FAIL_OUTPUT accordingly
- Run `python test/test-validator.py` via terminal, make sure the returned output reflects the input object 
- Write advanced tests for failures, etc.

## Upload your validator to the validator hub
- Update the [pyproject.toml](pyproject.toml) file and make necessary changes as follows:
    - Update the `name` field to the name of your validator
    - Update the `description` field to a short description of your validator
    - Update the `authors` field to your name and email
    - Add/update the `dependencies` field to include all dependencies your validator needs.
- If there are are any post-installation steps such as downloading tokenizers, logging into huggingface etc., update the [post-install.py](validator/post-install.py) file accordingly.
- You can add additional files to the [validator](validator) directory, but don't rename any existing files/directories.
    - e.g. Add any environment variables (without the values, just the keys) to the [.env](.env) file.
- Ensure that there are no other dependencies or any additional steps required to run your validator.
- Fill out this [form](https://forms.gle/nmxyKwzjypaqvWxbA) to get your new validator onboarded!
