#!/usr/local/bin/perl
#-----------------------------------------------------------------------------#
#	トピックス生成用ＣＧＩ
#	トピックス形式のデータを表現する
#	create by Yuji Tominaga
#	
#	Version 3.1.4
#	2002-12-02:	編集後に順番が変わるバグを修正	
#       2002-11-30:     編集画面を修正
#	
#	version 3.1.3
#	2002-11-7:	コメントに,を入れると表示されなくなるバグを修正
#	2002-9-8:	何も入力されていないときに送信するとエラーになるようにした
#	2002-9-6:	メニュー画面の分離
#	
#	version 3.1.2
#	2002-9-6:	画像操作plの導入、実装
#	2002-9-6:	インターフェイスの変更・改良
#	2002-8-19:	画像アップ実装
#	2002-8-3:	リセット後自動的にパーミッションを変更
#	2002-8-3:	Ｆ５モード（リセットコマンド）完成
#	2002-8-3:	編集終了後の戻り先を追加、編集、削除の分岐点まで戻ることにした
#	2002-8-2:	リセットコマンドmode=5を設置
#	2002-8-2:	表示方式の変更
#	2002-8-1:	基本構成完了
#
###############################################################################
#
#	設置方法
#
#	
#	$logPath	ログファイルへのパスです。ルートにファイルを置きましょう。
#	$htmlPath	リンク元のＨＴＭＬファイルへのパスです。ルートにファイル
#				を置きましょう。
#	$commentPath	コメント出力時にひな形となるＨＴＭＬファイルへのパス
#					です。ルートに置きましょう。
#
#	以上のファイルは全てパーミッション666に指定してください。
#
#	topics.cgi
#	passCheck.cgi
#	は、パーミッション755
#
#	log.pl
#	jcode.pl
#	は、パーミッション644でかまいません
#
#
#	ＨＴＭＬファイルの設定の仕方は、サンプルのＨＴＭＬファイルを参考にして
#	ください。
###############################################################################
#
#
#
#	This program is free software; you can redistribute it and/or
#	modify it under the terms of the GNU General Public License
#	as published by the Free Software Foundation; either version 2
#	of the License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307,
#	USA.
#
#	Also add information on how to contact you by electronic and paper mail. 
#
#	If the program is interactive, make it output a short notice like this 
#	when it starts in an interactive mode: 
#
#	Gnomovision version 69, Copyright (C) year name of author
#	Gnomovision comes with ABSOLUTELY NO WARRANTY; for details
#	type `show w'.  This is free software, and you are welcome
#	to redistribute it under certain conditions; type `show c' 
#	for details.
#
#	The hypothetical commands `show w' and `show c' should show the 
#	appropriate parts of the General Public License. Of course, the 
#	commands you use may be called something other than `show w' and 
#	`show c'; they could even be mouse-clicks or menu items--whatever suits
#	your program. 
#
#	You should also get your employer (if you work as a programmer) or your
#	school, if any, to sign a "copyright disclaimer" for the program, if 
#	necessary. Here is a sample; alter the names: 
#
#	Yoyodyne, Inc., hereby disclaims all copyright
#	interest in the program `Gnomovision'
#	(which makes passes at compilers) written 
#	by James Hacker.
#
#	signature of Ty Coon, 1 April 1989
#	Ty Coon, President of Vice
#
#	This General Public License does not permit incorporating your program 
#	into proprietary programs. If your program is a subroutine library, you 
#	may consider it more useful to permit linking proprietary applications 
#	with the library. If this is what you want to do, use the GNU Library 
#	General Public License instead of this License. 
#-----------------------------------------------------------------------------#


######################################################
###	環境設定
###	CGIの環境を設定します
###	基本的な設定はこの部分だけで終了します

my $logPath		= "../logfile.csv";								#ログデータへのパス
my $htmlPath	= "../katudo.html";								#トップページのスキン
my $commentPath	= "../comment.html"; 							#内容表示用のスキン
my $upload_dir	= "../image";									#ファイルのアップロード先
my $htmlOutPath	= "../index.html";								#トップ出力データ
my $outDir		= "../";										#ファイルの出力位置
my $outImageDir = "image";										#イメージファイルの出力先


my $maxWidth	= "200";										#最大表示幅
my $maxHeight	= "200";										#最大表示高さ

######################################################


#外部モジュールの読み込み
require './jcode.pl';
require './log.pl';
require 'bimage.pl';

use CGI;

$query	= new CGI;

#各種処理
if($query->param('mode') eq '0'){
	&inputScreen;	
}elsif($query->param('mode') eq '1'){
	&editData;
	&showend;
}elsif($query->param('mode') eq '2'){
	&deleteScreen;
}elsif($query->param('mode') eq '3'){
	&deleteData;
	&showend;
}elsif($query->param('mode') eq '4'){
	&selectScreen;
}elsif($query->param('mode') eq '5'){
	&upDate;
	$showend;
}elsif($query->param('mode') eq '6'){
	&editScreen;
}elsif($query->param('mode') eq '7'){
	&editComment;
	&showend;
}elsif($query->param('mode') eq '8'){
	&addCommentScreen;	
}elsif($query->param('mode') eq '9'){
	&addCommentEdit;
	&showend;
}elsif($query->param('mode') eq '10'){
	&deleteComment;
	&showend;
}



