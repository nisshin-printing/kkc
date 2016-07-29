#!/usr/local/bin/perl

#��������������������������������������������������������������������
#��  DAY COUNTER-EX MANAGER v3.2 (2001/05/13)
#��  Copyright(C) KENT WEB 2001
#��  webmaster@kent-web.com
#��  http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'DayX v3.2'; # �o�[�W�������
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#��������������������������������������������������������������������

#============#
#  �ݒ荀��  #
#============#

# ���O�t�@�C��
$logfile = "./dayx.dat";

# �����L�^�t�@�C��
$dayfile = "./day.dat";

# �����L�^�t�@�C��
$monfile = "./mon.dat";

# �W�v�ꗗ����̖߂��
$home = "../index.html";

# �W�v�ꗗ�̃^�C�g����
$title = "�A�N�Z�X�W�v�ꗗ";

# �^�C�g�������F
$t_color = "#008080";

# �O���t�摜
$graph1 = "./blue.gif";
$graph2 = "./red.gif";

# ���ԃO���t���̒���
# 1�������� 4����50�`100  5����200�`500���x
$mKEY = 50;

# ���v�O���t���̒���
# 1������ 2����1�`2  3����5�`10  4����30�`60���x
$dKEY = 2;

# body�^�O
$body = '<body bgcolor="#F1F1F1" text="#000000" link="#0000FF" vlink="#0000FF">';

#============#
#  �ݒ芮��  #
#============#

# ���O�t�@�C���ǂݍ���
open(IN,"$logfile") || &error("Open Error : $logfile");
$data = <IN>;
close(IN);
($day,$yes,$to,$all,$week,$ip) = split(/<>/, $data);

# ���Ԏ擾
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
$date = sprintf("%02d/%02d (%s) ",$mon+1,$mday,$week[$wday]);
$D_Y  = sprintf("%04d/%02d",$year+1900,$mon+1);

# �����A�N�Z�X�t�@�C����ǂݍ���
open(IN,"$dayfile") || &error("Open Error : $dayfile");
@DayFile = <IN>;
close(IN);
push(@DayFile,"$date<>$to<>\n");

# ���ԃA�N�Z�X�t�@�C����ǂݍ���
open(IN,"$monfile") || &error("Open Error : $monfile");
@MonFile = <IN>;
close(IN);

$under = pop(@MonFile);
$under =~ s/\n//g;
($Y,$C) = split(/<>/, $under);
if ($Y eq "$D_Y") {
	$C2 = $C + $to;
	push(@MonFile,"$Y<>$C2<>\n");
} else {
	push(@MonFile,"$D_Y<>$to<>\n");
}

# HTML��\��
&header;
print <<"EOM";
<TABLE cellspacing="0" cellpadding="0" border="0">
<TR>
<TD bgcolor="#B4B4B4" width="50" height="20" align="center" nowrap>
<A href="$home" style="font-size:10pt; color:#000000; text-decoration: none">�߂�</A></TD></TR>
</TABLE>
<div align="center">
<hr width="70%" size=2 noshade>
<h2>$title</h2>
<hr width="70%" size=2 noshade>
<br><br>
<table><tr><td>
<OL>
  <LI><a href="#day">�����A�N�Z�X�ꗗ</a>
  <LI><a href="#mon">�����A�N�Z�X�ꗗ</a>
</OL>
</td></tr></table>
</div>
<br>
<table width="100%">
<tr><td bgcolor="#6D6D6D">�@<font color="#F9B606">��</font>
  <font color="#FFFFFF"><b><a name="day">�����A�N�Z�X�ꗗ</a></b></font>
</td></tr></table>
<br>
<blockquote>
<table border=0 cellpadding=1 cellspacing=0>
<!--
<tr>
  <th bgcolor=#D5FFD5>����</th><th bgcolor=#D5FFD5>�A�N�Z�X��</th>
  <th bgcolor=#D5FFD5>�O���t</th>
</tr>
-->
EOM

