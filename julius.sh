# Julius 起動スクリプト
julius -C julius.jconf -module > /dev/null &
echo $!
sleep 4
# -moduleオプション= Juliusをモジュールモードで起動
# /dev/nullはlinuxの特殊ファイルで、何も出力したくない時に指定する。
# $! = シェルが最後に実行したバックグラウンドプロセスのID
# サーバーが立ち上がる前にアクセスしようとするとエラーになるので数秒待つ
