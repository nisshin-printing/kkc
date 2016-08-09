#!/usr/local/bin/perl

#��������������������������������������������������������������������
#��  DAY COUNTER-EX v3.2 (2001/05/13)
#��  Copyright(C) KENT WEB 2001
#��  webmaster@kent-web.com
#��  http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'DayX v3.2';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# [�^�O�̏������̗�]
#   ���J�E���g��     <img src="count/dayx.cgi?gif">
#   �{���̃J�E���g�� <img src="count/dayx.cgi?today">
#   ����@�@�V	     <img src="count/dayx.cgi?yes">
#
# [���v�^�����ꗗ������]
#    http://www.host.xxx/~user/count/dayxmgr.cgi
#
# [�`�F�b�N�̂����� (�u���E�U����Ō�� ?check �����Čďo���j]
#    http://www.host.xxx/~user/count/dayx.cgi?check
# -------------------------------------------------------------------
# [�f�B���N�g���\���� (���ʓ��̓p�[�~�b�V����) ]
#
#    public_html / index.html ... �����ɃJ�E���^��ݒu
#        |
#        +-- count / dayx.cgi    [755]
#               |    dayxmgr.cgi [755]
#               |    gifcat.pl   [755]
#               |    dayx.dat    [666]
#               |    day.dat     [666]
#               |    mon.dat     [666]
#               |    blue.gif
#               |    red.gif
#               |
#               +-- gif1 / 1.gif 2.gif ... 0.gif
#               |
#               +-- gif2 / 1.gif 2.gif ... 0.gif
#               |
#               +-- lock [777] /

#============#
#  �ݒ荀��  #
#============#

# �摜�A�����C�u�����捞��
require './gifcat.pl';

# ���J�E���g���̌���
$digit1 = 6;

# �{/����J�E���g���̌���
$digit2 = 3;

# ���O�t�@�C��
$logfile = "./dayx.dat";

# �����L�^�t�@�C��
$dayfile = "./day.dat";

# �����L�^�t�@�C��
$monfile = "./mon.dat";

# ���J�E���g���pGIF�摜�̃f�B���N�g��
$gifdir1 = "./gif1";

# �{/����J�E���g���pGIF�摜�̃f�B���N�g��
$gifdir2 = "./gif2";

# �t�@�C�����b�N�@�\
#   0 : ���Ȃ�
#   1 : ���� (symlink�֐���)
#   2 : ���� (mkdir�֐���)
$lockkey = 0;

# ���b�N�t�@�C����
$lockfile = "./lock/dayx.lock";

# �J�E���^�̋@�\�^�C�v
#   0 : ���J�E���g���s�v�i����^�{���̂݁j
#   1 : �W���^�C�v
$type = 1;

# IP�A�h���X�̓�d�J�E���g�`�F�b�N
#   0 : �`�F�b�N���Ȃ�
#   1 : �`�F�b�N����
$ip_check = 0;

#============#
#  �ݒ芮��  #
#============#

# ����������
$mode = $ENV{'QUERY_STRING'};

# �X�V�n�����łȂ��Ȃ�� 1-2 �b�҂�����
if ($type == 1 && $mode eq "yes") { sleep(2); }
elsif ($type == 1 && $mode eq "today") { sleep(1); }
elsif ($type == 0 && $mode eq "yes") { sleep(1); }

# �`�F�b�N���[�h
if (!$mode || $mode eq 'check') { &check; }

# ���b�N�J�n
$lockflag=0;
if (($type && $mode eq "gif" && $lockkey) || (!$type && $mode eq "today" && $lockkey)) { $lockflag=1; &lock; }

# �L�^�t�@�C������ǂݍ���
open(IN,"$logfile") || &error("LK");
$data = <IN>;
close(IN);

# �L�^�t�@�C���𕪉�
($key,$yes,$today,$count,$youbi,$ip) = split(/<>/, $data);

