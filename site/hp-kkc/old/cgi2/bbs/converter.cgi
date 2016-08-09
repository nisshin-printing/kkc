#!/usr/local/bin/perl

# 
#   TBOARD 003 ���O�t�@�C���R���o�[�^
# 
#   Copyright(C) TOSHISRUS
#   E-mail   �F tboard@sk.redbit.ne.jp
#   HOMEPAGE �F http://sk.redbit.ne.jp/~tboard/

# ==== ���ӎ��� ========================================================
#
# 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#    �܂��A�{CGI�̓t���[�\�t�g�ł����A���쌠�͕������Ă͂��܂���B
#    �t�b�^�[�̒��쌠�\���͂����Ȃ鎖�������Ă��폜���Ă͂����܂���B
#
# 2. �ݒu�Ɋւ��鎿��͓��z�[���y�[�W�̌f���ɂĂ��肢�������܂��B
#    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#
# 3. �ݒ荀�ڂ����Ȃ��������߁A�J�X�^�}�C�Y�����X�h���ł��B
#    ���C�ɏ����܂�����A���g�����������B
#    �v�]�Ȃǂ���܂�����A���z�[���y�[�W�̌f���ɂĂ��肢�������܂��B
#
# ======================================================================

# 
# �g�p����O�ɕK�����O�t�@�C���̃o�b�N�A�b�v������Ă��������B
# ���̃R���o�[�^���g�p����ƈȑO�̃t�@�C���͂��ׂč폜����܂��B
# �ϊ���A���O�ۊǗp��logbox�̃t�H���_�݂̂́A�蓮�ō폜���Ă��������B
# 

# ==== �g�p���@ ========================================================
#
# 1. ��{�ݒ�ŁA���O�t�@�C���̃p�X�����ׂđ��΃p�X�Ŏw�肷��B
# 2. �u���E�U��converter.cgi�ɃA�N�Z�X����B
# 3. �u�ϊ������v�Əo�͂����΃R���o�[�g�����ł��B
#
# ======================================================================

# //// ��{�ݒ� (��������) ////////////////////////////////////////////////////////////////

# ==== TBOARD 0.**�̐ݒ� =============
# �e�L���p���O�t�@�C��
$oyalog = "logbox/oyalog.log";
# ���X�L���p���O�t�@�C��
$reslog = "logbox/reslog.log";

# ==== TBOARD 1.**�̐ݒ� =============
# ���O�t�@�C��
$logfile = "tboard003.log";

# ==== TBOARD���ʂ̐ݒ� ==============
# �ߋ����O�f�B���N�g��
$oldbox = "oldlog/";

# //// ��{�ݒ� (�����܂�) ////////////////////////////////////////////////////////////////

# //// ���O�t�@�C���̈ڍs ///////////////////////////////////////////////////////////////////
# ���O���J��
open(IN,"$oyalog") || &error("Can't open logfile");
@oyalog = <IN>;
close(IN);
open(IN,"$reslog") || &error("Can't open logfile");
@reslog = <IN>;
close(IN);
@new = ();
foreach $oya (@oyalog){
	($odate,$otdate,$oname,$oemail,$otitle,$ocom,$ourl,$okey,$omenu01,$omenu02,$omenu03,$omenu04,$omenu05) = split(/\t/,$oya);
	push(@new,$oya);
	foreach $res (@reslog){
		($rdate,$rtdate,$rname,$remail,$rtitle,$rcom,$rurl,$rkey,$rmenu01,$rmenu02,$rmenu03,$rmenu04,$rmenu05) = split(/\t/,$res);
		if($otdate eq $rtdate){push(@new,$res);}
	}
}
# ���O�̍X�V
open(OUT,">$logfile") || &error("Can't write logfile");
print OUT @new;
close(OUT);
# �����̕ύX
chmod(0666,"$logfile");

# //// �ߋ����O�t�@�C���̈ڍs ///////////////////////////////////////////////////////////////
# �ߋ�UP���f�B���N�g���̃I�[�v��
opendir(DIR,$oldbox);
@filelist = ();
while ($ofile = readdir(DIR)){
 if(index($ofile,"oya\.")>0){
  push(@filelist,$ofile);
 }
}
closedir(DIR);
# �t�@�C�������\�[�g����
@filelist = sort @filelist;
$s = 0;
while($s<@filelist){
	$oyalog = $oldbox.substr(@filelist[$s],0,6).'_oya.log';
	$reslog = $oldbox.substr(@filelist[$s],0,6).'_res.log';
	$logfile = $oldbox.substr(@filelist[$s],0,6).'.log';
	# ���O���J��
	open(IN,"$oyalog") || &error("Can't open logfile");
	@oyalog = <IN>;
	close(IN);
	open(IN,"$reslog") || &error("Can't open logfile");
	@reslog = <IN>;
	close(IN);
	@new = ();
	foreach $oya (@oyalog){
		($odate,$otdate,$oname,$oemail,$otitle,$ocom,$ourl,$okey,$omenu01,$omenu02,$omenu03,$omenu04,$omenu05) = split(/\t/,$oya);
		push(@new,$oya);
		foreach $res (@reslog){
			($rdate,$rtdate,$rname,$remail,$rtitle,$rcom,$rurl,$rkey,$rmenu01,$rmenu02,$rmenu03,$rmenu04,$rmenu05) = split(/\t/,$res);
			if($otdate eq $rtdate){push(@new,$res);}
		}
	}
	# ���O�̍X�V
	open(OUT,">$logfile") || &error("Can't write logfile");
	print OUT @new;
	close(OUT);
	# �����̕ύX
	chmod(0666,"$logfile");
	unlink($oyalog);
	unlink($reslog);
	$s++;
}

print "Content-type: text/html\n";
print "\n";
print<<HTML_END;
<html>
<head><title>$title</title>
<style type="text/css">
<!--
body,tr,td {font-size:9pt;font-family: "MS UI Gothic"}
table      {font-size:9pt;}
b          {font-size:10pt}
small      {font-size:10pt;line-height:18pt}
div        {line-height:14pt}
h4         {font-size:12pt}
/* a          {font-size:9pt;text-decoration:none;} */
/* a:hover    {color:$color05;text-decoration:underline;} */
.st1       {font-size:9pt;font-family:"MS UI Gothic";color:$color06;background-color:$color07;} /* ���� */
.st2       {color:$color09;$stylest1} /* ����2 */
-->
</style>
</head>
<body>
<center>
�ϊ�����
</center>
<div align=center><br>
$var<br>
- <a href='http://i.am/toshisrus' TARGET=_blank>TOSHISRUS</a> -
</div>
</body></html>
HTML_END
exit;

# //// Error���� ///////////////////////////////////////////////////////////////////////////
sub error {
	if(-e $_[1]){ unlink($_[1]);}
	print"<center><hr width=75%><h4>�G���[</h4>\n";
	print"<P><h4>$_[0]</h4>\n";
	print"<P><hr width=75%><br>�u���E�U�̖߂�Ŗ߂��Ă��������B</center>\n";
	&footer;
	exit;
}
