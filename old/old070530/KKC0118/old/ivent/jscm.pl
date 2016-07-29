;#===============================================================================
;# ���傶��̂v�����H�[
;# ���ʃ��C�u���� ver.1.02	Copyright 1997-2001 JoJo's Web Lab.
;#
;#	 File:	jscm.pl
;#	 URL: http://www.starwars.jp/web/		 Email: webmaster@starwars.jp
;#
;#	 ���̃\�t�g�̓t���[�\�t�g�ł��B
;#	 �����E���p���p�͎��R�ł����A�Ĕz�z�͋֎~���܂��B
;#	 ���p�̍ۂ̑��Q�ɂ��Ă͈�ؕۏ؂������܂���B
;#===============================================================================
;# �X�V����
;#
;# 2001/11/27	ver.1.02	�C�O�T�[�o�ɂ�鎞���̌v�Z�������I�ɍs����悤�ɂ����B
;# 2001/07/24	ver.1.01	���b�Z�[�W�T�C�Y���傫������ꍇ�̃G���[���b�Z�[�W��ǉ������B
;#							Content-Length�w�b�_�̏o�͉ۃt���O��ǉ������B
;#							GET���\�b�h���̃G���[���b�Z�[�W�������������Ă����̂��C�������B
;# 2001/05/09	ver.1.00	���񃊃��[�X
;#
;#===============================================================================
package jscm;

# �{���C�u�����̃o�[�W����
$version   = '1.02';

# ���C�u������
$libname   = 'jscm.pl';

#
# �O���j�b�W�W��������̎���
#
# 	���{�ł�+9���ԁB�C�O�T�[�o�ł��T�}�[�^�C�����܂߂Ă���ŕ��ʂ͋z���ł���͂������A
#	����ł��덷������ꍇ�͂����ŕ␳����i�b�P�ʁj�B
#
$difftime  = 9*60*60;

#
# Content-Length�w�b�_�̏o�̓t���O
#
#	�����I�ɍL�����}�������T�[�o�œ����Ȃ��ꍇ�͂����� 0 �ɂ���
#
$cntlenflg = 1;

;#===============================================================================
;# �t�@�C���̌�납��̓ǂݍ���
;#		�����F�t�@�C����, �s��, �z��̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub tailFile
{
	my ($file, $num, $ref) = @_;
	my $size = 0;
	my $pos = 0;
	my $bufsize = 1024;
	my $buf = '';
	my $tmp = '';
	my @dat = ();
	open(FILE, $file) || outError(3, $file);
	eval { flock(FILE, 1); };
	binmode(FILE);
	$size = (-s FILE) / $bufsize;
	$pos += $size <=> ($pos = int($size));
	while ($pos--) {
		seek(FILE, $bufsize * $pos, 0);
		read(FILE, $buf, $bufsize);
		$buf .= $tmp;
		($tmp, @dat) = $buf =~ /[^\r\n]*\r?\n?/g;
		pop(@dat);
		unshift(@$ref, @dat);
		last if @$ref >= $num;
	}
	close(FILE);
	unshift(@$ref, $tmp);
	@$ref = @$ref[-$num .. -1] if (@$ref > $num);
}

;#===============================================================================
;# �t�@�C���ꗗ�̓ǂݍ���
;#		�����F�f�B���N�g����, �z��̃��t�@�����X, [�g���q]
;#		�ߒl�F�擾�f�B���N�g����
;#===============================================================================
sub readDir
{
	my ($dir, $ref, $exp) = @_;
	my $cnt = 0;
	my @tmp = ();
	opendir(DIR, $dir) || outError(4, $dir);
	@tmp = readdir(DIR);
	foreach (@tmp) {
		next if ($exp && index($_, ".$exp") < 0);
		next if ($_ eq '.' || $_ eq '..');
		push(@$ref, $_);
		$cnt++;
	}
	closedir(DIR);
	return $cnt;
}

;#===============================================================================
;# �t�@�C���̉�ʕ\��
;#		�����F�t�@�C����
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub printFile
{
	my ($file) = @_;
	my $size;
	$size = (-s $file);
	print "Content-Length: $size\n" if ($cntlenflg);
	print "\n";
	open(FILE, $file) || outError(3, $file);
	eval { flock(FILE, 1); };
	print $_ while (<FILE>);
	close(FILE);
}