$flag = 0;
foreach (@DayFile) {
	chop;
	($m_d,$dcnt) = split(/<>/);

	# �O���t�����w��
	$width = $dcnt / $dKEY;
	$width = int($width);

	# ������
	$dcnt = &filler($dcnt);

	# �F�ύX
	$m_d =~ s/Sat/<font color=blue>Sat<\/font>/;
	$m_d =~ s/Sun/<font color=red>Sun<\/font>/;

	print "<tr><td nowrap>$m_d</td><td align=right> &nbsp; $dcnt &nbsp; </td>\n";
	print "<td><img src=\"$graph2\" width=$width height=5></td></tr>\n";
}

print <<"EOM";
</table></blockquote>
<br><br>
<table width="100%">
<tr><td bgcolor="#6D6D6D">�@<font color="#F9B606">��</font>
<font color="#FFFFFF"><b><a name="mon">�����A�N�Z�X�ꗗ</a></b></font>
</td></tr></table>
<br>
<blockquote>
<table border=0 cellpadding=2 cellspacing=0>
<tr>
  <th bgcolor=#D5FFD5 nowrap>�N��</th><th bgcolor=#D5FFD5 nowrap>����<br>�A�N�Z�X</th>
  <th bgcolor=#D5FFD5 nowrap>1������<br>�A�N�Z�X</th><th bgcolor=#D5FFD5>�O���t</th>
</tr>
EOM

$flag = 0;
foreach (@MonFile) {
	($y_m,$mcnt) = split(/<>/);
	($year,$mon) = split(/\//, $y_m);

	if ($_ eq "$MonFile[$#MonFile]") {
		if ($day == 1) { $avr = ' - '; }
		else {
			$waru = $day - 1;
			$avr = int (($C / $waru) +0.5);
			$avr = &filler($avr);
		}
	} else {
		$lastday = &LastDay("$year","$mon");
		$avr = int (($mcnt / $lastday) +0.5);
		$avr = &filler($avr);
	}

	# �O���t�����w��
	$width = $mcnt / $mKEY;
	$width = int($width);

	# ������
	$mcnt = &filler($mcnt);

	if ($year ne "$year2") { print "<tr><td colspan=4><hr size=1></td></tr>\n"; }

	print "<tr><th nowrap>$y_m</th><td align=right> &nbsp; $mcnt &nbsp; </td>";
	print "<td align=right>$avr &nbsp; </td>";
	print "<td><img src=\"$graph1\" width=$width height=10></td></tr>\n";

	$year2 = $year;
}

## ���쌠�\���i�폜���ϋ֎~�j
print <<"EOM";
</table>
</blockquote>
<div align="center">
<hr>
<small><!-- $ver -->
- <a href="http://www.kent-web.com/" target="_top">Day Counter-EX</a> -
</small>
</div>
</body>
</html>
EOM
exit;

#----------------#
#  ���̖����v�Z  #
#----------------#
sub LastDay {
	local($year, $mon) = @_;
	local($lastday);

	$lastday = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31) [$mon - 1]
	+ ($mon == 2 && (($year % 4 == 0 && $year % 100 != 0) ||
	$year % 400 == 0));

	return $lastday;
}

#--------------#
#  HTML�w�b�_  #
#--------------#
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>$title</title>
<STYLE TYPE="text/css">
<!--
body,tr,td,th { font-size: 10pt; }
small { font-size: 9pt; }
h2 { font-size:16pt; color:$t_color }
-->
</STYLE>
</head>
$body
EOM
}

#----------------#
#  ���悫�菈��  #
#----------------#
sub filler {
	local($_) = $_[0];
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	return $_;
}

#--------------#
#  �G���[����  #
#--------------#
sub error {
	&header;
	print <<"EOM";
<div align="center">
<hr width="70%">
<h3>ERROR !</h3>
<h4>$_[0]</h4>
<hr width="70%">
</div>
</body>
</html>
EOM
	exit;
}
