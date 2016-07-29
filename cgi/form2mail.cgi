#!/usr/local/bin/perl

# �t�H�[�����[�� v1.32  <FREESOFT>
# (�v������̃t�H�[�����瑗�M���ꂽ���e��d�q���[���Ŕz�M����)
#
;$vers = '1.32';
#
#  ����E���� CGI-RESCUE
#  http://www.rescue.ne.jp/
#
# [History]
# 1/FEB/1999 v1.00 <WebFORM> + <FileUPLOADER> = <FORM2MAIL>
# 12/FEB/1999 v1.01 �G���[�����̏C��(�ꎞ�t�@�C���̍폜�g���u��)
# 24/MAR/1999 v1.10 �A�N�Z�X���`�F�b�N�̏����̐ݒ�
# 25/JUL/1999 v1.11 �e�[�u���^�O���̃t�H�[���ɂ��ďC��
# 16/DEC/1999 v1.12 $ref_url�̏����~�X�C��
# 07/FEB/2000 v1.13 �č���
# 09/FEB/2000 v1.14 �����Ă����^�O������ǉ�,CSV�o�͓Y�t�@�\�̕t��
# 26/JUL/2000 v1.15 ���[���w�b�_�̏C��
# 05/OCT/2004 v1.20 Subject��RFC2045�Ή�(�Ȉ�),UUENCODE/BASE64�I��,�O���v���O����nkf�����uuencode���g��Ȃ��݌v
# 31/JAN/2005 v1.21 Content-Type�o�͂̏C��
# 16/Feb/2006 v1.22 �X�p���ɑ΂���Ǝ㐫���C��
# 18/Mar/2006 v1.23 ���[���̃^�C�g�����a�G���R�[�h�ɂ��Ȃ��ꍇ�Ƀ^�C�g�����ݒ肳��Ȃ��s����C��
# 12/May/2006 v1.30 �K�{���ڃG���[�̕\�������A�t�H�[���ŗ��񂵂����ɏC��
# 31/May/2006 v1.31 v1.30�C���̃o�O�̏C��
# 22/Jun/2006 v1.32 �a�G���R�[�h���Ȃ��ꍇ�Ƀ^�C�g���̕����R�[�h��JIS�ɂȂ�Ȃ��o�O�̏C��

#-------------------------------------------------------------------------------------------

# [�ݒu��] ( )���̓p�[�~�b�V�����̑����l
#
# /�C�ӂ̃f�B���N�g��/
#         |
#         |-- /tmp/ <777> ... ��Ɨp
#         |-- base64.pl <644> ... �l�h�l�d�ϊ����C�u����
#         |-- cgi-lib217.pl <644> ... �b�f�h���C�u����
#         |-- form2mail.cgi <755> ... �{�́i���̃v���O�����j
#         |-- jcode.pl <644> ... ���{��R�[�h�ϊ����C�u����
#

#------ �����ݒ� ---------------------------------------------------------------------------

#�����{��R�[�h�ϊ����C�u����    # require './***.pl'; �� require '***.pl';�͈Ӗ����Ⴂ�܂��̂ŁA���ӁB
require './jcode.pl';

#���b�f�h���C�u����
require "./cgi-lib217.pl";

#���l�h�l�d�ϊ����C�u����
require "./base64.pl";

#��sendmail�̐ݒ�
$sendmail = '/usr/sbin/sendmail';

#����Ɨp�f�B���N�g���̐ݒ�
#�@�����f�B���N�g����tmp�Ƃ������O�̃f�B���N�g�����쐬���A�p�[�~�b�V������777(�T�[�o�̍œK�Ȓl�ɂ��킹�邱��)�ɂ��܂��B
$tmp = "./tmp/";

#���󂯎�郁�[���A�h���X
$mailto = 'info@keizai-kassei.net';

#���t�H�[����ʂɕt����^�C�g��
$title = '�v���[���e�[�V�������\������';

#���Q�ƃ`�F�b�N
#���M�t�H�[���̂t�q�k�������ɐݒ肵����������܂܂Ȃ��ꍇ�͑��M���Ȃ�
$ref_url = 'keizai-kassei.net';

