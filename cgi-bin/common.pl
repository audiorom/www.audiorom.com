#!/usr/bin/perl#########################################################################################################################################################use CGI;### declare variables ############################sub declare_vars {  $arcpath = "/export/ftp/audiorom-up";  $curtime = time;  ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($curtime);  @months = ("JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"); }sub show_result {  my ($title,$head,$dates, @messages) = @_;  print $q->header;  print $q->start_html(-title=>"$title",    			-BGCOLOR        =>'white',                        -TEXT           =>'#000000',                        -LINK           =>'#356E6B',                        -VLINK          =>'#356E6B',                        -ALINK          =>'#356E6B');  print "<center><h1>$head</h1></center><UL>\n";  print "<p>$dates</p>";  for (@messages) {    print ("$_\n");  }  print"</UL>\n";  print $q->end_html}                       ### HTML error print ###sub HTML_error {  my(@msg) = @_;  my($i,$name);  if (!@msg) {   $name = &script_name();   @msg = ("Error: script $name encountered an unknown error");  }  print $q->header;    print $q->start_html (-title => "Total Telecom: Error",         		-BGCOLOR	=>'white',			-TEXT		=>'#000000',			-LINK		=>'#356E6B',			-VLINK		=>'#356E6B',			-ALINK		=>'#356E6B'),	"<H3>$msg[0]</H3>\n";  foreach $i (1..$#msg) {    print ("<P>$msg[$i]\n");  }  print($q->end_html);}### HTML Death ###sub HtmlDie {  my(@msg)=@_;  &HTML_error(@msg);  die @msg;}1;	