# �������擾
$ENV{'TZ'} = "JST-9";
($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
$year += 1900;
$mon++;
$thisday = (Sun,Mon,Tue,Wed,Thu,Fri,Sat) [$wday];
if ($mon < 10) { $mon = "0$mon"; }
$date = "$year\/$mon";

# IP�`�F�b�N
$flag=0;
if ($ip_check) {
	$addr = $ENV{'REMOTE_ADDR'};
	if ($addr eq "$ip") { $flag=1; }
}

# �{���̃J�E���g�����L�[�ɃJ�E���g�A�b�v
if ((!$flag && $type && $mode eq 'gif') || (!$flag && !$type && $mode eq 'today')) {

	$count++;

	## ��������
	if ($key eq "$mday") {
		$today++;

		# ���O���t�H�[�}�b�g
		$data = "$key<>$yes<>$today<>$count<>$thisday<>$addr<>\n";
	}
	## ��������
	else {
		# ���O���t�H�[�}�b�g
		$data = "$mday<>$today<>1<>$count<>$thisday<>$addr<>\n";

		&day_count;
		&mon_count;
	}

	# ���O���X�V
	open(OUT,">$logfile") || &error("LK");
	print OUT $data;
	close(OUT);
}

# ���b�N����
if ($lockflag) { &unlock; }

# �J�E���^�摜�o��
&count_view;
exit;

#-------------------#
# �J�E���^�o�͏���  #
#-------------------#
sub count_view {
	while (length($count) < $digit1) { $count = '0' . $count; }
	while (length($today) < $digit2) { $today = '0' . $today; }
	while (length($yes) < $digit2) { $yes = '0' . $yes; }

	@outfile=();

	if ($mode eq "gif") {
		@array = split(//, $count);
		foreach (@array) {
			push(@outfile,"$gifdir1\/$_\.gif");
		}
	}
	elsif ($mode eq "today") {
		@array = split(//, $today);
		foreach (@array) {
			push(@outfile,"$gifdir2\/$_\.gif");
		}
	}
	elsif ($mode eq "yes") {
		@array = split(//, $yes);
		foreach (@array) {
			push(@outfile,"$gifdir2\/$_\.gif");
		}
	}

	# �摜�o��
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat'gifcat(@outfile);
}

#--------------#
#  ���b�N����  #
#--------------#
sub lock {
	local($retry) = 5;
	# 3���ȏ�Â����b�N�͍폜����
	if (-e $lockfile) {
		($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 180) { &unlock; }
	}
	# symlink�֐������b�N
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('Lock is busy'); }
			sleep(1);
		}
	# mkdir�֐������b�N
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('Lock is busy'); }
			sleep(1);
		}
	}
}

#--------------#
#  ���b�N����  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
}

#------------------------#
#  �����J�E���g���̏���  #
#------------------------#
sub day_count {
	# ���O�̓����L�[���{���̓�����������Ό����ς�����Ɣ��f����
	if ($mday < $key) {
		open(DB,">$dayfile") || &error("LK");
		close(DB);
	}
	# �����ł̏���
	else {
		if ($key < 10) { $key = "0$key"; }
		open(DB,">>$dayfile") || &error("LK");
		print DB "$mon\/$key \($youbi\)<>$today<>\n";
		close(DB);
	}
}

