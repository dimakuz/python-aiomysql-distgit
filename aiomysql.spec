%global with_python3 1

# we don't want to provide private python extension libs in either the python2 or python3 dirs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%define name aiomysql
%define version 0.0.20
%define unmangled_version 0.0.20
%define release 1

Summary: MySQL driver for asyncio.
Name: python3-%{name}
Version: %{version}
Release: %{release}
Source0: python3-aiomysql-%{unmangled_version}.tar.gz
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Nikolay Novik <nickolainovik@gmail.com>
Url: https://github.com/aio-libs/aiomysql

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pytest >= 2.8

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
%py3_build

%install
%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%description
aiomysql
========
.. image:: https://travis-ci.com/aio-libs/aiomysql.svg?branch=master
    :target: https://travis-ci.com/aio-libs/aiomysql
.. image:: https://codecov.io/gh/aio-libs/aiomysql/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/aio-libs/aiomysql
    :alt: Code coverage
.. image:: https://badge.fury.io/py/aiomysql.svg
    :target: https://badge.fury.io/py/aiomysql
    :alt: Latest Version
.. image:: https://readthedocs.org/projects/aiomysql/badge/?version=latest
    :target: https://aiomysql.readthedocs.io/
    :alt: Documentation Status
.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/aio-libs/Lobby
    :alt: Chat on Gitter

**aiomysql** is a "driver" for accessing a `MySQL` database
from the asyncio_ (PEP-3156/tulip) framework. It depends on and reuses most
parts of PyMySQL_ . *aiomysql* tries to be like awesome aiopg_ library and
preserve same api, look and feel.

Internally **aiomysql** is copy of PyMySQL, underlying io calls switched
to async, basically ``yield from`` and ``asyncio.coroutine`` added in
proper places)). `sqlalchemy` support ported from aiopg_.


Documentation
-------------
https://aiomysql.readthedocs.io/


Mailing List
------------
https://groups.google.com/forum/#!forum/aio-libs


Basic Example
-------------

**aiomysql** based on PyMySQL_ , and provides same api, you just need
to use  ``await conn.f()`` or ``yield from conn.f()`` instead of calling
``conn.f()`` for every method.

Properties are unchanged, so ``conn.prop`` is correct as well as
``conn.prop = val``.

.. code:: python

    import asyncio
    import aiomysql


    async def test_example(loop):
        pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                          user='root', password='',
                                          db='mysql', loop=loop)
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 42;")
                print(cur.description)
                (r,) = await cur.fetchone()
                assert r == 42
        pool.close()
        await pool.wait_closed()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_example(loop))


Example of SQLAlchemy optional integration
------------------------------------------
Sqlalchemy support has been ported from aiopg_ so api should be very familiar
for aiopg_ user.:

.. code:: python

    import asyncio
    import sqlalchemy as sa

    from aiomysql.sa import create_engine


    metadata = sa.MetaData()

    tbl = sa.Table('tbl', metadata,
                   sa.Column('id', sa.Integer, primary_key=True),
                   sa.Column('val', sa.String(255)))


    async def go(loop):
        engine = await create_engine(user='root', db='test_pymysql',
                                     host='127.0.0.1', password='', loop=loop)
        async with engine.acquire() as conn:
            await conn.execute(tbl.insert().values(val='abc'))
            await conn.execute(tbl.insert().values(val='xyz'))

            async for row in conn.execute(tbl.select()):
                print(row.id, row.val)

        engine.close()
        await engine.wait_closed()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(go(loop))


Requirements
------------

* Python_ 3.5.3+
* PyMySQL_


.. _Python: https://www.python.org
.. _asyncio: http://docs.python.org/3.4/library/asyncio.html
.. _aiopg: https://github.com/aio-libs/aiopg
.. _PyMySQL: https://github.com/PyMySQL/PyMySQL
.. _Tornado-MySQL: https://github.com/PyMySQL/Tornado-MySQL

Changes
-------

0.0.20 (2018-12-19)
^^^^^^^^^^^^^^^^^^^

* Fixed connect_timeout #360

* Fixed support for SQLA executemany #324

* Fix the python 3.7 compatibility #357

* Fixed reuse connections when StreamReader has an exception #339

* Fixes warning when inserting binary strings #326


0.0.19 (2018-07-12)
^^^^^^^^^^^^^^^^^^^

* See v0.0.18


