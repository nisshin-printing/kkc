package log;
###########################################################
#	filectl.pl
#	ファイルを調整するplモジュール
#	create by Yuji Tominaga
#
#		    GNU GENERAL PUBLIC LICENSE
#		       Version 2, June 1991
#
# Copyright (C) 1989, 1991 Free Software Foundation, Inc.
#                       59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.
#
#			    Preamble
#
#  The licenses for most software are designed to take away your
#freedom to share and change it.  By contrast, the GNU General Public
#License is intended to guarantee your freedom to share and change free
#software--to make sure the software is free for all its users.  This
#General Public License applies to most of the Free Software
#Foundation's software and to any other program whose authors commit to
#using it.  (Some other Free Software Foundation software is covered by
#the GNU Library General Public License instead.)  You can apply it to
#your programs, too.
#
#  When we speak of free software, we are referring to freedom, not
#price.  Our General Public Licenses are designed to make sure that you
#have the freedom to distribute copies of free software (and charge for
#this service if you wish), that you receive source code or can get it
#if you want it, that you can change the software or use pieces of it
#in new free programs; and that you know you can do these things.
#
#  To protect your rights, we need to make restrictions that forbid
#anyone to deny you these rights or to ask you to surrender the rights.
#These restrictions translate to certain responsibilities for you if you
#distribute copies of the software, or if you modify it.
#
#  For example, if you distribute copies of such a program, whether
#gratis or for a fee, you must give the recipients all the rights that
#you have.  You must make sure that they, too, receive or can get the
#source code.  And you must show them these terms so they know their
#rights.
#
#  We protect your rights with two steps: (1) copyright the software, and
#(2) offer you this license which gives you legal permission to copy,
#distribute and/or modify the software.
#
#  Also, for each author's protection and ours, we want to make certain
#that everyone understands that there is no warranty for this free
#software.  If the software is modified by someone else and passed on, we
#want its recipients to know that what they have is not the original, so
#that any problems introduced by others will not reflect on the original
#authors' reputations.
#
#  Finally, any free program is threatened constantly by software
#patents.  We wish to avoid the danger that redistributors of a free
#program will individually obtain patent licenses, in effect making the
#program proprietary.  To prevent this, we have made it clear that any
#patent must be licensed for everyone's free use or not licensed at all.
#
#  The precise terms and conditions for copying, distribution and
#modification follow.
#
#----------------------------------------------------------
#
#	openFile()
#	指定したファイルを開く関数
#@param		$fileName	ファイルへのパス(ファイル名)
#@return	$fileData	ファイルのデータ
#	@fileData	= openFile("index.html");
#
#----------------------------------------------------------
#	writeFile()
#	指定したファイルにデータを書き込む
#@param		$filePath	ファイルへのパス(ファイル名)
#			$message	ファイルへ書き込むデータ
#	writeFile("index.html","$index");
#
#----------------------------------------------------------
#	mixData()
#	htmlファイルとlogファイルを結合する
#@param		$length	logファイルのサイズ
#			$ret	ログの表示数
#			@log	logファイルのデータ
#			@htmls	htmlファイルのデータ
#@return 	$mixd	混合したデータ
#
#	$message = mixData($length, $ret, @log, @htmls);
#----------------------------------------------------------
#
#	writeLog()
#	Logファイルを書き込む
#@param		$filePath		logのファイル先
#			$message		logファイルへ書き出すメッセージ
#	writeLog($filePath, $message);
###########################################################	

###########################################################
#	openFile()
#	指定したファイルを開く
#@param		$fileName	ファイルへのパス
#@return	@fileData	ファイルのデータ
###########################################################
sub openFile
{
	#引数の受け取り
	#および仕様変数の宣言・初期化
	my($fileName) = @_;
	my @fileData;
		
	#ファイルを開く
	#エラー処理付き
	if(!open(DF, "$fileName")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$fileName";
		exit;
	}
	
	#ファイルのデータを受け取る
	@fileData = <DF>;
	close(DF);
	
	return @fileData;
}

###########################################################
#	writeFile()
#	ファイルへデータを書き込む
#@param		$filePath		logのファイル先
#			$message		logファイルへ
###########################################################
sub writeFile
{
	#引数の処理
	my($filePath, $message)		= @_;
	
	#ファイルを開く
	if(!open(OUT, ">$filePath")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$filePath";
		exit;
	}
	
	#ファイルへの書き込み
	print OUT "$message\n";
	close(OUT);
}

