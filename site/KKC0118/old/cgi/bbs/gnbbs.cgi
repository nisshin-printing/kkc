#!/usr/bin/perl

#******************************************************************************
#gnbbs.cgi - General BBS Ver.1.22
#
#Version   	:1.22
#modified  	:2001/05/22
#Copyright 	:The Room
#E-Mail		:dream@lib.net
#URL		:http://dream.lib.net/room/
#
#これはフリー素材です。
#転載・商用目的の利用の際には、メールをお願いします。
#
#******************************************************************************
#1行目のperlのディレクトリ指定は、サーバによって異なります。
#詳しくは、管理者にお聞きください。
#******************************************************************************
#画面設定
#
#タイトル
$title = "広島経済活性化倶楽部　掲示板";

#BODYタグ
$bodytag='<body text=#092875 bgcolor=#ffffff link=303060 vlink=303060 alink=8080cf background="../../image/back.gif">';

#ページ上部に表示する題名
$pagetop = '<div align=center><TABLE><TBODY><TR><TD bgcolor="#666666" height="3"></TD></TR><TR><TD bgcolor="#666666" width="353" align="center" height="70"><IMG src="../../image2.gif" width="258" height="17" border="0"><IMG src="../../image3.gif" width="311" height="29" border="0"></TD></TR><TR><TD height="3" bgcolor="#666666"></TD></TR></TBODY></TABLE></div><br><br>';

#ホームページURL
# 設定しない場合とリンクは表示されません。
$homeback = "http://www.keizai-kassei.net/";

#******************************************************************************
#メッセージ欄の色

#題名部分の背景色
$msgcl1 = "#adcae7";

#名前部分の背景色
$msgcl2 = "#bed5eb";

#時間表示部分の背景色
$msgcl3 = "#cedff0";

#本文の背景色
$msgcl4 = "#e4eef8";

#******************************************************************************
#入力欄の色

#名前入力欄の背景色
$entercl1 = "#e4eef8";

#E-Mail入力欄の背景色
$entercl2 = "#cedff0";

#URL入力欄の背景色
$entercl3 = "#bed5eb";

#題名入力欄の背景色
$entercl4 = "#adcae7";

#メッセージ入力欄の背景色
$entercl5 = "#9dbfe1";

#削除キー入力欄の背景色
$entercl6 = "#adcae7";

#******************************************************************************
#
#スタイルシート設定
# inputは入力するボックス、buttonはSubmitなどのボタンを表します。
# 使用しない場合は、削除してください。
#$sheet = <<EOD;	
#<style type = "text/css">
#BODY,TD,TH{font-size: 10pt;}
#.input 	{border-color:a0a0ff;
#		border-style:dotted dotted dotted dotted;
#		}
#.button	{border-color:6060ff;
#		border-style:dotted dotted dotted dotted;
#		background-color: b0b0ff;
#		color: 0000ff;
#		}
#</style>
#EOD

#******************************************************************************
#
#マスターパスワード
# すべての記事の削除キーに使えます。
$adminpass = "npo";

#ログ保存ファイル名
$logfile = "./log.dat";

#親記事のログ保存の最大数
$maxlog = 50;

#１ページに表示する最大記事数
$maxpage = 10;

#名前入力が無い場合の名前
# 設定しないと名前の入力が必須となります。
$newname = "";

#題名入力が無い場合の題名
# 設定しないと題名の入力が必須となります。
$newsubject = "無題";


#時刻設定
sub timeset{$timeword = "$month/$day $hour:$min";}
#                        ~~~~~~~~~~~~~~~~~~~~
#２つの " の間に時刻表示のフォーマットを書きます
#以下の変数を書くと、表示されるときに
#その値が表示されます
# $year  年
# $month 月
# $day   日
# $hour	 時
# $min   分
# $sec   秒
# $week  曜日

#時刻表示のゼロ補完の有無
# 10以下を表示するときは 04 のように頭に 0 を追加します。
# この機能を使う場合は 1 を、使わない場合は 0 を。
$spzero[0] = 0;#月の補完
$spzero[1] = 0;#日の補完
$spzero[2] = 0;#時の補完
$spzero[3] = 1;#分の補完
$spzero[4] = 0;#秒の補完

#曜日の設定
# 日～土の順番です。
@weekday = ("Sun","Mon","Tue","Wed","Thr","Fri","Sat");

#******************************************************************************

#ソースにIP/ホスト名を表示するときは1を設定。
$ipindicate = 1;

#jcode.plのパス
$jcode = './jcode.pl';

