# event-parser
イベント情報が載っているウェブページから情報を抽出し、特定のデータ形式に変換するパッケージ。

## Usage
### install
`pip` を利用する場合(主にインストールした後バージョン管理をpipでしたい人向け)
```bash
$ pip install kueventparser
```

### run script
```bash
parse_event [-h] [--help]
```

## Develop
```bash
git clone https://github.com/kkiyama117/KUEventParser.git
# recommend using pipenv
pipenv install --dev
```
you can also use venv with requirements.txt

## Docs
### `get`
```python
from kueventparser import get
get(url="url of event")
```

### `get_all`
```python
from kueventparser import get_all
get_all()
```

### kueventparser
```python
import kueventparser
kueventparser.kueventparser('get_all', year=2019, month=2)
```

`event`は指定URLのイベントページから抽出したイベント情報(`Event`)で、以下の構造になっている。
```python
class Event:
    """イベント情報を含んだclass
    """

    def __init__(self, name:str, url: str, location: str, description: str, date: datetime.date,
                 start: datetime.time,
                 end: datetime.time):
        """イニシャライザー
        
        Args:
            name: イベント名
            url: イベント情報のURL
            location: 開催地
            description: 詳細説明文
            date: 開催日
            start: 開始時間
            end: 終了時間
        """
```

### detail
より正確なドキュメント群は[sphinx](http://www.sphinx-doc.org/ja/stable/index.html)で書かれている.

```bash
# /docs/build/html/ にドキュメントが作成される.
cd docs
python make_docs.py
```
