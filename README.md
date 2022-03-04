# papack
A utility to discover possibly missing dependencies and get rid of ones you don't need

## Why do I need it
When you're working on a project that tends to change quickly, such as a startup, or if you're trying out various technologies to solve some problem, you might find yourself
stuck with a large requirements file not knowing which packages are really required for your project and which are not necessary. This is what papack aims to solve.<br>
Another use case might be when you have been included to work on a project, and it turns out it has no `requirements.txt` file (happens all the time on freelance). With papack
you can get the approximate list of packages you need to install.

## How to run it
To run papack you can use
```Python
python -m papack
```
Papack comes with some options. You can access these options with `papack --help`:
```
optional arguments:
  -h, --help            show this help message and exit
  --path PATH           Path to project folder I should check
  --nocheck NOCHECK [NOCHECK ...]
                        List of files and folders I should not look into. Ignores `venv` if not specified
  --implim IMPLIM       Max number of lines that will be checked for presence of imports. Default=50
  --reqs REQS           Path to requirements.txt for this project. Used unless --noreqs flag is set. Defaults to requirements.txt in specified directory
  --noreqs NOREQS       If True, I will not compare data in requirements and installed packages and list differences
  --freeze FREEZE       If True, papack-reqs.txt file with deduced requirements will be generated in project root
  --verbose, -v         Verbosity level (0-3)
```

## Tests
Tests are located in `/tests/` folder. To demonstrate features of papack I typically use the following approach:<br>
- `requirements.txt` file usually contains some irrelevant requirements along with required packages
- `papack-reqs.txt` file contains what papack deduced the requirements to be
- `corr-reqs.txt` file (if present) contains correct requirements. Usually I put this file when papack's prediction is incorrect.<br><br>
###Currently, there are the following tests:
- **Simple flask app** (`/tests/flask/`). There is only a single dependency - `flask`, and papack was able to predict it.

### All code formatted with `autopep8`. It wasn't me who made it hideous)).