;#===============================================================================
;# ���t������̍쐬
;#		�����F�t�H�[�}�b�g, [time�ϐ�], [����]
;#		�ߒl�F���t������
;#===============================================================================
sub makeDate
{
	my ($fmt, $tt, $diff) = @_;
	$tt = time unless ($tt);
	$diff *= 3600;
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = gmtime($tt + $difftime + $diff);
	$year += 1900;
	$mon  = sprintf("%02d", ++$mon);
	$mday = sprintf("%02d", $mday);
	$hour = sprintf("%02d", $hour);
	$min  = sprintf("%02d", $min);
	$day  = ('��','��','��','��','��','��','�y')[$wday];
	$fmt =~ s/yyyy/$year/;
	$fmt =~ s/mm/$mon/;
	$fmt =~ s/dd/$mday/;
	$fmt =~ s/w/$day/;
	$fmt =~ s/hh/$hour/;
	$fmt =~ s/nn/$min/;
	return $fmt;
}

;#===============================================================================
;# �t�H�[���̃f�R�[�h
;#		�����F�n�b�V���̃��t�@�����X, [GET���e�t���O], [�����R�[�h�Z�b�g]
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub getForm
{
	my ($ref, $get, $charset) = @_;
	my $str  = '';
	if ($ENV{'REQUEST_METHOD'} eq 'POST') {
		read(STDIN, $str, $ENV{'CONTENT_LENGTH'});
	} else {
		$str = $ENV{'QUERY_STRING'} if ($get);
	}
	foreach (split(/[&;]/, $str)) {
		my ($name, $value) = split(/=/);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/\t/ /d;
		jcode::convert(*value, $charset) if ($charset);
		$$ref{$name} = $value;
	}
}

;#===============================================================================
;# Last-Modified�w�b�_�̏�������
;#		�����F�t�@�C���p�X
;#		�ߒl�F�o�͂��ׂ�Last-Modified�w�b�_�̒l
;#===============================================================================
sub getLastModified
{
	my ($file) = @_;
	my ($mtime, $day, $mon);
	my $last = '';
	($mtime) = (stat($file))[9];
	my ($gsec, $gmin, $ghour, $gmday, $gmon, $gyear, $gwday, $gyday, $gisdst) = gmtime($mtime);
	$day = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$gwday];
	$mon = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$gmon];
	$last = sprintf("%s, %02d %s %04d %02d:%02d:%02d GMT",
			$day, $gmday, $mon, $gyear+1900, $ghour, $gmin, $gsec);
	return $last;
}

