#!/usr/local/bin/perl

;# WebFORM v4.0 is Free. (SJIS仕様)
;#
;#  (c)rescue.ne.jp
;#  http://www.rescue.ne.jp/

;# Hostory
;# 06/Jun/1998 v3.0 セキュリティ強化
;# 08/Aug/1998 v3.1 カーボンコピー処理改善
;# 29/Oct/1998 v4.0 カーボンコピー処理はセキュリティの問題で廃止

#------ 初期設定 ----------------------------------------------------------

#■日本語コード変換ライブラリ
require 'jcode.pl';

#■SENDMAILの設定
$sendmail = '/usr/sbin/sendmail';

#■受信先メールアドレス
$mailto = 'info@bscl.co.jp';

#■名称
$title = '「広島経済活性化推進倶楽部」オンライン・サインアップ';

#■処理画面のボディ設定
$body = '<body bgcolor="#ffffff">';

#■記入者申告メールアドレス( name="email"の時 )未入力でも送信する  1:する 0:しない
$mailcheck = 1;

#--------------------------------------------------------------------------

#時刻取得
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$wday = ('SUN','MON','TUE','WED','THU','FRI','SAT')[$wday];
$date_now = sprintf("%02d/%02d %s %02d:%02d",$mon +1,$mday,$wday,$hour,$min);

#タイトル欄に入力がない場合のデフォルト値
$subject = "- NO SUBJECT -";

#データ入力
if ($ENV{'REQUEST_METHOD'} ne "POST") { &error('エラー','標準入力 METHOD=POST を設定してください.<br>&lt;form method=post action=........&gt;'); }
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
if ($buffer eq '') { &error('エラー','このＣＧＩは直接起動されません.'); }
$ref = $ENV{'HTTP_REFERER'};
$buffer2 = $ENV{'QUERY_STRING'};
if ($buffer2 ne '') { &error('エラー','標準入力 METHOD=POST に設定してください.<br>&lt;form method=post action=........&gt;'); }

