package cgiroompostlimit;

# Copyright (c) CGIROOM.                              http://cgiroom.nu
#======================================================================#
# [Ver  1.00] 投稿制限機能
#
# このプログラムによって起きた事にCGIROOMは責任を負いません。
# 利用契約に同意できない方のご利用は、遠慮下さい。

#======================================================================#
# 設    定

#◇ 記録データファイル名
$data = "ipdata.dat";

#◇ 投稿許可回数
$count = 1 ;

#◇ ＩＰ記録をしないなら 1 を 0 に
$ip = 1 ;

#◇ ＩＰ記録最大数
$ip_max = 100 ;

#◇ クッキー記録をしないなら 1 を 0に
$cookie= 1;

#◇ 投稿制限期間 秒数で指定
$sec =  120 ;

#◇ 戻り先アドレス
$url = 'http://www.bar-rotten.com/cgi/bbs/tboard003.cgi';

#◇ GETの場合[投稿時に必ず使用するフォーム部品名(半角英数字)]
$get = '****';

#======================================================================#

if($ENV{'REQUEST_METHOD'} eq "POST" || $ENV{'REQUEST_METHOD'} eq "post" || $ENV{'QUERY_STRING'} =~ /\Q$get\E=/){
	if($ip){
		$time=time;
		$c=1;
		$IN  = "< " . $data;
		$OUT = "> " . $data;
		open IN or &msg('データファイルがありません');
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
				&msg('すでに投稿制限数に達していますので投稿できませんでした。<br>時間がたってからまた改めて投稿してください');
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
		open OUT or &msg('データファイルに書き込めません');
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
				&msg('すでに投稿制限数に達していますので投稿できませんでした。<br>時間がたってからまた投稿してください');
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
# エラー表示

sub msg{
	print "Content-type: text/html\n\n";
	print <<HTML;
<HTML>
	<HEAD>
		<TITLE>投稿制限</TITLE>
	</HEAD>
	<BODY bgcolor="#FFFFFF" text="#FF0000">
		<TABLE height="100%" width="100%">
			<TR>
				<TD align=center>
					$_[0]<p>
					<HR width=200>
					<A href="http://cgiroom.nu">CGIROOM</A>
					<HR width=200>
					<A href="$url">戻 る</A>
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
