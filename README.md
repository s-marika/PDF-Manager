# PDF-Manager

PDFファイルを結合・分割．抽出するGUIアプリケーションです．
python3で実行できます．

## install

* リポジトリをクローン

```bash
git clone git@github.com:s-marika/PDF-Manager.git
```

* python3.7以上([参考](https://www.python.jp/install/windows/install.html))，pipのインストール

* pipenvのインストール

```bash
pip install pipenv
```

* 依存ライブラリをインストール

```bash
pipenv install  # 仮想環境の作成
pipenv shell    # 仮想環境へログイン
```

## usage

### 起動

```bash
python app.py   # Windows
python3 app.py  # mac or Linux
```

### 各種機能

起動後，画面上にあるラジオボタンを切り替えることで，各種機能が使えます．

#### 結合機能

**選んだPDFファイルをすべて結合する．**

1. 「ファイル読み込み」ボタンから結合したいファイルを選択する．複数選択可能．  
2. 選択したファイルは下のボックスにパスが表示される．  
3. ファイルを追加したい場合は，再度「ファイル読み込み」ボタンを押し，追加したいファイルを選択する．
4. 要らないファイルはクリックで選択し，「削除」ボタンを押すことで削除できる．  
5. 結合される順番は，ボックスの上にあるものが前のページに表示される．ファイルの並びは，ドラッグアンドドロップで入れ替えることができる．
6. 「処理開始」ボタンを押すと結合処理が開始され，ファイルが保存される．

#### 分割機能

**読み込んだファイルを指定のページで2つに分割する．**

1. 「ファイル読み込み」ボタンから分割したいファイルを選択する．  
1. 読み込んだファイルのパスが，ボタンの下のボックスに表示される．  
1. 対象のファイルを変えたい場合は，再度「ファイル読み込み」ボタンから読み込む．  
1. 分割開始ページを整数値で入力する．入力した数のページから2つ目のファイルが始まるように分割される．  
1. 「処理開始」ボタンを押すと結合処理が開始され，ファイルが保存される．この時，ファイルは2つ出力される．

#### 抽出機能

**読み込んだファイルから指定のページを抽出する．**

1. 「ファイル読み込み」ボタンからページを抽出したいファイルを選択する．  
1. 読み込んだファイルのパスが，ボタンの下のボックスに表示される．  
1. 対象のファイルを変えたい場合は，再度「ファイル読み込み」ボタンから読み込む．  
1. 抽出開始ページと終了ページを入力する．終了ページは，抽出されたPDFファイルに含まれる．  
1. 「処理開始」ボタンを押すと結合処理が開始され，ファイルが保存される．

#### ファイルの保存パスについて

本アプリでは，ファイルの保存先ディレクトリは「ダウンロードフォルダ」がデフォルトになっている．  
また，出力ファイル名は8文字のランダム文字列になっている．  
**分割機能の出力**のみ，「8文字のランダム文字列_(1 or 2).pdf」として出力される．

## environment

* Windows10
* Python3.7