#デコード
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name,$value) = split(/=/,$pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
	$name =~ tr/+/ /;
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;

	&jcode'convert(*name,'sjis'); &jcode'convert(*value,'sjis');

	if ($value =~ /\r\n/) { $value =~ s/\r//g; }
	elsif ($value =~ /\r/) { $value =~ s/\r/\n/g; }

	if ($name eq "location") { $lct = $value; }
	elsif ($name eq "c_copy" && $value eq "on") { $cc = "on"; }
	elsif ($name eq "no_check" && $value eq "on") { $nocheck = "on"; }
	elsif ($name eq "space_check" && $value eq "on") { $spcheck = "on"; }
	elsif ($name eq "no_check") { ; }
	elsif ($name eq "ref_url") { $ref_url = $value; }
	elsif ($name eq "ref_name") { $ref_name = $value; }
	elsif ($name eq "subject" && $value ne "") { $subject = $value; }
	elsif ($name eq "subject") { ; }
	elsif ($name eq "ref_page") { $ref = $value; }
	elsif ($name eq "password") {

		$password = $value;
		push(@DATA_N,$name);
		push(@DATA_V,$value);
	}
	else {

		if ($name =~ /^email/i || $name =~ /^e\-mail/i) {

			$value =~ s/　/ /g;
			if ($value =~ / / || $value =~ /;/) { $value = ""; }
			if (!($value =~ /(.*)\@(.*)\.(.*)/)) { $value = ""; }

			$email = $value;
		}

		push(@DATA_N,$name); push(@DATA_V,$value);

		$name =~ s/\</&lt;/g; $value =~ s/\</&lt;/g;
		$name =~ s/\>/&gt;/g; $value =~ s/\>/&gt;/g;
		$name =~ s/\"/&quot;/g; $value =~ s/\"/&quot;/g;
		push(@DATA_NS,$name); push(@DATA_VS,$value);
	}
}

#入力チェック
if (!$mailcheck && $email eq '') { &error('Ｅメールを入力してください',''); }
if ($mailcheck && $email eq '') { $email = 'anonymous@on.the.net'; }
if ($spcheck eq "on") {	foreach (@DATA_V) { if ($_ eq "") { &error('送信不可','受信者の意向により、全ての項目を埋めないと送信できません.'); } }}
if ($mailto eq '' || !($mailto =~ /(.*)\@(.*)\.(.*)/)) { &error('設定ミス','受信先メールアドレスが設定されていません.'); }

if ($nocheck eq "on") { &sendmail; }

#内容確認画面出力
print "Content-type: text/html\n\n";
print "

<html><head><title>$title</title></head>
$body
<h1>内容確認</h1>
<form method=\"post\" action=\"webform.cgi\">
<blockquote>
<table border=0 cellpadding=3 cellspacing=3>
<tr><td bgcolor=\"#ffcccc\"><b><font size=+1>項目</font></b></td><td bgcolor=\"#ffcccc\"><b><font size=+1>内容</font></b></td></tr>

";

$count = @DATA_NS;

foreach (0..$count-1) {

	print "<input type=hidden name=\"$DATA_NS[($_)]\" value=\"$DATA_VS[($_)]\">\n";
	print "<tr><td bgcolor=\"#ffeedd\">$DATA_NS[($_)] <br></td>";

	if ($DATA_VS[($_)] =~ /\n/) { print "<td bgcolor=\"#ffffff\"><pre>$DATA_VS[($_)]</pre></td></tr>\n"; }
	else { print "<td bgcolor=\"#ffffff\">$DATA_VS[($_)]</td></tr>\n"; }
	print "</td></tr>\n";
}

print "</table></blockquote><p>\n";

if ($lct ne "") { print "<input type=hidden name=\"location\" value=\"$lct\">\n"; }

print "<input type=hidden name=\"no_check\" value=\"on\">\n";
print "<input type=hidden name=\"ref_page\" value=\"$ref\">\n";

if ($cc eq "on") { print "<input type=hidden name=\"c_copy\" value=\"on\">\n"; }
if ($ref_url ne "") { print "<input type=hidden name=\"ref_url\" value=\"$ref_url\">\n"; }
if ($ref_name ne "") { print "<input type=hidden name=\"ref_name\" value=\"$ref_name\">\n"; }
if ($subject ne "") { print "<input type=hidden name=\"subject\" value=\"$subject\">\n"; }
if ($password ne "") { print "<input type=hidden name=\"password\" value=\"$password\">\n"; }

if ($email eq '') { print "<font size=+2><b>メールアドレスを入力しないと送信できません</b></font><p>\n"; }
else { print "<input type=submit value=\"　送信 -submit-　\"><p>\n"; }

print "</form><p><hr>\n";
print "<i>利用責任者(送信先)：<a href=\"mailto:$mailto\">$mailto</a><i>\n";
print "<p></body></html>\n";
exit;

sub sendmail {

	if (!(open(OUT,"| $sendmail -t"))) { &error('システム異常','申し訳ありませんが何らかの原因で処理できません.'); }

	print OUT "X-Mailer: WebFORM v4.0 by www.rescue.ne.jp\n";
	print OUT "X-HTTP_REFERER: $ref\n";
	print OUT "Errors-To: $mailto\n";
	print OUT "To: $mailto\n";
	print OUT "From: $email\n";
	&jis("Subject: $subject"); print OUT "$msg\n";
	print OUT "Content-Transfer-Encoding: 7bit\n";
	print OUT "Content-Type: text/plain\; charset=\"ISO-2022-JP\"\n\n\n";

	&jis("--- ここから ---"); print OUT "$msg\n\n";

	$count = @DATA_N;
	foreach (0..$count-1) {

		if ($DATA_V[$_] =~ /\n/) { &jis("$DATA_N[$_] =\n\n$DATA_V[$_]\n"); print OUT "$msg\n"; }
		else { &jis("$DATA_N[$_] = $DATA_V[$_]"); print OUT "$msg\n"; }
	}

	&jis("--- ここまで ---"); print OUT "\n$msg\n\n";

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

	print OUT "\n";
	print OUT "----------------------------------------\n";
	print OUT "Processed         : $date_now\n";
	print OUT "Server-Name       : $ENV{'SERVER_NAME'}\n";
	print OUT "Server-Protocol   : $ENV{'SERVER_PROTOCOL'}\n";
	print OUT "Server-Port       : $ENV{'SERVER_PORT'}\n";
	print OUT "Gateway-Interface : $ENV{'GATEWAY_INTERFACE'}\n";
	print OUT "Request-Method    : $ENV{'REQUEST_METHOD'}\n";
	print OUT "Script-Name       : $ENV{'SCRIPT_NAME'}\n";
	print OUT "HTTP-Referer      : $ref\n";
	print OUT "HTTP-User-Agent   : $ENV{'HTTP_USER_AGENT'}\n";
	print OUT "Remote-host       : $host\n";
	print OUT "Remote-Addr       : $ENV{'REMOTE_ADDR'}\n";
	print OUT "----------------------------------------\n";
	print OUT "\n";

	close(OUT);

	if ($cc eq "on" && $lct ne '') {

		print "Content-type: text/html\n\n";
		print "<html><head><title>$title</title></head>\n";
		print "$body\n";
		print "<h1>送信完了</h1>\n";
		print "ただ今<a href=\"mailto:$mailto\">$mailto</a>宛てに送信された内容は以下の通りです.<br>\n";
		print "内容の写しとしてお控えください.<p>\n";
		print "<form>\n";
		print "<blockquote>\n";
		print "<textarea cols=70 rows=20>";
		&cc;
		print "</textarea></form></blockquote><p>\n";
		print "<h3>[<a href=\"$lct\" target=\"_top\">コピーしたら次へ</a>]</h3>";
	}
	elsif ($cc eq "on") {

		print "Content-type: text/html\n\n";
		print "<html><head><title>$title</title></head>\n";
		print "$body\n";
		print "<h1>送信完了</h1>\n";
		print "ただ今<a href=\"mailto:$mailto\">$mailto</a>宛てに送信された内容は以下の通りです.<br>\n";
		print "内容の写しとしてお控えください.<p>\n";
		print "<form>\n";
		print "<blockquote>\n";
		print "<textarea cols=70 rows=20>";
		&cc;
		print "</textarea></form></blockquote><p>\n";
		if ($ref_url ne '' && $ref_name ne '') { &jcode'convert(*ref_name,'sjis'); print "<h3>[<a href=\"$ref_url\" target=\"_top\">$ref_name</a>]</h3>"; }
		print "</body></html>\n";
	}
	elsif ($lct ne '') { print "Location: $lct\n\n"; }
	else {
		print "Content-type: text/html\n\n";
        	print "<html><head><title>$title</title></head>\n";
        	print "$body\n";
		print "<H1>送信完了</H1>\n";
		print "ご記入されたものは<a href=\"mailto:$mailto\">$mailto</a>宛てに電子メールされました.<br>\n";
		print "Thank you for sending comments to $mailto .<p>\n";
		if ($ref_url ne '' && $ref_name ne '') { &jcode'convert(*ref_name,'sjis'); print "<h3>[<a href=\"$ref_url\" target=\"_top\">$ref_name</a>]</h3>"; }
		print "<p></body></html>\n";
	}
	exit;
}

sub cc {

	print "X-Processed: $date_now\n";
	print "X-HTTP_REFERER: $ref\n";
	print "X-HTTP-User-Agent: $ENV{'HTTP_USER_AGENT'}\n";
	print "X-Remote-host: $host \[$ENV{'REMOTE_ADDR'}\]\n";
	print "To: $mailto\n";
	print "Subject: $subject\n\n";

	foreach (0..$count-1) {

		$DATA_NS[$_] =~ s/\</&lt;/g;
		$DATA_NS[$_] =~ s/\>/&gt;/g;
		$DATA_NS[$_] =~ s/\"/&quot;/g;

		$DATA_VS[$_] =~ s/\</&lt;/g;
		$DATA_VS[$_] =~ s/\>/&gt;/g;
		$DATA_VS[$_] =~ s/\"/&quot;/g;

		if ($DATA_VS[$_] =~ /\n/) { print "$DATA_NS[$_] =\n\n$DATA_VS[$_]\n"; }
		else { print "$DATA_NS[$_] = $DATA_VS[$_]\n"; }
	}
}

sub jis { $msg = $_[0]; &jcode'convert(*msg, 'jis'); }

sub error {

	print "Content-type: text/html\n\n";
        print "<html><head><title>$title</title></head>\n";
        print "$body\n";
        print "<h1>$_[0]</h1>\n";
	print "<h3>$_[1]</h3>\n";

	if ($ref eq '') {

		print "※ フォームページが取得できません.<br>\n";
		print "※ ブラウザの[戻る]ボタンを押して前の画面に移動してください.<p>\n";
	}
	else {

		print "※ フォームページ　<a href=\"$ref\">$ref</a><br>\n";
		print "※ フォームページへ戻るか、ブラウザの[戻る]ボタンを押して前の画面に移動してください.<p>\n";
	}

	print "<p></body></html>\n";
	exit;
}
