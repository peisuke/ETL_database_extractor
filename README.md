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

#### 文字の抽出

```
$ ./01_download.sh
$ python 02_jis_mapper.py
$ python 03_extract_ETL.py --data ETL1
$ python 03_extract_ETL.py --data ETL6
$ python 03_extract_ETL.py --data ETL7
$ python 03_extract_ETL.py --data ETL8B
$ python 03_extract_ETL.py --data ETL8G
$ python 03_extract_ETL.py --data ETL9B
$ python 03_extract_ETL.py --data ETL9G
```

#### 文字の抽出

```
$ python 04_denoise.py --data ETL1 --input output --output denoised
$ python 04_denoise.py --data ETL6 --input output --output denoised
$ python 04_denoise.py --data ETL7 --input output --output denoised
$ python 04_denoise.py --data ETL8B --input output --output denoised
$ python 04_denoise.py --data ETL8G --input output --output denoised
$ python 04_denoise.py --data ETL9B --input output --output denoised
$ python 04_denoise.py --data ETL9G --input output --output denoised
$ ./05_archive.sh
```

### 実行結果

- データの可視化サンプル
  - https://github.com/peisuke/ETL_database_extractor/blob/master/06_show_data.ipynb
  - https://github.com/peisuke/ETL_database_extractor/blob/master/07_show_data.ipynb
