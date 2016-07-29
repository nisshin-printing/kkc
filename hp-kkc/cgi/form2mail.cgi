#!/usr/local/bin/perl

# フォームメール v1.32  <FREESOFT>
# (Ｗｅｂ上のフォームから送信された内容を電子メールで配信する)
#
;$vers = '1.32';
#
#  製作・著作 CGI-RESCUE
#  http://www.rescue.ne.jp/
#
# [History]
# 1/FEB/1999 v1.00 <WebFORM> + <FileUPLOADER> = <FORM2MAIL>
# 12/FEB/1999 v1.01 エラー処理の修正(一時ファイルの削除トラブル)
# 24/MAR/1999 v1.10 アクセス元チェックの処理の設定
# 25/JUL/1999 v1.11 テーブルタグ内のフォームについて修正
# 16/DEC/1999 v1.12 $ref_urlの処理ミス修正
# 07/FEB/2000 v1.13 再梱包
# 09/FEB/2000 v1.14 抜けていたタグ処理を追加,CSV出力添付機能の付加
# 26/JUL/2000 v1.15 メールヘッダの修正
# 05/OCT/2004 v1.20 SubjectのRFC2045対応(簡易),UUENCODE/BASE64選択,外部プログラムnkfおよびuuencodeを使わない設計
# 31/JAN/2005 v1.21 Content-Type出力の修正
# 16/Feb/2006 v1.22 スパムに対する脆弱性を修正
# 18/Mar/2006 v1.23 メールのタイトルをＢエンコードにしない場合にタイトルが設定されない不具合を修正
# 12/May/2006 v1.30 必須項目エラーの表示順を、フォームで羅列した順に修正
# 31/May/2006 v1.31 v1.30修正のバグの修正
# 22/Jun/2006 v1.32 Ｂエンコードしない場合にタイトルの文字コードがJISにならないバグの修正

#-------------------------------------------------------------------------------------------

# [設置例] ( )内はパーミッションの相当値
#
# /任意のディレクトリ/
#         |
#         |-- /tmp/ <777> ... 作業用
#         |-- base64.pl <644> ... ＭＩＭＥ変換ライブラリ
#         |-- cgi-lib217.pl <644> ... ＣＧＩライブラリ
#         |-- form2mail.cgi <755> ... 本体（このプログラム）
#         |-- jcode.pl <644> ... 日本語コード変換ライブラリ
#

#------ 初期設定 ---------------------------------------------------------------------------

#■日本語コード変換ライブラリ    # require './***.pl'; と require '***.pl';は意味が違いますので、注意。
require './jcode.pl';

#■ＣＧＩライブラリ
require "./cgi-lib217.pl";

#■ＭＩＭＥ変換ライブラリ
require "./base64.pl";

#■sendmailの設定
$sendmail = '/usr/sbin/sendmail';

#■作業用ディレクトリの設定
#　同じディレクトリにtmpという名前のディレクトリを作成し、パーミッションを777(サーバの最適な値にあわせること)にします。
$tmp = "./tmp/";

#■受け取るメールアドレス
$mailto = 'info@keizai-kassei.net';

#■フォーム画面に付けるタイトル
$title = 'プレゼンテーションお申し込み';

#■参照チェック
#送信フォームのＵＲＬがここに設定した文字列を含まない場合は送信しない
$ref_url = 'keizai-kassei.net';

#■このスクリプトを設置する日本語コード (sjis,euc)
$convert = 'sjis';

#■アクセス元をチェックする(いたずらで困っている場合のみ) 0:しない 1:する
$ref_check = 0;

#■メールのタイトルをＢエンコード化するかどうか -- 0:しない 1:する
$EncodeB = 1;

	# (参考) メール"Subject"について
	# メールのヘッダ部分に２バイト文字を使う場合は、RFC2045に依り、BASE64でエンコードしたＢエンコード形式
	# =?ISO-2022-JP?B?<BASE64コード>?= にしなければなりませんが、昨今のほとんどのメールソフトでは、そう
	# しなくても正しく表示してくれます。この規則に従うように加工することは非常に面倒なため、その特殊な加工
	# を必要としない程度の仕様に留めているため、メール題名の文字数に制限を設けています。

#■ファイル添付形式 # 0:BASE64 1:UUENCODE
$uuencode = 0;

	# (参考) このプログラムのuuencodeの仕様
	# メールゲートウェイの中に行末を含む空白文字を除去してしまうものがあるため、空白文字は"`"(0x60)に変換しています。
	# デコードする際はそれは空白文字(0x00)として解釈してください。<MODE>は当プログラムでは600に設定しています。
	#
	# begin <MODE> <ファイル名>
	# ～内容～
	# `
	# end

