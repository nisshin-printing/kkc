package log;
###########################################################
#	filectl.pl
#	�t�@�C���𒲐�����pl���W���[��
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
#	�w�肵���t�@�C�����J���֐�
#@param		$fileName	�t�@�C���ւ̃p�X(�t�@�C����)
#@return	$fileData	�t�@�C���̃f�[�^
#	@fileData	= openFile("index.html");
#
#----------------------------------------------------------
#	writeFile()
#	�w�肵���t�@�C���Ƀf�[�^����������
#@param		$filePath	�t�@�C���ւ̃p�X(�t�@�C����)
#			$message	�t�@�C���֏������ރf�[�^
#	writeFile("index.html","$index");
#
#----------------------------------------------------------
#	mixData()
#	html�t�@�C����log�t�@�C������������
#@param		$length	log�t�@�C���̃T�C�Y
#			$ret	���O�̕\����
#			@log	log�t�@�C���̃f�[�^
#			@htmls	html�t�@�C���̃f�[�^
#@return 	$mixd	���������f�[�^
#
#	$message = mixData($length, $ret, @log, @htmls);
#----------------------------------------------------------
#
#	writeLog()
#	Log�t�@�C������������
#@param		$filePath		log�̃t�@�C����
#			$message		log�t�@�C���֏����o�����b�Z�[�W
#	writeLog($filePath, $message);
###########################################################	

###########################################################
#	openFile()
#	�w�肵���t�@�C�����J��
#@param		$fileName	�t�@�C���ւ̃p�X
#@return	@fileData	�t�@�C���̃f�[�^
###########################################################
sub openFile
{
	#�����̎󂯎��
	#����юd�l�ϐ��̐錾�E������
	my($fileName) = @_;
	my @fileData;
		
	#�t�@�C�����J��
	#�G���[�����t��
	if(!open(DF, "$fileName")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$fileName";
		exit;
	}
	
	#�t�@�C���̃f�[�^���󂯎��
	@fileData = <DF>;
	close(DF);
	
	return @fileData;
}

###########################################################
#	writeFile()
#	�t�@�C���փf�[�^����������
#@param		$filePath		log�̃t�@�C����
#			$message		log�t�@�C����
###########################################################
sub writeFile
{
	#�����̏���
	my($filePath, $message)		= @_;
	
	#�t�@�C�����J��
	if(!open(OUT, ">$filePath")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$filePath";
		exit;
	}
	
	#�t�@�C���ւ̏�������
	print OUT "$message\n";
	close(OUT);
}

###########################################################
#	mixData()
#	log�f�[�^��html�f�[�^����������
#@param		$length	log�t�@�C���̃T�C�Y
#			$ret	���O�̕\����
#			@log	log�t�@�C���̃f�[�^
#			@htmls	html�t�@�C���̃f�[�^
#@return 	$mixd	���������f�[�^
###########################################################
sub mixData
{
	#�����̏���
	my($length, $ret, @buf)	= @_;
	
	my @log		= @buf[0..$length-1];
	my @htmls	= @buf[$length..$#buf];
	
	#�ϐ��̏�����
	my $html1	= "";			#<!--start2-->�ȑO�̃f�[�^������
	my $html2	= "";			#<!--start2-->�`<!--last2-->�܂ł̃f�[�^������
	my $html3	= "";			#<!--last2-->�ȍ~�̃f�[�^������
	my $line	= "";			#�f�[�^�̎��o���悤�ϐ�
	my $htmlno	= "1";			#�����ύX�t���O
	my $mixd 	= "";			#�������html�t�@�C���f�[�^
	my $i;
	
	#log�t�@�C���̐���
	@log		= reverse @log;
	
	#�f�[�^�̏���
	foreach $line (@htmls) {
		if($line =~/<!--start-->/){
			$htmlno = "2";
		}elsif($line =~/<!--stop-->/){
			$htmlno = "3";
		}
		
		if($htmlno eq "1"){
			$html1 ="$html1$line";
		}elsif($htmlno eq "2"){
			#log�f�[�^�̖��ߍ���
			$html2 = "$html2<!--start2-->\n";
			for($i = 0; $i < $ret; $i++){
				$html2 = "$html2$log[$i]";
			}
			$htmlno = "3"	
		}elsif($htmlno eq "3"){
			$html3 ="$html3$line";
		}
	}

	#�f�[�^�̍���
	$mixd		= "$html1$html2$html3\n";
	return $mixd;
}

###########################################################
#	writeLog()
#	Log�t�@�C������������
#@param		$filePath		log�̃t�@�C����
#			$message		log�t�@�C����
###########################################################
sub writeLog
{
	#�����̏���
	my($filePath, $message)		= @_;
	
	#���s�R�[�h��؂藎�Ƃ�
	chomp $message;
	
	#�ϐ�������
	my @data;					#�`�F�b�N�p�f�[�^�t�@�C��
	my $dataSize;				#�f�[�^�t�@�C���̃T�C�Y
	
	#�G���[�������t�@�C������
	if(!open(DF, "$filePath")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$filePath";
		exit;
	}
	
	#�t�@�C���̃f�[�^���ʂ�
	@data = <DF>;
	close(DF);
	
	#�f�[�^�T�C�Y�̃`�F�b�N
	$dataSize	= @data;
	
	#�f�[�^����
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
	
	#�f�[�^�̏����o��
	foreach $line (@data){
		print OUT "$line";
	}
	close(OUT);
	
	#�t�@�C�����J��
	if(!open(OUT, ">>$filePath")){
		print "Content-type: text/html\n\n";
		print "Can't open file<br>\n";
		print "$filePath";
		exit;
	}
	
	#�t�@�C���ւ̏�������
	print OUT "$message\n";
	close(OUT);
}

###########################################################
#	show()
#	�f�[�^��ǂݍ���ŕ\�����s��
#@param		$maxData	�\���f�[�^�ő吔
#			@showData	�\���f�[�^
#			@skinData	�\���X�L��
###########################################################
sub show
{
	#�����̏���
	my ($maxData,@buf)	= @_;
	
	#�\���f�[�^�ƕ\���X�L���̊��U��
	#�e�험�p�ϐ��̏�����
	my @showData		= $buf[0..$maxData];		#���O�t�@�C���f�[�^�̒��o
	my @skinData		= @buf;						#�X�L���f�[�^�̒��o
	my $htmlno			= "1";						#��������p�t���O
	
	my $html1,$html2,$html3;						#�����p�f�[�^�ꎞ�ۑ��̈�
	my $mixData;									#������̃f�[�^
	
	#��������
	foreach $line (@skinData){
		#��������t���O�����ɏ���������U��
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