#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Verify that we handle %module(directors="1") statements, both with and
without white space before the opening parenthesis.
"""

import TestSCons

test = TestSCons.TestSCons()

swig = test.where_is('swig')

if not swig:
    test.skip_test('Can not find installed "swig", skipping test.\n')

python_include_dir = test.get_python_inc()

test.write(['SConstruct'], """\
env = Environment(SWIGFLAGS = '-python',
                  CPPPATH=r"%(python_include_dir)s")

import sys
if sys.version[0] == '1':
    # SWIG requires the -classic flag on pre-2.0 Python versions.
    env.Append(SWIGFLAGS = ' -classic')

env.SharedLibrary('test1.so', 'test1.i')
env.SharedLibrary('test2.so', 'test2.i')
""" % locals())

test.write(['test1.cc'], """\
int test1func()
{
  return 0;
}
""")

test.write(['test1.h'], """\
int test1func();
""")

test.write(['test1.i'], """\
%module(directors="1") test1

%{
#include "test1.h"
%}

%include "test1.h"
""")

test.write(['test2.cc'], """\
int test2func()
{
  return 0;
}
""")

test.write(['test2.h'], """\
int test2func();
""")

test.write(['test2.i'], """\
%module (directors="1") test2

%{
#include "test2.h"
%}

%include "test2.h"
""")

test.run(arguments = '.')

test.up_to_date(arguments = '.')

test.pass_test()
