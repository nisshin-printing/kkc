#!/usr/local/bin/perl
#-----------------------------------------------------------------------------#
#	�g�s�b�N�X�����p�b�f�h
#	�g�s�b�N�X�`���̃f�[�^��\������
#	create by Yuji Tominaga
#	
#	Version 3.1.4
#	2002-12-02:	�ҏW��ɏ��Ԃ��ς��o�O���C��	
#       2002-11-30:     �ҏW��ʂ��C��
#	
#	version 3.1.3
#	2002-11-7:	�R�����g��,������ƕ\������Ȃ��Ȃ�o�O���C��
#	2002-9-8:	�������͂���Ă��Ȃ��Ƃ��ɑ��M����ƃG���[�ɂȂ�悤�ɂ���
#	2002-9-6:	���j���[��ʂ̕���
#	
#	version 3.1.2
#	2002-9-6:	�摜����pl�̓����A����
#	2002-9-6:	�C���^�[�t�F�C�X�̕ύX�E����
#	2002-8-19:	�摜�A�b�v����
#	2002-8-3:	���Z�b�g�㎩���I�Ƀp�[�~�b�V������ύX
#	2002-8-3:	�e�T���[�h�i���Z�b�g�R�}���h�j����
#	2002-8-3:	�ҏW�I����̖߂���ǉ��A�ҏW�A�폜�̕���_�܂Ŗ߂邱�Ƃɂ���
#	2002-8-2:	���Z�b�g�R�}���hmode=5��ݒu
#	2002-8-2:	�\�������̕ύX
#	2002-8-1:	��{�\������
#
###############################################################################
#
#	�ݒu���@
#
#	
#	$logPath	���O�t�@�C���ւ̃p�X�ł��B���[�g�Ƀt�@�C����u���܂��傤�B
#	$htmlPath	�����N���̂g�s�l�k�t�@�C���ւ̃p�X�ł��B���[�g�Ƀt�@�C��
#				��u���܂��傤�B
#	$commentPath	�R�����g�o�͎��ɂЂȌ`�ƂȂ�g�s�l�k�t�@�C���ւ̃p�X
#					�ł��B���[�g�ɒu���܂��傤�B
#
#	�ȏ�̃t�@�C���͑S�ăp�[�~�b�V����666�Ɏw�肵�Ă��������B
#
#	topics.cgi
#	passCheck.cgi
#	�́A�p�[�~�b�V����755
#
#	log.pl
#	jcode.pl
#	�́A�p�[�~�b�V����644�ł��܂��܂���
#
#
#	�g�s�l�k�t�@�C���̐ݒ�̎d���́A�T���v���̂g�s�l�k�t�@�C�����Q�l�ɂ���
#	���������B
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
###	���ݒ�
###	CGI�̊���ݒ肵�܂�
###	��{�I�Ȑݒ�͂��̕��������ŏI�����܂�

my $logPath		= "../logfile.csv";								#���O�f�[�^�ւ̃p�X
my $htmlPath	= "../katudo.html";								#�g�b�v�y�[�W�̃X�L��
my $commentPath	= "../comment.html"; 							#���e�\���p�̃X�L��
my $upload_dir	= "../image";									#�t�@�C���̃A�b�v���[�h��
my $htmlOutPath	= "../index.html";								#�g�b�v�o�̓f�[�^
my $outDir		= "../";										#�t�@�C���̏o�͈ʒu
my $outImageDir = "image";										#�C���[�W�t�@�C���̏o�͐�


my $maxWidth	= "200";										#�ő�\����
my $maxHeight	= "200";										#�ő�\������

######################################################


#�O�����W���[���̓ǂݍ���
require './jcode.pl';
require './log.pl';
require 'bimage.pl';

use CGI;

$query	= new CGI;

