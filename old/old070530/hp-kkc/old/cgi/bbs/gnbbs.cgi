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
#����̓t���[�f�ނł��B
#�]�ځE���p�ړI�̗��p�̍ۂɂ́A���[�������肢���܂��B
#
#******************************************************************************
#1�s�ڂ�perl�̃f�B���N�g���w��́A�T�[�o�ɂ���ĈقȂ�܂��B
#�ڂ����́A�Ǘ��҂ɂ��������������B
#******************************************************************************
#��ʐݒ�
#
#�^�C�g��
$title = "�L���o�ϊ�������y���@�f����";

#BODY�^�O
$bodytag='<body text=#092875 bgcolor=#ffffff link=303060 vlink=303060 alink=8080cf background="../../image/back.gif">';

#�y�[�W�㕔�ɕ\������薼
$pagetop = '<div align=center><TABLE><TBODY><TR><TD bgcolor="#666666" height="3"></TD></TR><TR><TD bgcolor="#666666" width="353" align="center" height="70"><IMG src="../../image2.gif" width="258" height="17" border="0"><IMG src="../../image3.gif" width="311" height="29" border="0"></TD></TR><TR><TD height="3" bgcolor="#666666"></TD></TR></TBODY></TABLE></div><br><br>';

#�z�[���y�[�WURL
# �ݒ肵�Ȃ��ꍇ�ƃ����N�͕\������܂���B
$homeback = "http://www.keizai-kassei.net/";

#******************************************************************************
#���b�Z�[�W���̐F

#�薼�����̔w�i�F
$msgcl1 = "#adcae7";

#���O�����̔w�i�F
$msgcl2 = "#bed5eb";

#���ԕ\�������̔w�i�F
$msgcl3 = "#cedff0";

#�{���̔w�i�F
$msgcl4 = "#e4eef8";

#******************************************************************************
#���͗��̐F

#���O���͗��̔w�i�F
$entercl1 = "#e4eef8";

#E-Mail���͗��̔w�i�F
$entercl2 = "#cedff0";

#URL���͗��̔w�i�F
$entercl3 = "#bed5eb";

#�薼���͗��̔w�i�F
$entercl4 = "#adcae7";

#���b�Z�[�W���͗��̔w�i�F
$entercl5 = "#9dbfe1";

#�폜�L�[���͗��̔w�i�F
$entercl6 = "#adcae7";

#******************************************************************************
#
#�X�^�C���V�[�g�ݒ�
# input�͓��͂���{�b�N�X�Abutton��Submit�Ȃǂ̃{�^����\���܂��B
# �g�p���Ȃ��ꍇ�́A�폜���Ă��������B
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
#�}�X�^�[�p�X���[�h
# ���ׂĂ̋L���̍폜�L�[�Ɏg���܂��B
$adminpass = "npo";

#���O�ۑ��t�@�C����
$logfile = "./log.dat";

#�e�L���̃��O�ۑ��̍ő吔
$maxlog = 50;

#�P�y�[�W�ɕ\������ő�L����
$maxpage = 10;

#���O���͂������ꍇ�̖��O
# �ݒ肵�Ȃ��Ɩ��O�̓��͂��K�{�ƂȂ�܂��B
$newname = "";

#�薼���͂������ꍇ�̑薼
# �ݒ肵�Ȃ��Ƒ薼�̓��͂��K�{�ƂȂ�܂��B
$newsubject = "����";


#�����ݒ�
sub timeset{$timeword = "$month/$day $hour:$min";}
#                        ~~~~~~~~~~~~~~~~~~~~
#�Q�� " �̊ԂɎ����\���̃t�H�[�}�b�g�������܂�
#�ȉ��̕ϐ��������ƁA�\�������Ƃ���
#���̒l���\������܂�
# $year  �N
# $month ��
# $day   ��
# $hour	 ��
# $min   ��
# $sec   �b
# $week  �j��

#�����\���̃[���⊮�̗L��
# 10�ȉ���\������Ƃ��� 04 �̂悤�ɓ��� 0 ��ǉ����܂��B
# ���̋@�\���g���ꍇ�� 1 ���A�g��Ȃ��ꍇ�� 0 ���B
$spzero[0] = 0;#���̕⊮
$spzero[1] = 0;#���̕⊮
$spzero[2] = 0;#���̕⊮
$spzero[3] = 1;#���̕⊮
$spzero[4] = 0;#�b�̕⊮