#-------------------------------------------------------------------------------------------

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
($seco,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@mon_array = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
@wday_array = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
$date_now = sprintf("%s, %02d %s %04d %02d:%02d:%02d +0900 (JST)",$wday_array[$wday],$mday,$mon_array[$mon],$year +1900,$hour,$min,$sec);

#-------------------------------------------------------------------------------------------

$ref = $ENV{'HTTP_REFERER'};
$ref =~ s/\n|\r//g;
$addr = $ENV{'REMOTE_ADDR'};
if ($host eq "" || $host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr; }
$via = $ENV{'HTTP_VIA'};
$xfor = $ENV{'HTTP_X_FORWARDED_FOR'};
$for = $ENV{'HTTP_FORWARDED'};
$agent = $ENV{'HTTP_USER_AGENT'}; $agent =~ s/</(/g; $agent =~ s/>/)/g;
if ($via ne "") { $trueip = $xfor; }
else { $trueip = $addr; }
if ($xfor ne "") { $xfor_name = gethostbyaddr(pack('C4',split(/\./,$xfor)),2) || $xfor; }
$access_data = "host;$host addr;$addr via;$via xfor;$xfor for;$for agent;$agent trueip;$trueip xfor_name;$xfor_name";
$access_data =~ s/\n|\r//g;

#-------------------------------------------------------------------------------------------

$ret = &ReadParse;
if ($ret == 0) { &error('入力がありません.'); }

if ($ref_check) {

	$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if (!($ref =~ /$ref_url/i)) { &error('不正な手順を検知しました','正規のフォーム以外からのアクセスです.'); }
}

#-------------------------------------------------------------------------------------------

$filenum = 0;
foreach $data (@in) {

	unless ($ENV{'CONTENT_TYPE'} =~ m#^multipart/form-data#) {

		$ENCTYPE = "multipart/form-data";
		$data =~ s/\+/ /g;
		($key,$val) = split(/=/,$data,2);
		$key =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;
		push(@name,"$key\0$filename");
	}
	else {
		($key) = $data =~ /\bname="([^"]+)"/i;
		($filename) = $data =~ /\bfilename="([^"]*)"/i;
		if ($filename eq '' && $data =~ /\bfilename="([^"]*)"/i) { next; }
		push(@name,"$key\0$filename");
	}
}

#-------------------------------------------------------------------------------------------

$fileC1 = $fileC2 = 0;
foreach $name (@name) {

	($name,$filename) = split("\0",$name);

	if ($filename ne '') {

		if (exists $out{$name}) { $fileC1 = 1; next; }
		$fileC2 = 1;

		$ps = $$;
		if ($ps eq '') { $ps = time; }

		$filename = reverse(($filename) = split(/\\|\/|\:/,reverse($filename)));
		push(@FILE,"$name\0$ps\_$filenum\0$filename");
		push(@FILEDATA,$in{$name});

		$filenum++;
		$out{$name} = $name;
		push(@atf,"[添付] $name\0$filename");

		next;
	}

	&jcode'convert(*name,$convert);

	$num = $lastspc = 0;

	foreach $value (split("\0",$in{$name})) {

		if (!exists $out{$name}{$num}) {

			$lastspc = 1;
			&jcode'convert(*value,$convert);

			($cmd) = &checkval($name,$value);
			if ($cmd) { next; }

			$value =~ s/&/&amp;/g;
			$value =~ s/"/&quot;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;

			push(@out,"$name\0$value");
			$out{$name}{$num} = $value;
			last;
		}

		$num++;
	}

	if (!$lastspc) {

		if ($name =~ /^_(.*)$/) { next; }
		push(@out,$name);
	}
}

#-------------------------------------------------------------------------------------------

foreach $out (@out) {

	($name,$value) = split("\0",$out);
	if ($indispen{$name} && $in{$name} eq '') { push(@INDISPENs,$name); }
}

if (@INDISPENs) { &error("未記入があります",'<h3>次の項目は必須入力です.</h3>',"<i>@INDISPENs</i>"); }

#-------------------------------------------------------------------------------------------

