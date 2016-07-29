#!/usr/local/bin/perl
#       ↑あなたが加入しているプロバイダの｢perl｣言語が使用できる
#         パスを指定します。一般的に｢#!/usr/local/bin/perl｣で大丈夫

#=======================================================================================
#				logcounter Version 98.5
#=======================================================================================
#ログファイル
$datafile = './cnt.dat';
#----------------------------------------------------------
#タイトル画像
$title_gif = './z.gif';
#ラッキータイトル画像（ラッキーナンバーで表示する画像）
$lucky_gif = './lucky.gif';
#----------------------------------------------------------
#ラッキーナンバー（このカウントでラッキー画像が表示される）
@LUCKYNO = (5000,10000,12345,15000,2000);
#----------------------------------------------------------
#メインカウンタに使用するカウント画像
$MAINGIF[0] = './0.gif';
$MAINGIF[1] = './1.gif';
$MAINGIF[2] = './2.gif';
$MAINGIF[3] = './3.gif';
$MAINGIF[4] = './4.gif';
$MAINGIF[5] = './5.gif';
$MAINGIF[6] = './6.gif';
$MAINGIF[7] = './7.gif';
$MAINGIF[8] = './8.gif';
$MAINGIF[9] = './9.gif';
#----------------------------------------------------------
#サブ１カウンタに使用するカウント画像
$SUB_GIF1[0] = '../counter/img1/0.gif';
$SUB_GIF1[1] = '../counter/img1/1.gif';
$SUB_GIF1[2] = '../counter/img1/2.gif';
$SUB_GIF1[3] = '../counter/img1/3.gif';
$SUB_GIF1[4] = '../counter/img1/4.gif';
$SUB_GIF1[5] = '../counter/img1/5.gif';
$SUB_GIF1[6] = '../counter/img1/6.gif';
$SUB_GIF1[7] = '../counter/img1/7.gif';
$SUB_GIF1[8] = '../counter/img1/8.gif';
$SUB_GIF1[9] = '../counter/img1/9.gif';
#----------------------------------------------------------
#サブ２カウンタに使用するカウント画像
$SUB_GIF2[0] = '0.gif';
$SUB_GIF2[1] = '1.gif';
$SUB_GIF2[2] = '2.gif';
$SUB_GIF2[3] = '3.gif';
$SUB_GIF2[4] = '4.gif';
$SUB_GIF2[5] = '5.gif';
$SUB_GIF2[6] = '6.gif';
$SUB_GIF2[7] = '7.gif';
$SUB_GIF2[8] = '8.gif';
$SUB_GIF2[9] = '9.gif';
#----------------------------------------------------------
#ログを記録する日数　極端に大きくすると重くなる
$max = 31;
#=======================================================================================
#			初期設定が必要なのはここまでです。
#=======================================================================================
#日付を取得して、すべて２桁に統一する
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$date_now = sprintf("%02d/%02d/%02d",$year + 1900,$mon + 1,$mday);
$buffer = $ENV{'QUERY_STRING'};
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$QUERY{$name} = $value;
}
&data_read;
if ($QUERY{'cnt'} == 1) {
	($date,$count,$total) = split(/\,/,$DATA[1]);
	if ($count < 1) { $count = 0; }
} elsif ($QUERY{'cnt'} eq 'vew') {
	foreach $line (@DATA) {
		($date,$count,$to) = split(/\,/,$line);
		if ($count > $max) { $max = $count; }
	}
	print "Content-type: text/html\n\n";
	print "<html><head><title>access</title></head>\n";
	print "<body bgcolor=#000000 text=#FFFFFF link=#FF00FF vlink=#FF00FF>\n";
	print "<div align=center><center>\n";
	print "<p align=center><font size=7><b><em>Log Counter Access</em></b></font></p>\n";
	print "<table border=1 cellspacing=1>\n";
	foreach $line (@DATA) {
		($date,$count,$to) = split(/\,/,$line);
		print "<tr><td align=center width=10%>$date</td>\n";
		print "<td align=right width=10%>$count</td>\n";
		print "<td>\n";
		if ($max == 0) { $chrlen = 0; }
		else { $chrlen = int($count / $max * 200); }
		print "<img src=bar.gif width=$chrlen height=10>\n";
		$total = $total + $count;
		print "<td width=10% align=right>$to\n";
		print "</td></tr>\n";
	}
	print "<tr><td align=center width=10%>合計</td><td align=right width=10%>$total</td><td>　</td><td width=10%>　</td></tr>\n";
	print "</table><p>\n";
	print "<p align=right><font size=2><a href=http://www2.inforyoma.or.jp/~terra/>LuckyCounter by Terra</a></font></p>\n";
	print "</center></div>\n";
	print "</body></html>\n";
	exit;
} else {
	$newcount = 1;
	$match = 0;
	($date,$count,$total) = split(/\,/,$DATA[0]);
	if ($date eq $date_now) {
		$match = 1;
		$newcount = $count + 1;
	}
	$total++;
	if ($QUERY{'cnt'} == 2) {
		$count = $newcount;
		if ($QUERY{'c'} == 1) {
			$value = "$date_now\,$newcount\,$total\n";
			if ($match == 0) { unshift(@DATA,$value); }
			else { $DATA[0] = $value; }
			$da = @DATA;
			if ($da > $max) { pop(@DATA); }
			&data_save;
		}
	} else { $count = $total; }
}
if ($QUERY{'cnt'} eq 'title') {
	$match = 0;
	foreach (@LUCKYNO) {
		if ($_ == $count) { $match = 1; last; }
	}
	if ($match) { $img = $lucky_gif; }
	else { $img = $title_gif; }
} else {
	$count = "000000$count";
	$len = length($count);
	$count = substr($count,$len - $QUERY{'c'},$QUERY{'c'});
	$c = substr($count,0,1);
	if ($QUERY{'cnt'} == 1) { $img = $SUB_GIF1[$c]; }
	elsif ($QUERY{'cnt'} == 2) { $img = $SUB_GIF2[$c]; }
	else { $img = $MAINGIF[$c]; }
}
#画像を返す
print "Content-type: image/jpeg\n\n";
open(IMG, "$img") || die "Can't open: $dir/$img";
print $_ while (<IMG>);
close(IMG);
exit;
#=======================================================================================
sub data_read {
	if (open(DB,"$datafile")) {
		@DATA = <DB>;
		close(DB);
	}
}
#=======================================================================================
sub data_save {
	$tmpfile = 'cnt.tmp';
	foreach (1 .. 10) {
		unless (-f $tmpfile) { $tmpflag = 1; last; }
		$tmpflag = 0;
		sleep(1);
	}
	if ($tmpflag == 1) {
		$tmp_dummy = "$$\.tmp";
		if (!open(TMP,">$tmp_dummy")) { &error(bad_tmpfile); }
		close(TMP);
		chmod 0666,$tmp_dummy;
		if (!open(TMP,">$tmp_dummy")) { &error(bad_tmpfile); }
		print TMP @DATA;
		close(TMP);
		foreach (1 .. 10) {
			unless (-f $tmpfile) {
				if (!open(TMP,">$tmpfile")) { &error(bad_tmpfile); }
				close(TMP);
				rename($tmp_dummy,$datafile);
				unlink $tmpfile;
				$tmpflag = 1;
				last;
			}
			$tmpflag = 0;
			sleep(1);
		}
	}
	$tmpflag;
}
