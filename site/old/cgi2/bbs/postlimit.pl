package cgiroompostlimit;

# Copyright (c) CGIROOM.                              http://cgiroom.nu
#======================================================================#
# [Ver  1.00] ���e�����@�\
#
# ���̃v���O�����ɂ���ċN��������CGIROOM�͐ӔC�𕉂��܂���B
# ���p�_��ɓ��ӂł��Ȃ����̂����p�́A�����������B

#======================================================================#
# ��    ��

#�� �L�^�f�[�^�t�@�C����
$data = "ipdata.dat";

#�� ���e����
$count = 1 ;

#�� �h�o�L�^�����Ȃ��Ȃ� 1 �� 0 ��
$ip = 1 ;

#�� �h�o�L�^�ő吔
$ip_max = 100 ;

#�� �N�b�L�[�L�^�����Ȃ��Ȃ� 1 �� 0��
$cookie= 1;

#�� ���e�������� �b���Ŏw��
$sec =  120 ;

#�� �߂��A�h���X
$url = 'http://www.bar-rotten.com/cgi/bbs/tboard003.cgi';

#�� GET�̏ꍇ[���e���ɕK���g�p����t�H�[�����i��(���p�p����)]
$get = '****';

#======================================================================#

if($ENV{'REQUEST_METHOD'} eq "POST" || $ENV{'REQUEST_METHOD'} eq "post" || $ENV{'QUERY_STRING'} =~ /\Q$get\E=/){
	if($ip){
		$time=time;
		$c=1;
		$IN  = "< " . $data;
		$OUT = "> " . $data;
		open IN or &msg('�f�[�^�t�@�C��������܂���');
		@data = <IN>;
		close IN;
		$ipdata=$ENV{'REMOTE_ADDR'};
		foreach $ip (@data){
			($ips  , $counts , @date) = split(/\t/,$ip);
			$ip=() if ($date[$#date - 1] + $sec) < $time ;
			next unless $ip =~ /^\Q$ipdata\E\t/;
			pop(@date);
			if(($date[0] + $sec) < $time){
				if($count > 1){
					shift @date;
					push(@date,$time);
					$time = join("\t",@date);
					$c = $counts;
				}
			}elsif($counts == $count){
				&msg('���łɓ��e�������ɒB���Ă��܂��̂œ��e�ł��܂���ł����B<br>���Ԃ������Ă���܂����߂ē��e���Ă�������');
			}else{
				$date=join("\t",@date);
				$time = $date . "\t" . $time;
				$c = ++$counts;
			}
			$ip=();
			last;
		}
		unshift(@data,"$ipdata\t$c\t$time\t\n");
		pop @data if $data[$ip_max];
		open OUT or &msg('�f�[�^�t�@�C���ɏ������߂܂���');
		print OUT @data;
		close OUT;
	}
	if($cookie){
		$time=time;
		$ENV{'HTTP_COOKIE'} =~ s/ //g;
		@COOKIE=split(/;/, $ENV{'HTTP_COOKIE'});
		foreach (@COOKIE){
			($name,$value) = split(/=/);
			$COOKIE{$name} = $value;
		}
		if($COOKIE{'postlimit'}){
			( $counts , @date ) = split(/\t/,$COOKIE{'postlimit'});
			if(($date[0] + $sec ) < $time){
				if($count > 1){
					shift @date;
					$date=join("\t",@date);
					$value="$counts\t$date\t$time";
				}else{
					$value="1\t$time";
				}
			}elsif($counts == $count){
				&msg('���łɓ��e�������ɒB���Ă��܂��̂œ��e�ł��܂���ł����B<br>���Ԃ������Ă���܂����e���Ă�������');
			}else{
				$counts++;
				$date=join("\t",@date);
				$value = "$counts\t$date\t$time";
			}
		}else{
			$value="1\t$time";
		}
		print "Set-Cookie: postlimit=$value; expires=Fri, 31-Dec-2010 00:00:00 GMT\n";
	}
}

#======================================================================#
# �G���[�\��

sub msg{
	print "Content-type: text/html\n\n";
	print <<HTML;
<HTML>
	<HEAD>
		<TITLE>���e����</TITLE>
	</HEAD>
	<BODY bgcolor="#FFFFFF" text="#FF0000">
		<TABLE height="100%" width="100%">
			<TR>
				<TD align=center>
					$_[0]<p>
					<HR width=200>
					<A href="http://cgiroom.nu">CGIROOM</A>
					<HR width=200>
					<A href="$url">�� ��</A>
				</TD>
			</TR>
		</TABLE>
	</BODY>
</HTML>
HTML
	exit;
}
1;
__END__
2000/03/16 Ver  1.00