#�j���̐ݒ�
# ���`�y�̏��Ԃł��B
@weekday = ("Sun","Mon","Tue","Wed","Thr","Fri","Sat");

#******************************************************************************

#�\�[�X��IP/�z�X�g����\������Ƃ���1��ݒ�B
$ipindicate = 1;

#jcode.pl�̃p�X
$jcode = './jcode.pl';

#�A�N�Z�X���ۂ�����z�X�g������͂��܂��B
# @denyhost = ("anonymizer","cache*.*",�c�c);
# ���̂悤�ɓ��͂��Ă����܂��B
# ��̂悤�ɁA���C���h�J�[�h���g�p�ł��܂��B
@denyhost = ();

#�g�p��������^�O�������܂��B
# �S�ĕs���̏ꍇ�́A
# @permittag = ();
# �Ƃ��Ă��������B
@permittag = ("a","i","b","font");


#URL�̏������݂Ɏ����I�Ƀ����N��\��Ȃ�1��ݒ�B
$autolink = 1;

#�ʃy�[�W����̓��e���֎~����ꍇ��1��ݒ�B
$referercheck = 0;

#��d���e���֎~����ꍇ��1��ݒ�B
$double = 1;	

#�O���j�b�W�W��������̂���i�b�P�ʁj
# �����ݒ�� +32400�b = 9���Ԃ̓��{���Ԑݒ�ł��B
$areatime = 32400;

#******************************************************************************

#jcode.pl�̓ǂ݂���
require $jcode;
srand;

#�f�[�^�󂯎��
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

#���ϐ��擾
$ip = $ENV{'REMOTE_ADDR'};
$host = gethostbyaddr(pack("C4", split(/\./, $ip)), 2);
$host ||= $ENV{'REMOTE_HOST'};
$host ||= $ip;
$referer=$ENV{'HTTP_REFERER'};
$script=$ENV{'SCRIPT_NAME'};

#�A�N�Z�X���ۃ`�F�b�N
foreach (@denyhost){
	if ($host =~ /$_/i){
		&error("���Ȃ��̎g�p���Ă���z�X�g����̃A�N�Z�X�͋֎~����Ă��܂��B");
		last;
		}
	}

#�f�[�^�`�F�b�N
$page||=0;

if ($act eq "write"){
	$a1 = $msg;
	$a1 =~ s/[\r\n\t]//g;
	$act = "" if $a1 eq "";
	}

#id�̒l�Ŗ��ߕ���

if ($act eq "delete"){&delete;}