#------------------------#
#  ���ԃJ�E���g���̏���  #
#------------------------#
sub mon_count {
	# ���߂ẴA�N�Z�X�̏ꍇ
	if (-z $monfile) { $mons[0] = "$date<>$today<>\n"; }
	else {
		open(IN,"$monfile") || &error("LK");
		@mons = <IN>;
		close(IN);

		# ���O�z��̍ŏI�s�𕪉�
		$mons[$#mons] =~ s/\n//;
		($y_m,$cnt) = split(/<>/,$mons[$#mons]);

		# ��������
		if ($y_m eq "$date") {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
		}
		# ��������
		#�i���O�z��̍ŏI�s�� $date�ƈقȂ�΁A�����ς����Ɣ��f����j
		else {
			$cnt = $cnt + $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
			push(@mons,"$date<>0<>\n");
		}
	}

	# ���O�t�@�C�����X�V
	open(OUT,">$monfile") || &error("LK");
	print OUT @mons;
	close(OUT);
}

#--------------#
#  �G���[����  #
#--------------#
sub error {
	if ($lockflag && $_[0] eq "LK") { &unlock; }

	@err_gif = ('47','49','46','38','39','61','2d','00','0f','00','80','00','00','00','00','00','ff','ff','ff','2c', '00','00','00','00','2d','00','0f','00','00','02','49','8c','8f','a9','cb','ed','0f','a3','9c','34', '81','7b','03','ce','7a','23','7c','6c','00','c4','19','5c','76','8e','dd','ca','96','8c','9b','b6', '63','89','aa','ee','22','ca','3a','3d','db','6a','03','f3','74','40','ac','55','ee','11','dc','f9', '42','bd','22','f0','a7','34','2d','63','4e','9c','87','c7','93','fe','b2','95','ae','f7','0b','0e', '8b','c7','de','02','00','3b');

	print "Content-type: image/gif\n\n";
	foreach (@err_gif) {
		$data = pack('C*',hex($_));
		print $data;
	}
	exit;
}

#------------------#
#  �`�F�b�N���[�h  #
#------------------#
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>DAY COUNTER-EX</title></head>\n";
	print "<body>\n<h2>Check Mode</h2>\n<UL>\n";

	# ���O�t�@�C���̃p�X�m�F
	if (-e $logfile && -e $dayfile && -e $monfile) {
		print "<LI>���O�t�@�C���̃p�X : OK!\n";
	}
	unless (-e $logfile) { print "<LI>���O�t�@�C�� $logfile ������܂���B\n"; }
	unless (-e $dayfile) { print "<LI>���O�t�@�C�� $dayfile ������܂���B\n"; }
	unless (-e $monfile) { print "<LI>���O�t�@�C�� $monfile ������܂���B\n"; }

	# ���O�t�@�C���̃p�[�~�b�V�����i�ǂ݂��݁j
	if (-r $logfile && -r $dayfile && -r $monfile) {
		print "<LI>���O�t�@�C���̓ǂ݂��݃p�[�~�b�V���� : OK!\n";
	}
	unless (-r $logfile){ print "<LI>���O�t�@�C�� $logfile
					 �̓ǂ݂��݃p�[�~�b�V�������s���ł��B\n"; }
	unless (-r $dayfile) { print "<LI>���O�t�@�C�� $dayfile
					 �̓ǂ݂��݃p�[�~�b�V�������s���ł��B\n"; }
	unless (-r $monfile) { print "<LI>���O�t�@�C�� $monfile
					 �̓ǂ݂��݃p�[�~�b�V�������s���ł��B\n"; }

	# ���O�t�@�C���̃p�[�~�b�V�����i�������݁j
	if (-w $logfile && -w $dayfile && -w $monfile) {
		print "<LI>���O�t�@�C���̏������݃p�[�~�b�V���� : OK!\n";
	}
	unless (-w $logfile) { print "<LI>���O�t�@�C�� $logfile
					�̏������݃p�[�~�b�V�������s���ł��B\n"; }
	unless (-w $dayfile) { print "<LI>���O�t�@�C�� $dayfile
					�̏������݃p�[�~�b�V�������s���ł��B\n"; }
	unless (-w $monfile) { print "<LI>���O�t�@�C�� $monfile
					�̏������݃p�[�~�b�V�������s���ł��B\n"; }

	# �摜�f�B���N�g���P�̃p�X�m�F
	if (-d $gifdir1) { print "<LI>gif1�f�B���N�g���̃p�X : OK!\n"; }
	else { print "<LI>gif1�f�B���N�g��������܂���B: $gifdir1\n"; }

	# �摜�f�B���N�g���Q�̃p�X�m�F
	if (-d $gifdir2) { print "<LI>gif2�f�B���N�g���̃p�X : OK!\n"; }
	else { print "<LI>gif2�f�B���N�g��������܂���B: $gifdir2\n"; }

	# ���b�N�f�B���N�g��
	print "<LI>���b�N�`���F";
	if ($lockkey == 0) { print "���b�N�ݒ�Ȃ�\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }

		$lockfile =~ s/(.*)[\\\/].*$/$lockdir = $1/e;
		print "<LI>���b�N�f�B���N�g���F$lockdir\n";

		if (-d $lockdir) { print "<LI>���b�N�f�B���N�g���̃p�X�FOK\n"; }
		else { print "<LI>���b�N�f�B���N�g���̃p�X�FNG �� $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FOK\n";
		} else {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FNG �� $lockdir\n";
		}
	}

	# �摜�`�F�b�N(1)
	foreach (0 .. 9) {
		$flag=0;
		$giffile = $_ . '.gif';
		unless (-e "$gifdir1\/$giffile") {
			$flag=1;
			print "<LI>$gifdir1\/$giffile ������܂���B\n";
		}
	}
	if (!$flag) { print "<LI>gif1�f�B���N�g����GIF�摜 : OK!\n"; }

	# �摜�`�F�b�N(2)
	foreach (0 .. 9) {
		$flag=0;
		$giffile = $_ . '.gif';
		unless (-e "$gifdir2\/$giffile") {
			$flag=1;
			print "<LI>$gifdir2\/$giffile ������܂���B\n";
		}
	}
	if (!$flag) { print "<LI>gif2�f�B���N�g����GIF�摜 : OK!\n"; }

	# ���쌠�\���F�폜�֎~
	print "<P><small><!-- $ver -->\n";
	print "- <a href=\"http://www.kent-web.com/\">Day Counter-EX</a> -\n";
	print "</small>\n</UL>\n</body></html>\n";
	exit;
}
