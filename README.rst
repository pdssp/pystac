.. highlight:: shell

===============================
pySTAC
===============================

.. image:: https://img.shields.io/github/v/tag/pole-surfaces-planetaires/pystac
.. image:: https://img.shields.io/github/v/release/pole-surfaces-planetaires/pystac?include_prereleases

.. image:: https://img.shields.io/pypi/v/pystac

.. image https://img.shields.io/github/downloads/pole-surfaces-planetaires/pystac/total
.. image https://img.shields.io/github/issues-raw/pole-surfaces-planetaires/pystac
.. image https://img.shields.io/github/issues-pr-raw/pole-surfaces-planetaires/pystac
.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/pole-surfaces-planetaires/pystac/graphs/commit-activity
.. image https://img.shields.io/github/license/pole-surfaces-planetaires/pystac
.. image https://img.shields.io/github/forks/pole-surfaces-planetaires/pystac?style=social


Library implementing STAC protocole


Stable release
--------------

To install pySTAC, run this command in your terminal:

.. code-block:: console

    $ pip install pystac

This is the preferred method to install pySTAC, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for pySTAC can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/pole-surfaces-planetaires/pystac

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/pole-surfaces-planetaires/pystac/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make  # install in the system root
    $ make user # or Install for non-root usage


.. _Github repo: https://github.com/pole-surfaces-planetaires/pystac
.. _tarball: https://github.com/pole-surfaces-planetaires/pystac/tarball/master



Development
-----------

.. code-block:: console

        $ git clone https://github.com/pole-surfaces-planetaires/pystac
        $ cd pystac
        $ make prepare-dev
        $ source .pystac
        $ make install-dev


To get more information about the preconfigured tasks:

.. code-block:: console

        $ make help

Usage
-----

To use pySTAC in a project::

    import pystac



Run tests
---------

.. code-block:: console

        $make tests



Author
------
👤 **Jean-Christophe Malapert**



🤝 Contributing
---------------
Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/pole-surfaces-planetaires/pystac/issues). You can also take a look at the [contributing guide](https://github.com/pole-surfaces-planetaires/pystac/blob/master/CONTRIBUTING.rst)


📝 License
----------
This project is [GNU General Public License v3](https://github.com/pole-surfaces-planetaires/pystac/blob/master/LICENSE) licensed.
