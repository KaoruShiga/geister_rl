# geister_rl
 geister ai大会に強化学習を使おうというプロジェクトです．
 不完全情報ゲームというマルコフ性を満たさない環境において学習することを目指します．
 => (追記)2021年のGATにて優勝しました．
 
プログラムの実行方法
 1. ダウンロードして解凍する
 2. numpyをインストールしたpythonを用意する
 3. 解凍したフォルダに移動してpythonを実行する

    例: ファイル名vsself500_theta.npyをθとしてjavaserver(https://github.com/miyo/geister_server.java)に接続したい場合
    
    tcpで対戦する場合 > python tcp_player.py --port 10000 --games 5000 --path weights\vsself2\vsself500
    
    例:学習を継続したい場合
    
    学習をする場合 > python self_play.py -i 500
    
    (学習を新しく始める場合はソースコードの改変が必要です)

2021年大会で用いたプログラムの概要
1. 一手先の盤面の行動優先度が最も高い手を選択する．
2. 盤面から行動優先度を計算する方法は二駒関係を使う．
3. encoderとして二駒関係を用いる．
4. 探索はしていない．
