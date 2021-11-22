# geister_rl
 geister ai大会に強化学習を使おうというプロジェクトです．
 => (追記)2021年のGATにて優勝しました．

インストール手順
 1. pythonをインストールする．
 2. pythonにnumpyをインストールする．

         pip install numpy

 4. geister_rlをダウンロード&解凍する．
 5. 解凍したフォルダに移動して任意のpythonコードを実行する．


プログラムの実行方法
 1. ガイスターjavaserver
https://github.com/miyo/geister_server.java
に接続し，weights\vsself2\vsself900_theta.npy(=500万回時点でのθ)をθとするプレイヤーと対戦させる場合

        python tcp_player.py --port 10000 --games 5000 --path weights/vsself2/vsself900

 2. 900万回時点でのθを使い，学習回数をさらに増やしたい場合
    
          python self_play.py -i 900
          
 3. 学習を新しく始める場合などはソースコードを改変が必要です．

2021年大会で用いたプログラムの概要
1. 一手先の盤面の行動優先度が最も高い手を選択する．
2. 盤面から行動優先度を計算する方法は二駒関係を使う．
3. 探索はしていない．


θの要素数に関する補足 : 論文などではθの要素数を7503だと書きましたが，この実装では無駄な0があるためにθの要素数は8128になっています．