0.0.18 (2018-07-09)
^^^^^^^^^^^^^^^^^^^

* Updated to support latest PyMySQL changes.

* aiomysql now sends client connection info.

* MySQL8+ Support including sha256_password and cached_sha2_password authentication plugins.

* Default max packet length sent to the server is no longer 1.

* Fixes issue where cursor.nextset can hang on query sets that raise errors.


0.0.17 (2018-07-06)
^^^^^^^^^^^^^^^^^^^

* Pinned version of PyMySQL


0.0.16 (2018-06-03)
^^^^^^^^^^^^^^^^^^^

* Added ability to execute precompiled sqlalchemy queries #294 (Thanks @vlanse)


0.0.15 (2018-05-20)
^^^^^^^^^^^^^^^^^^^

* Fixed handling of user-defined types for sqlalchemy  #290

* Fix KeyError when server reports unknown collation #289


0.0.14 (2018-04-22)
^^^^^^^^^^^^^^^^^^^

* Fixed SSL connection finalization  #282


0.0.13 (2018-04-19)
^^^^^^^^^^^^^^^^^^^

* Added SSL support #280 (Thanks @terrycain)

* Fixed __all__ in aiomysql/__init__ #270 (Thanks @matianjun1)

* Added docker fixtures #275 (Thanks @terrycain)


0.0.12 (2018-01-18)
^^^^^^^^^^^^^^^^^^^

* Fixed support for SQLAlchemy 1.2.0

* Fixed argument for cursor.execute in sa engine #239 (Thanks @NotSoSuper)


0.0.11 (2017-12-06)
^^^^^^^^^^^^^^^^^^^

* Fixed README formatting on pypi


0.0.10 (2017-12-06)
^^^^^^^^^^^^^^^^^^^

* Updated regular expressions to be compatible with pymysql #167 (Thanks @AlexLisovoy)

* Added connection recycling in the pool #216


0.0.9 (2016-09-14)
^^^^^^^^^^^^^^^^^^

* Fixed AttributeError in  _request_authentication function #104 (Thanks @ttlttl)

* Fixed legacy auth #105

* uvloop added to test suite #106

* Fixed bug with unicode in json field #107 (Thanks @methane)


0.0.8 (2016-08-24)
^^^^^^^^^^^^^^^^^^

* Default min pool size reduced to 1 #80 (Thanks @Drizzt1991)

* Update to PyMySQL 0.7.5 #89

* Fixed connection cancellation in process of executing a query #79 (Thanks @Drizzt1991)


0.0.7 (2016-01-27)
^^^^^^^^^^^^^^^^^^

* Fix for multiple results issue, ported from pymysql #52

* Fixed useless warning with no_delay option #55

* Added async/await support for Engine, SAConnection, Transaction #57

* pool.release returns future so we can wait on it in __aexit__ #60

* Update to PyMySQL 0.6.7


0.0.6 (2015-12-11)
^^^^^^^^^^^^^^^^^^

* Fixed bug with SA rollback (Thanks @khlyestovillarion!)

* Fixed issue with default no_delay option (Thanks @khlyestovillarion!)


0.0.5 (2015-10-28)
^^^^^^^^^^^^^^^^^^

* no_delay option is deprecated and True by default

* Add Cursor.mogrify() method

* Support for "LOAD LOCAL INFILE" query.

* Check connection inside pool, in case of timeout drop it, fixes #25

* Add support of python 3.5 features to pool, connection and cursor


0.0.4 (2015-05-23)
^^^^^^^^^^^^^^^^^^

* Allow to call connection.wait_closed twice.

* Fixed sqlalchemy 1.0.0 support.

* Fix #11: Rename Connection.wait_closed() to .ensure_closed()

* Raise ResourceWarning on non-closed Connection

* Rename Connection.connect to _connect


0.0.3 (2015-03-10)
^^^^^^^^^^^^^^^^^^

* Added support for PyMySQL up to 0.6.6.

* Ported improvements from PyMySQL.

* Added basic documentation.

* Fixed and added more examples.


0.0.2 (2015-02-17)
^^^^^^^^^^^^^^^^^^

* Added MANIFEST.in.


0.0.1 (2015-02-17)
^^^^^^^^^^^^^^^^^^

* Initial release.

* Implemented plain connections: connect, Connection, Cursor.

* Implemented database pools.

* Ported sqlalchemy optional support.

