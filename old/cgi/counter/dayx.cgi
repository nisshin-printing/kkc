#!/usr/local/bin/perl

#┌─────────────────────────────────
#│  DAY COUNTER-EX v3.2 (2001/05/13)
#│  Copyright(C) KENT WEB 2001
#│  webmaster@kent-web.com
#│  http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'DayX v3.2';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────
#
# [タグの書き方の例]
#   総カウント数     <img src="count/dayx.cgi?gif">
#   本日のカウント数 <img src="count/dayx.cgi?today">
#   昨日　　〃	     <img src="count/dayx.cgi?yes">
#
# [日計／月次一覧を見る]
#    http://www.host.xxx/~user/count/dayxmgr.cgi
#
# [チェックのしかた (ブラウザから最後に ?check をつけて呼出す）]
#    http://www.host.xxx/~user/count/dayx.cgi?check
# -------------------------------------------------------------------
# [ディレクトリ構成例 (括弧内はパーミッション) ]
#
#    public_html / index.html ... ここにカウンタを設置
#        |
#        +-- count / dayx.cgi    [755]
#               |    dayxmgr.cgi [755]
#               |    gifcat.pl   [755]
#               |    dayx.dat    [666]
#               |    day.dat     [666]
#               |    mon.dat     [666]
#               |    blue.gif
#               |    red.gif
#               |
#               +-- gif1 / 1.gif 2.gif ... 0.gif
#               |
#               +-- gif2 / 1.gif 2.gif ... 0.gif
#               |
#               +-- lock [777] /

#============#
#  設定項目  #
#============#

# 画像連結ライブラリ取込み
require './gifcat.pl';

# 総カウント数の桁数
$digit1 = 6;

# 本/昨日カウント数の桁数
$digit2 = 3;

# ログファイル
$logfile = "./dayx.dat";

# 日次記録ファイル
$dayfile = "./day.dat";

# 月次記録ファイル
$monfile = "./mon.dat";

# 総カウント数用GIF画像のディレクトリ
$gifdir1 = "./gif1";

# 本/昨日カウント数用GIF画像のディレクトリ
$gifdir2 = "./gif2";

# ファイルロック機構
#   0 : しない
#   1 : する (symlink関数式)
#   2 : する (mkdir関数式)
$lockkey = 0;

# ロックファイル名
$lockfile = "./lock/dayx.lock";

# カウンタの機能タイプ
#   0 : 総カウント数不要（昨日／本日のみ）
#   1 : 標準タイプ
$type = 1;

# IPアドレスの二重カウントチェック
#   0 : チェックしない
#   1 : チェックする
$ip_check = 0;

#============#
#  設定完了  #
#============#

# 引数を解釈
$mode = $ENV{'QUERY_STRING'};

# 更新系処理でないならば 1-2 秒待たせる
if ($type == 1 && $mode eq "yes") { sleep(2); }
elsif ($type == 1 && $mode eq "today") { sleep(1); }
elsif ($type == 0 && $mode eq "yes") { sleep(1); }

# チェックモード
if (!$mode || $mode eq 'check') { &check; }

# ロック開始
$lockflag=0;
if (($type && $mode eq "gif" && $lockkey) || (!$type && $mode eq "today" && $lockkey)) { $lockflag=1; &lock; }

# 記録ファイルから読み込み
open(IN,"$logfile") || &error("LK");
$data = <IN>;
close(IN);

# 記録ファイルを分解
($key,$yes,$today,$count,$youbi,$ip) = split(/<>/, $data);

# 日時を取得
$ENV{'TZ'} = "JST-9";
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
$year += 1900;
$mon++;
$thisday = (Sun,Mon,Tue,Wed,Thu,Fri,Sat) [$wday];
if ($mon < 10) { $mon = "0$mon"; }
$date = "$year\/$mon";

# IPチェック
$flag=0;
if ($ip_check) {
	$addr = $ENV{'REMOTE_ADDR'};
	if ($addr eq "$ip") { $flag=1; }
}

