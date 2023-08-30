---
layout: default
title: monty.termcolor.md
nav_exclude: true
---

# monty.termcolor module

Copyright (c) 2008-2011 Volvox Development Team

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: Konstantin Lepa <[konstantin.lepa@gmail.com](mailto:konstantin.lepa@gmail.com)>

ANSII Color formatting for output in terminal.


### monty.termcolor.colored(text, color=None, on_color=None, attrs=None)
Colorize text.

Available text colors:

    red, green, yellow, blue, magenta, cyan, white.

Available text highlights:

    on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

Available attributes:

    bold, dark, underline, blink, reverse, concealed.

### Example

colored(‘Hello, World!’, ‘red’, ‘on_grey’, [‘blue’, ‘blink’])
colored(‘Hello, World!’, ‘green’)


### monty.termcolor.cprint(text, color=None, on_color=None, attrs=None, \*\*kwargs)
Print colorize text.

It accepts arguments of print function.