#�����̃X�N���v�g��ݒu������{��R�[�h (sjis,euc)
$convert = 'sjis';

#���A�N�Z�X�����`�F�b�N����(��������ō����Ă���ꍇ�̂�) 0:���Ȃ� 1:����
$ref_check = 0;

#�����[���̃^�C�g�����a�G���R�[�h�����邩�ǂ��� -- 0:���Ȃ� 1:����
$EncodeB = 1;

	# (�Q�l) ���[��"Subject"�ɂ���
	# ���[���̃w�b�_�����ɂQ�o�C�g�������g���ꍇ�́ARFC2045�Ɉ˂�ABASE64�ŃG���R�[�h�����a�G���R�[�h�`��
	# =?ISO-2022-JP?B?<BASE64�R�[�h>?= �ɂ��Ȃ���΂Ȃ�܂��񂪁A�����̂قƂ�ǂ̃��[���\�t�g�ł́A����
	# ���Ȃ��Ă��������\�����Ă���܂��B���̋K���ɏ]���悤�ɉ��H���邱�Ƃ͔��ɖʓ|�Ȃ��߁A���̓���ȉ��H
	# ��K�v�Ƃ��Ȃ����x�̎d�l�ɗ��߂Ă��邽�߁A���[���薼�̕������ɐ�����݂��Ă��܂��B

#���t�@�C���Y�t�`�� # 0:BASE64 1:UUENCODE
$uuencode = 0;

	# (�Q�l) ���̃v���O������uuencode�̎d�l
	# ���[���Q�[�g�E�F�C�̒��ɍs�����܂ދ󔒕������������Ă��܂����̂����邽�߁A�󔒕�����"`"(0x60)�ɕϊ����Ă��܂��B
	# �f�R�[�h����ۂ͂���͋󔒕���(0x00)�Ƃ��ĉ��߂��Ă��������B<MODE>�͓��v���O�����ł�600�ɐݒ肵�Ă��܂��B
	#
	# begin <MODE> <�t�@�C����>
	# �`���e�`
	# `
	# end

#-------------------------------------------------------------------------------------------

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
($seco,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@mon_array = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
@wday_array = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
$date_now = sprintf("%s, %02d %s %04d %02d:%02d:%02d +0900 (JST)",$wday_array[$wday],$mday,$mon_array[$mon],$year +1900,$hour,$min,$sec);

#-------------------------------------------------------------------------------------------

$ref = $ENV{'HTTP_REFERER'};
$ref =~ s/\n|\r//g;
$addr = $ENV{'REMOTE_ADDR'};
if ($host eq "" || $host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr; }
$via = $ENV{'HTTP_VIA'};
$xfor = $ENV{'HTTP_X_FORWARDED_FOR'};
$for = $ENV{'HTTP_FORWARDED'};
$agent = $ENV{'HTTP_USER_AGENT'}; $agent =~ s/</(/g; $agent =~ s/>/)/g;
if ($via ne "") { $trueip = $xfor; }
else { $trueip = $addr; }
if ($xfor ne "") { $xfor_name = gethostbyaddr(pack('C4',split(/\./,$xfor)),2) || $xfor; }
$access_data = "host;$host addr;$addr via;$via xfor;$xfor for;$for agent;$agent trueip;$trueip xfor_name;$xfor_name";
$access_data =~ s/\n|\r//g;

#-------------------------------------------------------------------------------------------

$ret = &ReadParse;
if ($ret == 0) { &error('���͂�����܂���.'); }

if ($ref_check) {

	$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if (!($ref =~ /$ref_url/i)) { &error('�s���Ȏ菇�����m���܂���','���K�̃t�H�[���ȊO����̃A�N�Z�X�ł�.'); }
}

#-------------------------------------------------------------------------------------------

$filenum = 0;
foreach $data (@in) {

	unless ($ENV{'CONTENT_TYPE'} =~ m#^multipart/form-data#) {

		$ENCTYPE = "multipart/form-data";
		$data =~ s/\+/ /g;
		($key,$val) = split(/=/,$data,2);
		$key =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;
		push(@name,"$key\0$filename");
	}
	else {
		($key) = $data =~ /\bname="([^"]+)"/i;
		($filename) = $data =~ /\bfilename="([^"]*)"/i;
		if ($filename eq '' && $data =~ /\bfilename="([^"]*)"/i) { next; }
		push(@name,"$key\0$filename");
	}
}