# 本日のカウント数をキーにカウントアップ
if ((!$flag && $type && $mode eq 'gif') || (!$flag && !$type && $mode eq 'today')) {

	$count++;

	## 当日処理
	if ($key eq "$mday") {
		$today++;

		# ログをフォーマット
		$data = "$key<>$yes<>$today<>$count<>$thisday<>$addr<>\n";
	}
	## 翌日処理
	else {
		# ログをフォーマット
		$data = "$mday<>$today<>1<>$count<>$thisday<>$addr<>\n";

		&day_count;
		&mon_count;
	}

	# ログを更新
	open(OUT,">$logfile") || &error("LK");
	print OUT $data;
	close(OUT);
}

# ロック解除
if ($lockflag) { &unlock; }

# カウンタ画像出力
&count_view;
exit;

#-------------------#
# カウンタ出力処理  #
#-------------------#
sub count_view {
	while (length($count) < $digit1) { $count = '0' . $count; }
	while (length($today) < $digit2) { $today = '0' . $today; }
	while (length($yes) < $digit2) { $yes = '0' . $yes; }

	@outfile=();

	if ($mode eq "gif") {
		@array = split(//, $count);
		foreach (@array) {
			push(@outfile,"$gifdir1\/$_\.gif");
		}
	}
	elsif ($mode eq "today") {
		@array = split(//, $today);
		foreach (@array) {
			push(@outfile,"$gifdir2\/$_\.gif");
		}
	}
	elsif ($mode eq "yes") {
		@array = split(//, $yes);
		foreach (@array) {
			push(@outfile,"$gifdir2\/$_\.gif");
		}
	}

	# 画像出力
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat'gifcat(@outfile);
}

#--------------#
#  ロック処理  #
#--------------#
sub lock {
	local($retry) = 5;
	# 3分以上古いロックは削除する
	if (-e $lockfile) {
		($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 180) { &unlock; }
	}
	# symlink関数式ロック
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('Lock is busy'); }
			sleep(1);
		}
	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('Lock is busy'); }
			sleep(1);
		}
	}
}

#--------------#
#  ロック解除  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
}

#------------------------#
#  日次カウント数の処理  #
#------------------------#
sub day_count {
	# ログの日次キーより本日の日が小さければ月が変わったと判断する
	if ($mday < $key) {
		open(DB,">$dayfile") || &error("LK");
		close(DB);
	}
	# 月内での処理
	else {
		if ($key < 10) { $key = "0$key"; }
		open(DB,">>$dayfile") || &error("LK");
		print DB "$mon\/$key \($youbi\)<>$today<>\n";
		close(DB);
	}
}