#######################################################
#	inputScreen()
#	大見出し入力画面
sub inputScreen
{
	my($sec, $min, $hour, $mday, $mon, $year)	= localtime();			#ローカルタイムの取得
	$year	= $year + 1900;												#年の計算
	$mon	= $mon  + 1;												#月の計算
	
	#入力フォームの表示
print <<HTML_HEAD;
Content-type: text/html


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>入力フォーム</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META http-equiv="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
TD{
font-size : 14px;
}
-->
</STYLE>
</HEAD>

<BODY>
	<TABLE width="100%" height="100%">
	<TBODY>
		<TR>
			<TD align="center" valign="middle">
				<FORM action="topics.cgi" method="POST"><INPUT type="hidden" name="mode" value="1">
				<TABLE width="400" bgcolor="#ffd668" cellspacing="1" cellpadding="5">
				<TBODY>
					<TR>
						<TD align="center" style="font-weight : bold;color : #ff6f6f;">トピックの入力</TD>
					</TR>
					<TR>
						<TD bgcolor="#ffffff" align="center"><BR>
HTML_HEAD

print "<form action=\"topics.cgi\" method=\"POST\">\n";
print "日付：<input type=\"text\" name=\"year\" value=\"$year\">年";
print "<select name=\"month\">"; 
for(my $i = 1; $i <= 12; $i++){
	if($i eq "$mon"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>月\n";
print "<select name=\"day\">";
for(my $i = 1; $i <= 31; $i++){
	if($i eq "$mday"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>日<br><br>\n";
print "<div align=\"left\">　　　　タイトル：<input type=\"text\" name=\"title\" size=\"50\"></div><br>";
print "<div align=\"left\">　　本文:</div>\n";
print "<textarea name=\"comment\" rows=\"7\" cols=\"50\" maxlength=\"50\"></textarea><br><br>\n";
print "<input type=\"submit\" value=\"　送　信　\">　<input type=\"reset\" value=\"　取　消　\"><br><br>\n";
print "</form>\n";

print <<HTML_FUT;
						</TD>
					</TR>
				</TBODY>
				</TABLE>
				<BR>
				<A href="$home">戻る</A></FORM>
			</TD>
		</TR>
		<TR>
		<TD></TD>
		</TR>
	</TBODY>
	</TABLE>
</BODY>
</HTML>
HTML_FUT

}



#######################################################
#	editData()
#	入力されたデータを編集して保存
sub editData
{
	#トピックス管理用IDの生成
	my @key		= localtime();
	my $key		= sprintf("%02d%02d%02d%02d%02d",$key[4]+1,$key[3],$key[2],$key[1],$key[0]);
	my $id		= $key;									#生成されたID
	my $year	= $query->param('year');				#年
	my $month	= $query->param('month');				#月
	my $day		= $query->param('day');					#日
	my $date	= "$year年$month月$day日";				#日付データ
	
	#エラーチェック
	#本文の入力データをチェックする
	if($query->param('title') eq "" and $query->param('comment') eq ""){
		&errorOut("記事に何も入力されていません。<br>\nタイトルとコメントの入力は必須です<br>\n");
		exit;
	}

	my $title	= $query->param('title');				#タイトル
	$title		=~ s/,/，/g;							#入っている半角カンマを全て全角に
	my $comment	= $query->param('comment');				#コメント
	$comment	=~ s/,/，/g;							#コメントに入っている半角カンマを全て全角に
	my @commentData	= &log::openFile("$commentPath");	#コメント出力用ファイルへのパス
	$comment	=~ s/\r\n/<br>/g;						#改行コードを<br>タグに変更
	$comment	.= "\n";								#最後に改行コードを１つだけ追加
	my $outLog	= "$id,$date,$title,$comment";			#出力用ログデータの作成
	my $outFileName	= "../$id.html";					#出力ファイルのファイル名
	my $dataFlag	= 0;								#処理識別フラグ
		
	#ログデータの書き込み
	&log::writeLog("$logPath","$outLog");
	&convert;											#新しいデータを追加する
	
	#データの結合pert2
	#本文の出力
	foreach $line (@commentData){
		my $buf = $line;
		if($buf =~ /<!--start1-->/ or $buf =~ /<!--start2-->/){
			$dataFlag = 1;
		}elsif($buf =~ /<!--end1-->/ or $buf =~ /<!--end2-->/){
			$dataFlag = 0;
		}

		#出力画面の合成
		if($dataFlag != 1){
			if($line =~ /<!--date-->/){
				$line =~ s/<!--date-->/$date/;
				$outComment	= "$outComment$line";
			}elsif($line =~ /<!--title-->/){
				$line =~ s/<!--title-->/$title/;
				$outComment = "$outComment$line";
			}elsif($line =~ /<!--comment-->/){
				$line =~ s/<!--comment-->/$comment/;
				$outComment	= "$outComment$line";
			}else{
				$outComment = "$outComment$line";
			}
		}
	}
	
	&log::writeFile("$outFileName","$outComment");
	chmod 666,"$outFileName";
}



#######################################################
##	showend()
##	編集完了の表示
sub showend
{
#終了画面描画
print <<EOH;
Content-type: text/html\n\n

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>登録完了</title>
</head>
<body>
<TABLE width="100%" height="100%" cellpadding="0" cellspacing="0">
  <TBODY>
    <TR><TD>
<div align="center">
<font color="#ff8080">登録完了しました</font><br><br>
トピックスのトップページを開き<br>更新ボタンを押して正しく追加できている<br>
ことを確認してください<br><br>
EOH

print "<a href=\"$htmlOutPath\">ホームページを見る</a><br>\n";
print "（必ず更新ボタンを押してください）<br><br>\n";
print "<a href=\"menu.html\">編集に戻る</a>\n";
print <<EOD;

</TD>
</div>
    </TR>
  </TBODY>
</TABLE>
</body>
</html>
EOD
	
}



#######################################################
##	convert()
##	データ形式を変換
sub convert
{
	local @htmlData		= &log::openFile("$htmlPath");		#ＨＴＭＬのスキンデータ
	local @logData		= &log::openFile("$logPath");		#ログファイルのデータ
	local $outHtml;											#出力用のＨＴＭＬデータ(タイトル表示)
	local $outComment;										#出力用のＨＴＭＬデータ(本文表示)
	local $outFileName;										#出力ファイル名
	local $flag		= '1';									#処理用フラグ
	local @dataBuf;											#データの仮保存域
	local $html1,$html2,$html3;								#ＨＴＭＬデータのヘッダ、フッタ、本文
	local $id,$date,$title,$comment;						#ログデータの切り出し
	local $syoriFlag	= 'true';
		
	#データを反転させる
	@logData	= reverse @logData;
		
	#データの結合(以前のデータと新規のデータを組み合わせる
	#タイトル出力の作成
	#(今後変更する際はこのあたりを変更する)
	foreach $line (@htmlData){
		if($line =~ /<!--start-->/){
			$flag	= '2';
		}elsif($line =~ /<!--end-->/){
			$flag	= '3';
		}
		if($flag eq '1'){
			$html1 .= "$line";
		}
		if($flag eq '2'){
			push(@dataBuf,$line);
		}
		if($flag eq '3'){
			$html3 .= "$line";
		}
	}
	
	
	#ログデータとスキンの合成
	foreach $line (@logData){
		unless($line =~ m/\+/){
			($id, $date, $title, $comment)	= split(/,/, "$line");
			$outFilePath	= "$id.html";
			foreach $data (@dataBuf){
				$buf	= $data;
				$buf	=~ s/<!--title-->/<a href="$outFilePath">$title<\/a>/;
				$buf	=~ s/<!--date-->/$date/;
				$html2	= "$html2<!--$id-->$buf";
			}
		}
	}
	
	$outHtml	= "$html1$html2$html3";

	&log::writeFile("$htmlOutPath","$outHtml");
	chmod 666, "$htmlOutPath";
}


#######################################################
##	deleteScreen()
##	データ削除処理画面
sub deleteScreen
{
	my @logData				= &log::openFile("$logPath");						#ログファイルを開く		
	
	#削除処理用フォーム
print <<HTML_HEAD;
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>削除フォーム</title>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META http-equiv="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
TD{
font-size : 14px;
}
-->
</STYLE>
<script language="JavaScript">
<!--
function pageBack()
{
    history.back();
}
-->
</script>
</head>
<body>
<table border="0" width="100%" height="100%">
<tr><td align="center" valign="middle">
<div align="center">
<form action="topics.cgi" method="POST"><input type="hidden" name="mode" value="3">
<table border="0" width="500" bgcolor="#ffd668">
<tr>
	<td width="20%" style="font-weight : bold;color : #ff6f6f;" algin="center"></td><td width="30%" style="font-weight : bold;color : #ff6f6f;" algin="center">日付</td><td width="50%" style="font-weight : bold;color : #ff6f6f;" algin="center">タイトル</td>
</tr>
HTML_HEAD

#ログデータの切り出し
foreach $line (@logData){
	unless($line =~ m/\+/){
		my ($key, $hi, $dai, $com) = split(/,/, $line);
		print "<tr>\n";
		print "<td width=\"20%\" bgcolor=\"#ffffff\"><input type=\"radio\" name=\"key\" value=\"$key\"></td><td width=\"30%\" bgcolor=\"#ffffff\">$hi</td><td width=\"50%\" bgcolor=\"#ffffff\">$dai</td>\n"; 
		print "</tr>\n";
	}
}

print "<tr>\n";
print "<td colspan=\"3\" align=\"center\" bgcolor=\"#ffffff\"><input type=\"submit\" value=\"送　信\">　　　　　<input type=\"reset\" value=\"戻　る\" onClick=\"pageBack()\"></td>\n";
print <<HTML_FUT;
</table>
</form>
</div>
</td></tr>
</table>
</body>
</html>
HTML_FUT

}



#######################################################
##	deleteData()
##	でーたの削除処理
sub deleteData
{
	#エラーチェック
	#記事が選択されているかどうか
	if($query->param('key') eq ""){
		&errorOut("削除する記事が選択されていません。<br>\n削除する記事を選択してください\n");
		exit;
	}
	
	$id				= $query->param('key');				#削除するファイルのＩＤ
	my	@htmlData	= &log::openFile("$htmlOutPath");	#データファイル
	my	@logData	= &log::openFile("$logPath");		#ログファイル
	my	$outHtml,$outLog;								#出力用データ
	unlink("../$id.html");								#本文ファイルを削除する
	
		
	#削除する行の検索
	foreach $line (@htmlData){
		unless($line =~ /<!--$id-->/){
			$outHtml	= "$outHtml$line";
		}
	}
	
	#ログファイルから削除する行を検索＆削除
	foreach $line (@logData){
		unless($line =~ /$id/){
			$outLog	= "$outLog$line";
		}
	}
	
	#削除したデータを書き込む
	open OUT, ">$htmlOutPath";
	print OUT "$outHtml";
	close(OUT);
	
	open OUT, ">$logPath";
	print OUT "$outLog";
	close(OUT);
}




#######################################################
##	selectScreen()
##	データ選択画面
sub selectScreen
{
	my @logData				= &log::openFile("$logPath");						#ログファイルを開く		
	
	#記事編集選択
print <<HTML_HEAD;
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>記事選択</title>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META http-equiv="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
TD{
font-size : 14px;
}
-->
</STYLE>
</head>
<body>
<div align="center">
<table border="0" width="100%" height="100%">
<tr><td align="center" valign="middle">
<table border="0" width="500" bgcolor="#ffd668">
<tr>
	<td width="30%" style="font-weight : bold;color : #ff6f6f;" algin="center">日付</td><td width="50%" style="font-weight : bold;color : #ff6f6f;" algin="center">タイトル</td>
</tr>
HTML_HEAD

#ログデータの切り出し
foreach $line (@logData){
	unless($line =~ m/\+/){
		my ($key, $hi, $dai, $com) = split(/,/, $line);
		print "<tr>\n";
		print "<td width=\"30%\" bgcolor=\"#ffffff\">$hi</td><td width=\"70%\" bgcolor=\"#ffffff\"><a href=\"topics.cgi?mode=6&key=$key\">$dai</a></td>\n"; 
		print "</tr>\n";
	}
}

print "<tr>\n";
print "<td colspan=\"3\" align=\"center\" bgcolor=\"#ffffff\"><a href=\"javascript:history.back()\">戻　る</a></td>\n";
print <<HTML_FUT;
</table>
</td></tr>
</table>
</form>
</div>
</body>
</html>
HTML_FUT
	
}

#######################################################
##	editScreen()
##	データ編集用画面
sub editScreen
{
		
	my @logData		= &log::openFile("$logPath");
	my $key			= $query->param('key');
	
	if($key eq ""){
		&errorOut("編集するトピックが選択されていません");
		exit;
	}
	
	my ($id,$date,$title,$comment,@minComments);
	my ($year,$mon,$mday);
	
	foreach $line (@logData){
		if($line =~ m/$key/){
			if($line =~ m/\+/){
				push(@minComments,$line);
			}else{
				($id, $date, $title, $comment) = split(/,/,"$line");
			}
		}
	}
	
	$comment =~ s/<br>/\n/g;	
	($year,$buf)	= split(/年/,"$date");
	($mon,$buf)		= split(/月/,"$buf");
	($mday,$buf)	= split(/日/,"$buf");
	

print <<HTML_HEAD;
Content-type: text/html


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>入力フォーム</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META http-equiv="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
TD{
font-size : 14px;
}
-->
</STYLE>
</HEAD>

<BODY>
	<TABLE width="100%" height="100%">
	<TBODY>
		<TR>
			<TD align="center" valign="middle" colspan="2">
				<FORM action="topics.cgi" method="POST"><INPUT type="hidden" name="mode" value="7">
				<TABLE width="400" bgcolor="#ffd668" cellspacing="1" cellpadding="5">
				<TBODY>
					<TR>
						<TD align="center" style="font-weight : bold;color : #ff6f6f;" colspan="2">トピックの入力</TD>
					</TR>
					<TR>
						<TD bgcolor="#ffffff" align="center"><BR>
HTML_HEAD


print "<form action=\"topics.cgi\" method=\"POST\">\n<input type=\"hidden\" name=\"key\" value=\"$key\">";
print "日付：<input type=\"text\" name=\"year\" value=\"$year\">年";
print "<select name=\"month\">"; 
for(my $i = 1; $i <= 12; $i++){
	if($i eq "$mon"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>月\n";
print "<select name=\"day\">";
for(my $i = 1; $i <= 31; $i++){
	if($i eq "$mday"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>日<br><br>\n";
print "<div align=\"left\">　　　　タイトル：<input type=\"text\" name=\"title\" size=\"50\" value=\"$title\"></div><br>";
print "<div align=\"left\">　　本文:</div>\n";
print "<textarea name=\"comment\" rows=\"7\" cols=\"50\" maxlength=\"50\">$comment</textarea><br><br>\n";
print "<input type=\"submit\" value=\"　送　信　\">　<input type=\"reset\" value=\"　取　消　\"><br><br>\n";
print "</form>\n";
print "</td>\n";
print "</tr>\n";
print("</tbody>\n");
print("</table>\n");
print("<br><br>\n");

#記事追加ボタン
print("<TABLE width=\"400\" height=\"50\" cellpadding=\"1\" cellspacing=\"1\">\n");
print("<TR>\n");
print("<TD valign=\"middle\" align=\"center\" bgcolor=\"#caed9a\"><br>\n");
print "<form action=\"./topics.cgi\" method=\"POST\"><input type=\"hidden\" name=\"mode\" value=\"8\"><input type=\"hidden\" name=\"key\" value=\"$key\">\n";
print "<input type=\"submit\" value=\"　記事追加　\">\n";
print "</form>\n";
print("</TD>\n");
print("</TR>\n");
print("</TABLE>\n");
print("<br><br>\n");


#詳細記事編集選択
print "<TABLE width=\"400\" bgcolor=\"#56ACE0\" cellspacing=\"1\" cellpadding=\"5\">";

foreach $line (@minComments){
	my($id,$op,$fileName,$text) = split(/,/,$line);
	
	if($fileName ne ""){
		my($act, $type, $width, $height) = &bimage::getsize("../$fileName");		#画像の幅と高さを取得
	
		#画像ファイルのチェック
		if($act eq 'f'){
			errorOut("$type");
			print("$fileName");
			exit;
		}
	
		#画像サイズのチェック
		if($width > $maxWidth and $width >= $height){
			#最大表示幅より大きかったとき
			#その比率で最大表示幅以下に納める
			$outWidth	= int($width*($maxWidth/$width));
			$outHeight 	= int($height*($maxWidth/$width));
		}elsif($height > $maxWidth and $width < $height){
			#最大表示高さより大きかったとき
			#その比率で最大表示高さ以下に納める
			$outWidth	= int($width*($maxHeight/$height));
			$outHeight	= int($height*($maxHeight/$height));
		}else{
			#最大表示以内ならそのサイズに合わせる
			$outWidth	= $width;
			$outHeight	= $height;
		}
	}
	
	$op =~ s/\+//g;
	print("<tr>\n");
	print("<td width=\"300\" bgcolor=\"#9be0ec\" align=\"center\" valign=\"middle\">\n");
	print("<img src=\"../$fileName\" width=\"$outWidth\" height=\"$outHeight\">\n");
	print("</td>\n");
	print("<td width=\"200\" bgcolor=\"#dff5f9\" valign=\"middle\">\n");
	print("$text\n");
	print("</td>\n");
	print("</tr>\n");
	print("<tr><td align=\"center\">\n");
	print("<form action=\"topics.cgi\" method=\"POST\" enctype=\"multipart/form-data\">");
	print("<input type=\"hidden\" name=\"mode\" value=\"8\">");
	print("<input type=\"hidden\" name=\"key\" value=\"$id\">\n");
	print("<input type=\"hidden\" name=\"subid\" value=\"$op\">");
	print("<input type=\"submit\" value=\"編　集\">");
	print("</form>");
	print("</td>\n");
	print("<td align=\"center\">\n");
	print("<form action=\"topics.cgi\" method=\"POST\" enctype=\"multipart/form-data\">");
	print("<input type=\"hidden\" name=\"key\" value=\"$id\">\n");
	print("<input type=\"hidden\" name=\"subid\" value=\"$op\">");
	print("<input type=\"hidden\" name=\"mode\" value=\"10\">\n");
	print("<input type=\"submit\" value=\"削　除\">\n");
	print("</form>\n");
	print("</td></tr>\n");
}

print("</table>");


print("<br>\n");
print("<A href=\"$home\">戻る</A></FORM>\n");
print("</TD>\n");
print("</tr>\n");
print("<tr>\n");
print("<td></td>\n");
print("</tr>\n");
print("</TBODY>\n");
print("</TABLE>\n");
print("</BODY>\n");
print("</HTML>\n");

}



#######################################################
##	addCommentScreen
##	画像＆コメントの追加を行います。
sub addCommentScreen
{
	my $id		= $query->param('key');
	my $subid	= $query->param('subid');
	my $text	= "";
	my $baseName= "";
	@logData	= &log::openFile("$logPath");
	@outData	= ();
	
	#データの切り出し
	if($subid ne ""){
		foreach (@logData){
			if($_ =~ /$id/ and $_ =~ /\+$subid/){
				my($a, $b) = ();
				($a, $b, $baseName, $text) = split(/,/,$_);
				$text =~ s/<br>/\r\n/g;
			}
		}	
	}
	
	if($baseName ne ""){
		my($act, $type, $width, $height) = &bimage::getsize("../$baseName");
	
		#画像サイズのチェック
		if($width > $maxWidth and $width >= $height){
			#最大表示幅より大きかったとき
			#その比率で最大表示幅以下に納める
			$outWidth	= int($width*($maxWidth/$width));
			$outHeight 	= int($height*($maxWidth/$width));
		}elsif($height > $maxWidth and $width < $height){
			#最大表示高さより大きかったとき
			#その比率で最大表示高さ以下に納める
			$outWidth	= int($width*($maxHeight/$height));
			$outHeight	= int($height*($maxHeight/$height));
		}else{
			#最大表示以内ならそのサイズに合わせる
			$outWidth	= $width;
			$outHeight	= $height;
		}
	}
	
#画像＆コメント追加画面表示
print <<HTML_HEAD;
Content-type: text/html


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>コメント編集フォーム</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META http-equiv="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
TD{
font-size : 14px;
}
-->
</STYLE>
</HEAD>

<BODY>
	<TABLE width="100%" height="100%">
	<TBODY>
		<TR>
			<TD align="center" valign="middle">
				<FORM action="topics.cgi" method="POST" ENCTYPE="multipart/form-data"><INPUT type="hidden" name="mode" value="9">
HTML_HEAD

print "<input type=\"hidden\" name=\"key\" value=\"$id\">\n";
print("<input type=\"hidden\" name=\"subkey\" value=\"$subid\">\n");

print <<HTML_FUT;
				<TABLE width="400" bgcolor="#ffd668" cellspacing="1" cellpadding="5">
				<TBODY>
					<TR>
						<TD align="center" style="font-weight : bold;color : #ff6f6f;">画像＆コメント追加</TD>
					</TR>
					
HTML_FUT

if($baseName ne ""){
	print("<tr><td bgcolor=\"#ffffff\">\n");
	print("<img src=\"../$baseName\" width=\"$outWidth\" height=\"$outHeight\">\n");
	print("</td></tr>\n");
	print("<input type=\"hidden\" name=\"upfile2\" value=\"$baseName\">\n");
}

print('<tr><td bgcolor="#ffffff">コメント<br>'."\n");
print('<textarea name="comment" cols="40" rows="4">'."$text".'</textarea>'."\n");

print <<HTML_FUT2;
						</td>
					</tr>
					<tr>
						<td bgcolor="#ffffff">
							画像ファイル<input type="file" name="upfile" value="参　照">
						</td>
					</tr>
					<tr>
						<td align="center" bgcolor="#ffffff">
							<input type="submit" value="送　 信">　　　<input type="reset" value="取　消">
						</td>
					</tr>
				</tbody>
				</table>
				</form>
			</td>
		</tr>
	</tbody>
	</table>
</body>
</html>
HTML_FUT2

}


#######################################################
##	addCommentEdit()
##	入力された画像＆コメントデータを編集する
sub addCommentEdit
{
	my $fileName	= $query->param('upfile');					#取り込んだファイルパス
	my $textData	= $query->param('comment');					#取り込んだコメント
	$textData		=~ s/,/，/g;								#コメントに入っている半角カンマを全て全角に
	$textData		=~ s/\r\n/<br>/g;							#改行を<br>に変換
	my $id			= $query->param('key');						#親記事のキーコード
	my $sub			= $query->param('subkey');					#サブキーのコード
	my @buf			= ();										#ファイルパスの分割保存
	if($fileName ne ""){
		@buf			= split(/\\/,$fileName);
	}
	
	my $baseName	= "";										#ファイル名の取得
	my $readBuf		= "";										#一時保存用領域
	my ($buffer,$dataSize) = ();								#利用する変数名
	my $type		= "";										#ファイルタイプ識別用
	my $outData		= "";										#出力データ
	my $outLogData	= "";										#出力ログデータ
	
	#初期化
	$dataSize		= 1024;										#一度に取り込むサイズ
	
	if($fileName eq "" and $query->param('upfile2') eq "" and $textData eq ""){
		errorOut("何も入力されていません。<br>コメント又は画像どちらかは必ず入力してください。<br>\n");
		exit;
	}
	
	if($fileName eq "" and $query->param('upfile2') ne ""){
		$baseName = $query->param('upfile2');
		my $a = "";
		($a,$baseName) = split(/\//,$baseName);
	}else{
		$baseName = $buf[$#buf];
	}
	
	#ファイル名が空じゃないとき
	#ファイルの転送を開始する
	if($fileName ne "" and $baseName ne ""){
		$type = $query->uploadInfo($fileName)->{'Content-type'};	#ファイルの種類を取得
		
		#ファイル形式取得に失敗しているときは拡張子から判別する
		if($type eq ""){
			($readBuf,$type) = split(/\./,$baseName);
		}
		
		#jpegとgifはアップロードを許可します
		if($type eq "jpeg" or $type eq "gif" or $type eq "jpg"){
			
			#ファイルのデータをコピーする
			while($readBuf = read($fileName, $buffer, $dataSize)){
				$outData .= $buffer;
			}
		
			#ファイルの書き込み
			open(OUTFILE, ">../$outImageDir/$baseName");
			binmode(OUTFILE);
			print(OUTFILE "$outData");
			close(OUTFILE);
			chmod(666,"$outImageDir/$baseName");
		}else{
			#ファイル形式に対応していないとき
			&errorOut("転送できないファイル形式でした。");
			exit;
		}
	}
	
	#出力ログデータの作成
	if($sub ne ""){
		$subid = "$sub";
	}
	
	if($baseName eq ""){
		$outLogData = "$id,\+$subid,,$textData\n";
	}else{
		$outLogData = "$id,\+$subid,$outImageDir\/$baseName,$textData\n";
	}
	@buf = &log::openFile("$logPath");
	my @data = ();

	#デバッグ出力
	if($sub ne ""){
		foreach (@buf){
			unless($_ =~ /$id/){
				push(@data, $_);
			}else{
				unless($_ =~ /\+$sub/){
					push(@data, $_);
				}
			}
		}
	}else{
		@data = @buf;
	}
	
	push(@data, $outLogData);
	@data = sort(@data);
	
	#ログデータの書き込み
	open(OUTFILE, ">$logPath");
	foreach (@data){
		print(OUTFILE "$_");
	}
	close(OUTFILE);
	chmod(666,"$logPath");
	
	&convert2;
}

#######################################################
##	convert2()
##	データ出力用変換処理
sub convert2
{
	my $key			= $query->param('key');
	my @commentData	= &log::openFile("$commentPath");			#出力用スキンファイルのデータ
	my @logData		= &log::openFile("$logPath");				#ログファイルのデータ
	my $flag		= '0';										#動作制御用フラグ
	my $leftorright	= '0';										#左右振り分けようのフラグ
											
	my $html1 = "";												#htmlのフッタ情報を保存する変数
	my $outHtmlData = "";										#出力用データファイル
	my (@htmlHead, @htmlBody1, @htmlBody2);						#スキンファイルの分割用領域
	my @outData = ();											#出力データ
	
	#スキンデータの加工	
	foreach (@commentData){
		#切り取り制御
		if($_ =~ m/<!--start1-->/ and $flag ne '1'){
			$flag = '1';										#body1の切り出し
		}
		if($_ =~ m/<!--end1-->/ and $flag eq '1'){
			$flag = '0';										#body1の切り出し終了
		}
		if($_ =~ m/<!--start2-->/ and $flag ne '2'){
			$flag = '2';										#body2の切り出し
		}
		if($_ =~ m/<!--end2-->/ and $flag eq '2'){
			$flag = '3';										#body2の切り出し終了
		}
		
		#データの保存
		if($flag eq '1'){
			unless($_ =~ m/<!--start1-->/){
				push(@htmlBody1,"$_");
			}
		}elsif($flag eq '2'){
			unless($_ =~ m/<!--start2-->/){
				push(@htmlBody2,"$_");
			}
		}elsif($flag eq '3'){
			$html1 .= "$_";
		}else{
			push(@htmlHead,"$_");
		}
	}
	
	
	#データの合成
	foreach $data (@logData){
		if($data =~ m/$key/){
			unless($data =~ m/\+/){
				#ヘッダ部分の合成
				foreach $line (@htmlHead){
					my($id,$date,$title,$comment) = split(/,/,$data);
					my $buf = $line;
					$buf =~ s/<!--title-->/$title/g;						#titleの書き込み
					$buf =~ s/<!--date-->/$date/g;							#日付の書き込み
					$buf =~ s/<!--comment-->/$comment/g;					#コメントの書き込み
					$outHtmlData .= "$buf";									#データを格納する
				}
			}else{
				my($id,$op,$fileName,$text) = split(/,/,$data);
				if(@htmlBody2 eq "" || $leftorright eq '0'){
					#body1の合成
					foreach $line (@htmlBody1){
						my $buf = $line;
						
						if($fileName ne ""){
							#ファイルサイズのチェック
							my($act, $type, $width, $height) = &bimage::getsize("../$fileName");
						
							#画像サイズのチェック
							if($width > $maxWidth and $width >= $height){
								#最大表示幅より大きかったとき
								#その比率で最大表示幅以下に納める
								$outWidth	= int($width*($maxWidth/$width));
								$outHeight 	= int($height*($maxWidth/$width));
							}elsif($height > $maxWidth and $width < $height){
								#最大表示高さより大きかったとき
								#その比率で最大表示高さ以下に納める
								$outWidth	= int($width*($maxHeight/$height));
								$outHeight	= int($height*($maxHeight/$height));
							}else{
								#最大表示以内ならそのサイズに合わせる
								$outWidth	= $width;
								$outHeight	= $height;
							}
						
							$buf =~ s/<!--image-->/<img src="$fileName" width="$outWidth" height="$outHeight">/g;	#画像データの埋め込み
						}
						$buf =~ s/<!--text-->/$text/g;					#小コメントを書き込み
							push(@outData,$buf);							#データの格納
							$leftorright = '1';								#左右の振り分けフラグを変更	
					}
				}else{
					#body2の合成
					foreach $line (@htmlBody2){
						my $buf = $line;
				
						if($fileName ne ""){
							#ファイルサイズのチェック
							my($act, $type, $width, $height) = &bimage::getsize("../$fileName");
						
							#画像サイズのチェック
							if($width > $maxWidth and $width >= $height){
								#最大表示幅より大きかったとき
								#その比率で最大表示幅以下に納める
								$outWidth	= int($width*($maxWidth/$width));
								$outHeight 	= int($height*($maxWidth/$width));
							}elsif($height > $maxWidth and $width < $height){
								#最大表示高さより大きかったとき
								#その比率で最大表示高さ以下に納める
								$outWidth	= int($width*($maxHeight/$height));
								$outHeight	= int($height*($maxHeight/$height));
							}else{
								#最大表示以内ならそのサイズに合わせる
								$outWidth	= $width;
								$outHeight	= $height;
							}
						
							$buf =~ s/<!--image-->/<img src="$fileName" width="$outWidth" height="$outHeight">/g;	#画像データの埋め込み
						}
						$buf =~ s/<!--text-->/$text/g;						#小コメントを書き込み
						push(@outData,$buf);								#データを格納
						$leftorright = '0';									#左右振り分けフラグの変更
					}
				}
			}
		}
	}
	
	#htmlデータの作成
	foreach (@outData){
		$outHtmlData .= "$_";
	}
	$outHtmlData .= "$html1";												#htmlのフッタ情報を書き込み
	my $outFileName = "$outDir$key".'.html';
	
	#データの書き出し
	open(OUT, ">$outFileName");
	print OUT "$outHtmlData";
	close(OUT);
}



#######################################################
#	SdeleteComment
#	画像などの消去
sub deleteComment
{
	my $id			= $query->param('key');									#記事検索用の主キー
	my $subid		= $query->param('subid');								#subID
	my @buf			= &log::openFile("$logPath");							#ログファイルのデータ
	my @outLogData	= ();													#出力用ログデータ
		
	#ログの削除処理
	foreach (@buf){
		#IDが一致しなければ無条件に書き出し
		unless($_ =~ /$id/){
			push(@outLogData, $_);
		}else{
			#IDが一致してもsubIDが一致しなければ書き出し
			unless($_ =~ /$subid/){
				push(@outLogData, $_);
			}
		}
	}
	
	#ログデータの書き戻し
	open(OUTFILE, ">$logPath");
	foreach (@outLogData){
		print(OUTFILE "$_");
	}
	close(OUTFILE);
	
	&convert2;
}

#######################################################
#	errorOut
#	エラー出力
sub errorOut
{
	#引数の処理
	my($outMessage) = @_;
	
print <<HTML_HEAD;
Content-type: text/html\n\n

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<title>エラー</title>
</html>
<body>
<table width="100%" height="100%">
<tr><td align="center" valign="middle">
HTML_HEAD

print("$outMessage<br>\n");
print("<a href=\"./menu.html\">編集画面トップへ</a>");

print <<HTML_FUT;
</td></tr>
</table>
</html>
</body>
</html>
HTML_FUT
	
}



#######################################################
#	editComment()
#	コメントの編集
sub editComment
{
	my $id		=	$query->param('key');				#主キー
	my $year	= 	$query->param('year');				#年
	my $month	= 	$query->param('month');				#月
	my $day		= 	$query->param('day');				#日
	my $date	= 	"$year年$month月$day日";			#日付データ
	my $title	= 	$query->param('title');				#タイトル
	$title		=~	s/,/，/g;							#入っている半角カンマを全て全角に
	my $comment	= 	$query->param('comment');			#コメント
	$comment	=~ 	s/,/，/g;							#コメントに入っている半角カンマを全て全角に
	my @commentData	= 	&log::openFile("$commentPath");	#コメント出力用ファイルへのパス
	$comment	=~ 	s/\r\n/<br>/g;						#改行コードを<br>タグに変更
	$comment	.= 	"\n";								#最後に改行コードを１つだけ追加
	my $outLog	= 	"$id,$date,$title,$comment";		#出力用ログデータの作成
	my($html1,@html2,$html3) = ();						#ｈｔｍｌデータの編集作業用
	
	my @logData		= &log::openFile("$logPath");		#ログデータの取得
	my @htmlData	= &log::openFile("$htmlPath");		#スキンデータ
	
	my @outLogData	= ();								#出力データ
	my $outTopData	= '';								#トップ出力データ
	
	#ログデータからいらないデータを切り捨てる
	foreach (@logData){
		if(!($_ =~ /\+/) and $_ =~ /$id/){
			push(@outLogData,$outLog);
		}else{
			push(@outLogData,$_);
		}
	}
	
	@outLogData = sort(@outLogData);
	
	#ログデータの書き戻し
	open(OUTFILE,">$logPath");
	foreach (@outLogData){
		print(OUTFILE "$_");
	}
	close(OUTFILE);
	
	my $flag = 0;
	
	#ヘッダ・ボディー・フッタへの分割
	foreach $line (@htmlData){
		my $buf = "$line";
		
		if($buf =~ /<!--start-->/){
			$flag = 1;
		}elsif($buf =~ /<!--end-->/){
			$flag = 2;
		}
		
		if($flag == 1){
			push(@html2,$line);
		}elsif($flag == 2){
			$html3 .= "$line";
		}else{
			$html1 .= "$line";
		}
	}
	
	my $outBuf = '';
	
	foreach (@outLogData){
		unless($_ =~ /\+/){
			my($subid,$date,$title,$comment) = split(/,/,$_);
			my $outPath = "$subid.html";
			foreach $line (@html2){
				my $buf = "$line";
			
				#htmlデータを編集する
				$buf =~ s/<!--date-->/$date/;
				$buf =~ s/<!--title-->/<a href="$outPath">$title<\/a>/;
				$outBuf .= "<!--$subid-->$buf";
			}
		}
	}
	
	$outTopData = "$html1$outBuf$html3";
	
	#トップの出力データ
	unlink("$htmlOutPath");
	open(OUTFILE, ">$htmlOutPath");
	print(OUTFILE "$outTopData");
	close(OUTFILE);
	
	#出力データの変換
	&convert2;
}



#######################################################
#	upDate()
#	ファイルの全更新を行う
sub upDate
{
	my @skinData	= &log::openFile("$htmlPath");				#トップのスキンファイルを読み込む
	my @logData		= &log::openFile("$logPath");				#ログのデータ
	
	my $flag		= 0;										#制御処理フラグ
	my $buf			= '';										#一時保存領域
	my ($html1,$html3,@html2) = ();								#ヘッダなどを保存する
	my $outTopData	= '';										#トップの出力データ
	
	#ヘッダ・ボディー・フッタへの分割
	foreach $line (@skinData){
		my $buf = "$line";
		
		if($buf =~ /<!--start-->/){
			$flag = 1;
		}elsif($buf =~ /<!--end-->/){
			$flag = 2;
		}
		
		if($flag == 1){
			push(@html2,$line);
		}elsif($flag == 2){
			$html3 .= "$line";
		}else{
			$html1 .= "$line";
		}
	}
	
	my $outBuf = '';
	
	foreach (@logData){
		unless($_ =~ /\+/){
			my($subid,$date,$title,$comment) = split(/,/,$_);
			my $outPath = "$subid.html";
			foreach $line (@html2){
				my $buf = "$line";
			
				#htmlデータを編集する
				$buf =~ s/<!--date-->/$date/;
				$buf =~ s/<!--title-->/<a href="$outPath">$title<\/a>/;
				$outBuf .= "<!--$subid-->$buf";
			}
		}
	}
	
	$outTopData = "$html1$outBuf$html3";
	
	#トップの出力データ
	unlink("$htmlOutPath");
	open(OUTFILE, ">$htmlOutPath");
	print(OUTFILE "$outTopData");
	close(OUTFILE);
}

exit;