if ($in{'_emailset'} ne '' && exists $in{$in{'_emailset'}}) {

	$EMAIL = $in{$in{'_emailset'}};
	if ($EMAIL ne '') {

		if ($EMAIL =~ /\s|\,/) { &error('Error','Ｅメールを正しくご記入ください.'); }
		unless ($EMAIL =~ /\b[-\w.]+@[-\w.]+\.[-\w]+\b/) { &error('エラー','Ｅメールは半角で正しくご記入ください.'); }
	}
}

if ($EMAIL eq '') { $EMAIL = 'anonymous@on.the.net'; }

#-------------------------------------------------------------------------------------------

if ($fileC1) { &error('エラー','アップロードファイルの項目名が重複しています.'); }

if ($fileC2) { 

	$mix = 1;

	foreach $file (0 .. $#FILE) {

		($name,$filenum,$filename) = split("\0",$FILE[$file]);

		if (!open(BIN,"> $tmp$filenum")) { &error('エラー','アップロードファイルの一時ファイルが作成できません.','テンポラリーフォルダのパーミッションを確認してください.'); }
		binmode(BIN);
		print BIN $FILEDATA[$file];
		close(BIN);
	}
}

if ($check{'_check'} && $mix) { &error('エラー','ファイルアップロード機能を使う場合は、内容確認処理は利用できません.'); }

if ($check{'_check'}) { &check; }

&sendmail;
exit;

#-------------------------------------------------------------------------------------------

sub check {

	print &PrintHeader;
	print &HtmlTop($title);

	print <<"EOF";
	<body $check{'_body'}>
	<h2>内容確認</h2>
	<form method="$ENV{'REQUEST_METHOD'}" action="form2mail.cgi" ENCTYPE="$ENCTYPE">
	<blockquote>
	<table border=3 cellpadding=2 cellspacing=1>
	<tr><td><b><font size=+1>項目</font></b></td><td><b><font size=+1>内容</font></b></td></tr>
EOF

	foreach (@out) {

		($name,$value) = split("\0");

		print "<tr><input type=hidden name=\"$name\" value=\"$value\">\n";
		print "<td>$name</td>\n";

		if ($value =~ /\n/) { print "<td><pre>$value</pre></td></tr>\n"; }
		else { print "<td>$value</td></tr>\n"; }

		print "</td></tr>\n";
	}

	print "</table></blockquote><p>\n";

	while (($key,$val) = each %check) {

		if ($key =~ /^_check$/i) { next; }
		print "<input type=hidden name=\"$key\" value=\"$val\">\n";
	}

	while (($key,$val) = each %indispen) {

		print "<input type=hidden name=\"_indispen\" value=\"$key\">\n";
	}

	print "<input type=hidden name=\"_refurl\" value=\"$ref\">\n";
	print "<input type=submit value=\"　○  送 信  \"><p>\n";

	print "</form><p><hr>\n";
	print "<i>送信先：<a href=\"mailto:$mailto\">$mailto</a><i>\n";

	print &HtmlBot;
	exit;
}

#-------------------------------------------------------------------------------------------

