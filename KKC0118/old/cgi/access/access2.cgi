#!/usr/local/bin/perl
#       �����Ȃ����������Ă���v���o�C�_�̢perl����ꂪ�g�p�ł���
#         �p�X���w�肵�܂��B��ʓI�ɢ#!/usr/local/bin/perl��ő��v

#=======================================================================================
#				access2 Version 98.1
#=======================================================================================
#���Ώۃy�[�W�̃^�C�g��
$hptitle = "�L���o�ϊ��������i��y���@�A�N�Z�X���";

#���w�i�̐F
$haikei = "#ffffff";

#�������̐F
$moji = "#666666";

#���e��ڕ����̐F
$daiiro = "#7bc0d7";

#���\��ڕ����̐F
$daimokumoji = "#63a7cf";

#�������N�̐F
$midoku = "#ff8080";

#�����ǃ����N�̐F
$kidoku = "#ff0080";

#���\���̐F
$hyouback = "#999999";

#���\�荀�ڂ̐F
$hyoudai = "#e1f5ff";

#���\���̐F
$hyounai = "#fffff0";

#�����t���b�V���b��
$byou = "30";

#��CGI�̂t�q�k
$cgiurl = "http://www.keizai-kassei.net/cgi/access/access2.cgi";

#���O���t�̃t�@�C���ۑ��ꏊ
$bargif = "http://www.keizai-kassei.net/cgi/access/bar.gif";

#���O�t�@�C��
$datafile = 'access2.txt';
#----------------------------------------------------------
#�_�~�[�Ŏg�p����摜�igif����jpg�`���j
$imgfile = 'z.gif';
#----------------------------------------------------------
#���Ȃ��̍ŒZ�̃A�h���X
#����y�[�W����̃����N���J�E���g���Ȃ�����
#���̏ꍇ��http://www2q.meshnet.or.jp/~terra/
$homepage = 'http://www.keizai-kassei.net/';
#----------------------------------------------------------
#�ő�L�^��
$max = 1000;
#----------------------------------------------------------
#���v�\�����̐ݒ�
#���ԑѕʓ��v�𓖓��P���ɂ��� 'yes' / 'no'
$timeflag = 'no';
#----------------------------------------------------------
#�z�X�g��
$hostvew = 32;
#----------------------------------------------------------
#�u���E�U�@�\�����Ȃ��ꍇ�͂O�ɂ���
$agentvew = 30;
#----------------------------------------------------------
#�����N��@�\�����Ȃ��ꍇ�͂O�ɂ���
$linkvew = 30;
#----------------------------------------------------------
#�O���t�̍ő�\����
$graphvew = 200;
#----------------------------------------------------------
#���̑��̃����N��i�u�b�N�}�[�N���j�̏W�v 'yes' / 'no'
$nolink = 'yes';
#----------------------------------------------------------
#�N�b�L�[���g�p���Đ��m�Ȑl�����J�E���g���� 'yes' / 'no'
$cookieFlag = 'yes';
#----------------------------------------------------------
#�N�b�L�[���i�[���閼�O��ݒ肷��
$CookieName = 'access2';
#=======================================================================================
#			�����ݒ肪�K�v�Ȃ̂͂����܂łł��B
#=======================================================================================
#���t�Ǝ������擾���āA���ׂĂQ���ɓ��ꂷ��
$ENV{'TZ'} = "JST-9"; #���{���Ԃɐݒ�
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900;
	$month = sprintf("%02d",$mon + 1);
	$mday = sprintf("%02d",$mday);
	#���t�����̃t�H�[�}�b�g�𐮂��܂�
	$youbi = ('��','��','��','��','��','��','�y') [$wday];
	$date_now = "$year�N$month��$mday��($youbi)";