###########################################################
#	mixData()
#	logデータとhtmlデータを混合する
#@param		$length	logファイルのサイズ
#			$ret	ログの表示数
#			@log	logファイルのデータ
#			@htmls	htmlファイルのデータ
#@return 	$mixd	混合したデータ
###########################################################
sub mixData
{
	#引数の処理
	my($length, $ret, @buf)	= @_;
	
	my @log		= @buf[0..$length-1];
	my @htmls	= @buf[$length..$#buf];
	
	#変数の初期化
	my $html1	= "";			#<!--start2-->以前のデータが入る
	my $html2	= "";			#<!--start2-->～<!--last2-->までのデータが入る
	my $html3	= "";			#<!--last2-->以降のデータが入る
	my $line	= "";			#データの取り出しよう変数
	my $htmlno	= "1";			#処理変更フラグ
	my $mixd 	= "";			#処理後のhtmlファイルデータ
	my $i;
	
	#logファイルの整列
	@log		= reverse @log;
	
	#データの処理
	foreach $line (@htmls) {
		if($line =~/<!--start-->/){
			$htmlno = "2";
		}elsif($line =~/<!--stop-->/){
			$htmlno = "3";
		}
		
		if($htmlno eq "1"){
			$html1 ="$html1$line";
		}elsif($htmlno eq "2"){
			#logデータの埋め込み
			$html2 = "$html2<!--start2-->\n";
			for($i = 0; $i < $ret; $i++){
				$html2 = "$html2$log[$i]";
			}
			$htmlno = "3"	
		}elsif($htmlno eq "3"){
			$html3 ="$html3$line";
		}
	}

	#データの合成
	$mixd		= "$html1$html2$html3\n";
	return $mixd;
}

###########################################################
#	writeLog()
#	Logファイルを書き込む
#@param		$filePath		logのファイル先
#			$message		logファイルへ
###########################################################
sub writeLog
{
	#引数の処理
	my($filePath, $message)		= @_;
	
	#改行コードを切り落とす
	chomp $message;
	
	#変数初期化
	my @data;					#チェック用データファイル
	my $dataSize;				#データファイルのサイズ
	
	#エラー処理兼ファイル処理
	if(!open(DF, "$filePath")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$filePath";
		exit;
	}
	
	#ファイルのデータを写す
	@data = <DF>;
	close(DF);
	
	#データサイズのチェック
	$dataSize	= @data;
	
	#データ処理
	if($dataSize >= 100){
		@data	= reverse @data;
		@data	= @data[0..49];
		@data	= reverse @data;
	}
	
	if(!open(OUT, ">$filePath")){
		print "Countent-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$filePath";
		exit;
	}
	
	#データの書き出し
	foreach $line (@data){
		print OUT "$line";
	}
	close(OUT);
	
	#ファイルを開く
	if(!open(OUT, ">>$filePath")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$filePath";
		exit;
	}
	
	#ファイルへの書き込み
	print OUT "$message\n";
	close(OUT);
}

###########################################################
#	show()
#	データを読み込んで表示を行う
#@param		$maxData	表示データ最大数
#			@showData	表示データ
#			@skinData	表示スキン
###########################################################
sub show
{
	#引数の処理
	my ($maxData,@buf)	= @_;
	
	#表示データと表示スキンの割振り
	#各種利用変数の初期化
	my @showData		= $buf[0..$maxData];		#ログファイルデータの抽出
	my @skinData		= @buf;						#スキンデータの抽出
	my $htmlno			= "1";						#処理判定用フラグ
	
	my $html1,$html2,$html3;						#合成用データ一時保存領域
	my $mixData;									#合成後のデータ
	
	#合成処理
	foreach $line (@skinData){
		#処理判定フラグを元に処理を割り振る
		if($htmlno eq "1"){
			$html1 		= "$html1$line";
		}elsif($htmlno eq "2"){
			foreach $data (@showData){
				$html2	= "$html2$line";
			}
			$html2		= "$html2<!--last-->\n";
			$htmlno		= "3";
		}elsif($htmlno eq "3"){
			$html3		= "$html3$line";
		}
		
		if($line =~ /<!--start-->/){
			$htmlno		= "2";
		}
	}
	
	foreach $line (@mixData){
		print "$line";
	}
}

return 1;