sub sendmail {

	push(@MailValue,"Date: $date_now\n");
	push(@MailValue,"X-Sender: $access_data\n");
	push(@MailValue,"X-Mailer: form2mail $vers by CGI-RESCUE\n");
	push(@MailValue,"X-Referer: $ref\n");

	push(@MailValue,"To: $mailto\n");
	if ($EMAIL eq 'anonymous@on.the.net') { push(@MailValue,"Reply-To: $mailto\n"); }

	$EMAIL =~ s/\n//g; $EMAIL =~ s/\r//g;
	if (length($EMAIL) > 255) { &error('エラー','メールアドレスの長さ制限は255文字までです.'); }
	if ($EMAIL =~ /\,/) { &error('エラー','メールアドレスを正しく１つ入力しないと送信できません.'); }
	push(@MailValue,"From: $EMAIL\n");

	$SUBJECT = $in{'_subject'};
	$SUBJECT =~ s/\n//g; $SUBJECT =~ s/\r//g;

	if ($EncodeB) {

		$SUBJECT = &mailSubject_base64encode($SUBJECT);
		if (!$SUBJECT) { &error("エラー","メールのタイトル(題名)を短くしてください。"); }
	}
	else { $SUBJECT = &jis("Subject: $SUBJECT\n"); }

	push(@MailValue,$SUBJECT);
	push(@MailValue,"MIME-Version: 1.0\n");
	push(@MailValue,"Content-Transfer-Encoding: 7bit\n");

	if ($mix) { &send_mix; }
	else { &send; }

	if (open(OUT,"| $sendmail -t")) {

		foreach (@MailValue) { print OUT $_; }
		close(OUT);
	}

	if ($check{'_ccopy'} && $check{'_location'} ne '') {

		print &PrintHeader;
		print &HtmlTop($title);

		print "<body $check{'_body'}>\n";
		print "<h2>送信しました</h2>\n";
		print "ただ今<a href=\"mailto:$mailto\">$mailto</a>宛てに送信された内容は以下の通りです.<br>\n";
		print "内容の写しとしてお控えください.<p>\n";
		print "<form>\n";
		print "<blockquote>\n";
		print "<textarea cols=70 rows=20>";
		&cc;
		print "</textarea></form></blockquote><p>\n";
		print "<h3>[<a href=\"$check{'_location'}\" target=\"_top\">コピーしたら次へ</a>]</h3>";
	}
	elsif ($check{'_ccopy'}) {

		print &PrintHeader;
		print &HtmlTop($title);

		print "<body $check{'_body'}>\n";
		print "<h2>送信しました</h2>\n";
		print "ただ今<a href=\"mailto:$mailto\">$mailto</a>宛てに送信された内容は以下の通りです.<br>\n";
		print "内容の写しとしてお控えください.<p>\n";
		print "<form>\n";
		print "<blockquote>\n";
		print "<textarea cols=70 rows=20>";
		&cc;
		print "</textarea></form></blockquote><p>\n";
		if ($check{'_gourl'} ne '' && $check{'_goname'} ne '') { print "<h3>[<a href=\"$check{'_gourl'}\" target=\"_top\">$check{'_goname'}</a>]</h3>"; }
	}
	elsif ($check{'_location'} ne '') { print "Location: $check{'_location'}\n\n"; }
	else {

		print &PrintHeader;
		print &HtmlTop($title);

        	print "<body $check{'_body'}>\n";
		print "<h2>送信しました</h2>\n";
		print "ご記入されたものは<a href=\"mailto:$mailto\">$mailto</a>宛てに電子メールされました.<br>\n";
		print "Thank you for sending comments to $mailto .<p>\n";
		if ($check{'_gourl'} ne '' && $check{'_goname'} ne '') { print "<h3>[<a href=\"$check{'_gourl'}\" target=\"_top\">$check{'_goname'}</a>]</h3>"; }
	}

	print &HtmlBot;
}

#-------------------------------------------------------------------------------------------

sub cc {

	print "Date: $date_now\n";
	print "To: $mailto\n";
	print "From: $EMAIL\n";
	print "Subject: $in{'_subject'}\n\n";

	foreach (@out) {

		s/&lt;/</g;
		s/&gt;/>/g;

		($name,$value) = split("\0");

		if ($check{'_type'} == 1) { print "\[$name\]\n$value\n\n"; }
		elsif ($value =~ /\n/) { print "$name =\n$value\n\n"; }
		else { print "$name = $value\n"; }
	}

	print "\n";

	foreach (@atf) {

		($name,$value) = split("\0");
		print "$name = $value\n";
	}
}

#-------------------------------------------------------------------------------------------

sub send {

	push(@MailValue,"Content-Type: text/plain; charset=\"ISO-2022-JP\"\n");

	$BODY .= "\n"; # ヘッダ終了の区切り

	foreach $line (@out) {

		($name,$value) = split("\0",$line,2);

		$value =~ s/&amp;/&/g;
		$value =~ s/&quot;/"/g;
		$value =~ s/&lt;/</g;
		$value =~ s/&gt;/>/g;

		if ($check{'_csv'} == 1) { push(@CSV,$value); }

		if ($check{'_type'} == 1) { $BODY .= "\[$name\]\n$value\n\n"; }
		elsif ($value =~ /\n/) { $BODY .= "$name =\n$value\n\n"; }
		else { $BODY .= "$name = $value\n"; }
	}

	$BODY .= "\n";
	$BODY .= &EncodeCSV(@CSV) . "\n\n";

	push(@MailValue,&jis($BODY));
}

#-------------------------------------------------------------------------------------------

