#!/usr/bin/perl
require './jcode.pl';

#--------------------------------------------------------------------------
# Perl Initialize
#--------------------------------------------------------------------------
########## �ݒ荀��

#<!--formaction:set-->
#<!--image:set-->
#<!--text:set-->
#<!--text:end-->

$password = "npo";					# �p�X���[�h
$cgifile = './changehtm.cgi';			# �b�f�h�t�@�C����


$help ="";
$imageflg = "1";						#1������Ɖ摜���͂��\�ɂȂ�܂�
									 	#(��������Ȃ��Ƃn�e�e�ɂȂ�܂�)
$linkflg = "1";							#1������Ɖ摜�Ƀ����N�����܂�(�ʑ�)
									 	#(��������Ȃ��Ƃn�e�e�ɂȂ�܂�)

$newHtmlLink = 'http://www.keizai-kassei.net/ivent/';# �쐬����Html�t�@�C���ւ̃����N
$datafile = './data.csv';				# ���̓f�[�^�̏ꏊ
$htmldata = './skin.html';			# �X�L���t�@�C���̏ꏊ
$newHtml = './index.html';			# �쐬����HTML�t�@�C���̏ꏊ
$inputskin = './skin.html';		# ���͗p�X�L���t�@�C���̏ꏊ
									 	#(�X�L���t�@�C���̏ꏊ�Ɠ����ł���)
$imageFile = './image';		# �b�f�h�t�@�C�������image�t�@�C���̊i�[�ꏊ
$imageLink = './image';			# �o�̓t�@�C�������image�t�@�C���ւ̃����N

$cols = "55";					#���b�Z�[�W���������ރe�L�X�g�G���A�̕������i���p�j
$rows = "10";					# ���b�Z�[�W���������ރe�L�X�g�G���A�̍s���i���p�j

$upsize = 50;						# �ő�T�C�Y<�P��Kb>
$imgMaxWeight = 450;				# �C���[�W�ő剡��
$imgMaxHeight = 500;				# �C���[�W�ő卂��
$ImgContentSize = 20;				# �C���[�W�R�����g�T�C�Y

