#!/usr/local/bin/perl
#       ↑あなたが加入しているプロバイダの｢perl｣言語が使用できる
#         パスを指定します。一般的に｢#!/usr/local/bin/perl｣で大丈夫

#=======================================================================================
#				access2 Version 98.1
#=======================================================================================
#★対象ページのタイトル
$hptitle = "広島経済活性化推進倶楽部　アクセス情報";

#★背景の色
$haikei = "#ffffff";

#★文字の色
$moji = "#666666";

#★各題目文字の色
$daiiro = "#7bc0d7";

#★表題目文字の色
$daimokumoji = "#63a7cf";

#★リンクの色
$midoku = "#ff8080";

#★既読リンクの色
$kidoku = "#ff0080";

#★表線の色
$hyouback = "#999999";

#★表題項目の色
$hyoudai = "#e1f5ff";

#★表内の色
$hyounai = "#fffff0";

#★リフレッシュ秒数
$byou = "30";

#★CGIのＵＲＬ
$cgiurl = "http://www.keizai-kassei.net/cgi/access/access2.cgi";

#★グラフのファイル保存場所
$bargif = "http://www.keizai-kassei.net/cgi/access/bar.gif";

#ログファイル
$datafile = 'access2.txt';
#----------------------------------------------------------
#ダミーで使用する画像（gif又はjpg形式）
$imgfile = 'z.gif';
#----------------------------------------------------------
#あなたの最短のアドレス
#同一ページからのリンクをカウントしないため
#私の場合はhttp://www2q.meshnet.or.jp/~terra/
$homepage = 'http://www.keizai-kassei.net/';
#----------------------------------------------------------
#最大記録数
$max = 1000;
#----------------------------------------------------------
#統計表示数の設定
#時間帯別統計を当日１日にする 'yes' / 'no'
$timeflag = 'no';
#----------------------------------------------------------
#ホスト名
$hostvew = 32;
#----------------------------------------------------------
#ブラウザ　表示しない場合は０にする
$agentvew = 30;
#----------------------------------------------------------
#リンク先　表示しない場合は０にする
$linkvew = 30;
#----------------------------------------------------------
#グラフの最大表示数
$graphvew = 200;
#----------------------------------------------------------
#その他のリンク先（ブックマーク等）の集計 'yes' / 'no'
$nolink = 'yes';
#----------------------------------------------------------
#クッキーを使用して正確な人数をカウントする 'yes' / 'no'
$cookieFlag = 'yes';
#----------------------------------------------------------
#クッキーを格納する名前を設定する
$CookieName = 'access2';
#=======================================================================================
#			初期設定が必要なのはここまでです。
#=======================================================================================
#日付と時刻を取得して、すべて２桁に統一する
$ENV{'TZ'} = "JST-9"; #日本時間に設定
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900;
	$month = sprintf("%02d",$mon + 1);
	$mday = sprintf("%02d",$mday);
	#日付時刻のフォーマットを整えます
	$youbi = ('日','月','火','水','木','金','土') [$wday];
	$date_now = "$year年$month月$mday日($youbi)";