#------------------------#
#  月間カウント数の処理  #
#------------------------#
sub mon_count {
	# 初めてのアクセスの場合
	if (-z $monfile) { $mons[0] = "$date<>$today<>\n"; }
	else {
		open(IN,"$monfile") || &error("LK");
		@mons = <IN>;
		close(IN);

		# ログ配列の最終行を分解
		$mons[$#mons] =~ s/\n//;
		($y_m,$cnt) = split(/<>/,$mons[$#mons]);

		# 当月処理
		if ($y_m eq "$date") {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
		}
		# 翌月処理
		#（ログ配列の最終行が $dateと異なれば、月が変ったと判断する）
		else {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
			push(@mons,"$date<>0<>\n");
		}
	}

	# ログファイルを更新
	open(OUT,">$monfile") || &error("LK");
	print OUT @mons;
	close(OUT);
}

#--------------#
#  エラー処理  #
#--------------#
sub error {
	if ($lockflag && $_[0] eq "LK") { &unlock; }

	@err_gif = ('47','49','46','38','39','61','2d','00','0f','00','80','00','00','00','00','00','ff','ff','ff','2c', '00','00','00','00','2d','00','0f','00','00','02','49','8c','8f','a9','cb','ed','0f','a3','9c','34', '81','7b','03','ce','7a','23','7c','6c','00','c4','19','5c','76','8e','dd','ca','96','8c','9b','b6', '63','89','aa','ee','22','ca','3a','3d','db','6a','03','f3','74','40','ac','55','ee','11','dc','f9', '42','bd','22','f0','a7','34','2d','63','4e','9c','87','c7','93','fe','b2','95','ae','f7','0b','0e', '8b','c7','de','02','00','3b');

	print "Content-type: image/gif\n\n";
	foreach (@err_gif) {
		$data = pack('C*',hex($_));
		print $data;
	}
	exit;
}

#------------------#
#  チェックモード  #
#------------------#
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>DAY COUNTER-EX</title></head>\n";
	print "<body>\n<h2>Check Mode</h2>\n<UL>\n";

	# ログファイルのパス確認
	if (-e $logfile && -e $dayfile && -e $monfile) {
		print "<LI>ログファイルのパス : OK!\n";
	}
	unless (-e $logfile) { print "<LI>ログファイル $logfile がありません。\n"; }
	unless (-e $dayfile) { print "<LI>ログファイル $dayfile がありません。\n"; }
	unless (-e $monfile) { print "<LI>ログファイル $monfile がありません。\n"; }

	# ログファイルのパーミッション（読みこみ）
	if (-r $logfile && -r $dayfile && -r $monfile) {
		print "<LI>ログファイルの読みこみパーミッション : OK!\n";
	}
	unless (-r $logfile){ print "<LI>ログファイル $logfile
					 の読みこみパーミッションが不正です。\n"; }
	unless (-r $dayfile) { print "<LI>ログファイル $dayfile
					 の読みこみパーミッションが不正です。\n"; }
	unless (-r $monfile) { print "<LI>ログファイル $monfile
					 の読みこみパーミッションが不正です。\n"; }

	# ログファイルのパーミッション（書きこみ）
	if (-w $logfile && -w $dayfile && -w $monfile) {
		print "<LI>ログファイルの書きこみパーミッション : OK!\n";
	}
	unless (-w $logfile) { print "<LI>ログファイル $logfile
					の書きこみパーミッションが不正です。\n"; }
	unless (-w $dayfile) { print "<LI>ログファイル $dayfile
					の書きこみパーミッションが不正です。\n"; }
	unless (-w $monfile) { print "<LI>ログファイル $monfile
					の書きこみパーミッションが不正です。\n"; }

	# 画像ディレクトリ１のパス確認
	if (-d $gifdir1) { print "<LI>gif1ディレクトリのパス : OK!\n"; }
	else { print "<LI>gif1ディレクトリがありません。: $gifdir1\n"; }

	# 画像ディレクトリ２のパス確認
	if (-d $gifdir2) { print "<LI>gif2ディレクトリのパス : OK!\n"; }
	else { print "<LI>gif2ディレクトリがありません。: $gifdir2\n"; }

	# ロックディレクトリ
	print "<LI>ロック形式：";
	if ($lockkey == 0) { print "ロック設定なし\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }

		$lockfile =~ s/(.*)[\\\/].*$/$lockdir = $1/e;
		print "<LI>ロックディレクトリ：$lockdir\n";

		if (-d $lockdir) { print "<LI>ロックディレクトリのパス：OK\n"; }
		else { print "<LI>ロックディレクトリのパス：NG → $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>ロックディレクトリのパーミッション：OK\n";
		} else {
			print "<LI>ロックディレクトリのパーミッション：NG → $lockdir\n";
		}
	}

	# 画像チェック(1)
	foreach (0 .. 9) {
		$flag=0;
		$giffile = $_ . '.gif';
		unless (-e "$gifdir1\/$giffile") {
			$flag=1;
			print "<LI>$gifdir1\/$giffile がありません。\n";
		}
	}
	if (!$flag) { print "<LI>gif1ディレクトリのGIF画像 : OK!\n"; }

	# 画像チェック(2)
	foreach (0 .. 9) {
		$flag=0;
		$giffile = $_ . '.gif';
		unless (-e "$gifdir2\/$giffile") {
			$flag=1;
			print "<LI>$gifdir2\/$giffile がありません。\n";
		}
	}
	if (!$flag) { print "<LI>gif2ディレクトリのGIF画像 : OK!\n"; }

	# 著作権表示：削除禁止
	print "<P><small><!-- $ver -->\n";
	print "- <a href=\"http://www.kent-web.com/\">Day Counter-EX</a> -\n";
	print "</small>\n</UL>\n</body></html>\n";
	exit;
}
