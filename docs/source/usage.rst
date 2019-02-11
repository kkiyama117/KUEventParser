Usage
#####

.. contents::
    :local:
    :backlinks: top
    :depth: 3


preparation
===========

download
--------
gitからcodeをdownloadします.

.. code-block:: bash

    git clone git@github.com:kkiyama117/scripts.git
    cd event-parser

もし,開発版( `develop` ブランチ)を使うなら

.. code-block:: bash

    git checkout develop

を続けてください.

次に進みます.

install
-------
もし可能なら,virtualenv等で仮想環境を作るとよいでしょう.
気にしない方は飛ばしていただいて構いません.

.. code-block:: bash

    python -m venv
    source venv/bin/activate

`pip` でインストールします.

.. code-block:: bash

    # by pip
    pip install -e .

`pip` の代わりに, `setup.py` を使うなら,下記のコマンドを使いましょう.

.. code-block:: bash

    # by script
    python setup.py install

update
------

.. todo:: documentの実装

uninstall
---------

`pip`

.. code-block:: bash

    # by pip
    pip uninstall eventparser

`setup.py` →アンインストールコマンドは無いので、manualで消します.

.. code-block:: bash

    python setup.py install --record files.txt
    cat files.txt | xargs rm -rvf
    rm -r ./dist ./build ./eventparser.egg-info
    # cd ..
    # rm -rf ./event-parser

windowsなら `PowerShell` で,

.. code-block:: PowerShell

    python setup.py install --record files.txt
    cat files.txt | ForEach-Object {$rpath = $_ ; rm $rpath}
    ("./dist", "./build", "./eventparser.egg-info") | ForEach-Object {$rpath = $_ ; rm $rpath --Force}

execution
=========

script
------

.. code-block:: bash

    parse-event [-h] [--help]

documents
=========

build
-----

基本的に前者を使うことを薦めます.

use setuptools
^^^^^^^^^^^^^^

.. code-block:: bash

    python setup.py build_sphinx
    # /docs/build/html/ にドキュメントが作成される.

use scripts
^^^^^^^^^^^

.. code-block:: bash

    # pip install sphinx
    # pip install -U sphinx
    cd ./docs
    python make_docs.py
    # docs/build にドキュメントが作成される.

API
===

packageの中の, apiモジュールがAPIの役割をする.

.. code-block:: python

    import src.api
    api.get_all(manager: str = 'official', *, date, year: int, month: int)

.. note::

    詳細は :doc:`src` を参照.

.. todo:: APIの改善