#-------------------------------------------------------------------------------------------

$fileC1 = $fileC2 = 0;
foreach $name (@name) {

	($name,$filename) = split("\0",$name);

	if ($filename ne '') {

		if (exists $out{$name}) { $fileC1 = 1; next; }
		$fileC2 = 1;

		$ps = $$;
		if ($ps eq '') { $ps = time; }

		$filename = reverse(($filename) = split(/\\|\/|\:/,reverse($filename)));
		push(@FILE,"$name\0$ps\_$filenum\0$filename");
		push(@FILEDATA,$in{$name});

		$filenum++;
		$out{$name} = $name;
		push(@atf,"[�Y�t] $name\0$filename");

		next;
	}

	&jcode'convert(*name,$convert);

	$num = $lastspc = 0;

	foreach $value (split("\0",$in{$name})) {

		if (!exists $out{$name}{$num}) {

			$lastspc = 1;
			&jcode'convert(*value,$convert);

			($cmd) = &checkval($name,$value);
			if ($cmd) { next; }

			$value =~ s/&/&amp;/g;
			$value =~ s/"/&quot;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;

			push(@out,"$name\0$value");
			$out{$name}{$num} = $value;
			last;
		}

		$num++;
	}

	if (!$lastspc) {

		if ($name =~ /^_(.*)$/) { next; }
		push(@out,$name);
	}
}

#-------------------------------------------------------------------------------------------

foreach $out (@out) {

	($name,$value) = split("\0",$out);
	if ($indispen{$name} && $in{$name} eq '') { push(@INDISPENs,$name); }
}

if (@INDISPENs) { &error("���L��������܂�",'<h3>���̍��ڂ͕K�{���͂ł�.</h3>',"<i>@INDISPENs</i>"); }

#-------------------------------------------------------------------------------------------

if ($in{'_emailset'} ne '' && exists $in{$in{'_emailset'}}) {

	$EMAIL = $in{$in{'_emailset'}};
	if ($EMAIL ne '') {

		if ($EMAIL =~ /\s|\,/) { &error('Error','�d���[���𐳂������L����������.'); }
		unless ($EMAIL =~ /\b[-\w.]+@[-\w.]+\.[-\w]+\b/) { &error('�G���[','�d���[���͔��p�Ő��������L����������.'); }
	}
}

if ($EMAIL eq '') { $EMAIL = 'anonymous@on.the.net'; }

#-------------------------------------------------------------------------------------------

if ($fileC1) { &error('�G���[','�A�b�v���[�h�t�@�C���̍��ږ����d�����Ă��܂�.'); }

if ($fileC2) { 

	$mix = 1;

	foreach $file (0 .. $#FILE) {

		($name,$filenum,$filename) = split("\0",$FILE[$file]);

		if (!open(BIN,"> $tmp$filenum")) { &error('�G���[','�A�b�v���[�h�t�@�C���̈ꎞ�t�@�C�����쐬�ł��܂���.','�e���|�����[�t�H���_�̃p�[�~�b�V�������m�F���Ă�������.'); }
		binmode(BIN);
		print BIN $FILEDATA[$file];
		close(BIN);
	}
}

if ($check{'_check'} && $mix) { &error('�G���[','�t�@�C���A�b�v���[�h�@�\���g���ꍇ�́A���e�m�F�����͗��p�ł��܂���.'); }

if ($check{'_check'}) { &check; }

&sendmail;
exit;

#-------------------------------------------------------------------------------------------