#アクセス拒否をするホスト名を入力します。
# @denyhost = ("anonymizer","cache*.*",……);
# このように入力していきます。
# 例のように、ワイルドカードも使用できます。
@denyhost = ();

#使用を許可するタグを書きます。
# 全て不許可の場合は、
# @permittag = ();
# としてください。
@permittag = ("a","i","b","font");


#URLの書きこみに自動的にリンクを貼るなら1を設定。
$autolink = 1;

#別ページからの投稿を禁止する場合は1を設定。
$referercheck = 0;

#二重投稿を禁止する場合は1を設定。
$double = 1;	

#グリニッジ標準時からのずれ（秒単位）
# 初期設定は +32400秒 = 9時間の日本時間設定です。
$areatime = 32400;

#******************************************************************************

#jcode.plの読みこみ
require $jcode;
srand;

#データ受け取り
$cl = $ENV{"CONTENT_LENGTH"};
if( $cl > 0 ){
	read(STDIN, $qs, $cl );
}else{
	$qs = $ENV{"QUERY_STRING"};
	}

@contents = split(/&/,$qs);
foreach $i (0 .. $#contents) {
	local($key,$text)= split(/=/,$contents[$i]);
	$text =~ s/\+/ /g;
	$text =~ s/%(..)/pack("c",hex($1))/ge;
	$text =~ s/\r\n/\n/g;
	&jcode'convert(*text,'sjis');
	$act = $text if $key eq 'act';
	$page = $text if $key eq 'page';
	$name = $text if $key eq 'name';
	$email = $text if $key eq 'email';
	$url = $text if $key eq 'url';
	$subject = $text if $key eq 'subject';
	$delkey = $text if $key eq 'delkey';
	$msg = $text if $key eq 'msg';
	$pass = $text if $key eq 'pass';
	$chdel = $text if $key eq 'chdel';
	}

#環境変数取得
$ip = $ENV{'REMOTE_ADDR'};
$host = gethostbyaddr(pack("C4", split(/\./, $ip)), 2);
$host ||= $ENV{'REMOTE_HOST'};
$host ||= $ip;
$referer=$ENV{'HTTP_REFERER'};
$script=$ENV{'SCRIPT_NAME'};

#アクセス拒否チェック
foreach (@denyhost){
	if ($host =~ /$_/i){
		&error("あなたの使用しているホストからのアクセスは禁止されています。");
		last;
		}
	}

#データチェック
$page||=0;

if ($act eq "write"){
	$a1 = $msg;
	$a1 =~ s/[\r\n\t]//g;
	$act = "" if $a1 eq "";
	}

#idの値で命令分岐

if ($act eq "delete"){&delete;}

#クッキー取得
for $xx (split(/; */, $ENV{'HTTP_COOKIE'})) {
	($chname, $value) = split(/=/, $xx);
	$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
	$cookie{$chname} = $value;
	}
$name||=$cookie{'name'};
$email||=$cookie{'email'};
$url||=$cookie{'url'};
$delkey||=$cookie{'delkey'};

$name||=$newname;
$subject||=$newsubject;