#�N�b�L�[�擾
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
	&error("���O����͂��Ă��������B") if $name eq "";
	&error("�薼����͂��Ă��������B") if $subject eq "";
	&error("�ʃy�[�W����̓��e�͋֎~����Ă��܂��B") if ($referercheck == 1) && ($referer !~ /$script/i);
	while(1){if (!(chomp($msg))){last;}}

	#���^�O�ȊO�𖳌��ɂ���
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

	#URL�ɂ͎����I�Ƀ����N���s��
	if (($msg !~ /<img/i) && ($autolink)){
		$msg =~ s/(http:\/\/[a-zA-Z0-9\.\/\-+#_?~&%=^\@:;]+)/<A HREF="$1">$1<\/A>/ig;
		}
	$msg =~ s/\n/<br>/g;
	$subject =~ s/</&lt;/g;
	$subject =~ s/>/&gt;/g;
	if ($url eq "http://"){$url = "";}

	#�t�@�C���ǂ݂���
	open (IO,"+<$logfile");
	eval{flock(IO,2)};
	@log = <IO>;
	@y2 = split(/<>/,$log[0]);
	#��d�������݂̋֎~
	if (($double == 1) && ($msg eq $y2[7])){close(IO);&error("��d���e�͋֎~����Ă��܂��B");}

	#���O�ǉ�
	$y2[0]++;
	unshift(@log,"$y2[0]<>$name<>$email<>$url<>" . time() . "<>$delkey<>$subject<>$msg<>$ip/$host<>\n");
	pop(@log) if $#log >= $maxlog;

	#��������
	truncate(IO,0);
	seek(IO,0,0);
	print IO @log;
	close(IO);

	if ($log[$maxpage] ne ""){$nextflag = 1;}
	}else{
	#�K�v�ȕ����������O�ǂ�
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

#�N�b�L�[��������
print "Set-Cookie:name=$name; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
print "Set-Cookie:email=$email; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
print "Set-Cookie:url=$url; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
print "Set-Cookie:delkey=$delkey; expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";

&hphead;

#�����Ń��b�Z�[�W���̓t�H�[����\�����Ă��܂��B
# form�^�O�Einput�^�O�Etextarea�^�O�͊�{�I�ɂ͕ύX���Ȃ��ł��������B
# input�^�O��size�Etextarea�^�O��cols/rows�͕ύX���Ă�OK�ł��B

print <<EOD;
<form method="post" action="./gnbbs.cgi">
<table border="0" align="center" cellspacing="0" cellpadding="5">
<tr bgcolor=$entercl1><td align="right">���O : <input type="text" class="input" name="name" size="20" value="$name">&nbsp;</td></tr>
<tr bgcolor=$entercl2><td align="right">E-Mail : <input type="text" class="input" name="email" size="20" value="$email">&nbsp;</td></tr>
<tr bgcolor=$entercl3><td align="right">URL : <input type="text" class="input" name="url" size="20" value="$url">&nbsp;</td></tr>
<tr bgcolor=$entercl4><td align="left">&nbsp;���� : <input type="text" class="input" name="subject" size="30">&nbsp;</td></tr>
<tr bgcolor=$entercl5><td align="left">&nbsp;���e : <br>
&nbsp;<textarea name="msg" class="input" cols="50" rows="6"></textarea>&nbsp;</th></tr>
<tr bgcolor=$entercl6><td align="left">&nbsp;�폜�L�[ : <input type="password" class="input" name="delkey" size="10" value="$delkey"></td></tr>
<tr bgcolor=$entercl6><td align="center"><input type="submit" class="button" value="���M"><input type="reset" class="button" value="���~"></td></tr>
</table>
<input type="hidden" name="act" value="write">
<input type="hidden" name="page" value="0">
</form>
EOD
#�����܂�

if ($homeback ne ""){
	print "<div align=\"center\"><a href=\"$homeback\">&lt;&lt;Back To Home</a></div>\n";
	}
print "<br><br>";


#�L���\��
for (0 .. $maxpage-1){
	last if $log[$_] eq "";
	@y2 = split(/<>/,$log[$_]);

	#���Ԍ`��
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

	#�����ŋL����\�����܂��B
	#�^�O������g��ł���̂ŁA�o�͂����HTML���悭�������������B
	#
	#���ϐ�������
	# $msgcl1~4	���b�Z�[�W�w�i�F�i�`���Őݒ�j
	# $y2[0]	�L���ԍ�
	# $y2[1]	���e�Җ�
	# $y2[2]	���[���A�h���X
	# $y2[3]	�z�[���y�[�WURL
	# $y2[6]	�薼
	# $y2[7]	�{��
	# $y2[8]	IP/�z�X�g��
	# $a1		���[���E�z�[���y�[�W�̃����N
	# $timeword	���e����

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
	#�����܂�
	}

#NEXT/BACK�̃{�^���\��
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


#�폜�t�H�[���\��
print <<EOD;
</tr>
</table>
<table align=center>
<form method="post" action="./gnbbs.cgi">
<tr><td bgcolor=$msgcl1 align=center>
�L���ԍ��F<input type="text" class="input" name="chdel" size=4>
�폜�L�[�F<input type="password" class="input" name="pass" size=9>
</td>
</tr>
<tr>
<td bgcolor=$msgcl2 align=center>
<input type="submit" class="button" value="�L���폜">
<input type="hidden" name="act" value="delete">
</td>
</tr>
</form>
</table>
EOD

&hpfoot;
#******************************************************************************
sub delete{
#�L���폜

#���̓f�[�^�`�F�b�N
&error("�L���ԍ����w�肵�Ă��������B") if ($chdel eq "") || ($chdel =~/[a-zA-Z]/);
&error("�폜�L�[����͂��Ă��������B") if $pass eq "";

#�폜
my $errmsg = "�폜�L�[���Ԉ���Ă��܂��B";
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
	$errmsg = "$chdel�Ԃ̋L�����폜���܂����B";
	}

#�\��
&error($errmsg);
}

#******************************************************************************
sub error{
#�G���[�\��
&hphead;
print <<EOD;
<div align=center>
<br><br><br>
<b>$_[0]</b>
<br><br><br>
<a href="./gnbbs.cgi">�߂�</a>
<br><br><br><br>
</div>
EOD
&hpfoot;
}
#******************************************************************************
sub hphead{
#�w�b�_�\��
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
#�t�b�^�\��
#
#���쌠�\�����������Ƃ��ւ��܂��B
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
