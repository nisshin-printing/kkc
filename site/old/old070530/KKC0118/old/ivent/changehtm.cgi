#!/usr/bin/perl
require './jcode.pl';

#--------------------------------------------------------------------------
# Perl Initialize
#--------------------------------------------------------------------------
########## 設定項目

#<!--formaction:set-->
#<!--image:set-->
#<!--text:set-->
#<!--text:end-->

$password = "npo";					# パスワード
$cgifile = './changehtm.cgi';			# ＣＧＩファイル名


$help ="";
$imageflg = "1";						#1を入れると画像入力が可能になります
									 	#(何も入れないとＯＦＦになります)
$linkflg = "1";							#1を入れると画像にリンクがつきます(別窓)
									 	#(何も入れないとＯＦＦになります)

$newHtmlLink = 'http://www.keizai-kassei.net/ivent/';# 作成したHtmlファイルへのリンク
$datafile = './data.csv';				# 入力データの場所
$htmldata = './skin.html';			# スキンファイルの場所
$newHtml = './index.html';			# 作成するHTMLファイルの場所
$inputskin = './skin.html';		# 入力用スキンファイルの場所
									 	#(スキンファイルの場所と同じでも可)
$imageFile = './image';		# ＣＧＩファイルからのimageファイルの格納場所
$imageLink = './image';			# 出力ファイルからのimageファイルへのリンク

$cols = "55";					#メッセージを書き込むテキストエリアの文字数（半角）
$rows = "10";					# メッセージを書き込むテキストエリアの行数（半角）

$upsize = 50;						# 最大サイズ<単位Kb>
$imgMaxWeight = 450;				# イメージ最大横幅
$imgMaxHeight = 500;				# イメージ最大高さ
$ImgContentSize = 20;				# イメージコメントサイズ

if($help){
$taghelp = '
<br><br>
<font color=#0080ff><b>※文字装飾メモ</b></font>
<hr>
下記のように文字を装飾することができます<br>
&lt;font&gt;～&lt;/font&gt;の様に、装飾の始まりの部分と終端の部分にタグを付けて下さい
<hr>
<font color=red>例)文字色赤　大きさ通常</font><br>
&lt;font color=red&gt;文字色赤　大きさ通常&lt;/font&gt;
<hr>
<b>例)太文字</b><br>
&lt;b&gt;太文字&lt;/b&gt;

<hr>
<font color=red><b>例)文字色赤＋太文字</b></font><br>
&lt;font color=red&gt;&lt;b&gt;文字色赤＋太文字&lt;/b&gt;&lt;/font&gt;
<hr>
<center>
<font color=red>例)中央寄せ＋文字色赤</font><br>
</center>
&lt;center&gt;<br>
&lt;font color=red&gt;強調したい文字&lt;/font&gt;<br>
&lt;/center&gt;<br>
<hr>
▽色見本▽  color= の後に続く文字を変えると文字色が変化します<br>
<FONT color="red">■赤 red</FONT>   <FONT color="blue">■青 blue</FONT>   <FONT color="darkblue">■紺 darkblue</FONT>   <FONT color="green">■緑 green</FONT>   <FONT color="orange">■橙 orange</FONT><br>
<A href="./colorlist.html" target="_blank">>>さらに詳しく色を見る</A>
<hr>
<A href="./tager.lzh" target="_blank">>>便利なソフトはこちら！</A>
<hr>

';
}#if

########## 設定項目END






########## メインへ
&main;
exit;

