# ETL文字データベースからの手書き文字抽出

本リポジトリは、産業技術総合研究所より公開されている[ETL文字データベース](http://etlcdb.db.aist.go.jp/)の読み取りコードです。
当該データベースは手書きまたは印刷の英数字、記号、ひらがな、カタカナ、教育漢字、JIS第1水準漢字など、 約120万の文字画像データを収集しています。
データベース内に含まれる画像はバイナリでエンコードされており、またラベル情報もJIS X 0201、JIS X 0208、読み方などが混在しています。
本リポジトリは、これを直接機械学習等で扱えるようにするため、画像をpngに変換しつつ、ラベル情報をJIS X 0208に変換するためのスクリプトです。
上から順に実行すると、`output/*.json`にファイル名およびラベルデータが出力されます。

## 使い方

### ETL文字データベースリンクの設定

- 以下のURLから申請を行い、データのリンクを受領する
  - http://etlcdb.db.aist.go.jp/obtaining-etl-character-database?lang=ja
- `01_download.sh`スクリプトのリンクを修正する

### 実行

```
$ ./01_download.sh
$ python 02_jis_mapper.py
$ python 03_extract_ETL1.py
$ python 03_extract_ETL6.py
$ python 03_extract_ETL7.py
$ python 03_extract_ETL8B.py
$ python 03_extract_ETL8G.py
$ python 03_extract_ETL9B.py
$ python 03_extract_ETL9G.py
$ ./04_archive.sh
```

### 実行結果

- データの可視化サンプル
  - https://github.com/peisuke/ETL_database_extractor/blob/master/05_show_data.ipynb