sub send_mix {

	($boundary) = $ENV{'CONTENT_TYPE'} =~ m#multipart/form-data; boundary=(.*)#;
	if ($boundary eq "") { $boundary = '0123456789zxcvbnmasdfghjklqwertyuiop'; }
	$bound = "--" . $boundary;

	$BODY .= "Content-Type: multipart/mixed; boundary=\"$bound\"\n\n";
	$BODY .= 'This is multipart message.' . "\n\n";

	$BODY .= "--$bound\n";
	$BODY .= "Content-Transfer-Encoding: 7bit\n";
	$BODY .= 'Content-Type: text/plain; charset="ISO-2022-JP"' . "\n\n";

	foreach $line (@out) {

		($name,$value) = split("\0",$line,2);

		$value =~ s/&amp;/&/g;
		$value =~ s/&quot;/"/g;
		$value =~ s/&lt;/</g;
		$value =~ s/&gt;/>/g;

		if ($check{'_csv'} == 1) { push(@CSV,$value); }

		if ($check{'_type'} == 1) { $BODY .= "\[$name\]\n$value\n\n"; }
		elsif ($value =~ /\n/) { $BODY .= "$name =\n$value\n\n"; }
		else { $BODY .= "$name = $value\n"; }
	}

	$BODY .= "\n";

	$BODY .= "\n";
	if ($check{'_csv'} == 1) { $BODY .= &EncodeCSV(@CSV) . "\n\n"; }

	foreach $line (@atf) {

		($name,$value) = split("\0",$line,2);
		$BODY .= "$name = $value\n";
	}

	$BODY .= "\n";

	push(@MailValue,&jis($BODY));

	#-----------------------------------------------------------------------------------

	$BODY = "";

	foreach $file (0 .. $#FILE) {

		($name,$filenum,$filename) = split("\0",$FILE[$file],3);

		$BODY .= "--$bound\n";
		$BODY .= "Content-Type: application/octet-stream; name=\"$filename\"\n";

		if ($uuencode) { $BODY .= 'Content-Transfer-Encoding: X-uuencode' . "\n"; }
		else { $BODY .= 'Content-Transfer-Encoding: base64' . "\n"; }

		$BODY .= "Content-Disposition: attachment; filename=\"$filename\"\n\n";

		$binary_string = "";
		if (open(UU,"$tmp$filenum")) {

			while (<UU>) { $binary_string .= $_; }
			close(UU);
		}

		if ($uuencode) {

			$ascii_string = &base64'uuencode($binary_string);
			$BODY .= "begin 600 $filename\n$ascii_string\`\n" . "end\n\n";
		}
		else {
			$ascii_string = &base64'b64encode($binary_string);
			$BODY .= "$ascii_string\n";
		}

		if (-e "$tmp$filenum") { unlink("$tmp$filenum"); }
	}

	$BODY .= "--$bound\-\-\n";
	push(@MailValue,$BODY);
}

#-------------------------------------------------------------------------------------------

sub checkval {

	local($key,$val) = @_;
	local($num,$cmd);

	if ($key =~ /^_indispen$/i) {

		$indispen{$val} = 1;
		return 1;
	}

	elsif ($key =~ /^_(.*)$/i) { $cmd = "\_$1"; $check{$cmd} = $val; return 1; }
	else { return 0; }
}

#-------------------------------------------------------------------------------------------

sub EncodeCSV {

	local(@fields) = @_;
	local(@CSV) = ();

	foreach $text (@fields) {

		$text =~ s/"/""/g;
		if ($text =~ /,|"/) { $text = "\"$text\""; }

		push(@CSV,$text);
	}

	return join(',',@CSV);
}

#-------------------------------------------------------------------------------------------

sub mailSubject_base64encode {

	local($line) = @_;
	jcode::convert(\$line,'jis','euc','z');
	$line = &base64'b64encode($line);
	eval 'chomp($line);'; chop($line) if $@ ne '';
	if (length($line) > 64) { return 0; }
	return "Subject: =?ISO-2022-JP?B?$line?=\n";
}

#-------------------------------------------------------------------------------------------

sub jis {

	local($line) = @_;
	&jcode'convert(*line,'jis');
	$line;
}

#-------------------------------------------------------------------------------------------

sub error {

	local (@msg) = @_;
	local ($i);

	foreach $file (@FILE) {

		($name,$filenum,$filename) = split("\0",$FILE[$file]);
		if (-e "$tmp$filenum") { unlink("$tmp$filenum"); }
	}

	print &PrintHeader;

	print <<"EOF";
	<HTML>
	<HEAD>
	<TITLE>$title</TITLE>
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	</HEAD>
	<body $check{'_body'}>
	<h1>$_[0]</h1>
EOF

	foreach $i (1 .. $#msg) { print "$msg[$i]<br>\n"; }

	print <<"EOF";
	<h3>[<A HREF="JavaScript:history.back()">戻る</A>]</h3>
EOF

	print &HtmlBot;
	exit;
}