#----------------------------------------------------------------------------------
# main()
#----------------------------------------------------------------------------------
sub main {
	&decode;		# デコード
	# 処理振り分け
	if($PARAM{'job'} ne "mod") {
	# HTML変更ページ表示
		if ($ENV{'QUERY_STRING'} eq "i") {
			&showhtmli;
		} else {
			&showhtml;
		}
	} else {
	# 新規HTML出力
		&htmlwrite;
	}
}
#------------------------------------------------------------------------------------
# decode()
#------------------------------------------------------------------------------------
sub decode {
	my $remain = $ENV{'CONTENT_LENGTH'};
	my $maxSize = $upsize * 1024;
	# POST
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		if ($remain > $maxSize) {
			&error("投稿量が大きすぎます。");
		}
		binmode(STDIN);
		while ($remain) {
			$remain -= sysread(STDIN, $read, $remain);
			$buffer .= $read;
		}
		###### name,value get
		my $line = "";
		my ($headLength,$valueLength) = (0,0);
		my ($value,$imageFlag,$image) = ("","","","");
		# cepaletar get
		my @headers = split(/Content-Disposition:/,$buffer);
		# last cepaletar delete
		my $leng = length($buffer) - (length($headers[0]) + 2);
		$buffer = substr($buffer,0,$leng);
		# names,values
		my @cell = split(/$headers[0]/,$buffer);
		foreach $line (@cell) {
			# パラメータ＆バイナリデータ取り出し
			if($line =~ /^Content-Disposition: form-data; name="([^;]*)"; filename="([^;]*)"/i) {
				&setParam('ImageLink',"");
				&setParam('BinaryData',$line);
			# パラメータ取り出し
			} elsif($line =~ /^Content-Disposition: form-data; name="([^;]*)"([\r\n]*)/i) {
				$headLength = 39 + length($1) + length($2);			# Content~name="***"\r\n\n\nまでの長さ
				my $end = &getWhitespace($line);
				$valueLength = (length($line) - $headLength - $end);	# Valueの長さ<誤差ある場合あり(-1にする)>
				$value = substr($line,$headLength,$valueLength);
				&setParam($1,$value);
			}
		}
	} else {
	# GET
		$buffer = $ENV{'QUERY_STRING'};
		@pairs = split(/&/, $buffer);
		foreach $pair (@pairs) {
			($name, $value) = split(/=/, $pair);
			&setParam($name,$value);
		}
	}
}
#------------------------------------------------------------------------------------
# getWhitespace()
#------------------------------------------------------------------------------------
sub getWhitespace{
	my ($line) = @_;
	my $leng = length($line) - 1;
	my ($i,$char);
	
	for($i = $leng; $i > 0; $i--) {
		$char = substr($line,$i,1);
		if($char =~ /[^\r\n]/) {
			last;
		}
	}
	return ($leng - $i);
}
#------------------------------------------------------------------------------------
# setParam()
#------------------------------------------------------------------------------------
sub setParam {
	my ($name,$value) = @_;
	if($name eq 'pass') {
		# パスワードの誤差修正
		$value =~ s/\r\n//g;
		$value =~ s/\r//g;
		$value =~ s/\n//g;
	}
	if($name ne 'BinaryData') {
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		&jcode'convert(*value ,'sjis');
		$value =~ s/&/&amp;/g;
		$value =~ s/\"/&quot;/g;
#		$value =~ s/</&lt;/g;		# タグ
#		$value =~ s/>/&gt;/g;
		$value =~ s/\r\n/<br \/>/g;	# 改行
		$value =~ s/\n/<br \/>/g;
		$value =~ s/&lt;br \/&gt;/<br \/>/g;	# 前の改行復帰
	}
	$PARAM{$name} = $value;
}
#------------------------------------------------------------------------------------
# checkImageFlag()
#------------------------------------------------------------------------------------
sub checkImageFlag {
	my ($imageFlag) = @_;
	if ($imageFlag =~ /image\/gif/i) { $imageFlag=".gif";}
	elsif ($imageFlag =~ /image\/jpeg/i) { $imageFlag=".jpg";}
	elsif ($imageFlag =~ /image\/pjpeg/i) {$imageFlag=".jpg";}
	elsif ($imageFlag =~ /image\/x-png/i) { $imageFlag=".png";}
	else {$imageFlag = "";}
	return $imageFlag;
}
#------------------------------------------------------------------------------------
#imagePush()
# ○戻り値：エラーメッセージ
#------------------------------------------------------------------------------------
sub imagePush {
	my $line = $PARAM{'BinaryData'};
	my $binary;
	my $imageFlag = "";
	# イメージファイルあるかどうか
	if($line =~ /Content-Type: ([^\r\n]*)([\r\n]*)/i) {
		# バイナリ取り出し
		# lineLeng 全体の長さ　leng1 Content-Typeまでの長さ leng2 lmage/???の長さ leng3 その後の改行の長さ
		my $lineLeng = length($line);
		my ($leng1,$leng2,$leng3) = (index($line,"Content-Type:"),length($1),length($2));
		my $BinaryStart = $leng1 + 14 + $leng2 + $leng3;		# 14 Content-Type: 部分の長さ＜スペースを含む＞ 
		my $BinaryLength = $lineLeng - $BinaryStart - 1;
		$binary = substr($line,$BinaryStart,$BinaryLength);
		# イメージ拡張子取り出し
		$imageFlag = $1;
		$imageFlag =~ s/\r//g;
		$imageFlag =~ s/\n//g;
	}
	if(! $binary) {return undef;}		# 今回イメージなし
	# 拡張子判定

	$imageFlag = &checkImageFlag($imageFlag);
	if($imageFlag) {
		# イメージファイル書き込み
		my $File = "$imageFile$imageFlag";
		open(OUT,"> $File") || return "画像の書き込みに失敗しました";
		binmode(OUT);
		binmode(STDOUT);
		print OUT $binary;
		close(OUT);
		chmod (0666,$File);
		$imageLink = "$imageLink$imageFlag";
		&setParam('imagelink',$imageLink);
		# イメージサイズ取得
		my ($weight,$height);
		open(SIZE,"< $File") || return "イメージのサイズ取得に失敗しました";
		binmode(SIZE);
		if($imageFlag eq ".gif") {
			($weight,$height) = &gifsize(\*SIZE);
		} else {
			($weight,$height) = &jpegsize(\*SIZE);
		}
		close(SIZE);
		&setParam('height',$height);
		&setParam('weight',$weight);
		return undef;
	} else {
		return "ファイル形式が不正です";
	}
}
#------------------------------------------------------------------------------------------
#	htmlwrite()	HTML出力
#------------------------------------------------------------------------------------------
sub htmlwrite {
	# パスワードチェック
	if(! &passCheck()) {
		&error("パスワードが違います!!$PARAM{'pass'}");
	}
	# イメージ書き込み
	my $errMessage = &imagePush;
	if($errMessage) {
		&error($errMessage);
	}
	# HTML読み取り

	if (!open(DF,"$htmldata")){ &error("HtmlRead Err1");}
	@DATAF = <DF>;
	close(DF);
	# HTML分割
	my $htmlno = "1";
	my ($html1,$html2,$html3,$html4)  = ("","","","");
	foreach $line (@DATAF) {
		if($line =~ /<!--formaction:set-->/) {
			next;
		}
		if($line =~ /<!--image:set-->/) {
			$htmlno = "2";
			next;
		}
		if($line =~ /<!--text:set-->/) {
			$htmlno = "3";
			next;
		}
		if($line =~ /<!--text:end-->/) {
			$htmlno = "4";
			next;
		}
		if($line =~ /<!--formaction:end-->/) {
			next;
		}
		###
   		if($htmlno eq "1") {
	   		$html1 ="$html1$line";
	   	} elsif($htmlno eq "2") {
		   	$html2 = "$html2$line";
		} elsif($htmlno eq "4") {
			$html4 = "$html4$line";
		}
	}
	# Parametar get
	my $ImageLink = $PARAM{'imagelink'};
	my $content = "$PARAM{'content'}";
	my $weight = $PARAM{'weight'};
	my $height = $PARAM{'height'};
	if($weight > $imgMaxWeight) {
		$height = int($imgMaxWeight * $height / $weight);  
		$weight = $imgMaxWeight;
	}
#	if($height > $imgMaxHeight) {
#		$height = $imgMaxHeight;
#	}
	if($ImageLink) {
		my $ImgContent = $PARAM{'imgcontent'};
		if(! $ImgContent) {$ImgContent = "イメージ";}
		# イメージリンク組み込み：この書き方はXmlの規律に反する
		if($linkflg == 1) {$html2 = "<a href='$ImageLink' target='_blank'><img src='$ImageLink' alt='$ImgContent' width='$weight' height='$height' border='0'></a>$html2";}
		else {$html2 = "<img src='$ImageLink' alt='$ImgContent' width='$weight' height='$height' border='0'>$html2";}
	}
	if($content) {
		$html3 = "$html3$content\n";
	}
	# HtmlFileOut
	chmod 0666, $newHtml;
	open OUT, ">$newHtml";       
	print OUT $html1;
	print OUT $html2;
	print OUT $html3;
	print OUT $html4;
	close OUT;
	chmod 0644, $newHtml;

	open OUT, ">$datafile";       
	print OUT $content;
	close OUT;


	# 書き込み成功
	print <<EOM;
Content-type: text/html

<html><head>
<meta http-equiv=Content-Type content=text/html; charset=Shift_JIS>
<title>htmlを作りました</title></head>
<body bgcolor=#FFFFFF>
<TABLE border="0" width="100%" height="100%">
  <TBODY>
    <TR>
      <TD align="center" valign="top"><BR>
      <BR>
      <BR>
      <BR>
      <BR>
      <FONT size="+3" color="#0080c0">ファイルを更新しました</FONT><BR>
      <BR>
      <BR>更新内容を確認して下さい<BR>
      <BR>
      <BR>
      <BR>
      &gt;<B><A href="$newHtmlLink">更新したページを見る</A></B>&lt;<BR>
      <BR>
      <FONT color="#cc0000">※必ず更新ボタンを押して、画面を更新して下さい</FONT><BR>
      <BR>
      <BR>
      </TD>
    </TR>
  </TBODY>
</TABLE>
</body>
</html>

EOM
	
	exit;
}
#----------------------------------------------------------------------------
#	htmlread()
#----------------------------------------------------------------------------
sub htmlread{
	my $htmlno = "1";
	my ($html1,$html2,$html3,$content,$html4,$html5) = ("","","","","","");
	if (!open(DF,"$inputskin")){ &error("HtmlRead Err2");}
	@DATAF = <DF>;
	close(DF);
	foreach $line (@DATAF) {
   		if($line =~ /<!--formaction:set-->/) {
      		$htmlno = "2";
	  		next;
      	}
   		if($line =~ /<!--image:set-->/) {
	   		$htmlno = "3";
	   		next;
	   	}
	   	if($line =~ /<!--text:set-->/) {
		   	$htmlno = "4";
		   	next;
		}
		if($line =~ /<!--text:end-->/) {
			$htmlno = "5";
			next;
		}
		if($line =~ /<!--formaction:end-->/) {
			$htmlno = "6";
			next;
		}
   		if($htmlno eq "1") {
	   		$html1 = "$html1$line";
	   	} elsif($htmlno eq "2") {
	   		$html2 = "$html2$line";
	   	} elsif($htmlno eq "3") {
		   	$html3 = "$html3$line";
		} elsif($htmlno eq "4") {
			$line =~ s/\r\n//g;
      		$line =~ s/\n//g;
      		$line =~ s/<br \/>/\n/g;
      		$content ="$content$line";
      	} elsif($htmlno eq "5") {
		  	$html4 = "$html4$line";
		} else {
			$html5 = "$html5$line";
		}
	}

	if (!open(DF,"$datafile")){ &error("HtmlRead Err99");}
	@DATAF = <DF>;
	close(DF);
	$content = "";
	foreach $line (@DATAF) {
			$line =~ s/\r\n//g;
      		$line =~ s/\n//g;
      		$line =~ s/<br \/>/\n/g;
      		$content ="$content$line";
	}
	return ($html1,$html2,$html3,$content,$html4,$html5);
}




