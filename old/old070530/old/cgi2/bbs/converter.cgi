#!/usr/local/bin/perl

# 
#   TBOARD 003 ログファイルコンバータ
# 
#   Copyright(C) TOSHISRUS
#   E-mail   ： tboard@sk.redbit.ne.jp
#   HOMEPAGE ： http://sk.redbit.ne.jp/~tboard/

# ==== 注意事項 ========================================================
#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#    いかなる損害に対して作者は一切の責任を負いません。
#    また、本CGIはフリーソフトですが、著作権は放棄してはいません。
#    フッターの著作権表示はいかなる事があっても削除してはいけません。
#
# 2. 設置に関する質問は当ホームページの掲示板にてお願いいたします。
#    直接メールによる質問は一切お受けいたしておりません。
#
# 3. 設定項目を少なくしたため、カスタマイズが少々辛いです。
#    お気に召しましたら、お使いください。
#    要望などありましたら、当ホームページの掲示板にてお願いいたします。
#
# ======================================================================

# 
# 使用する前に必ずログファイルのバックアップを取ってください。
# このコンバータを使用すると以前のファイルはすべて削除されます。
# 変換後、ログ保管用のlogboxのフォルダのみは、手動で削除してください。
# 

# ==== 使用方法 ========================================================
#
# 1. 基本設定で、ログファイルのパスをすべて相対パスで指定する。
# 2. ブラウザでconverter.cgiにアクセスする。
# 3. 「変換完了」と出力されればコンバート完了です。
#
# ======================================================================

# //// 基本設定 (ここから) ////////////////////////////////////////////////////////////////

# ==== TBOARD 0.**の設定 =============
# 親記事用ログファイル
$oyalog = "logbox/oyalog.log";
# レス記事用ログファイル
$reslog = "logbox/reslog.log";

# ==== TBOARD 1.**の設定 =============
# ログファイル
$logfile = "tboard003.log";

# ==== TBOARD共通の設定 ==============
# 過去ログディレクトリ
$oldbox = "oldlog/";

# //// 基本設定 (ここまで) ////////////////////////////////////////////////////////////////

# //// ログファイルの移行 ///////////////////////////////////////////////////////////////////
# ログを開く
open(IN,"$oyalog") || &error("Can't open logfile");
@oyalog = <IN>;
close(IN);
open(IN,"$reslog") || &error("Can't open logfile");
@reslog = <IN>;
close(IN);
@new = ();
foreach $oya (@oyalog){
	($odate,$otdate,$oname,$oemail,$otitle,$ocom,$ourl,$okey,$omenu01,$omenu02,$omenu03,$omenu04,$omenu05) = split(/\t/,$oya);
	push(@new,$oya);
	foreach $res (@reslog){
		($rdate,$rtdate,$rname,$remail,$rtitle,$rcom,$rurl,$rkey,$rmenu01,$rmenu02,$rmenu03,$rmenu04,$rmenu05) = split(/\t/,$res);
		if($otdate eq $rtdate){push(@new,$res);}
	}
}
# ログの更新
open(OUT,">$logfile") || &error("Can't write logfile");
print OUT @new;
close(OUT);
# 属性の変更
chmod(0666,"$logfile");

# //// 過去ログファイルの移行 ///////////////////////////////////////////////////////////////
# 過去UP物ディレクトリのオープン
opendir(DIR,$oldbox);
@filelist = ();
while ($ofile = readdir(DIR)){
 if(index($ofile,"oya\.")>0){
  push(@filelist,$ofile);
 }
}
closedir(DIR);
# ファイル名をソートする
@filelist = sort @filelist;
$s = 0;
while($s<@filelist){
	$oyalog = $oldbox.substr(@filelist[$s],0,6).'_oya.log';
	$reslog = $oldbox.substr(@filelist[$s],0,6).'_res.log';
	$logfile = $oldbox.substr(@filelist[$s],0,6).'.log';
	# ログを開く
	open(IN,"$oyalog") || &error("Can't open logfile");
	@oyalog = <IN>;
	close(IN);
	open(IN,"$reslog") || &error("Can't open logfile");
	@reslog = <IN>;
	close(IN);
	@new = ();
	foreach $oya (@oyalog){
		($odate,$otdate,$oname,$oemail,$otitle,$ocom,$ourl,$okey,$omenu01,$omenu02,$omenu03,$omenu04,$omenu05) = split(/\t/,$oya);
		push(@new,$oya);
		foreach $res (@reslog){
			($rdate,$rtdate,$rname,$remail,$rtitle,$rcom,$rurl,$rkey,$rmenu01,$rmenu02,$rmenu03,$rmenu04,$rmenu05) = split(/\t/,$res);
			if($otdate eq $rtdate){push(@new,$res);}
		}
	}
	# ログの更新
	open(OUT,">$logfile") || &error("Can't write logfile");
	print OUT @new;
	close(OUT);
	# 属性の変更
	chmod(0666,"$logfile");
	unlink($oyalog);
	unlink($reslog);
	$s++;
}

print "Content-type: text/html\n";
print "\n";
print<<HTML_END;
<html>
<head><title>$title</title>
<style type="text/css">
<!--
body,tr,td {font-size:9pt;font-family: "MS UI Gothic"}
table      {font-size:9pt;}
b          {font-size:10pt}
small      {font-size:10pt;line-height:18pt}
div        {line-height:14pt}
h4         {font-size:12pt}
/* a          {font-size:9pt;text-decoration:none;} */
/* a:hover    {color:$color05;text-decoration:underline;} */
.st1       {font-size:9pt;font-family:"MS UI Gothic";color:$color06;background-color:$color07;} /* 項目 */
.st2       {color:$color09;$stylest1} /* 項目2 */
-->
</style>
</head>
<body>
<center>
変換完了
</center>
<div align=center><br>
$var<br>
- <a href='http://i.am/toshisrus' TARGET=_blank>TOSHISRUS</a> -
</div>
</body></html>
HTML_END
exit;

# //// Error処理 ///////////////////////////////////////////////////////////////////////////
sub error {
	if(-e $_[1]){ unlink($_[1]);}
	print"<center><hr width=75%><h4>エラー</h4>\n";
	print"<P><h4>$_[0]</h4>\n";
	print"<P><hr width=75%><br>ブラウザの戻るで戻ってください。</center>\n";
	&footer;
	exit;
}