;#===============================================================================
;# ������HTML�^�O�̓W�J
;#		�����F"/"��؂�̋��^�O������, ���^�O�ꗗ�̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub getTag
{
	my ($str, $ref) = @_;
	$str =~ tr/A-Z/a-z/;
	@$ref = split(/\//, $str);
}

;#===============================================================================
;# HTML�^�O�̃`�F�b�N
;#		�����F�^�O���蕶����, ���^�O�ꗗ�̃��t�@�����X
;#		�ߒl�F�ϊ��㕶����
;#===============================================================================
sub checkTag
{
	my ($str, $ref) = @_;
	$$str =~ s/&/&amp;/g;
	$$str =~ s/"/&quot;/g;
	$$str =~ s/</&lt;/g;
	$$str =~ s/>/&gt;/g;
	foreach (@$ref) {
		$$str =~ s|&lt;$_&gt;|<$_>|gi;
		$$str =~ s|&lt;$_(\s+(.*?))&gt;|<$_$1>|gi;
		$$str =~ s|&lt;/(\s*$_\s*)&gt;|</$1>|gi;
		1 while $$str =~ s|(<$_\s+.+)&quot;(.+>)|$1"$2|g;
	}
}

;#===============================================================================
;# �����񒆂̉��s�R�[�h�� "\n" �ɕϊ�
;#		�����F������̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub encodeBr
{
	local($ref) = @_;
	$$ref =~ s/\\/\\\\/g;
	$$ref =~ s/\x0d\x0a/\\n/g;
	$$ref =~ s/\x0d/\\n/g;
	$$ref =~ s/\x0a/\\n/g;
}

;#===============================================================================
;# �����񒆂� "\n" �����s�R�[�h�ɕϊ�
;#		�����F������̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub decodeBr
{
	local($ref) = @_;
	$$ref =~ s/\\\\/\0/g;
	$$ref =~ s/\\n/\n/g;
	$$ref =~ s/\0/\\/g;
}

;#===============================================================================
;# �����񒆂�URL�A���[���A�h���X�������N�ɕϊ�
;#		�����F������̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub autoLink
{
	local($ref) = @_;
	$$ref =~ s/([^="',;]|^)((http|https|ftp):\/\/[\w\.\/\-+#?~&%=^\@:;]+)(["',]*)/$1<a href="$2">$2<\/a>$4/ig;
	$$ref =~ s/([\w\+-\.]+@[\w\+-]+\.[\w\+\.-]+)/<a href="mailto:$1">$1<\/a>/ig;
}

;#===============================================================================
;# �����񒆂̈��p�������}�[�N�A�b�v����
;#		�����F������̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub markQuote
{
	my ($ref) = @_;
	my $buf = '';
	my @tmp = ();
	@tmp = split(/\n/i, $$ref);
	foreach (@tmp) {
		$_ =~ s/(^( |�@)*(&gt;|��).*$)/<q>$1<\/q>/;
		$_ =~ s/^( |�@)*>(.*$)/<q>$1&gt;$2<\/q>/;
		$buf .= "$_\n";
	}
	$$ref = $buf;
}

;#===============================================================================
;# �������URL�G���R�[�h
;#		�����F������̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub encodeString
{
	local($ref) = @_;
	$$ref =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
}

;#===============================================================================
;# �������URL�f�R�[�h
;#		�����F������̃��t�@�����X
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub decodeString
{
	local($ref) = @_;
	$$ref =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
}

;#===============================================================================
;# �G���[��ʂ̕\��
;#		�����F[�G���[�ԍ�/�G���[���b�Z�[�W], [���l]
;#		�ߒl�F�Ȃ�
;#===============================================================================
sub outError
{
	my ($err, $etc) = @_;
	if	  ($err <	0) { $mes = "�����s���̃G���[�ł��B";										   }
	elsif ($err ==	1) { $mes = "�p�X���[�h���Ⴂ�܂��B";										   }
	elsif ($err ==	2) { $mes = "�K�v�ȏ��i$etc�j�ɕs��������܂��B"; 						   }
	elsif ($err ==	3) { $mes = "�t�@�C���G���[�ł��B[$etc]";									   }
	elsif ($err ==	4) { $mes = "�f�B���N�g���G���[�ł��B[$etc]";								   }
	elsif ($err ==	5) { $mes = "��d���e�͂ł��܂���B";										   }
	elsif ($err ==	6) { $mes = "�g�p�֎~�����i $etc �j���܂܂�Ă��܂��B"; 					   }
	elsif ($err ==	7) { $mes = "���ɑ��݂��Ă��܂��B"; 										   }
	elsif ($err ==	8) { $mes = "���̑���͋�����Ă��܂���B";								   }
	elsif ($err ==	9) { $mes = "�Ǘ��R�[�h���Ⴂ�܂��B";										   }
	elsif ($err == 10) { $mes = "�s���Ȏw��ł��B�i$etc�j"; 									   }
	elsif ($err == 11) { $mes = "�����݋֎~���[�h�ɂȂ��Ă��܂��B"; 							   }
	elsif ($err == 12) { $mes = "GET���\\�b�h�ɂ�鏑�����݂��֎~����Ă��܂��B";				   }
	elsif ($err == 13) { $mes = "���M��URL���s���ł��B";										   }
	elsif ($err == 14) { $mes = "���b�Z�[�W���������܂��B${etc}byte�ȉ��ɂ��Ă��������B";		   }
	elsif ($err == 99) { $mes = "$libname �̃o�[�W�������Ⴂ�܂��Bver.$etc�ȍ~�������p���������B"; }
	else			   { $mes = $err; }

print <<"EOF";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html40/strict.dtd">
<html>
<head>
<title>�G���[</title>
</head>
<body>
<p>$mes<br>�u���E�U��Back�{�^���ł��߂肭�������B</p>
</body>
</html>
EOF

	exit(-1);
}

1;

;# end_of_file