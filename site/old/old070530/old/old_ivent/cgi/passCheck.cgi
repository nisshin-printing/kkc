#!/usr/local/bin/perl

use CGI;
#

my $login	= "../login.html";
my $cgi		= CGI->new();
my $pass	= "npo";

if($cgi->param('passKey') ne "$pass"){
	print <<EOH;
Content-type: text/html

<html>
<head>
<title>管理画面</title>
</head>

<body>
パスワードが違います<br>
<a href="$login">ログイン</a>
</body>
</html>
EOH
exit;
}

print <<EOH;
Content-type: text/html

<html>
<head>
<title>メニュー</title>
</head>

<body>
<CENTER>
<TABLE width="100%" height="100%">
  <TBODY>
    <TR>
      <TD valign="middle" align="center">
      <TABLE width="300" height="200" cellpadding="1" cellspacing="1" bgcolor="#ffffff">
  <TBODY>
    <TR>
            <TD colspan="2" align="center" bgcolor="#c1eafd" height="80">編集メニュー</TD>
          </TR>
    <TR>
            <TD align="center" bgcolor="#d8f3fe" height="40">新規作成</TD>
            <TD bgcolor="#b9ccff" height="40" nowrap valign="middle" align="center"><BR>
            <form action="topics.cgi" method="GET"><INPUT type="submit" value="新規"><input type="hidden" name="mode" value="0"></form>
</TD>
          </TR>
    <TR>
            <TD align="center" bgcolor="#d8f3fe" height="40">削除</TD>
            <TD align="center" bgcolor="#b9ccff" height="40" valign="middle"><BR>
            <form action="topics.cgi" method="GET"><INPUT type="submit" value="削除"><input type="hidden" name="mode" value="2"></form>
</TD>
          </TR>
    <TR>
            <TD align="center" bgcolor="#d8f3fe" height="40">編集・詳細追加</TD>
            <TD align="center" bgcolor="#b9ccff" height="40" valign="middle"><BR>
            <form action="topics.cgi" method="GET"><INPUT type="submit" value="編集"><input type="hidden" name="mode" value="4"></form>
</TD>
          </TR>
  </TBODY>
</TABLE>
      </TD>
    </TR>
  </TBODY>
</TABLE>
</CENTER>
</BODY>
</html>
EOH
exit;