sub check {

	print &PrintHeader;
	print &HtmlTop($title);

	print <<"EOF";
	<body $check{'_body'}>
	<h2>���e�m�F</h2>
	<form method="$ENV{'REQUEST_METHOD'}" action="form2mail.cgi" ENCTYPE="$ENCTYPE">
	<blockquote>
	<table border=3 cellpadding=2 cellspacing=1>
	<tr><td><b><font size=+1>����</font></b></td><td><b><font size=+1>���e</font></b></td></tr>
EOF

	foreach (@out) {

		($name,$value) = split("\0");

		print "<tr><input type=hidden name=\"$name\" value=\"$value\">\n";
		print "<td>$name</td>\n";

		if ($value =~ /\n/) { print "<td><pre>$value</pre></td></tr>\n"; }
		else { print "<td>$value</td></tr>\n"; }

		print "</td></tr>\n";
	}

	print "</table></blockquote><p>\n";

	while (($key,$val) = each %check) {

		if ($key =~ /^_check$/i) { next; }
		print "<input type=hidden name=\"$key\" value=\"$val\">\n";
	}

	while (($key,$val) = each %indispen) {

		print "<input type=hidden name=\"_indispen\" value=\"$key\">\n";
	}

	print "<input type=hidden name=\"_refurl\" value=\"$ref\">\n";
	print "<input type=submit value=\"�@��  �� �M  \"><p>\n";

	print "</form><p><hr>\n";
	print "<i>���M��F<a href=\"mailto:$mailto\">$mailto</a><i>\n";

	print &HtmlBot;
	exit;
}

#-------------------------------------------------------------------------------------------

sub sendmail {

	push(@MailValue,"Date: $date_now\n");
	push(@MailValue,"X-Sender: $access_data\n");
	push(@MailValue,"X-Mailer: form2mail $vers by CGI-RESCUE\n");
	push(@MailValue,"X-Referer: $ref\n");

	push(@MailValue,"To: $mailto\n");
	if ($EMAIL eq 'anonymous@on.the.net') { push(@MailValue,"Reply-To: $mailto\n"); }

	$EMAIL =~ s/\n//g; $EMAIL =~ s/\r//g;
	if (length($EMAIL) > 255) { &error('�G���[','���[���A�h���X�̒���������255�����܂łł�.'); }
	if ($EMAIL =~ /\,/) { &error('�G���[','���[���A�h���X�𐳂����P���͂��Ȃ��Ƒ��M�ł��܂���.'); }
	push(@MailValue,"From: $EMAIL\n");

	$SUBJECT = $in{'_subject'};
	$SUBJECT =~ s/\n//g; $SUBJECT =~ s/\r//g;

	if ($EncodeB) {

		$SUBJECT = &mailSubject_base64encode($SUBJECT);
		if (!$SUBJECT) { &error("�G���[","���[���̃^�C�g��(�薼)��Z�����Ă��������B"); }
	}
	else { $SUBJECT = &jis("Subject: $SUBJECT\n"); }

	push(@MailValue,$SUBJECT);
	push(@MailValue,"MIME-Version: 1.0\n");
	push(@MailValue,"Content-Transfer-Encoding: 7bit\n");

	if ($mix) { &send_mix; }
	else { &send; }

	if (open(OUT,"| $sendmail -t")) {

		foreach (@MailValue) { print OUT $_; }
		close(OUT);
	}

	if ($check{'_ccopy'} && $check{'_location'} ne '') {

		print &PrintHeader;
		print &HtmlTop($title);

		print "<body $check{'_body'}>\n";
		print "<h2>���M���܂���</h2>\n";
		print "������<a href=\"mailto:$mailto\">$mailto</a>���Ăɑ��M���ꂽ���e�͈ȉ��̒ʂ�ł�.<br>\n";
		print "���e�̎ʂ��Ƃ��Ă��T����������.<p>\n";
		print "<form>\n";
		print "<blockquote>\n";
		print "<textarea cols=70 rows=20>";
		&cc;
		print "</textarea></form></blockquote><p>\n";
		print "<h3>[<a href=\"$check{'_location'}\" target=\"_top\">�R�s�[�����玟��</a>]</h3>";
	}
	elsif ($check{'_ccopy'}) {

		print &PrintHeader;
		print &HtmlTop($title);

		print "<body $check{'_body'}>\n";
		print "<h2>���M���܂���</h2>\n";
		print "������<a href=\"mailto:$mailto\">$mailto</a>���Ăɑ��M���ꂽ���e�͈ȉ��̒ʂ�ł�.<br>\n";
		print "���e�̎ʂ��Ƃ��Ă��T����������.<p>\n";
		print "<form>\n";
		print "<blockquote>\n";
		print "<textarea cols=70 rows=20>";
		&cc;
		print "</textarea></form></blockquote><p>\n";
		if ($check{'_gourl'} ne '' && $check{'_goname'} ne '') { print "<h3>[<a href=\"$check{'_gourl'}\" target=\"_top\">$check{'_goname'}</a>]</h3>"; }
	}
	elsif ($check{'_location'} ne '') { print "Location: $check{'_location'}\n\n"; }
	else {

		print &PrintHeader;
		print &HtmlTop($title);

        	print "<body $check{'_body'}>\n";
		print "<h2>���M���܂���</h2>\n";
		print "���L�����ꂽ���̂�<a href=\"mailto:$mailto\">$mailto</a>���Ăɓd�q���[������܂���.<br>\n";
		print "Thank you for sending comments to $mailto .<p>\n";
		if ($check{'_gourl'} ne '' && $check{'_goname'} ne '') { print "<h3>[<a href=\"$check{'_gourl'}\" target=\"_top\">$check{'_goname'}</a>]</h3>"; }
	}

	print &HtmlBot;
}

