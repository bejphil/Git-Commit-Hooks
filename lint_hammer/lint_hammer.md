# Super Lint-Hammer

## Intro

This hook applies an code formatter, `autopep8`, to all Python files in a git repository.
It can be particularly useful for improving linter scores or correcting minor
stylistic errors before code is submitted for review.

## Dependencies

The Lint-Hammer is requires the use of a python3 interpreter and the following
packages.

* [autopep8](https://github.com/hhatto/autopep8)
* [gitpython](https://github.com/gitpython-developers/GitPython)

Both of the these packages are hosted on PyPi and can be installed using `pip`.

## Script Structure

First we need to identity the root directory of the Git repo that is currently
running the script.

```python
def git_root_directory(self, path):

    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")

    return git_root
```

Next we need to be able to find all files with a particular extension in a directory
and all sub-directories.

```python
def find_files( directory, pattern ):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def files_with_extension( root_directory, extension ):

    valid_files = []

    for filename in self.__find_files(root_directory, extension):
        valid_files.append(filename)

    return valid_files
```

Next we need a way to apply `autopep8` to a single file. This involves reading the
file, applying the formatter and overwritting the file if any changes were made.

```python
def fix_files( file_path, args ):

    with io.open(file_path, encoding='UTF-8') as f:
        original_contents = f.read()

    corrected_text = autopep8.fix_code(original_contents, args)

    if original_contents != corrected_text:

        print( "Applying autopep8 to: ", file_path )
        with io.open(file_path, 'w', encoding='UTF-8') as output_file:
            output_file.write(corrected_text)

```

To complete the hook all we need to do if find all files with the `*.py` extension
in any sub-directories of the Git root and apply the code formatter.

```python
def lint_hammer():
    py_files = self.__files_with_extension(self.__root_dir, '*.py')

    for py_file in py_files:
        self.__fix_files(py_file, self.__args)

```
