# SeiEMG Pro

筋電位信号計測プログラムです。
計測だけではなく、計測時に必要な機能を搭載しています。

## ディレクトリ構造

```
├── README.md         # プロジェクトに関する様々な情報を書いておく
|
├── setting.ini       # 各種設定ファイルを保存する場所
|
├── data              # 計測データ格納用
|   └── raw           # 不変の生データ
|
├── classification       # 実験用のスクリプト
|   └── images
|   └── parameter
|   └── classification_menu.py
|   └── learning_window.py
|   └── prediction_window.py
|   └── probability_window.py
|
├── images
|
├── max_emg_data
|
├── src
|   └── delsys.py
|   └── delsys2.py
|   └── pytrigno.py
|
├── EMGsignal.py         # ノートブック
|
├── get
|
├── reports           # 報告用の綺麗な図などを保存
|
├── src               # プロジェクトで利用するソースコード
|   ├── __init__.py   # Pythonモジュールのsrcを設定
|   ├── data          # データのダウンロード・処理・整形・生成用のスクリプト
|   ├── models        # モデルの実装を置いておく場所
|   └── utils         # その他さまざまなスクリプトを置いておく場所
|
└── results           # ログや結果を保存する場所
```

## 注意点など

- 基本的に `data` と `results` はGitの管理対象から外した方が良い（ファイルサイズが大きい／頻繁に書き変わるため）
  - `.gitignore` を編集する
- ハイパーパラメータやイテレーション回数、データのパスなどは頻繁に変わる（切り替える）ため，ハードコードせずに `config` 中の設定ファイルから読み込むべき
  - 設定ファイルの形式としては， `yaml` や `ini` など．オススメは `yaml` 形式．
- `results` の中は，どのようなデータ／設定によってその結果が得られたのかがわかるように階層やフォルダ／ファイル名を工夫する．
  - 実験条件（ハイパーパラメータなど）を変えるとそれに対応した保存フォルダ／ファイル名となるようにしておくと，誤って結果を上書きするリスクが少なくなる
    - [TensorBoard](https://www.tensorflow.org/tensorboard?hl=ja) 等を適宜活用する