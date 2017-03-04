# Julius起動スクリプト　自然言語版
julius -C juliusNL.jconf -module > /dev/null &
echo $!
sleep 3
# -moduleオプション= Juliusをモジュールモードで起動
# /dev/nullはlinuxの特殊ファイルで、何も出力したくない時に指定する。
# $! = シェルが最後に実行したバックグラウンドプロセスのID
# サーバーが立ち上がる前にアクセスしようとするとエラーになるので数秒待つ