#----------------------------------------------------------------------------
#	df htmlread()
#----------------------------------------------------------------------------
sub dfhtmlread{
	my $htmlno = "1";
	my ($html1,$html2,$html3,$content,$html4,$html5) = ("","","","","","");
	if (!open(DF,"$inputskin")){ &error("HtmlRead Err2");}
	@DATAF = <DF>;
	close(DF);
	foreach $line (@DATAF) {
   		if($line =~ /<!--formaction:set-->/) {
      		$htmlno = "2";
	  		next;
      	}
   		if($line =~ /<!--image:set-->/) {
	   		$htmlno = "3";
	   		next;
	   	}
	   	if($line =~ /<!--text:set-->/) {
		   	$htmlno = "4";
		   	next;
		}
		if($line =~ /<!--text:end-->/) {
			$htmlno = "5";
			next;
		}
		if($line =~ /<!--formaction:end-->/) {
			$htmlno = "6";
			next;
		}
   		if($htmlno eq "1") {
	   		$html1 = "$html1$line";
	   	} elsif($htmlno eq "2") {
	   		$html2 = "$html2$line";
	   	} elsif($htmlno eq "3") {
		   	$html3 = "$html3$line";
		} elsif($htmlno eq "4") {
			$line =~ s/\r\n//g;
      		$line =~ s/\n//g;
      		$line =~ s/<br \/>/\n/g;
      		$content ="$content$line";
      	} elsif($htmlno eq "5") {
		  	$html4 = "$html4$line";
		} else {
			$html5 = "$html5$line";
		}
	}


	if (!open(DF,"$datafile")){ &error("HtmlRead Err99");}
	@DATAF = <DF>;
	close(DF);
	$content = "";
	foreach $line (@DATAF) {
			$line =~ s/\r\n//g;
      		$line =~ s/\n//g;
      		$line =~ s/<br \/>/\n/g;
      		$content ="$content$line";
	}
	return ($html1,$html2,$html3,$content,$html4,$html5);
}



