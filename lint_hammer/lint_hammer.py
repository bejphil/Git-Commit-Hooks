#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import sys
import os
import fnmatch

import autopep8
import git


class LintHammer:

    def __init__(self, args):

        self.__args = args
        path = os.path.dirname(os.path.realpath(__file__))

        self.__root_dir = self.__git_root_directory(path)

    def __call__(self):
        py_files = self.__files_with_extension(self.__root_dir, '*.py')

        for py_file in py_files:
            self.__fix_files(py_file, self.__args)

    def __git_root_directory(self, path):

        git_repo = git.Repo(path, search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")

        return git_root

    def __find_files(self, directory, pattern):
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename

    def __files_with_extension(self, root_directory, extension):

        valid_files = []

        for filename in self.__find_files(root_directory, extension):
            valid_files.append(filename)

        return valid_files

    def __fix_files(self, file_path, args):

        with io.open(file_path, encoding='UTF-8') as f:
            original_contents = f.read()

        corrected_text = autopep8.fix_code(original_contents, args)

        if original_contents != corrected_text:

            print( "Applying autopep8 to: ", file_path )
            with io.open(file_path, 'w', encoding='UTF-8') as output_file:
                output_file.write(corrected_text)

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = argv
    # args = autopep8.parse_args(argv, apply_config=True)

    hammer = LintHammer( args )
    hammer()


if __name__ == '__main__':
    exit(main())
