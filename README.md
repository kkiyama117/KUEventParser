# event-parser
イベント情報が載っているウェブページから情報を抽出し、京大マップへ投稿しやすいデータ形式に変換するパッケージ。

## 使い方
### インストール
```bash
virtualenv venv
source venv/bin/activate
pip install -e .
```

### アップデート
```bash
pip install -U -e .
```

### 京大公式 `eventparser.kyoto_u`
#### 指定年月のイベントURLリストを取得 `get_event_list`
```python
from datetime import date
from eventparser.kyoto_u import get_event_list

august = date(2014, 8, 1)
urls = get_event_list(august)
```
`urls`は2014年8月の行事カレンダーに載っているイベントのURL(`str`)のリスト。

#### イベントURLからイベント情報抽出 `get_event`
```python
from eventparser.kyoto_u import get_event

event = get_event("http://www.kyoto-u.ac.jp/ja/news_data/h/h1/news4/2013_1/140801_1.htm")
```
`event`は指定URLのイベントページから抽出したイベント情報(`dict`)で、以下の構造になっている。
```json
{
    "event": {
        "name": "第51回品川セミナー",
        "location": "東京オフィス",
        "start": 2014-08-01 17:30:00+09:00,
        "end": 2014-08-01 19:00:00+09:00,
        "description": <省略>,
        "url": "http://www.kyoto-u.ac.jp/ja/news_data/h/h1/news4/2013_1/140801_1.htm"
    },
    "source": {
        "url": "http://www.kyoto-u.ac.jp/ja/news_data/h/h1/news4/2013_1/140801_1.htm",
        "body": <省略>
    }
}
```
`start`, `end`は`datetime.date`オブジェクトが入る。
`description`にはイベント詳細文、`body`には抽出元のイベントページの内容が文字列として入っている。

`get_event`は
```bash
kyoto_u http://www.kyoto-u.ac.jp/ja/news_data/h/h1/news4/2013_1/140801_1.htm
```
で動作確認することもできる。

### テスト
```bash
python setup.py test
```