$QUERY_DATA = $ENV{'QUERY_STRING'};
if ($QUERY_DATA eq 'vew') {
	&data_read;
	$datacount = @DATA;
	foreach $line (@DATA) {
		($da,$ho,$ag,$hr,$dm) = split(/\,/,$line);
		chop($dm);
		$dm += 0;
		if (!($hr =~ /^http:\/\//i)) { $hr = ''; }
		if ($hr =~ /$homepage/i) { $hr = ''; }
		if ($hr eq '') { $hr = 'その他（ブックマーク等）' }
		#日付ごとの集計
		$DA{$da}++;
		#時間ごとの集計
		if ($timeflag eq 'yes') {
			if ($date_now eq $da) { $seaflag = 1; } else { $seaflag = 0; }
		} else { $seaflag = 1; }
		if ($seaflag == 1) {
			$TI{$dm}++;
		}
		#ホストごとの集計
		$HO{$ho}++;
		if ($agentvew != 0) {
			#ブラウザごとの集計
			$AG{$ag}++;
		}
		if ($linkvew != 0) {
			#リンク先ごとの集計
			if ($nolink eq 'yes' || $hr ne 'その他（ブックマーク等）') { $HR{$hr}++; }
		}
	}
	#並べ替え
	foreach (keys %DA) {
		$dummy = "$_\,$_\,$DA{$_}";
		push(@DATE,$dummy);
		if ($datemax < $DA{$_}) { $datemax = $DA{$_}; }
	}
	@DATE = sort(@DATE); @DATE = reverse(@DATE);
	($s,$d,$datecount) = split(/\,/,$DATE[0]);
	foreach (keys %TI) {
		$s = sprintf("%04d",$_);
		$dummy = "$s\,$_\,$TI{$_}";
		push(@TIME,$dummy);
		if ($timemax < $TI{$_}) { $timemax = $TI{$_}; }
	}
	@TIME = sort(@TIME);
	foreach (keys %HO) {
		$s = sprintf("%04d",$HO{$_});
		$dummy = "$s\,$_\,$HO{$_}";
		push(@HOST,$dummy);
		if ($hostmax < $HO{$_}) { $hostmax = $HO{$_}; }
	}
	@HOST = sort(@HOST); @HOST = reverse(@HOST);
	if ($agentvew != 0) {
		foreach (keys %AG) {
			$s = sprintf("%04d",$AG{$_});
			$dummy = "$s\,$_\,$AG{$_}";
			push(@AGENT,$dummy);
			if ($agentmax < $AG{$_}) { $agentmax = $AG{$_}; }
		}
		@AGENT = sort(@AGENT); @AGENT = reverse(@AGENT);
	}
	if ($linkvew != 0) {
		foreach (keys %HR) {
			$s = sprintf("%04d",$HR{$_});
			$dummy = "$s\,$_\,$HR{$_}";
			push(@HREFLINK,$dummy);
			if ($linkmax < $HR{$_}) { $linkmax = $HR{$_}; }
		}
		@HREFLINK = sort(@HREFLINK); @HREFLINK = reverse(@HREFLINK);
	}
	#ＨＴＭＬを生成
	print "Content-type: text/html\n\n";
	print "<html><head><title>access</title>\n";
	print "</head>\n";
	print "<body bgcolor=$haikei text=$moji link=$midoku vlink=$kidoku>\n";
	print "<div align=center><center>\n";
	print "<p align=center><font size=6>$hptitle</font><br>";
	print "現在のサンプル数 $datacount アクセスです。";
	if ($cookieFlag eq 'yes') { print "<br>重複アクセスを排除した正確な人数を表\示しています。"; }
	print "</p>\n";
	print "<font size=5 color=$daiiro>◆日別統計</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>日付</font></td>\n";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>カウント</font></td>\n";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>ポイント</font></td>\n";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>グラフ</font></td></tr>\n";
		foreach $dummy (@DATE) {
			($s,$d,$c) = split(/\,/,$dummy);
			if ($d =~ /\d{4}\年\d{2}\月\d{2}\日/) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($datemax != 0) { $chrlen = int($c / $datemax * $graphvew); }
				}
				print "<tr><td bgcolor=$hyounai>$d</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai><img src=$bargif width=$chrlen height=10></td></tr>\n";
			}
		}
		print "</table>\n";
		print "<br><font size=5 color=$daiiro>◆時間別統計</font>\n";
		if ($timeflag eq 'yes') {
			print "$date_now\n";
		}
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>時間</font></td>";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>カウント</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>ポイント</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>グラフ</font></td></tr>\n";
		foreach $dummy (@TIME) {
			($s,$d,$c) = split(/\,/,$dummy);
			if ($d < 1) { $d = 0; }
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					if ($timeflag eq 'yes') {
						if ($datecount > 0) { $per = $c / $datecount * 100; }
						else { $per = 0; $chrlen = 0; }
					} else {
						$per = $c / $datacount * 100;
					}
					if ($timemax != 0) { $chrlen = int($c / $timemax * $graphvew); }
				}
				print "<tr><td align=center bgcolor=$hyounai>$d 時</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "　"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
		}
		print "</table><br>\n";
		print "<font size=5 color=$daiiro>◆ホスト統計</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>ホスト名</font></td>";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>カウント</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>ポイント</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>グラフ</font></td></tr>\n";
		$vew = 1;
		foreach $dummy (@HOST) {
			($s,$h,$c) = split(/\,/,$dummy);
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($hostmax != 0) { $chrlen = int($c / $hostmax * $graphvew); }
				}
				print "<tr><td bgcolor=$hyounai>$h</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "　"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
			$vew++;
			if ($vew > $hostvew) { last; }
		}
		print "</table>\n";
	if ($agentvew != 0) {
		print "<br><font size=5 color=$daiiro>◆ブラウザ統計</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>ブラウザ</font></td>";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>カウント</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>ポイント</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>グラフ</font></td></tr>\n";
		$vew = 1;
		foreach $dummy (@AGENT) {
			($s,$a,$c) = split(/\,/,$dummy);
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($agentmax != 0) { $chrlen = int($c / $agentmax * $graphvew); }
				}
				print "<tr><td bgcolor=$hyounai>$a</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print " <td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "　"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
			$vew++;
			if ($vew > $agentvew) { last; }
		}
		print "</table>\n";
	}
	if ($linkvew != 0) {
		print "<br><font size=5 color=$daiiro>◆リンク先統計</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai width=\"260\"><font color=$daimokumoji>リンク先</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"70\"><font color=$daimokumoji>カウント</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>ポイント</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>グラフ</font></td></tr>\n";
		$vew = 1;
		foreach $dummy (@HREFLINK) {
			($s,$a,$c) = split(/\,/,$dummy);
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($linkmax != 0) { $chrlen = int($c / $linkmax * $graphvew); }
				}
				print "<tr> <td bgcolor=$hyounai>";
				print "<a href=$a>$a</a>";
				print "</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "　"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
			$vew++;
			if ($vew > $linkvew) { last; }
		}
		print "</table>\n";
	}
	print "</center></div>\n";
	print "<p align=right><font size=-1><a href=http://www2.inforyoma.or.jp/~terra/>Access2 by Terra</a></font></p>\n";
	print "</body></html>\n";
	exit;
} else {
	if ($cookieFlag eq 'yes') {
		$ENV{'TZ'} = "GMT"; 
		($c_sec,$c_min,$c_hour,$c_mday,$c_mon,$c_year,$c_wday,$c_yday,$c_isdst) = localtime(time + 3 * 86400);
		$cookies = $ENV{'HTTP_COOKIE'};
		@pairs = split(/;/,$cookies);
		foreach $pair (@pairs) {
			($name, $value) = split(/=/, $pair);
			$name =~ s/ //g;
			$DUMMY{$name} = $value;
		}
		@pairs = split(/,/,$DUMMY{$CookieName});
		foreach $pair (@pairs) {
			($name, $value) = split(/\!/, $pair);
			$COOKIE{$name} = $value;
		}
	}
	if ($COOKIE{'date'} ne $date_now) {
		&data_read;
		$datacount = @DATA;
		$hostadd = &domain_name;
		$agent = $ENV{'HTTP_USER_AGENT'};
		$agent =~ s/,/./g;
		$agent =~ s/\; Yahoo\! JAPAN Version Windows 95\/NT CD\-ROM Edition 1\.0\.//;
		$hreflink = $QUERY_DATA;
		$value = "$date_now\,$hostadd\,$agent\,$hreflink\,$hour\n";
		while ($datacount >= $max) {
			pop(@DATA);
			$datacount = @DATA;
		}
		unshift(@DATA,$value);
		&data_save;
		if ($cookieFlag eq 'yes') {
			$c_year += 1900;
			$c_sec  = sprintf("%02d",$c_sec);
			$c_min  = sprintf("%02d",$c_min);
			$c_hour = sprintf("%02d",$c_hour);
			$c_mday = sprintf("%02d",$c_mday);
			$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') [$c_wday];
			$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') [$c_mon];
			$date_gmt = "$youbi, $c_mday\-$month\-$c_year $c_hour:$c_min:$c_sec GMT";
			$cook = "date\!$date_now";
			print "Set-Cookie: $CookieName=$cook; expires=$date_gmt\n";
		}
	}
	print "Content-type: image/jpeg\n\n";
	open(IMG, "$imgfile") || die "Can't open: $dir/$img";
	print $_ while (<IMG>);
	close(IMG);
	exit;
}
#=======================================================================================
sub domain_name {
	local($addr) = $ENV{'REMOTE_ADDR'};
	local($_) = gethostbyaddr(pack("C4",split(/\./,$addr)),2);
	if ($_ eq '') { $_ = $addr; }
	else {
		if (/.+\.(.+)\.(.+)\.(.+)$/) { $_ = "\*\.$1\.$2\.$3"; }
		elsif (/.+\.(.+)\.(.+)$/) { $_ = "\*\.$1\.$2"; }
		elsif (/.+\.(.+)$/) { $_ = "\*\.$1"; }
		else { $_ = "on the internet"; }
	}
	$_;
}
#=======================================================================================
sub data_read {
	if (open(DB,"$datafile")) {
		@DATA = <DB>;
		close(DB);
	}
}
#=======================================================================================
sub data_save {
	$tmpfile = 'access2.tmp';
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
		if (-f $tmp_dummy) { unlink $tmp_dummy; }
	}
	$tmpflag;
}