$QUERY_DATA = $ENV{'QUERY_STRING'};
if ($QUERY_DATA eq 'vew') {
	&data_read;
	$datacount = @DATA;
	foreach $line (@DATA) {
		($da,$ho,$ag,$hr,$dm) = split(/\,/,$line);
		chop($dm);
		$dm += 0;
		if (!($hr =~ /^http:\/\//i)) { $hr = ''; }
		if ($hr =~ /$homepage/i) { $hr = ''; }
		if ($hr eq '') { $hr = '���̑��i�u�b�N�}�[�N���j' }
		#���t���Ƃ̏W�v
		$DA{$da}++;
		#���Ԃ��Ƃ̏W�v
		if ($timeflag eq 'yes') {
			if ($date_now eq $da) { $seaflag = 1; } else { $seaflag = 0; }
		} else { $seaflag = 1; }
		if ($seaflag == 1) {
			$TI{$dm}++;
		}
		#�z�X�g���Ƃ̏W�v
		$HO{$ho}++;
		if ($agentvew != 0) {
			#�u���E�U���Ƃ̏W�v
			$AG{$ag}++;
		}
		if ($linkvew != 0) {
			#�����N�悲�Ƃ̏W�v
			if ($nolink eq 'yes' || $hr ne '���̑��i�u�b�N�}�[�N���j') { $HR{$hr}++; }
		}
	}
	#���בւ�
	foreach (keys %DA) {
		$dummy = "$_\,$_\,$DA{$_}";
		push(@DATE,$dummy);
		if ($datemax < $DA{$_}) { $datemax = $DA{$_}; }
	}
	@DATE = sort(@DATE); @DATE = reverse(@DATE);
	($s,$d,$datecount) = split(/\,/,$DATE[0]);
	foreach (keys %TI) {
		$s = sprintf("%04d",$_);
		$dummy = "$s\,$_\,$TI{$_}";
		push(@TIME,$dummy);
		if ($timemax < $TI{$_}) { $timemax = $TI{$_}; }
	}
	@TIME = sort(@TIME);
	foreach (keys %HO) {
		$s = sprintf("%04d",$HO{$_});
		$dummy = "$s\,$_\,$HO{$_}";
		push(@HOST,$dummy);
		if ($hostmax < $HO{$_}) { $hostmax = $HO{$_}; }
	}
	@HOST = sort(@HOST); @HOST = reverse(@HOST);
	if ($agentvew != 0) {
		foreach (keys %AG) {
			$s = sprintf("%04d",$AG{$_});
			$dummy = "$s\,$_\,$AG{$_}";
			push(@AGENT,$dummy);
			if ($agentmax < $AG{$_}) { $agentmax = $AG{$_}; }
		}
		@AGENT = sort(@AGENT); @AGENT = reverse(@AGENT);
	}
	if ($linkvew != 0) {
		foreach (keys %HR) {
			$s = sprintf("%04d",$HR{$_});
			$dummy = "$s\,$_\,$HR{$_}";
			push(@HREFLINK,$dummy);
			if ($linkmax < $HR{$_}) { $linkmax = $HR{$_}; }
		}
		@HREFLINK = sort(@HREFLINK); @HREFLINK = reverse(@HREFLINK);
	}
	#�g�s�l�k�𐶐�
	print "Content-type: text/html\n\n";
	print "<html><head><title>access</title>\n";
	print "</head>\n";
	print "<body bgcolor=$haikei text=$moji link=$midoku vlink=$kidoku>\n";
	print "<div align=center><center>\n";
	print "<p align=center><font size=6>$hptitle</font><br>";
	print "���݂̃T���v���� $datacount �A�N�Z�X�ł��B";
	if ($cookieFlag eq 'yes') { print "<br>�d���A�N�Z�X��r���������m�Ȑl����\\�����Ă��܂��B"; }
	print "</p>\n";
	print "<font size=5 color=$daiiro>�����ʓ��v</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>���t</font></td>\n";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>�J�E���g</font></td>\n";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>�|�C���g</font></td>\n";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>�O���t</font></td></tr>\n";
		foreach $dummy (@DATE) {
			($s,$d,$c) = split(/\,/,$dummy);
			if ($d =~ /\d{4}\�N\d{2}\��\d{2}\��/) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($datemax != 0) { $chrlen = int($c / $datemax * $graphvew); }
				}
				print "<tr><td bgcolor=$hyounai>$d</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai><img src=$bargif width=$chrlen height=10></td></tr>\n";
			}
		}
		print "</table>\n";
		print "<br><font size=5 color=$daiiro>�����ԕʓ��v</font>\n";
		if ($timeflag eq 'yes') {
			print "$date_now\n";
		}
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>����</font></td>";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>�J�E���g</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>�|�C���g</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>�O���t</font></td></tr>\n";
		foreach $dummy (@TIME) {
			($s,$d,$c) = split(/\,/,$dummy);
			if ($d < 1) { $d = 0; }
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					if ($timeflag eq 'yes') {
						if ($datecount > 0) { $per = $c / $datecount * 100; }
						else { $per = 0; $chrlen = 0; }
					} else {
						$per = $c / $datacount * 100;
					}
					if ($timemax != 0) { $chrlen = int($c / $timemax * $graphvew); }
				}
				print "<tr><td align=center bgcolor=$hyounai>$d ��</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "�@"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
		}
		print "</table><br>\n";
		print "<font size=5 color=$daiiro>���z�X�g���v</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>�z�X�g��</font></td>";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>�J�E���g</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>�|�C���g</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>�O���t</font></td></tr>\n";
		$vew = 1;
		foreach $dummy (@HOST) {
			($s,$h,$c) = split(/\,/,$dummy);
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($hostmax != 0) { $chrlen = int($c / $hostmax * $graphvew); }
				}
				print "<tr><td bgcolor=$hyounai>$h</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "�@"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
			$vew++;
			if ($vew > $hostvew) { last; }
		}
		print "</table>\n";
	if ($agentvew != 0) {
		print "<br><font size=5 color=$daiiro>���u���E�U���v</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai><font color=$daimokumoji>�u���E�U</font></td>";
		print "<td align=center bgcolor=$hyoudai   width=\"70\"><font color=$daimokumoji>�J�E���g</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>�|�C���g</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>�O���t</font></td></tr>\n";
		$vew = 1;
		foreach $dummy (@AGENT) {
			($s,$a,$c) = split(/\,/,$dummy);
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($agentmax != 0) { $chrlen = int($c / $agentmax * $graphvew); }
				}
				print "<tr><td bgcolor=$hyounai>$a</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print " <td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "�@"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
			$vew++;
			if ($vew > $agentvew) { last; }
		}
		print "</table>\n";
	}
	if ($linkvew != 0) {
		print "<br><font size=5 color=$daiiro>�������N�擝�v</font>\n";
		print "<table width=\"600\" border=\"1\" bordercolor=\"$hyouback\" bgcolor=\"#FFFFFF\" cellspacing=\"2\"><tr>\n";
		print "<td align=center bgcolor=$hyoudai width=\"260\"><font color=$daimokumoji>�����N��</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"70\"><font color=$daimokumoji>�J�E���g</font></td>";
		print "<td align=center bgcolor=$hyoudai  width=\"70\"><font color=$daimokumoji>�|�C���g</font></td>";
		print "<td align=center bgcolor=$hyoudai width=\"200\"><font color=$daimokumoji>�O���t</font></td></tr>\n";
		$vew = 1;
		foreach $dummy (@HREFLINK) {
			($s,$a,$c) = split(/\,/,$dummy);
			if ($c != 0) {
				if ($datacount == 0) {
					$per = 0;
					$chrlen = 0;
				} else {
					$per = $c / $datacount * 100;
					if ($linkmax != 0) { $chrlen = int($c / $linkmax * $graphvew); }
				}
				print "<tr> <td bgcolor=$hyounai>";
				print "<a href=$a>$a</a>";
				print "</td>\n";
				print "<td align=right bgcolor=$hyounai>$c</td>\n";
				print "<td align=right bgcolor=$hyounai>\n";
				printf "%10.2f\n" , $per;
				print "\%</td>\n";
				print "<td bgcolor=$hyounai>";
				if ($chrlen < 1) { print "�@"; }
				else {
					print "<img src=$bargif width=$chrlen height=10>\n";
				}
				print "</td></tr>\n";
			}
			$vew++;
			if ($vew > $linkvew) { last; }
		}
		print "</table>\n";
	}
	print "</center></div>\n";
	print "<p align=right><font size=-1><a href=http://www2.inforyoma.or.jp/~terra/>Access2 by Terra</a></font></p>\n";
	print "</body></html>\n";
	exit;
} else {
	if ($cookieFlag eq 'yes') {
		$ENV{'TZ'} = "GMT"; 
		($c_sec,$c_min,$c_hour,$c_mday,$c_mon,$c_year,$c_wday,$c_yday,$c_isdst) = localtime(time + 3 * 86400);
		$cookies = $ENV{'HTTP_COOKIE'};
		@pairs = split(/;/,$cookies);
		foreach $pair (@pairs) {
			($name, $value) = split(/=/, $pair);
			$name =~ s/ //g;
			$DUMMY{$name} = $value;
		}
		@pairs = split(/,/,$DUMMY{$CookieName});
		foreach $pair (@pairs) {
			($name, $value) = split(/\!/, $pair);
			$COOKIE{$name} = $value;
		}
	}
	if ($COOKIE{'date'} ne $date_now) {
		&data_read;
		$datacount = @DATA;
		$hostadd = &domain_name;
		$agent = $ENV{'HTTP_USER_AGENT'};
		$agent =~ s/,/./g;
		$agent =~ s/\; Yahoo\! JAPAN Version Windows 95\/NT CD\-ROM Edition 1\.0\.//;
		$hreflink = $QUERY_DATA;
		$value = "$date_now\,$hostadd\,$agent\,$hreflink\,$hour\n";
		while ($datacount >= $max) {
			pop(@DATA);
			$datacount = @DATA;
		}
		unshift(@DATA,$value);
		&data_save;
		if ($cookieFlag eq 'yes') {
			$c_year += 1900;
			$c_sec  = sprintf("%02d",$c_sec);
			$c_min  = sprintf("%02d",$c_min);
			$c_hour = sprintf("%02d",$c_hour);
			$c_mday = sprintf("%02d",$c_mday);
			$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') [$c_wday];
			$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') [$c_mon];
			$date_gmt = "$youbi, $c_mday\-$month\-$c_year $c_hour:$c_min:$c_sec GMT";
			$cook = "date\!$date_now";
			print "Set-Cookie: $CookieName=$cook; expires=$date_gmt\n";
		}
	}
	print "Content-type: image/jpeg\n\n";
	open(IMG, "$imgfile") || die "Can't open: $dir/$img";
	print $_ while (<IMG>);
	close(IMG);
	exit;
}
#=======================================================================================
sub domain_name {
	local($addr) = $ENV{'REMOTE_ADDR'};
	local($_) = gethostbyaddr(pack("C4",split(/\./,$addr)),2);
	if ($_ eq '') { $_ = $addr; }
	else {
		if (/.+\.(.+)\.(.+)\.(.+)$/) { $_ = "\*\.$1\.$2\.$3"; }
		elsif (/.+\.(.+)\.(.+)$/) { $_ = "\*\.$1\.$2"; }
		elsif (/.+\.(.+)$/) { $_ = "\*\.$1"; }
		else { $_ = "on the internet"; }
	}
	$_;
}
#=======================================================================================
sub data_read {
	if (open(DB,"$datafile")) {
		@DATA = <DB>;
		close(DB);
	}
}
#=======================================================================================
sub data_save {
	$tmpfile = 'access2.tmp';
	foreach (1 .. 10) {
		unless (-f $tmpfile) { $tmpflag = 1; last; }
		$tmpflag = 0;
		sleep(1);
	}
	if ($tmpflag == 1) {
		$tmp_dummy = "$$\.tmp";
		if (!open(TMP,">$tmp_dummy")) { &error(bad_tmpfile); }
		close(TMP);
		chmod 0666,$tmp_dummy;
		if (!open(TMP,">$tmp_dummy")) { &error(bad_tmpfile); }
		print TMP @DATA;
		close(TMP);
		foreach (1 .. 10) {
			unless (-f $tmpfile) {
				if (!open(TMP,">$tmpfile")) { &error(bad_tmpfile); }
				close(TMP);
				rename($tmp_dummy,$datafile);
				unlink $tmpfile;
				$tmpflag = 1;
				last;
			}
			$tmpflag = 0;
			sleep(1);
		}
		if (-f $tmp_dummy) { unlink $tmp_dummy; }
	}
	$tmpflag;
}