#-------------------------------------------------------------------------------------------

sub cc {

	print "Date: $date_now\n";
	print "To: $mailto\n";
	print "From: $EMAIL\n";
	print "Subject: $in{'_subject'}\n\n";

	foreach (@out) {

		s/&lt;/</g;
		s/&gt;/>/g;

		($name,$value) = split("\0");

		if ($check{'_type'} == 1) { print "\[$name\]\n$value\n\n"; }
		elsif ($value =~ /\n/) { print "$name =\n$value\n\n"; }
		else { print "$name = $value\n"; }
	}

	print "\n";

	foreach (@atf) {

		($name,$value) = split("\0");
		print "$name = $value\n";
	}
}

#-------------------------------------------------------------------------------------------

sub send {

	push(@MailValue,"Content-Type: text/plain; charset=\"ISO-2022-JP\"\n");

	$BODY .= "\n"; # �w�b�_�I���̋�؂�

	foreach $line (@out) {

		($name,$value) = split("\0",$line,2);

		$value =~ s/&amp;/&/g;
		$value =~ s/&quot;/"/g;
		$value =~ s/&lt;/</g;
		$value =~ s/&gt;/>/g;

		if ($check{'_csv'} == 1) { push(@CSV,$value); }

		if ($check{'_type'} == 1) { $BODY .= "\[$name\]\n$value\n\n"; }
		elsif ($value =~ /\n/) { $BODY .= "$name =\n$value\n\n"; }
		else { $BODY .= "$name = $value\n"; }
	}

	$BODY .= "\n";
	$BODY .= &EncodeCSV(@CSV) . "\n\n";

	push(@MailValue,&jis($BODY));
}

#-------------------------------------------------------------------------------------------