#�e�폈��
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
#	�匩�o�����͉��
sub inputScreen
{
	my($sec, $min, $hour, $mday, $mon, $year)	= localtime();			#���[�J���^�C���̎擾
	$year	= $year + 1900;												#�N�̌v�Z
	$mon	= $mon  + 1;												#���̌v�Z
	
	#���̓t�H�[���̕\��
print <<HTML_HEAD;
Content-type: text/html


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>���̓t�H�[��</TITLE>
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
						<TD align="center" style="font-weight : bold;color : #ff6f6f;">�g�s�b�N�̓���</TD>
					</TR>
					<TR>
						<TD bgcolor="#ffffff" align="center"><BR>
HTML_HEAD

print "<form action=\"topics.cgi\" method=\"POST\">\n";
print "���t�F<input type=\"text\" name=\"year\" value=\"$year\">�N";
print "<select name=\"month\">"; 
for(my $i = 1; $i <= 12; $i++){
	if($i eq "$mon"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>��\n";
print "<select name=\"day\">";
for(my $i = 1; $i <= 31; $i++){
	if($i eq "$mday"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>��<br><br>\n";
print "<div align=\"left\">�@�@�@�@�^�C�g���F<input type=\"text\" name=\"title\" size=\"50\"></div><br>";
print "<div align=\"left\">�@�@�{��:</div>\n";
print "<textarea name=\"comment\" rows=\"7\" cols=\"50\" maxlength=\"50\"></textarea><br><br>\n";
print "<input type=\"submit\" value=\"�@���@�M�@\">�@<input type=\"reset\" value=\"�@��@���@\"><br><br>\n";
print "</form>\n";

print <<HTML_FUT;
						</TD>
					</TR>
				</TBODY>
				</TABLE>
				<BR>
				<A href="$home">�߂�</A></FORM>
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
#	���͂��ꂽ�f�[�^��ҏW���ĕۑ�
sub editData
{
	#�g�s�b�N�X�Ǘ��pID�̐���
	my @key		= localtime();
	my $key		= sprintf("%02d%02d%02d%02d%02d",$key[4]+1,$key[3],$key[2],$key[1],$key[0]);
	my $id		= $key;									#�������ꂽID
	my $year	= $query->param('year');				#�N
	my $month	= $query->param('month');				#��
	my $day		= $query->param('day');					#��
	my $date	= "$year�N$month��$day��";				#���t�f�[�^
	
	#�G���[�`�F�b�N
	#�{���̓��̓f�[�^���`�F�b�N����
	if($query->param('title') eq "" and $query->param('comment') eq ""){
		&errorOut("�L���ɉ������͂���Ă��܂���B<br>\n�^�C�g���ƃR�����g�̓��͕͂K�{�ł�<br>\n");
		exit;
	}

	my $title	= $query->param('title');				#�^�C�g��
	$title		=~ s/,/�C/g;							#�����Ă��锼�p�J���}��S�đS�p��
	my $comment	= $query->param('comment');				#�R�����g
	$comment	=~ s/,/�C/g;							#�R�����g�ɓ����Ă��锼�p�J���}��S�đS�p��
	my @commentData	= &log::openFile("$commentPath");	#�R�����g�o�͗p�t�@�C���ւ̃p�X
	$comment	=~ s/\r\n/<br>/g;						#���s�R�[�h��<br>�^�O�ɕύX
	$comment	.= "\n";								#�Ō�ɉ��s�R�[�h���P�����ǉ�
	my $outLog	= "$id,$date,$title,$comment";			#�o�͗p���O�f�[�^�̍쐬
	my $outFileName	= "../$id.html";					#�o�̓t�@�C���̃t�@�C����
	my $dataFlag	= 0;								#�������ʃt���O
		
	#���O�f�[�^�̏�������
	&log::writeLog("$logPath","$outLog");
	&convert;											#�V�����f�[�^��ǉ�����
	
	#�f�[�^�̌���pert2
	#�{���̏o��
	foreach $line (@commentData){
		my $buf = $line;
		if($buf =~ /<!--start1-->/ or $buf =~ /<!--start2-->/){
			$dataFlag = 1;
		}elsif($buf =~ /<!--end1-->/ or $buf =~ /<!--end2-->/){
			$dataFlag = 0;
		}

		#�o�͉�ʂ̍���
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
##	�ҏW�����̕\��
sub showend
{
#�I����ʕ`��
print <<EOH;
Content-type: text/html\n\n

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>�o�^����</title>
</head>
<body>
<TABLE width="100%" height="100%" cellpadding="0" cellspacing="0">
  <TBODY>
    <TR><TD>
<div align="center">
<font color="#ff8080">�o�^�������܂���</font><br><br>
�g�s�b�N�X�̃g�b�v�y�[�W���J��<br>�X�V�{�^���������Đ������ǉ��ł��Ă���<br>
���Ƃ��m�F���Ă�������<br><br>
EOH

print "<a href=\"$htmlOutPath\">�z�[���y�[�W������</a><br>\n";
print "�i�K���X�V�{�^���������Ă��������j<br><br>\n";
print "<a href=\"menu.html\">�ҏW�ɖ߂�</a>\n";
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
##	�f�[�^�`����ϊ�
sub convert
{
	local @htmlData		= &log::openFile("$htmlPath");		#�g�s�l�k�̃X�L���f�[�^
	local @logData		= &log::openFile("$logPath");		#���O�t�@�C���̃f�[�^
	local $outHtml;											#�o�͗p�̂g�s�l�k�f�[�^(�^�C�g���\��)
	local $outComment;										#�o�͗p�̂g�s�l�k�f�[�^(�{���\��)
	local $outFileName;										#�o�̓t�@�C����
	local $flag		= '1';									#�����p�t���O
	local @dataBuf;											#�f�[�^�̉��ۑ���
	local $html1,$html2,$html3;								#�g�s�l�k�f�[�^�̃w�b�_�A�t�b�^�A�{��
	local $id,$date,$title,$comment;						#���O�f�[�^�̐؂�o��
	local $syoriFlag	= 'true';
		
	#�f�[�^�𔽓]������
	@logData	= reverse @logData;
		
	#�f�[�^�̌���(�ȑO�̃f�[�^�ƐV�K�̃f�[�^��g�ݍ��킹��
	#�^�C�g���o�͂̍쐬
	#(����ύX����ۂ͂��̂������ύX����)
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
	
	
	#���O�f�[�^�ƃX�L���̍���
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
##	�f�[�^�폜�������
sub deleteScreen
{
	my @logData				= &log::openFile("$logPath");						#���O�t�@�C�����J��		
	
	#�폜�����p�t�H�[��
print <<HTML_HEAD;
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>�폜�t�H�[��</title>
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
	<td width="20%" style="font-weight : bold;color : #ff6f6f;" algin="center"></td><td width="30%" style="font-weight : bold;color : #ff6f6f;" algin="center">���t</td><td width="50%" style="font-weight : bold;color : #ff6f6f;" algin="center">�^�C�g��</td>
</tr>
HTML_HEAD

#���O�f�[�^�̐؂�o��
foreach $line (@logData){
	unless($line =~ m/\+/){
		my ($key, $hi, $dai, $com) = split(/,/, $line);
		print "<tr>\n";
		print "<td width=\"20%\" bgcolor=\"#ffffff\"><input type=\"radio\" name=\"key\" value=\"$key\"></td><td width=\"30%\" bgcolor=\"#ffffff\">$hi</td><td width=\"50%\" bgcolor=\"#ffffff\">$dai</td>\n"; 
		print "</tr>\n";
	}
}

print "<tr>\n";
print "<td colspan=\"3\" align=\"center\" bgcolor=\"#ffffff\"><input type=\"submit\" value=\"���@�M\">�@�@�@�@�@<input type=\"reset\" value=\"�߁@��\" onClick=\"pageBack()\"></td>\n";
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
##	�Ł[���̍폜����
sub deleteData
{
	#�G���[�`�F�b�N
	#�L�����I������Ă��邩�ǂ���
	if($query->param('key') eq ""){
		&errorOut("�폜����L�����I������Ă��܂���B<br>\n�폜����L����I�����Ă�������\n");
		exit;
	}
	
	$id				= $query->param('key');				#�폜����t�@�C���̂h�c
	my	@htmlData	= &log::openFile("$htmlOutPath");	#�f�[�^�t�@�C��
	my	@logData	= &log::openFile("$logPath");		#���O�t�@�C��
	my	$outHtml,$outLog;								#�o�͗p�f�[�^
	unlink("../$id.html");								#�{���t�@�C�����폜����
	
		
	#�폜����s�̌���
	foreach $line (@htmlData){
		unless($line =~ /<!--$id-->/){
			$outHtml	= "$outHtml$line";
		}
	}
	
	#���O�t�@�C������폜����s���������폜
	foreach $line (@logData){
		unless($line =~ /$id/){
			$outLog	= "$outLog$line";
		}
	}
	
	#�폜�����f�[�^����������
	open OUT, ">$htmlOutPath";
	print OUT "$outHtml";
	close(OUT);
	
	open OUT, ">$logPath";
	print OUT "$outLog";
	close(OUT);
}




#######################################################
##	selectScreen()
##	�f�[�^�I�����
sub selectScreen
{
	my @logData				= &log::openFile("$logPath");						#���O�t�@�C�����J��		
	
	#�L���ҏW�I��
print <<HTML_HEAD;
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>�L���I��</title>
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
	<td width="30%" style="font-weight : bold;color : #ff6f6f;" algin="center">���t</td><td width="50%" style="font-weight : bold;color : #ff6f6f;" algin="center">�^�C�g��</td>
</tr>
HTML_HEAD

#���O�f�[�^�̐؂�o��
foreach $line (@logData){
	unless($line =~ m/\+/){
		my ($key, $hi, $dai, $com) = split(/,/, $line);
		print "<tr>\n";
		print "<td width=\"30%\" bgcolor=\"#ffffff\">$hi</td><td width=\"70%\" bgcolor=\"#ffffff\"><a href=\"topics.cgi?mode=6&key=$key\">$dai</a></td>\n"; 
		print "</tr>\n";
	}
}

print "<tr>\n";
print "<td colspan=\"3\" align=\"center\" bgcolor=\"#ffffff\"><a href=\"javascript:history.back()\">�߁@��</a></td>\n";
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
##	�f�[�^�ҏW�p���
sub editScreen
{
		
	my @logData		= &log::openFile("$logPath");
	my $key			= $query->param('key');
	
	if($key eq ""){
		&errorOut("�ҏW����g�s�b�N���I������Ă��܂���");
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
	($year,$buf)	= split(/�N/,"$date");
	($mon,$buf)		= split(/��/,"$buf");
	($mday,$buf)	= split(/��/,"$buf");
	

print <<HTML_HEAD;
Content-type: text/html


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>���̓t�H�[��</TITLE>
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
						<TD align="center" style="font-weight : bold;color : #ff6f6f;" colspan="2">�g�s�b�N�̓���</TD>
					</TR>
					<TR>
						<TD bgcolor="#ffffff" align="center"><BR>
HTML_HEAD


print "<form action=\"topics.cgi\" method=\"POST\">\n<input type=\"hidden\" name=\"key\" value=\"$key\">";
print "���t�F<input type=\"text\" name=\"year\" value=\"$year\">�N";
print "<select name=\"month\">"; 
for(my $i = 1; $i <= 12; $i++){
	if($i eq "$mon"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>��\n";
print "<select name=\"day\">";
for(my $i = 1; $i <= 31; $i++){
	if($i eq "$mday"){
		print "<option value=\"$i\" SELECTED>$i\n";
	}else{
		print "<option value=\"$i\">$i\n";
	}
}
print "</select>��<br><br>\n";
print "<div align=\"left\">�@�@�@�@�^�C�g���F<input type=\"text\" name=\"title\" size=\"50\" value=\"$title\"></div><br>";
print "<div align=\"left\">�@�@�{��:</div>\n";
print "<textarea name=\"comment\" rows=\"7\" cols=\"50\" maxlength=\"50\">$comment</textarea><br><br>\n";
print "<input type=\"submit\" value=\"�@���@�M�@\">�@<input type=\"reset\" value=\"�@��@���@\"><br><br>\n";
print "</form>\n";
print "</td>\n";
print "</tr>\n";
print("</tbody>\n");
print("</table>\n");
print("<br><br>\n");

#�L���ǉ��{�^��
print("<TABLE width=\"400\" height=\"50\" cellpadding=\"1\" cellspacing=\"1\">\n");
print("<TR>\n");
print("<TD valign=\"middle\" align=\"center\" bgcolor=\"#caed9a\"><br>\n");
print "<form action=\"./topics.cgi\" method=\"POST\"><input type=\"hidden\" name=\"mode\" value=\"8\"><input type=\"hidden\" name=\"key\" value=\"$key\">\n";
print "<input type=\"submit\" value=\"�@�L���ǉ��@\">\n";
print "</form>\n";
print("</TD>\n");
print("</TR>\n");
print("</TABLE>\n");
print("<br><br>\n");


#�ڍ׋L���ҏW�I��
print "<TABLE width=\"400\" bgcolor=\"#56ACE0\" cellspacing=\"1\" cellpadding=\"5\">";

foreach $line (@minComments){
	my($id,$op,$fileName,$text) = split(/,/,$line);
	
	if($fileName ne ""){
		my($act, $type, $width, $height) = &bimage::getsize("../$fileName");		#�摜�̕��ƍ������擾
	
		#�摜�t�@�C���̃`�F�b�N
		if($act eq 'f'){
			errorOut("$type");
			print("$fileName");
			exit;
		}
	
		#�摜�T�C�Y�̃`�F�b�N
		if($width > $maxWidth and $width >= $height){
			#�ő�\�������傫�������Ƃ�
			#���̔䗦�ōő�\�����ȉ��ɔ[�߂�
			$outWidth	= int($width*($maxWidth/$width));
			$outHeight 	= int($height*($maxWidth/$width));
		}elsif($height > $maxWidth and $width < $height){
			#�ő�\���������傫�������Ƃ�
			#���̔䗦�ōő�\�������ȉ��ɔ[�߂�
			$outWidth	= int($width*($maxHeight/$height));
			$outHeight	= int($height*($maxHeight/$height));
		}else{
			#�ő�\���ȓ��Ȃ炻�̃T�C�Y�ɍ��킹��
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
	print("<input type=\"submit\" value=\"�ҁ@�W\">");
	print("</form>");
	print("</td>\n");
	print("<td align=\"center\">\n");
	print("<form action=\"topics.cgi\" method=\"POST\" enctype=\"multipart/form-data\">");
	print("<input type=\"hidden\" name=\"key\" value=\"$id\">\n");
	print("<input type=\"hidden\" name=\"subid\" value=\"$op\">");
	print("<input type=\"hidden\" name=\"mode\" value=\"10\">\n");
	print("<input type=\"submit\" value=\"��@��\">\n");
	print("</form>\n");
	print("</td></tr>\n");
}

print("</table>");


print("<br>\n");
print("<A href=\"$home\">�߂�</A></FORM>\n");
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
##	�摜���R�����g�̒ǉ����s���܂��B
sub addCommentScreen
{
	my $id		= $query->param('key');
	my $subid	= $query->param('subid');
	my $text	= "";
	my $baseName= "";
	@logData	= &log::openFile("$logPath");
	@outData	= ();
	
	#�f�[�^�̐؂�o��
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
	
		#�摜�T�C�Y�̃`�F�b�N
		if($width > $maxWidth and $width >= $height){
			#�ő�\�������傫�������Ƃ�
			#���̔䗦�ōő�\�����ȉ��ɔ[�߂�
			$outWidth	= int($width*($maxWidth/$width));
			$outHeight 	= int($height*($maxWidth/$width));
		}elsif($height > $maxWidth and $width < $height){
			#�ő�\���������傫�������Ƃ�
			#���̔䗦�ōő�\�������ȉ��ɔ[�߂�
			$outWidth	= int($width*($maxHeight/$height));
			$outHeight	= int($height*($maxHeight/$height));
		}else{
			#�ő�\���ȓ��Ȃ炻�̃T�C�Y�ɍ��킹��
			$outWidth	= $width;
			$outHeight	= $height;
		}
	}
	
#�摜���R�����g�ǉ���ʕ\��
print <<HTML_HEAD;
Content-type: text/html


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>�R�����g�ҏW�t�H�[��</TITLE>
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
						<TD align="center" style="font-weight : bold;color : #ff6f6f;">�摜���R�����g�ǉ�</TD>
					</TR>
					
HTML_FUT

if($baseName ne ""){
	print("<tr><td bgcolor=\"#ffffff\">\n");
	print("<img src=\"../$baseName\" width=\"$outWidth\" height=\"$outHeight\">\n");
	print("</td></tr>\n");
	print("<input type=\"hidden\" name=\"upfile2\" value=\"$baseName\">\n");
}

print('<tr><td bgcolor="#ffffff">�R�����g<br>'."\n");
print('<textarea name="comment" cols="40" rows="4">'."$text".'</textarea>'."\n");

print <<HTML_FUT2;
						</td>
					</tr>
					<tr>
						<td bgcolor="#ffffff">
							�摜�t�@�C��<input type="file" name="upfile" value="�Q�@��">
						</td>
					</tr>
					<tr>
						<td align="center" bgcolor="#ffffff">
							<input type="submit" value="���@ �M">�@�@�@<input type="reset" value="��@��">
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
##	���͂��ꂽ�摜���R�����g�f�[�^��ҏW����
sub addCommentEdit
{
	my $fileName	= $query->param('upfile');					#��荞�񂾃t�@�C���p�X
	my $textData	= $query->param('comment');					#��荞�񂾃R�����g
	$textData		=~ s/,/�C/g;								#�R�����g�ɓ����Ă��锼�p�J���}��S�đS�p��
	$textData		=~ s/\r\n/<br>/g;							#���s��<br>�ɕϊ�
	my $id			= $query->param('key');						#�e�L���̃L�[�R�[�h
	my $sub			= $query->param('subkey');					#�T�u�L�[�̃R�[�h
	my @buf			= ();										#�t�@�C���p�X�̕����ۑ�
	if($fileName ne ""){
		@buf			= split(/\\/,$fileName);
	}
	
	my $baseName	= "";										#�t�@�C�����̎擾
	my $readBuf		= "";										#�ꎞ�ۑ��p�̈�
	my ($buffer,$dataSize) = ();								#���p����ϐ���
	my $type		= "";										#�t�@�C���^�C�v���ʗp
	my $outData		= "";										#�o�̓f�[�^
	my $outLogData	= "";										#�o�̓��O�f�[�^
	
	#������
	$dataSize		= 1024;										#��x�Ɏ�荞�ރT�C�Y
	
	if($fileName eq "" and $query->param('upfile2') eq "" and $textData eq ""){
		errorOut("�������͂���Ă��܂���B<br>�R�����g���͉摜�ǂ��炩�͕K�����͂��Ă��������B<br>\n");
		exit;
	}
	
	if($fileName eq "" and $query->param('upfile2') ne ""){
		$baseName = $query->param('upfile2');
		my $a = "";
		($a,$baseName) = split(/\//,$baseName);
	}else{
		$baseName = $buf[$#buf];
	}
	
	#�t�@�C�������󂶂�Ȃ��Ƃ�
	#�t�@�C���̓]�����J�n����
	if($fileName ne "" and $baseName ne ""){
		$type = $query->uploadInfo($fileName)->{'Content-type'};	#�t�@�C���̎�ނ��擾
		
		#�t�@�C���`���擾�Ɏ��s���Ă���Ƃ��͊g���q���画�ʂ���
		if($type eq ""){
			($readBuf,$type) = split(/\./,$baseName);
		}
		
		#jpeg��gif�̓A�b�v���[�h�������܂�
		if($type eq "jpeg" or $type eq "gif" or $type eq "jpg"){
			
			#�t�@�C���̃f�[�^���R�s�[����
			while($readBuf = read($fileName, $buffer, $dataSize)){
				$outData .= $buffer;
			}
		
			#�t�@�C���̏�������
			open(OUTFILE, ">../$outImageDir/$baseName");
			binmode(OUTFILE);
			print(OUTFILE "$outData");
			close(OUTFILE);
			chmod(666,"$outImageDir/$baseName");
		}else{
			#�t�@�C���`���ɑΉ����Ă��Ȃ��Ƃ�
			&errorOut("�]���ł��Ȃ��t�@�C���`���ł����B");
			exit;
		}
	}
	
	#�o�̓��O�f�[�^�̍쐬
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

	#�f�o�b�O�o��
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
	
	#���O�f�[�^�̏�������
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
##	�f�[�^�o�͗p�ϊ�����
sub convert2
{
	my $key			= $query->param('key');
	my @commentData	= &log::openFile("$commentPath");			#�o�͗p�X�L���t�@�C���̃f�[�^
	my @logData		= &log::openFile("$logPath");				#���O�t�@�C���̃f�[�^
	my $flag		= '0';										#���쐧��p�t���O
	my $leftorright	= '0';										#���E�U�蕪���悤�̃t���O
											
	my $html1 = "";												#html�̃t�b�^����ۑ�����ϐ�
	my $outHtmlData = "";										#�o�͗p�f�[�^�t�@�C��
	my (@htmlHead, @htmlBody1, @htmlBody2);						#�X�L���t�@�C���̕����p�̈�
	my @outData = ();											#�o�̓f�[�^
	
	#�X�L���f�[�^�̉��H	
	foreach (@commentData){
		#�؂��萧��
		if($_ =~ m/<!--start1-->/ and $flag ne '1'){
			$flag = '1';										#body1�̐؂�o��
		}
		if($_ =~ m/<!--end1-->/ and $flag eq '1'){
			$flag = '0';										#body1�̐؂�o���I��
		}
		if($_ =~ m/<!--start2-->/ and $flag ne '2'){
			$flag = '2';										#body2�̐؂�o��
		}
		if($_ =~ m/<!--end2-->/ and $flag eq '2'){
			$flag = '3';										#body2�̐؂�o���I��
		}
		
		#�f�[�^�̕ۑ�
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
	
	
	#�f�[�^�̍���
	foreach $data (@logData){
		if($data =~ m/$key/){
			unless($data =~ m/\+/){
				#�w�b�_�����̍���
				foreach $line (@htmlHead){
					my($id,$date,$title,$comment) = split(/,/,$data);
					my $buf = $line;
					$buf =~ s/<!--title-->/$title/g;						#title�̏�������
					$buf =~ s/<!--date-->/$date/g;							#���t�̏�������
					$buf =~ s/<!--comment-->/$comment/g;					#�R�����g�̏�������
					$outHtmlData .= "$buf";									#�f�[�^���i�[����
				}
			}else{
				my($id,$op,$fileName,$text) = split(/,/,$data);
				if(@htmlBody2 eq "" || $leftorright eq '0'){
					#body1�̍���
					foreach $line (@htmlBody1){
						my $buf = $line;
						
						if($fileName ne ""){
							#�t�@�C���T�C�Y�̃`�F�b�N
							my($act, $type, $width, $height) = &bimage::getsize("../$fileName");
						
							#�摜�T�C�Y�̃`�F�b�N
							if($width > $maxWidth and $width >= $height){
								#�ő�\�������傫�������Ƃ�
								#���̔䗦�ōő�\�����ȉ��ɔ[�߂�
								$outWidth	= int($width*($maxWidth/$width));
								$outHeight 	= int($height*($maxWidth/$width));
							}elsif($height > $maxWidth and $width < $height){
								#�ő�\���������傫�������Ƃ�
								#���̔䗦�ōő�\�������ȉ��ɔ[�߂�
								$outWidth	= int($width*($maxHeight/$height));
								$outHeight	= int($height*($maxHeight/$height));
							}else{
								#�ő�\���ȓ��Ȃ炻�̃T�C�Y�ɍ��킹��
								$outWidth	= $width;
								$outHeight	= $height;
							}
						
							$buf =~ s/<!--image-->/<img src="$fileName" width="$outWidth" height="$outHeight">/g;	#�摜�f�[�^�̖��ߍ���
						}
						$buf =~ s/<!--text-->/$text/g;					#���R�����g����������
							push(@outData,$buf);							#�f�[�^�̊i�[
							$leftorright = '1';								#���E�̐U�蕪���t���O��ύX	
					}
				}else{
					#body2�̍���
					foreach $line (@htmlBody2){
						my $buf = $line;
				
						if($fileName ne ""){
							#�t�@�C���T�C�Y�̃`�F�b�N
							my($act, $type, $width, $height) = &bimage::getsize("../$fileName");
						
							#�摜�T�C�Y�̃`�F�b�N
							if($width > $maxWidth and $width >= $height){
								#�ő�\�������傫�������Ƃ�
								#���̔䗦�ōő�\�����ȉ��ɔ[�߂�
								$outWidth	= int($width*($maxWidth/$width));
								$outHeight 	= int($height*($maxWidth/$width));
							}elsif($height > $maxWidth and $width < $height){
								#�ő�\���������傫�������Ƃ�
								#���̔䗦�ōő�\�������ȉ��ɔ[�߂�
								$outWidth	= int($width*($maxHeight/$height));
								$outHeight	= int($height*($maxHeight/$height));
							}else{
								#�ő�\���ȓ��Ȃ炻�̃T�C�Y�ɍ��킹��
								$outWidth	= $width;
								$outHeight	= $height;
							}
						
							$buf =~ s/<!--image-->/<img src="$fileName" width="$outWidth" height="$outHeight">/g;	#�摜�f�[�^�̖��ߍ���
						}
						$buf =~ s/<!--text-->/$text/g;						#���R�����g����������
						push(@outData,$buf);								#�f�[�^���i�[
						$leftorright = '0';									#���E�U�蕪���t���O�̕ύX
					}
				}
			}
		}
	}
	
	#html�f�[�^�̍쐬
	foreach (@outData){
		$outHtmlData .= "$_";
	}
	$outHtmlData .= "$html1";												#html�̃t�b�^������������
	my $outFileName = "$outDir$key".'.html';
	
	#�f�[�^�̏����o��
	open(OUT, ">$outFileName");
	print OUT "$outHtmlData";
	close(OUT);
}



#######################################################
#	SdeleteComment
#	�摜�Ȃǂ̏���
sub deleteComment
{
	my $id			= $query->param('key');									#�L�������p�̎�L�[
	my $subid		= $query->param('subid');								#subID
	my @buf			= &log::openFile("$logPath");							#���O�t�@�C���̃f�[�^
	my @outLogData	= ();													#�o�͗p���O�f�[�^
		
	#���O�̍폜����
	foreach (@buf){
		#ID����v���Ȃ���Ζ������ɏ����o��
		unless($_ =~ /$id/){
			push(@outLogData, $_);
		}else{
			#ID����v���Ă�subID����v���Ȃ���Ώ����o��
			unless($_ =~ /$subid/){
				push(@outLogData, $_);
			}
		}
	}
	
	#���O�f�[�^�̏����߂�
	open(OUTFILE, ">$logPath");
	foreach (@outLogData){
		print(OUTFILE "$_");
	}
	close(OUTFILE);
	
	&convert2;
}

#######################################################
#	errorOut
#	�G���[�o��
sub errorOut
{
	#�����̏���
	my($outMessage) = @_;
	
print <<HTML_HEAD;
Content-type: text/html\n\n

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<title>�G���[</title>
</html>
<body>
<table width="100%" height="100%">
<tr><td align="center" valign="middle">
HTML_HEAD

print("$outMessage<br>\n");
print("<a href=\"./menu.html\">�ҏW��ʃg�b�v��</a>");

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
#	�R�����g�̕ҏW
sub editComment
{
	my $id		=	$query->param('key');				#��L�[
	my $year	= 	$query->param('year');				#�N
	my $month	= 	$query->param('month');				#��
	my $day		= 	$query->param('day');				#��
	my $date	= 	"$year�N$month��$day��";			#���t�f�[�^
	my $title	= 	$query->param('title');				#�^�C�g��
	$title		=~	s/,/�C/g;							#�����Ă��锼�p�J���}��S�đS�p��
	my $comment	= 	$query->param('comment');			#�R�����g
	$comment	=~ 	s/,/�C/g;							#�R�����g�ɓ����Ă��锼�p�J���}��S�đS�p��
	my @commentData	= 	&log::openFile("$commentPath");	#�R�����g�o�͗p�t�@�C���ւ̃p�X
	$comment	=~ 	s/\r\n/<br>/g;						#���s�R�[�h��<br>�^�O�ɕύX
	$comment	.= 	"\n";								#�Ō�ɉ��s�R�[�h���P�����ǉ�
	my $outLog	= 	"$id,$date,$title,$comment";		#�o�͗p���O�f�[�^�̍쐬
	my($html1,@html2,$html3) = ();						#���������f�[�^�̕ҏW��Ɨp
	
	my @logData		= &log::openFile("$logPath");		#���O�f�[�^�̎擾
	my @htmlData	= &log::openFile("$htmlPath");		#�X�L���f�[�^
	
	my @outLogData	= ();								#�o�̓f�[�^
	my $outTopData	= '';								#�g�b�v�o�̓f�[�^
	
	#���O�f�[�^���炢��Ȃ��f�[�^��؂�̂Ă�
	foreach (@logData){
		if(!($_ =~ /\+/) and $_ =~ /$id/){
			push(@outLogData,$outLog);
		}else{
			push(@outLogData,$_);
		}
	}
	
	@outLogData = sort(@outLogData);
	
	#���O�f�[�^�̏����߂�
	open(OUTFILE,">$logPath");
	foreach (@outLogData){
		print(OUTFILE "$_");
	}
	close(OUTFILE);
	
	my $flag = 0;
	
	#�w�b�_�E�{�f�B�[�E�t�b�^�ւ̕���
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
			
				#html�f�[�^��ҏW����
				$buf =~ s/<!--date-->/$date/;
				$buf =~ s/<!--title-->/<a href="$outPath">$title<\/a>/;
				$outBuf .= "<!--$subid-->$buf";
			}
		}
	}
	
	$outTopData = "$html1$outBuf$html3";
	
	#�g�b�v�̏o�̓f�[�^
	unlink("$htmlOutPath");
	open(OUTFILE, ">$htmlOutPath");
	print(OUTFILE "$outTopData");
	close(OUTFILE);
	
	#�o�̓f�[�^�̕ϊ�
	&convert2;
}



#######################################################
#	upDate()
#	�t�@�C���̑S�X�V���s��
sub upDate
{
	my @skinData	= &log::openFile("$htmlPath");				#�g�b�v�̃X�L���t�@�C����ǂݍ���
	my @logData		= &log::openFile("$logPath");				#���O�̃f�[�^
	
	my $flag		= 0;										#���䏈���t���O
	my $buf			= '';										#�ꎞ�ۑ��̈�
	my ($html1,$html3,@html2) = ();								#�w�b�_�Ȃǂ�ۑ�����
	my $outTopData	= '';										#�g�b�v�̏o�̓f�[�^
	
	#�w�b�_�E�{�f�B�[�E�t�b�^�ւ̕���
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
			
				#html�f�[�^��ҏW����
				$buf =~ s/<!--date-->/$date/;
				$buf =~ s/<!--title-->/<a href="$outPath">$title<\/a>/;
				$outBuf .= "<!--$subid-->$buf";
			}
		}
	}
	
	$outTopData = "$html1$outBuf$html3";
	
	#�g�b�v�̏o�̓f�[�^
	unlink("$htmlOutPath");
	open(OUTFILE, ">$htmlOutPath");
	print(OUTFILE "$outTopData");
	close(OUTFILE);
}

exit;
