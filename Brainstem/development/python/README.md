
# BrainStem Python Library

The BrainStem python package allows you to interact with a collection
of BrainStem devices using simple python commands.

# Features


- Easily interact with BrainStem devices using python.
- You can learn more about the capabilities of BrainStems at; https://acroname.com/reference/

# Requirements


## python

The brainstem python package is currently compatible with python 2.7 only. It is
recommended that your python version be at least 2.7.9.

MS Windows generally does not include Python, and a suitable Python package will
need to be downloaded and installed before proceeding with the following guide.
The BrainStem wheel is compatible with both 32 and 64bit python 2.7 packages.
At least Python version 2.7.9 is recommended.

MacOS X and most Linux distributions generally include a Python installation.
However, the installation may not include pip and setuptools which are required
to install the BrainStem Python module.

## pip

The brainstem python package is installed via a platform specific wheel. To install
these wheels you need a relatively up to date version of pip and setuptools. Pip
can be installed by following the instructions at:

https://pip.pypa.io/en/latest/installing.html

If you do have pip installed it may be helpful to update pip. To do so, run the
following command from your command line. You may need to have administrator
privileges on MacOS and Linux. Instructions for updating pip can be found at:

https://pip.pypa.io/en/latest/installing.html#upgrade-pip


## libffi

The Brainstem python library relies on libffi. On MacOS X and Windows, this is
generally available. On Linux you may need to install libffi via your distro's
package manager. The package is generally named libffi-dev or similar.

## Python development headers

On Linux, you may need to install the development package for python
via your distro's package manager before you can install. The package is generally
named python-dev or similar.

## CentOS package manager

On CentOS and yum based distros the following command will install the required packages.

```bash
$> sudo yum install libffi-devel python-devel
```

# Installation

Install the python package.

### Note:

`#>`

indicates that the command must be run with admin privileges on MacOS and Linux, either via sudo or su.

```bash
#> pip install brainstem-2.x.x-py2-none-any.whl
```

If you have previously installed the BrainStem python module, you need to specify
the --upgrade flag:

```bash
#> pip install brainstem-2.x.x-py2-none-any.whl --upgrade
```

If you need to uninstall the library, the easiest way to do so is with pip.

```bash
$> pip uninstall brainstem
```

# A Tour of the Python Example


To run the example, simply type:

```bash
$> python brainstem_example.py
```

The example requires that you have a USB BrainStem link module connected to
your host computer. If you see the following message, you probably don't have
a module connected:

```
'Could not find a module.'
```

Once the example starts running, it will print out some basic information about
the module and then blink the user LED on the module. The following is a brief
introduction to writing a python program that talks to your BrainStem.

# Working with BrainStem from the Interpreter

Start up the python interpreter

```bash
$> python
```

The first step is to import the brainstem package:

```python
>>>  import brainstem
```

stem, and discover are the two primary modules. stem contains classes for each
of the distinct module types.

 * USBStem
 * EtherStem
 * MTMIOSerial
 * MTMUSBStem
 * MTMEtherStem
 * USBHub2x4
 * MTMRelay
 * MTMPM1
 * USBHub3p
 * MTMDAQ1
 * USBCSwitch

Next we look for all connected modules:

```python
>>> specs = brainstem.discover.findAllModules(brainstem.link.Spec.USB)
>>> print [str(s) for s in specs]
```

And then looking for the first USB module:

```python
>>>  spec = brainstem.discover.findFirstModule(brainstem.link.Spec.USB)
>>> print spec
```

If we found a USB module, we create a USBStem object and connect to it using
the spec object that was returned by discover:

```python
>>> stem = brainstem.stem.USBStem()
>>> stem.connectFromSpec(spec)
```

And get some information about the module:

```python
>>> result = stem.system.getModel()
>>> print brainstem.defs.model_info(result.value)
```

Finally, we'll flash the user LED, on or off every 100ms.

```python
>>> from time import sleep
>>> for i in range(0,51):
...     err = stem.system.setLED(i % 2)
...     if err != brainstem.result.Result.NO_ERROR:
...         break
...     sleep(0.1)
...
>>>
```

That's it! Once you have this basic example running, a good place to go is the
documentation to learn about all the other features available.

At the prompt type the following:

```python
>>> help(stem.system)
# or
>>> help(brainstem.stem)
```

# Support

If you are having issues, please let us know.
We have a mailing list located at: support@acroname.com

Enjoy!

The Acroname Team.
