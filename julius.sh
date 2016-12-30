julius -C julius.jconf -module > /dev/null &
echo $!
sleep 3
# -moduleオプション= Juliusをモジュールモードで起動
# $!=シェルが最後に実行したバックグラウンドプロセスのPID
# サーバーが立ち上がる前にアクセスしようとするとエラーになるので３秒待つ
