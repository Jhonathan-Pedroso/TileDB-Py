# multi_attribute.py
#
# LICENSE
#
# The MIT License
#
# Copyright (c) 2018 TileDB, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# DESCRIPTION
#
# This is a part of the TileDB tutorial:
#   https://docs.tiledb.io/en/1.3.0/tutorials/multi-attribute-arrays.html
#
# When run, this program will create a simple 2D dense array with two
# attributes, write some data to it, and read a slice of the data back on
# (i) both attributes, and (ii) subselecting on only one of the attributes.
#


import numpy as np
import sys
import tiledb

# Name of the array to create.
array_name = "multi_attribute"


def create_array():
    # Create a TileDB context
    ctx = tiledb.Ctx()

    # Check if the array already exists.
    if tiledb.object_type(ctx, array_name) == "array":
        return

    # The array will be 4x4 with dimensions "rows" and "cols", with domain [1,4].
    dom = tiledb.Domain(ctx,
                        tiledb.Dim(ctx, name="rows", domain=(1, 4), tile=4, dtype=np.int32),
                        tiledb.Dim(ctx, name="cols", domain=(1, 4), tile=4, dtype=np.int32))

    # Add two attributes "a1" and "a2", so each (i,j) cell can store
    # a character on "a1" and a vector of two floats on "a2".
    schema = tiledb.ArraySchema(ctx, domain=dom, sparse=False,
                                attrs=[tiledb.Attr(ctx, name="a1", dtype=np.uint8),
                                       tiledb.Attr(ctx, name="a2",
                                                   dtype=np.dtype([("", np.float32), ("", np.float32)]))])

    # Create the (empty) array on disk.
    tiledb.DenseArray.create(array_name, schema)


def write_array():
    ctx = tiledb.Ctx()
    # Open the array and write to it.
    with tiledb.DenseArray(ctx, array_name, mode='w') as A:
        data_a1 = np.array((list(map(ord, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                           'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']))))
        data_a2 = np.array(([(1.1, 1.2), (2.1, 2.2), (3.1, 3.2), (4.1, 4.2),
                             (5.1, 5.2), (6.1, 6.2), (7.1, 7.2), (8.1, 8.2),
                             (9.1, 9.2), (10.1, 10.2), (11.1, 11.2), (12.1, 12.2),
                             (13.1, 13.2), (14.1, 14.2), (15.1, 15.2), (16.1, 16.2)]),
                           dtype=[("", np.float32), ("", np.float32)])
        A[:, :] = {"a1": data_a1, "a2": data_a2}


def read_array():
    ctx = tiledb.Ctx()
    # Open the array and read from it.
    with tiledb.DenseArray(ctx, array_name, mode='r') as A:
        # Slice only rows 1, 2 and cols 2, 3, 4.
        data = A[1:3, 2:5]
        print("Reading both attributes a1 and a2:")
        a1, a2 = data["a1"].flat, data["a2"].flat
        for i, v in enumerate(a1):
            print("a1: '%s', a2: (%.1f, %.1f)" % (chr(v), a2[i][0], a2[i][1]))


def read_array_subselect():
    ctx = tiledb.Ctx()
    # Open the array and read from it.
    with tiledb.DenseArray(ctx, array_name, mode='r') as A:
        # Slice only rows 1, 2 and cols 2, 3, 4, attribute 'a1' only.
        # We use the '.query()' syntax which allows attribute subselection.
        data = A.query(attrs=["a1"])[1:3, 2:5]
        print("Subselecting on attribute a1:")
        for a in data["a1"].flat:
            print("a1: '%s'" % chr(a))


create_array()
write_array()
read_array()
read_array_subselect()