if($help){
$taghelp = '
<br><br>
<font color=#0080ff><b>��������������</b></font>
<hr>
���L�̂悤�ɕ����𑕏����邱�Ƃ��ł��܂�<br>
&lt;font&gt;�`&lt;/font&gt;�̗l�ɁA�����̎n�܂�̕����ƏI�[�̕����Ƀ^�O��t���ĉ�����
<hr>
<font color=red>��)�����F�ԁ@�傫���ʏ�</font><br>
&lt;font color=red&gt;�����F�ԁ@�傫���ʏ�&lt;/font&gt;
<hr>
<b>��)������</b><br>
&lt;b&gt;������&lt;/b&gt;

<hr>
<font color=red><b>��)�����F�ԁ{������</b></font><br>
&lt;font color=red&gt;&lt;b&gt;�����F�ԁ{������&lt;/b&gt;&lt;/font&gt;
<hr>
<center>
<font color=red>��)�����񂹁{�����F��</font><br>
</center>
&lt;center&gt;<br>
&lt;font color=red&gt;��������������&lt;/font&gt;<br>
&lt;/center&gt;<br>
<hr>
���F���{��  color= �̌�ɑ���������ς���ƕ����F���ω����܂�<br>
<FONT color="red">���� red</FONT>   <FONT color="blue">���� blue</FONT>   <FONT color="darkblue">���� darkblue</FONT>   <FONT color="green">���� green</FONT>   <FONT color="orange">���� orange</FONT><br>
<A href="./colorlist.html" target="_blank">>>����ɏڂ����F������</A>
<hr>
<A href="./tager.lzh" target="_blank">>>�֗��ȃ\�t�g�͂�����I</A>
<hr>

';
}#if

########## �ݒ荀��END






########## ���C����
&main;
exit;

#----------------------------------------------------------------------------------
# main()
#----------------------------------------------------------------------------------
sub main {
	&decode;		# �f�R�[�h
	# �����U�蕪��
	if($PARAM{'job'} ne "mod") {
	# HTML�ύX�y�[�W�\��
		if ($ENV{'QUERY_STRING'} eq "i") {
			&showhtmli;
		} else {
			&showhtml;
		}
	} else {
	# �V�KHTML�o��
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
			&error("���e�ʂ��傫�����܂��B");
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
			# �p�����[�^���o�C�i���f�[�^���o��
			if($line =~ /^Content-Disposition: form-data; name="([^;]*)"; filename="([^;]*)"/i) {
				&setParam('ImageLink',"");
				&setParam('BinaryData',$line);
			# �p�����[�^���o��
			} elsif($line =~ /^Content-Disposition: form-data; name="([^;]*)"([\r\n]*)/i) {
				$headLength = 39 + length($1) + length($2);			# Content~name="***"\r\n\n\n�܂ł̒���
				my $end = &getWhitespace($line);
				$valueLength = (length($line) - $headLength - $end);	# Value�̒���<�덷����ꍇ����(-1�ɂ���)>
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
		# �p�X���[�h�̌덷�C��
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
#		$value =~ s/</&lt;/g;		# �^�O
#		$value =~ s/>/&gt;/g;
		$value =~ s/\r\n/<br \/>/g;	# ���s
		$value =~ s/\n/<br \/>/g;
		$value =~ s/&lt;br \/&gt;/<br \/>/g;	# �O�̉��s���A
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
# ���߂�l�F�G���[���b�Z�[�W
#------------------------------------------------------------------------------------
sub imagePush {
	my $line = $PARAM{'BinaryData'};
	my $binary;
	my $imageFlag = "";
	# �C���[�W�t�@�C�����邩�ǂ���
	if($line =~ /Content-Type: ([^\r\n]*)([\r\n]*)/i) {
		# �o�C�i�����o��
		# lineLeng �S�̂̒����@leng1 Content-Type�܂ł̒��� leng2 lmage/???�̒��� leng3 ���̌�̉��s�̒���
		my $lineLeng = length($line);
		my ($leng1,$leng2,$leng3) = (index($line,"Content-Type:"),length($1),length($2));
		my $BinaryStart = $leng1 + 14 + $leng2 + $leng3;		# 14 Content-Type: �����̒������X�y�[�X���܂ށ� 
		my $BinaryLength = $lineLeng - $BinaryStart - 1;
		$binary = substr($line,$BinaryStart,$BinaryLength);
		# �C���[�W�g���q���o��
		$imageFlag = $1;
		$imageFlag =~ s/\r//g;
		$imageFlag =~ s/\n//g;
	}
	if(! $binary) {return undef;}		# ����C���[�W�Ȃ�
	# �g���q����

	$imageFlag = &checkImageFlag($imageFlag);
	if($imageFlag) {
		# �C���[�W�t�@�C����������
		my $File = "$imageFile$imageFlag";
		open(OUT,"> $File") || return "�摜�̏������݂Ɏ��s���܂���";
		binmode(OUT);
		binmode(STDOUT);
		print OUT $binary;
		close(OUT);
		chmod (0666,$File);
		$imageLink = "$imageLink$imageFlag";
		&setParam('imagelink',$imageLink);
		# �C���[�W�T�C�Y�擾
		my ($weight,$height);
		open(SIZE,"< $File") || return "�C���[�W�̃T�C�Y�擾�Ɏ��s���܂���";
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
		return "�t�@�C���`�����s���ł�";
	}
}
#------------------------------------------------------------------------------------------
#	htmlwrite()	HTML�o��
#------------------------------------------------------------------------------------------
sub htmlwrite {
	# �p�X���[�h�`�F�b�N
	if(! &passCheck()) {
		&error("�p�X���[�h���Ⴂ�܂�!!$PARAM{'pass'}");
	}
	# �C���[�W��������
	my $errMessage = &imagePush;
	if($errMessage) {
		&error($errMessage);
	}
	# HTML�ǂݎ��

	if (!open(DF,"$htmldata")){ &error("HtmlRead Err1");}
	@DATAF = <DF>;
	close(DF);
	# HTML����
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
		if(! $ImgContent) {$ImgContent = "�C���[�W";}
		# �C���[�W�����N�g�ݍ��݁F���̏�������Xml�̋K���ɔ�����
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


	# �������ݐ���
	print <<EOM;
Content-type: text/html

<html><head>
<meta http-equiv=Content-Type content=text/html; charset=Shift_JIS>
<title>html�����܂���</title></head>
<body bgcolor=#FFFFFF>
<TABLE border="0" width="100%" height="100%">
  <TBODY>
    <TR>
      <TD align="center" valign="top"><BR>
      <BR>
      <BR>
      <BR>
      <BR>
      <FONT size="+3" color="#0080c0">�t�@�C�����X�V���܂���</FONT><BR>
      <BR>
      <BR>�X�V���e���m�F���ĉ�����<BR>
      <BR>
      <BR>
      <BR>
      &gt;<B><A href="$newHtmlLink">�X�V�����y�[�W������</A></B>&lt;<BR>
      <BR>
      <FONT color="#cc0000">���K���X�V�{�^���������āA��ʂ��X�V���ĉ�����</FONT><BR>
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
�摜�t�@�C���F�ȗ���<br>
<input type="file" name="image" size="25"><br><br>
�C���[�W�R�����g�F�ȗ���<br>
<input type="text" name="imgcontent" size=$ImgContentSize>
$html3	
<textarea name ="content" rows="$rows" cols="$cols">$content
</textarea>
$taghelp
$html4
<table><tr><td>PASS<input type="password" name="pass" size="10"></td>
<td><input type="submit" value="�@�X�@�V�@"></td></tr></table>
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
<td><input type="submit" value="�@�X�@�V�@"></td></tr></table>
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
<title>�y�[�W�X�V</title></head>
<body bgcolor=#FFFFFF>
<center>
<form action="$cgifile" method="POST" enctype="multipart/form-data">
<input type="hidden" name="job" value="mod">
$html2
�t�@�C���Q�ƁF�ȗ���<br>
<input type="file" name="image" size="30"><br><br>
�C���[�W�R�����g�F�ȗ���<br>
<input type="text" name="imgcontent" size=$ImgContentSize>
$html3
<textarea name ="content" rows="$rows" cols="$cols">
$taghelp
$content
</textarea>
$html4
<table><tr><td>PASS<input type="text" name="pass" size="10"></td>
<td><input type="submit" value="���M"></td></tr></table>
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
	my ($msg) = @_;		# �G���[���b�Z�[�W�擾
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
# //// GIF,JPG �T�C�Y�擾 /////////////////////////////////////////////////////////////

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
