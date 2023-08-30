---
layout: default
title: monty.string.md
nav_exclude: true
---

# monty.string module

Useful additional string functions.


### monty.string.boxed(msg, ch='=', pad=5)
Returns a string in a box


* **Parameters**


    * **msg** – Input string.


    * **ch** – Character used to form the box.


    * **pad** – Number of characters ch added before and after msg.


```python
>>> print(boxed("hello", ch="*", pad=2))
***********
** hello **
***********
```


### monty.string.indent(lines, amount, ch=' ')
Indent the lines in a string by padding each one with proper number of pad
characters


### monty.string.is_string(s)
True if s behaves like a string (duck typing test).


### monty.string.list_strings(arg)
Always return a list of strings, given a string or list of strings as
input.


* **Examples**


```python
>>> list_strings('A single string')
['A single string']
```

```python
>>> list_strings(['A single string in a list'])
['A single string in a list']
```

```python
>>> list_strings(['A','list','of','strings'])
['A', 'list', 'of', 'strings']
```


### monty.string.make_banner(s, width=78, mark='\*')

* **Parameters**


    * **s** – String


    * **width** – Width of banner. Defaults to 78.


    * **mark** – The mark used to create the banner.



* **Returns**

    Banner string.



### monty.string.marquee(text='', width=78, mark='\*')
Return the input string centered in a ‘marquee’.


* **Parameters**


    * **text** (*str*) – Input string


    * **width** (*int*) – Width of final output string.


    * **mark** (*str*) – Character used to fill string.



* **Examples**


```python
>>> marquee('A test', width=40)
'**************** A test ****************'
```

```python
>>> marquee('A test', width=40, mark='-')
'---------------- A test ----------------'
```

marquee(‘A test’,40, ‘ ‘)
‘                 A test                 ‘


### monty.string.remove_non_ascii(s)
Remove non-ascii characters in a file. Needed when support for non-ASCII
is not available.


* **Parameters**

    **s** (*str*) – Input string



* **Returns**

    String with all non-ascii characters removed.



### monty.string.unicode2str(s)
Forces a unicode to a string in Python 2, but transparently handles
Python 3.


* **Parameters**

    **s** (*str/unicode*) – Input string / unicode.



* **Returns**

    str in Python 2. Unchanged otherwise.