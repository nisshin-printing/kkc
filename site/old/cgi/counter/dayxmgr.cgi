#!/usr/local/bin/perl

#┌─────────────────────────────────
#│  DAY COUNTER-EX MANAGER v3.2 (2001/05/13)
#│  Copyright(C) KENT WEB 2001
#│  webmaster@kent-web.com
#│  http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'DayX v3.2'; # バージョン情報
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────

#============#
#  設定項目  #
#============#

# ログファイル
$logfile = "./dayx.dat";

# 日次記録ファイル
$dayfile = "./day.dat";

# 月次記録ファイル
$monfile = "./mon.dat";

# 集計一覧からの戻り先
$home = "../index.html";

# 集計一覧のタイトル名
$title = "アクセス集計一覧";

# タイトル文字色
$t_color = "#008080";

# グラフ画像
$graph1 = "./blue.gif";
$graph2 = "./red.gif";

# 月間グラフ幅の調整
# 1か月平均 4桁で50～100  5桁で200～500程度
$mKEY = 50;

# 日計グラフ幅の調整
# 1日平均 2桁で1～2  3桁で5～10  4桁で30～60程度
$dKEY = 2;

# bodyタグ
$body = '<body bgcolor="#F1F1F1" text="#000000" link="#0000FF" vlink="#0000FF">';

#============#
#  設定完了  #
#============#

# ログファイル読み込み
open(IN,"$logfile") || &error("Open Error : $logfile");
$data = <IN>;
close(IN);
($day,$yes,$to,$all,$week,$ip) = split(/<>/, $data);

# 時間取得
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
$date = sprintf("%02d/%02d (%s) ",$mon+1,$mday,$week[$wday]);
$D_Y  = sprintf("%04d/%02d",$year+1900,$mon+1);

# 日次アクセスファイルを読み込み
open(IN,"$dayfile") || &error("Open Error : $dayfile");
@DayFile = <IN>;
close(IN);
push(@DayFile,"$date<>$to<>\n");

# 月間アクセスファイルを読み込み
open(IN,"$monfile") || &error("Open Error : $monfile");
@MonFile = <IN>;
close(IN);

$under = pop(@MonFile);
$under =~ s/\n//g;
($Y,$C) = split(/<>/, $under);
if ($Y eq "$D_Y") {
	$C2 = $C + $to;
	push(@MonFile,"$Y<>$C2<>\n");
} else {
	push(@MonFile,"$D_Y<>$to<>\n");
}

# HTMLを表示
&header;
print <<"EOM";
<TABLE cellspacing="0" cellpadding="0" border="0">
<TR>
<TD bgcolor="#B4B4B4" width="50" height="20" align="center" nowrap>
<A href="$home" style="font-size:10pt; color:#000000; text-decoration: none">戻る</A></TD></TR>
</TABLE>
<div align="center">
<hr width="70%" size=2 noshade>
<h2>$title</h2>
<hr width="70%" size=2 noshade>
<br><br>
<table><tr><td>
<OL>
  <LI><a href="#day">日次アクセス一覧</a>
  <LI><a href="#mon">月次アクセス一覧</a>
</OL>
</td></tr></table>
</div>
<br>
<table width="100%">
<tr><td bgcolor="#6D6D6D">　<font color="#F9B606">■</font>
  <font color="#FFFFFF"><b><a name="day">日次アクセス一覧</a></b></font>
</td></tr></table>
<br>
<blockquote>
<table border=0 cellpadding=1 cellspacing=0>
<!--
<tr>
  <th bgcolor=#D5FFD5>月日</th><th bgcolor=#D5FFD5>アクセス数</th>
  <th bgcolor=#D5FFD5>グラフ</th>
</tr>
-->
EOM

$flag = 0;
foreach (@DayFile) {
	chop;
	($m_d,$dcnt) = split(/<>/);

	# グラフ幅を指定
	$width = $dcnt / $dKEY;
	$width = int($width);

	# 桁処理
	$dcnt = &filler($dcnt);

	# 色変更
	$m_d =~ s/Sat/<font color=blue>Sat<\/font>/;
	$m_d =~ s/Sun/<font color=red>Sun<\/font>/;

	print "<tr><td nowrap>$m_d</td><td align=right> &nbsp; $dcnt &nbsp; </td>\n";
	print "<td><img src=\"$graph2\" width=$width height=5></td></tr>\n";
}

print <<"EOM";
</table></blockquote>
<br><br>
<table width="100%">
<tr><td bgcolor="#6D6D6D">　<font color="#F9B606">■</font>
<font color="#FFFFFF"><b><a name="mon">月次アクセス一覧</a></b></font>
</td></tr></table>
<br>
<blockquote>
<table border=0 cellpadding=2 cellspacing=0>
<tr>
  <th bgcolor=#D5FFD5 nowrap>年月</th><th bgcolor=#D5FFD5 nowrap>月間<br>アクセス</th>
  <th bgcolor=#D5FFD5 nowrap>1日平均<br>アクセス</th><th bgcolor=#D5FFD5>グラフ</th>
</tr>
EOM

$flag = 0;
foreach (@MonFile) {
	($y_m,$mcnt) = split(/<>/);
	($year,$mon) = split(/\//, $y_m);

	if ($_ eq "$MonFile[$#MonFile]") {
		if ($day == 1) { $avr = ' - '; }
		else {
			$waru = $day - 1;
			$avr = int (($C / $waru) +0.5);
			$avr = &filler($avr);
		}
	} else {
		$lastday = &LastDay("$year","$mon");
		$avr = int (($mcnt / $lastday) +0.5);
		$avr = &filler($avr);
	}

	# グラフ幅を指定
	$width = $mcnt / $mKEY;
	$width = int($width);

	# 桁処理
	$mcnt = &filler($mcnt);

	if ($year ne "$year2") { print "<tr><td colspan=4><hr size=1></td></tr>\n"; }

	print "<tr><th nowrap>$y_m</th><td align=right> &nbsp; $mcnt &nbsp; </td>";
	print "<td align=right>$avr &nbsp; </td>";
	print "<td><img src=\"$graph1\" width=$width height=10></td></tr>\n";

	$year2 = $year;
}

## 著作権表示（削除改変禁止）
print <<"EOM";
</table>
</blockquote>
<div align="center">
<hr>
<small><!-- $ver -->
- <a href="http://www.kent-web.com/" target="_top">Day Counter-EX</a> -
</small>
</div>
</body>
</html>
EOM
exit;

#----------------#
#  月の末日計算  #
#----------------#
sub LastDay {
	local($year, $mon) = @_;
	local($lastday);

	$lastday = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31) [$mon - 1]
	+ ($mon == 2 && (($year % 4 == 0 && $year % 100 != 0) ||
	$year % 400 == 0));

	return $lastday;
}

#--------------#
#  HTMLヘッダ  #
#--------------#
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>$title</title>
<STYLE TYPE="text/css">
<!--
body,tr,td,th { font-size: 10pt; }
small { font-size: 9pt; }
h2 { font-size:16pt; color:$t_color }
-->
</STYLE>
</head>
$body
EOM
}

#----------------#
#  桁区きり処理  #
#----------------#
sub filler {
	local($_) = $_[0];
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	return $_;
}

#--------------#
#  エラー処理  #
#--------------#
sub error {
	&header;
	print <<"EOM";
<div align="center">
<hr width="70%">
<h3>ERROR !</h3>
<h4>$_[0]</h4>
<hr width="70%">
</div>
</body>
</html>
EOM
	exit;
}