@log=();
$nextflag = 0;
$prevflag = 1 if $page != 0;
if ($act eq "write"){
	&error("名前を入力してください。") if $name eq "";
	&error("題名を入力してください。") if $subject eq "";
	&error("別ページからの投稿は禁止されています。") if ($referercheck == 1) && ($referer !~ /$script/i);
	while(1){if (!(chomp($msg))){last;}}

	#許可タグ以外を無効にする
	$msg =~ s/[\t\a]//g;
	$msg =~ s/&/&amp;/g;
	$msg =~ s/</\t/g;
	$msg =~ s/>/\a/g;
	foreach (@permittag){
		$msg =~ s/\t(\/?$_)\a/<$1>/ig;
		$msg =~ s/\t$_ ([^\a]*)\a/<$_ $1>/ig;
		}
	$msg =~ s/\t/&lt;/g;
	$msg =~ s/\a/&gt;/g;
	$msg =~ s/&amp;/&/g;

	foreach (@permittag){
	if (($msg =~ /<$_/i) && ($msg !~ /<\/$_/i)){$msg .="<\/$_>";}
		}

	#URLには自動的にリンクを行う
	if (($msg !~ /<img/i) && ($autolink)){
		$msg =~ s/(http:\/\/[a-zA-Z0-9\.\/\-+#_?~&%=^\@:;]+)/<A HREF="$1">$1<\/A>/ig;
		}
	$msg =~ s/\n/<br>/g;
	$subject =~ s/</&lt;/g;
	$subject =~ s/>/&gt;/g;
	if ($url eq "http://"){$url = "";}

	#ファイル読みこみ
	open (IO,"+<$logfile");
	eval{flock(IO,2)};
	@log = <IO>;
	@y2 = split(/<>/,$log[0]);
	#二重書きこみの禁止
	if (($double == 1) && ($msg eq $y2[7])){close(IO);&error("二重投稿は禁止されています。");}

	#ログ追加
	$y2[0]++;
	unshift(@log,"$y2[0]<>$name<>$email<>$url<>" . time() . "<>$delkey<>$subject<>$msg<>$ip/$host<>\n");
	pop(@log) if $#log >= $maxlog;

	#書きこみ
	truncate(IO,0);
	seek(IO,0,0);
	print IO @log;
	close(IO);

	if ($log[$maxpage] ne ""){$nextflag = 1;}
	}else{
	#必要な部分だけログ読み
	open (IN,"$logfile");
	eval{flock(IN,1)};
	for (1 .. $page*$maxpage){
		$a1=<IN>;
		}
	for (1 .. $maxpage+1){
		$a1=<IN>;
		push(@log,$a1);
		}
	if ($log[$#log] ne ""){$nextflag = 1;}
	close (IN);
	}

#クッキー書きこみ
print "Set-Cookie:name=$name; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
print "Set-Cookie:email=$email; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
print "Set-Cookie:url=$url; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
print "Set-Cookie:delkey=$delkey; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";

&hphead;

#ここでメッセージ入力フォームを表示しています。
# formタグ・inputタグ・textareaタグは基本的には変更しないでください。
# inputタグのsize・textareaタグのcols/rowsは変更してもOKです。

print <<EOD;
<form method="post" action="./gnbbs.cgi">
<table border="0" align="center" cellspacing="0" cellpadding="5">
<tr bgcolor=$entercl1><td align="right">名前 : <input type="text" class="input" name="name" size="20" value="$name">&nbsp;</td></tr>
<tr bgcolor=$entercl2><td align="right">E-Mail : <input type="text" class="input" name="email" size="20" value="$email">&nbsp;</td></tr>
<tr bgcolor=$entercl3><td align="right">URL : <input type="text" class="input" name="url" size="20" value="$url">&nbsp;</td></tr>
<tr bgcolor=$entercl4><td align="left">&nbsp;件名 : <input type="text" class="input" name="subject" size="30">&nbsp;</td></tr>
<tr bgcolor=$entercl5><td align="left">&nbsp;内容 : <br>
&nbsp;<textarea name="msg" class="input" cols="50" rows="6"></textarea>&nbsp;</th></tr>
<tr bgcolor=$entercl6><td align="left">&nbsp;削除キー : <input type="password" class="input" name="delkey" size="10" value="$delkey"></td></tr>
<tr bgcolor=$entercl6><td align="center"><input type="submit" class="button" value="送信"><input type="reset" class="button" value="中止"></td></tr>
</table>
<input type="hidden" name="act" value="write">
<input type="hidden" name="page" value="0">
</form>
EOD
#ここまで

if ($homeback ne ""){
	print "<div align=\"center\"><a href=\"$homeback\">&lt;&lt;Back To Home</a></div>\n";
	}
print "<br><br>";


#記事表示
for (0 .. $maxpage-1){
	last if $log[$_] eq "";
	@y2 = split(/<>/,$log[$_]);

	#時間形式
	($sec,$min,$hour,$day,$month,$year,$week) = gmtime($areatime+$y2[4]);
	$month++;
	$year += 1900;
	if (($spzero[4] == 1) && ($sec < 10)){$sec="0$sec";}
	if (($spzero[3] == 1) && ($min < 10)){$min="0$min";}
	if (($spzero[2] == 1) && ($hour < 10)){$hour="0$hour";}
	if (($spzero[1] == 1) && ($month < 10)){$month ="0$month";}
	if (($spzero[0] == 1) && ($day < 10)){$day ="0$day";}
	$week=$weekday[$week];
	&timeset;

	$a1 = "";
	if ($y2[2] ne ""){
		$a1 = "[<a href=\"mailto:$y2[2]\">Mail</a>]";
		}
	if ($y2[3] ne ""){
		$a1 .= "[<a href=\"$y2[3]\" target=\"_blank\">HomePage</a>]";
		}
	if ($a1 ne ""){$a1="&nbsp;$a1";}

	if ($ipindicate == 1){$y2[7].="\n<!--$y2[8]-->\n";}

	#ここで記事を表示します。
	#タグが入り組んでいるので、出力されるHTMLをよくご覧ください。
	#
	#☆変数説明☆
	# $msgcl1~4	メッセージ背景色（冒頭で設定）
	# $y2[0]	記事番号
	# $y2[1]	投稿者名
	# $y2[2]	メールアドレス
	# $y2[3]	ホームページURL
	# $y2[6]	題名
	# $y2[7]	本文
	# $y2[8]	IP/ホスト名
	# $a1		メール・ホームページのリンク
	# $timeword	投稿時間

print <<EOD;
<table width="550px" border="0" align="center" cellspacing="0" cellpadding="5">
<tr><td bgcolor="$msgcl1" align="left">
&nbsp;<b>[$y2[0]]$y2[6]</b>
</td></tr>
<tr><td bgcolor="$msgcl2" align="right">
<b>$y2[1]</b>$a1&nbsp;
</td></tr>
<tr><td bgcolor="$msgcl3" align="right">
$timeword&nbsp;</td></tr>
<tr><td bgcolor="$msgcl4" align="center">
<table width="98%">
<tr><td align="left" bgcolor="#ffffff">
$y2[7]
</td></tr>
</table>
</td></tr>
</table>
<br>
EOD
	#ここまで
	}

#NEXT/BACKのボタン表示
print "<table border=0 align=center><tr>";
if ($prevflag == 1){
	$a1 = $page-1;
print <<EOD;
<td>
<form method="post" action="./gnbbs.cgi">
<input type="hidden" name="page" value="$a1">
<input type="submit" class="button" value="Prev">
</form>
</td>
EOD
	}
if ($nextflag == 1){
	$a1 = $page+1;
print <<EOD;
<td>
<form method="post" action="./gnbbs.cgi">
<input type="hidden" name="page" value="$a1">
<input type="submit" class="button" value="Next">
</form>
</td>
EOD
	}


#削除フォーム表示
print <<EOD;
</tr>
</table>
<table align=center>
<form method="post" action="./gnbbs.cgi">
<tr><td bgcolor=$msgcl1 align=center>
記事番号：<input type="text" class="input" name="chdel" size=4>
削除キー：<input type="password" class="input" name="pass" size=9>
</td>
</tr>
<tr>
<td bgcolor=$msgcl2 align=center>
<input type="submit" class="button" value="記事削除">
<input type="hidden" name="act" value="delete">
</td>
</tr>
</form>
</table>
EOD

&hpfoot;
#******************************************************************************
sub delete{
#記事削除

#入力データチェック
&error("記事番号を指定してください。") if ($chdel eq "") || ($chdel =~/[a-zA-Z]/);
&error("削除キーを入力してください。") if $pass eq "";

#削除
my $errmsg = "削除キーが間違っています。";
my $i;
open (IO,"+<$logfile");
eval{flock(IO,2)};
@log = <IO>;
for ($i=0;$i<=$#log;$i++){
	@y2 = split(/<>/,$log[$i]);
	if (($y2[0] eq $chdel) && ($y2[5] eq $pass)){
		splice(@log,$i,1);
		$errmsg = "";
		last;
		}
	elsif(($y2[0] eq $chdel) && ($pass eq $adminpass)){
		splice(@log,$i,1);
		$errmsg = "";
		last;
		}
	}
if ($errmsg eq ""){
	truncate(IO,0);
	seek(IO,0,0);
	print IO @log;
	close (IO);
	$errmsg = "$chdel番の記事を削除しました。";
	}

#表示
&error($errmsg);
}

#******************************************************************************
sub error{
#エラー表示
&hphead;
print <<EOD;
<div align=center>
<br><br><br>
<b>$_[0]</b>
<br><br><br>
<a href="./gnbbs.cgi">戻る</a>
<br><br><br><br>
</div>
EOD
&hpfoot;
}
#******************************************************************************
sub hphead{
#ヘッダ表示
print "Content-type: text/html; charset=shift_jis\n\n";
print <<EOD;
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="pragma" content="no-cache">
<title>$title</title>
$sheet
</head>
$bodytag
$pagetop
EOD
}
#******************************************************************************
sub hpfoot{
#フッタ表示
#
#著作権表示を消すことを禁じます。
print <<EOD;
<br><br>
<div align=center><a href="http://dream.lib.net/room/" target="_blank">General BBS by The Room</a></div>
<br>
</body>
</html>
EOD
exit;
}
#******************************************************************************