#----------------------------------------------------------------------------
#	showhtml()
#----------------------------------------------------------------------------
sub showhtml{
	# test.html read
	my ($html1,$html2,$html3,$content,$html4,$html5) = &htmlread;
	# showHtml Out
	
	
if($imageflg){
print <<EOM;
Content-type: text/html

$html1
<form action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="job" value="mod">
$html2
画像ファイル：省略可<br>
<input type="file" name="image" size="25"><br><br>
イメージコメント：省略可<br>
<input type="text" name="imgcontent" size=$ImgContentSize>
$html3	
<textarea name ="content" rows="$rows" cols="$cols">$content
</textarea>
$taghelp
$html4
<table><tr><td>PASS<input type="password" name="pass" size="10"></td>
<td><input type="submit" value="　更　新　"></td></tr></table>
</form>
$html5

EOM
}else{
print <<EOM;
Content-type: text/html

$html1
<form action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="job" value="mod">
$html2
$html3	
<textarea name ="content" rows="$rows" cols="$cols">$content
</textarea>
$taghelp
$html4
<table><tr><td>PASS<input type="password" name="pass" size="10"></td>
<td><input type="submit" value="　更　新　"></td></tr></table>
</form>
$html5

EOM
}

	exit;
}
#-----------------------------------------------------------------------------
#	showhtml1()
#-----------------------------------------------------------------------------
sub showhtmli{
	# test.html read
	my ($html1,$html2,$html3,$content,$html4,$html5) = &htmlread;
	# showHtmli Out
	print <<EOM;
Content-type: text/html

<html><head>
<meta http-equiv=Content-Type content=text/html; charset=Shift_JIS>
<title>ページ更新</title></head>
<body bgcolor=#FFFFFF>
<center>
<form action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="job" value="mod">
$html2
ファイル参照：省略可<br>
<input type="file" name="image" size="30"><br><br>
イメージコメント：省略可<br>
<input type="text" name="imgcontent" size=$ImgContentSize>
$html3
<textarea name ="content" rows="$rows" cols="$cols">
$taghelp
$content
</textarea>
$html4
<table><tr><td>PASS<input type="text" name="pass" size="10"></td>
<td><input type="submit" value="送信"></td></tr></table>
</form>
</center>
</body>
</html>
EOM
	
	exit;
}
#------------------------------------------------------------------------------------------
# passCheck()
#------------------------------------------------------------------------------------------
sub passCheck {
	if($PARAM{'pass'} ne $password) {
		return undef;
	} else {
		return "true";
	}
}
#----------------------------------------------------------------------------
#	error()
#----------------------------------------------------------------------------
sub error{
	my ($msg) = @_;		# エラーメッセージ取得
print <<EOM;
Content-type: text/html

<html><head>
<meta http-equiv=Content-Type content=text/html; charset=Shift_JIS>
<title>Err</title></head>
<body bgcolor=#FFFFFF>
<br /><br /><br /><center>$msg</center>
</body>
</html>
EOM

exit;
}
# //// GIF,JPG サイズ取得 /////////////////////////////////////////////////////////////