sub send_mix {

	($boundary) = $ENV{'CONTENT_TYPE'} =~ m#multipart/form-data; boundary=(.*)#;
	if ($boundary eq "") { $boundary = '0123456789zxcvbnmasdfghjklqwertyuiop'; }
	$bound = "--" . $boundary;

	$BODY .= "Content-Type: multipart/mixed; boundary=\"$bound\"\n\n";
	$BODY .= 'This is multipart message.' . "\n\n";

	$BODY .= "--$bound\n";
	$BODY .= "Content-Transfer-Encoding: 7bit\n";
	$BODY .= 'Content-Type: text/plain; charset="ISO-2022-JP"' . "\n\n";

	foreach $line (@out) {

		($name,$value) = split("\0",$line,2);

		$value =~ s/&amp;/&/g;
		$value =~ s/&quot;/"/g;
		$value =~ s/&lt;/</g;
		$value =~ s/&gt;/>/g;

		if ($check{'_csv'} == 1) { push(@CSV,$value); }

		if ($check{'_type'} == 1) { $BODY .= "\[$name\]\n$value\n\n"; }
		elsif ($value =~ /\n/) { $BODY .= "$name =\n$value\n\n"; }
		else { $BODY .= "$name = $value\n"; }
	}

	$BODY .= "\n";

	$BODY .= "\n";
	if ($check{'_csv'} == 1) { $BODY .= &EncodeCSV(@CSV) . "\n\n"; }

	foreach $line (@atf) {

		($name,$value) = split("\0",$line,2);
		$BODY .= "$name = $value\n";
	}

	$BODY .= "\n";

	push(@MailValue,&jis($BODY));

	#-----------------------------------------------------------------------------------

	$BODY = "";

	foreach $file (0 .. $#FILE) {

		($name,$filenum,$filename) = split("\0",$FILE[$file],3);

		$BODY .= "--$bound\n";
		$BODY .= "Content-Type: application/octet-stream; name=\"$filename\"\n";

		if ($uuencode) { $BODY .= 'Content-Transfer-Encoding: X-uuencode' . "\n"; }
		else { $BODY .= 'Content-Transfer-Encoding: base64' . "\n"; }

		$BODY .= "Content-Disposition: attachment; filename=\"$filename\"\n\n";

		$binary_string = "";
		if (open(UU,"$tmp$filenum")) {

			while (<UU>) { $binary_string .= $_; }
			close(UU);
		}

		if ($uuencode) {

			$ascii_string = &base64'uuencode($binary_string);
			$BODY .= "begin 600 $filename\n$ascii_string\`\n" . "end\n\n";
		}
		else {
			$ascii_string = &base64'b64encode($binary_string);
			$BODY .= "$ascii_string\n";
		}

		if (-e "$tmp$filenum") { unlink("$tmp$filenum"); }
	}

	$BODY .= "--$bound\-\-\n";
	push(@MailValue,$BODY);
}

#-------------------------------------------------------------------------------------------

sub checkval {

	local($key,$val) = @_;
	local($num,$cmd);

	if ($key =~ /^_indispen$/i) {

		$indispen{$val} = 1;
		return 1;
	}

	elsif ($key =~ /^_(.*)$/i) { $cmd = "\_$1"; $check{$cmd} = $val; return 1; }
	else { return 0; }
}

#-------------------------------------------------------------------------------------------

sub EncodeCSV {

	local(@fields) = @_;
	local(@CSV) = ();

	foreach $text (@fields) {

		$text =~ s/"/""/g;
		if ($text =~ /,|"/) { $text = "\"$text\""; }

		push(@CSV,$text);
	}

	return join(',',@CSV);
}

#-------------------------------------------------------------------------------------------

sub mailSubject_base64encode {

	local($line) = @_;
	jcode::convert(\$line,'jis','euc','z');
	$line = &base64'b64encode($line);
	eval 'chomp($line);'; chop($line) if $@ ne '';
	if (length($line) > 64) { return 0; }
	return "Subject: =?ISO-2022-JP?B?$line?=\n";
}

#-------------------------------------------------------------------------------------------

sub jis {

	local($line) = @_;
	&jcode'convert(*line,'jis');
	$line;
}

#-------------------------------------------------------------------------------------------

sub error {

	local (@msg) = @_;
	local ($i);

	foreach $file (@FILE) {

		($name,$filenum,$filename) = split("\0",$FILE[$file]);
		if (-e "$tmp$filenum") { unlink("$tmp$filenum"); }
	}

	print &PrintHeader;

	print <<"EOF";
	<HTML>
	<HEAD>
	<TITLE>$title</TITLE>
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	</HEAD>
	<body $check{'_body'}>
	<h1>$_[0]</h1>
EOF

	foreach $i (1 .. $#msg) { print "$msg[$i]<br>\n"; }

	print <<"EOF";
	<h3>[<A HREF="JavaScript:history.back()">�߂�</A>]</h3>
EOF

	print &HtmlBot;
	exit;
}
