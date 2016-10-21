# Custom PyDev Build

Using the PyDev module requires configuring a debugger path mapping inside of the code.
Path mappings relate file paths on the server with the corresponding path in the local development environment.
For example…

 - `/communityshare/community_share/app.py`
 - `~/projects/communityshare/community_share/app.py`

This is inconvenient for a community project where every local development environment might have a different local path for the code.

The solution taken in this project is to pull in the `LOCAL_CODE_PATH` environment variable directly into the `pydevd/pydevd_file_utils.py` module, [assigning its value to `PATHS_FROM_ECLIPSE_TO_PYTHON`](https://brianfisher.name/content/remote-debugging-python-eclipse-and-pydev). The environment variable is easily set in `docker-compose.yml` with `$PWD` interpolation.

Unfortunately, adding the `pydevd` module and code changes into this repository added over 41,000 lines of code, making for one impossible PR to review.

Therefore, after making the appropriate changes to the `pydevd` module, I [created an egg](http://www.blog.pythonlibrary.org/2012/07/12/python-101-easy_install-or-how-to-create-eggs/) to package all of the code into a single-file _egg_ archive.

## To build custom `pydevd` module

 - Copy `pydev` [source code](http://www.pydev.org/download.html) into the `pydev` sub-directory.
 - Update file utility to load in `LOCAL_CODE_PATH` from the `debugger` module. See below for the required code.
 - From within the Docker console, rebuild the egg with `python setup.py bdist_egg`
 - Move the egg from `pydev/dist/` into this directory and rename to `pydev-custom-eclipse.egg`
 - Remove the `pydev` directory

### Custom path-mapping

```python
# Find this assignment in pydevd_file_utils.py
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
import debugger

PATHS_FROM_ECLIPSE_TO_PYTHON = [(
    debugger.local_path,
    '/communityshare/'
)]
```