sub gifsize{
	my ($GIF) = @_;
  	my ($type,$a,$b,$c,$d,$s)=(0,0,0,0,0,0);

  	if(defined( $GIF )		&&
     	read($GIF, $type, 6)	&&
     	$type =~ /GIF8[7,9]a/	&&
     	read($GIF, $s, 4) == 4	){
    		($a,$b,$c,$d)=unpack("C"x4,$s);
    		return ($b<<8|$a,$d<<8|$c);
  	}
  	return (0,0);
}
sub jpegsize {
	my ($JPEG) = @_;
	my ($done)=0;
	my ($c1,$c2,$ch,$s,$length, $dummy)=(0,0,0,0,0,0);
	my ($a,$b,$c,$d);

	if(defined($JPEG)		&&
		read($JPEG, $c1, 1)	&&
    	read($JPEG, $c2, 1)	&&
    	ord($c1) == 0xFF		&&
    	ord($c2) == 0xD8		){
			while (ord($ch) != 0xDA && !$done) {
				# Find next marker (JPEG markers begin with 0xFF)
      			# This can hang the program!!
     			while (ord($ch) != 0xFF) { return(0,0) unless read($JPEG, $ch, 1); }
      			# JPEG markers can be padded with unlimited 0xFF's
      			while (ord($ch) == 0xFF) { return(0,0) unless read($JPEG, $ch, 1); }
      			# Now, $ch contains the value of the marker.
      			if ((ord($ch) >= 0xC0) && (ord($ch) <= 0xC3)) {
					return(0,0) unless read ($JPEG, $dummy, 3);
					return(0,0) unless read($JPEG, $s, 4);
					($a,$b,$c,$d)=unpack("C"x4,$s);
					return ($c<<8|$d, $a<<8|$b );
      			} else {
					# We **MUST** skip variables, since FF's within variable names are
					# NOT valid JPEG markers
					return(0,0) unless read ($JPEG, $s, 2);
					($c1, $c2) = unpack("C"x2,$s);
					$length = $c1<<8|$c2;
					last if (!defined($length) || $length < 2);
					read($JPEG, $dummy, $length-2);
      			}
    		}
  	}
  	return (0,0);
}
