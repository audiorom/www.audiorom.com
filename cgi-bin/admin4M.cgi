#!/usr/bin/perl############################## Admin4M 1.0 - Multi-forum Administration Tool# Copyright 1996 by Innergy Inc.# # Developed by:  # 	Gordon Benett		<gbenett@innergy.com># from the freeware original 'WWWadmin' by:# 	Matt Wright			<mattw@worldwidemart.com>## Requires Perl 5.x (for hard references).# Use constitutes acceptance of terms:# Script is offered as-is, with NO WARRANTY whatsoever.# May be copied, distributed and used with attribution # as long as copyright notice is intact.# Bug reports can be sent to <ThisOldWeb@innergy.com>############################# Revision history##	v1.00 [11.16.96]#	- added control console for managing multiple forums# 	Version 0.2 [08.25.96]#	- trimmed config setup# 	Version 0.1 [02.02.96]# 	- Added pagination for Remove and Remove_by_Number options#	- Deleted superfluous bolding of table headers#############################  use strict 'refs';	# ensures safe pointers in Perl 5  require( 'multi4M.cfg' );############################## Setup (hard-coded portion)## URL of this script    $cgiURL = "/cgi-bin/$adminProg";	# Miscellaneous config settings	$delExt = 'x';			# mark files for deletion	$use_sig  = '1';		# 1 = yes, 0 = no	# Time- as well as date-stamp threads?    $timeStyle = 1;     	# 1=date/time; 0=date only# Page length for tables	$pgRows = 72;	# set <90 to avoid browser problems# ----------------# signature stuff # ----------------	$divider="$homeURL/pix/divider.gif";	$siglink="http://www.innergy.com/tg/";	$sigimg= "$homeURL/pix/tg_logo.gif";	$sigtext="Techne Group: tgroup\@innergy.com";	## Setup ends####################################################################################################################################### Main sequence#  # Script can be called in three ways:  if (($ENV{'CONTENT_LENGTH'} == 0) && ($ENV{'QUERY_STRING'} eq '')) {	  # First call, no parameters passed	  print "Content-type: text/html\n\n";	  &showConsole;	  exit(0);  }  elsif ($ENV{'QUERY_STRING'} ne '') {      # Called by URL, method GET	  ($FORM{'command'}, $FORM{'bb_id'}) = &parseQuery;  }  else {      # Else called by Form using method POST	  &parseForm;  }  $command = $FORM{'command'};  ($bb_dir, $bb_name) = split(/$sep/, $FORM{'bb_id'});  if ($command eq 'browse') {	  # Redirect and quit	  print "Location: $homeURL/$bb_dir/$bb_file\n\n";  }  elsif ($command eq 'archive') {	  # Jump to Archive module	  exec( $archivProg, $FORM{'bb_id'}, $FORM{'month'}, $FORM{'day'}, $FORM{'year'} );  }  else {	  # Prepare server for HTML output and continue	  print "Content-type: text/html\n\n";	  $pwPath = "$homepath/$bb_dir/$shiboleth";	# Macros for navigation bars	  $AdminLink = "<a href=\"$cgiDir/$adminProg\">Admin Console</a>";	  $HomeLink = "<a href=\"$homeURL\">Site Home</a>";	  $ForumLink = "<a href=\"$homeURL/$bb_dir/$bb_file\">Forum</a>";	  $mode = $FORM{'mode'};	  $verb = ($mode == 'del') ? 'Remove' : 'Archive';      $banner = "$verb Messages";	  $slurpref = \@bbLines;	  &read4M( $slurpref );  }###################################################################### 	Remove#      = Shows threads in order they appear in bb_file#####################################################################if ($command =~ /^remove([1-9]*)/) {   $thisPage = ($1 eq '') ? 1 : $1;   &mkHead("$banner", "$homeURL/$bb_dir", STDOUT);   &mkPageIntro( $banner );print <<'bLurB';   <p><font size=+2>S</font>elect postings you wish to remove ...   Checking the Button marked 'Thread' will remove the whole thread,   while checking the Button marked 'Single' will remove just that posting.   These messages have been left in the order they appear in the page    to indicate what the threads look like --    which is often more helpful than a sorted view.</p>bLurB   &mkRemovalForm;		# starts <form>   &buildMsgTable( \@ENTRIES );   &mkPageFooter;		# ends </form>}###################################################################### 	Remove By Number#       = Shows messages in ascending numerical order#####################################################################elsif ($command =~ /^remByNum([1-9]*)/) {   $thisPage = ($1 eq '') ? 1 : $1;   $banner .= " by Number";   &mkHead("$banner", "$homeURL/$bb_dir", STDOUT);   &mkPageIntro( $banner );print <<'bLurB';   <p><font size=+2>S</font>elect below to remove those postings you wish to remove.   Checking the Button marked 'Thread' will remove the whole thread,   while checking the Button marked 'Single' will remove just that posting.</p>bLurB   &mkRemovalForm;		# starts <form>   &buildMsgTable( \@SORTED_ENTRIES );   &mkPageFooter;		# ends </form>}############################################################## 	Remove By Date											##       = Shows messages in date order, earliest first		##############################################################elsif ($command eq 'remByDate') {   $banner .= " by Date";   &mkHead("$banner", "$homeURL/$bb_dir", STDOUT);   &mkPageIntro( $banner );print <<'bLurB';   <p><font size=+2>T</font>his option summarizes messages received by date. Set the    checkbox to mark the messages in a row for deletion. The table is    also useful for seeing how many postings arrived on a given date.</p>bLurB   print "<form method=POST action=\"$cgiURL\">\n";   print "<input type=hidden name=\"action\" value=\"remByDateAuthor\">\n";   print "<input type=hidden name=\"type\" value=\"remByDate\">\n";   print "<input type=hidden name=\"bb_id\" value=\"$FORM{'bb_id'}\">\n";   print "<center><table cellpadding=4 border=1>\n";   print "<tr>\n";   print "<th colspan=4>Username: <input type=text name=\"username\"> -- Password: <input type=password name=\"password\"><br></th>\n";   print "</tr><tr>\n";   print "<th>X </th><th>Date </th><th># of Messages </th><th>Message Numbers<br></th></tr>\n";   my( $msgnum );   foreach (@bbLines) {	   next unless m#<\!--top: (\d*)-->#;	   $msgnum = $1;	   m#"$msgdir/$msgnum[^>]+>.*</a>[ -]+<b>.*</b>\s+<i>(.*)</i>#;	   $date = $1;	   if ($timeStyle == 1) {	      ($day, $_) = split(/[ ]+/,$date);	# cull date, trash time	   }	   else {	      $day = $date;	   }	   $DATE{$msgnum} = $day;   }   &hash2Table( \%DATE );   print "<pre>\n\n</pre>\n";   print "<p align=\"center\">[ $AdminLink | $ForumLink | $HomeLink ]</p>\n";   print "</body></html>\n";}################################################################## 	Remove By Author											##		= Lists message authors in ascending alpha order		##################################################################elsif ($command eq 'remByAuthor') {   $banner .= " by Author";   &mkHead("$banner", "$homeURL/$bb_dir", STDOUT);   &mkPageIntro( $banner );print <<'bLurB';   <p><font size=+2>C</font>hecking the checkbox beside the name of an    author will remove all postings which that author has created.</p>bLurB   print "<FORM method=POST action=\"$cgiURL\">\n";   print "<input type=hidden name=\"action\" value=\"remByDateAuthor\">\n";   print "<input type=hidden name=\"type\" value=\"remByAuthor\">\n";   print "<input type=hidden name=\"bb_id\" value=\"$FORM{'bb_id'}\">\n";   print "<center><table cellpadding=4 border=1>\n";   print "<tr>\n";   print "<th colspan=4>Username: <input type=text name=\"username\"> -- Password: <input type=password name=\"password\"><br></th>\n";   print "</tr><tr>\n";   print "<th>X </th><th>Author </th><th># of Messages </th><th>Message #'s<br></th></tr>\n";   foreach (@bbLines) {      next unless (m%<\!--top: (.*)-->.+"$msgdir/$1[^>]+>.*</a>[ -]+<b>(.*)</b>\s+<i>.*</i>%i);      ($AUTHOR{$1} = $2) =~ tr/A-Z/a-z/;	# remove case ambiguity in names   }   &hash2Table( \%AUTHOR );   print "<pre>\n\n</pre>\n";   print "<p align=\"center\">[ $AdminLink | $ForumLink | $HomeLink ]</p>\n";   print "</body></html>\n";}######################################################################	Change Password													##		= Routine enabling authenticated users to change password	######################################################################elsif ($command eq 'chgPasswd') {   $banner = "Change Admin Password";   &mkHead("$banner", "$homeURL/$bb_dir", STDOUT);   &mkPageIntro( $banner );print <<'bLurB';   <p>Fill out the form below completely to change your password and user name.   If new username is left blank, your old one will be assumed.</p>bLurB   print "<form method=POST action=\"$cgiURL\">\n";   print "<input type=hidden name=\"action\" value=\"chgPasswd\">\n";   print "<input type=hidden name=\"bb_id\" value=\"$FORM{'bb_id'}\">\n";   print "<center><table cellpadding=4 border=1>\n";   print "<tr>\n";   print "<th>Username: </th><td><input type=text name=\"username\"><br></td>\n";   print "</tr><tr>\n";   print "<th>Password: </th><td><input type=password name=\"password\"><br></td>\n";   print "</tr><tr>\n";   print "<th>New Username: </th><td><input type=text name=\"newUsername\"><br></td>\n";   print "</tr><tr>\n";   print "<th>New Password: </th><td><input type=password name=\"passwd_1\"><br></td>\n";   print "</tr><tr>\n";   print "<th>Re-type New Password: </th><td><input type=password name=\"passwd_2\"><br></td>\n";   print "</tr><tr>\n";   print "<td align=\"center\"><input type=submit value=\"Change Password\"></td>\n";   print "<td align=center><input type=reset value=\"Cancel\"}></td>\n";   print "</tr></table></center></form>\n";   &printSig;   print "</body></html>\n";}###################################################################### 	Remove Action (by thread or number)#		= This block is used by the methods 'remove' and 'remByNum'#####################################################################elsif ($FORM{'action'} eq 'remove') {# ------------------------------------# Implements msg deletion in main board by splicing # memory image @bbLines. Marks msg files for deletion.# Builds three status lists -- @NOT_REMOVED,# @NO_FILE, @ATTEMPTED -- used by &sendStatus# ------------------------------------   &authenticateUser($FORM{'username'}, $FORM{'password'}, $pwPath);   # exits with notice on failure   &write4M( "$homepath/$bb_dir/$bb_file.$rollbackExt" ) || &error(badBackup);   # back up current bb or quit   #------------------------------------   # build deletion lists @ALL, @SINGLE   #------------------------------------   for ($i=$FORM{'min'}; $i<=$FORM{'max'}; $i++) {      if ($FORM{$i} eq 'all') {		# add msgnum $i to list that         push(@ALL,$i);				# deletes entire thread      }	  elsif ($FORM{$i} eq 'single') {		 push(@SINGLE,$i);			# add msgnum $i to list that      }   							# deletes one message   }   #-----------------   # process @SINGLE   #-----------------   foreach $msg2del (@SINGLE) {      for ($j=0; $j<=@bbLines; ) {         if ($bbLines[$j] =~ /<\!--top: $msg2del-->/) {            push(@arcLines, splice(@bbLines, $j, 3));         }         elsif ($bbLines[$j] =~ /<\!--end: $msg2del-->/) {            push(@arcLines, splice(@bbLines, $j, 1));         }		 else { $j++; }      }   }   &modifyMsgs( \@SINGLE );   #-----------------   # process @ALL   #-----------------   foreach $msg2del (@ALL) {      undef($top); undef($bottom);      for ($j=0; $j<=@bbLines; $j++) {         if ($bbLines[$j] =~ /<!--top: $msg2del-->/) {             $top = $j;		# target found at top of thread         }         elsif ($bbLines[$j] =~ /<!--end: $msg2del-->/) {            $bottom = $j;	# thread ends         }      }      $diff = $bottom - $top + 1;      for ($k=$top; $k<=$bottom; $k++) {		  if ($bbLines[$k] =~ /<!--top: (.*)-->/) {			  push(@DELETE,$1);		  }	  }	        push(@arcLines, splice(@bbLines, $top, $diff));	# delete from bb_file	  &modifyMsgs( \@DELETE );   }   # write modified over existing bb_file   &update4M;}###################################################################### 	Remove Action (by Date or Author)								##		= This block is used to implement deletions by methods 		##		remByDate or remByAuthor.     		  						######################################################################elsif ($FORM{'action'} eq 'remByDateAuthor') {   # Exits with notice on failure   &authenticateUser($FORM{'username'}, $FORM{'password'}, $pwPath);   # Back-up current forum or Fail   &write4M( "$homepath/$bb_dir/$bb_file\.$rollbackExt" ) || &error(badBackup);   @keyList = split(/\s/,$FORM{'usedValues'});   foreach $hit (@keyList) {      # Read embedded, space-separated lists from remBy* form	  # and grow a list of msg numbers 2b deleted	  @MSG2DEL = ( @MSG2DEL, split(/\s/,$FORM{"$hit"}) );   }   foreach $msg2del (@MSG2DEL) {      for ($j=0; $j<=@bbLines; ) {         if ($bbLines[$j] =~ /<!--top: ${msg2del}-->/) {            push(@arcLines, splice(@bbLines, $j, 3));         }         elsif ($bbLines[$j] =~ /<!--end: ${msg2del}-->/) {            push(@arcLines, splice(@bbLines, $j, 1));         }		 else { $j++; }      }   }   &modifyMsgs( \@MSG2DEL );   # write modified over existing bb_file   &update4M;}elsif ($FORM{'action'} eq 'chgPasswd') {   # Check typing   if ($FORM{'passwd_1'} ne $FORM{'passwd_2'}) {      &error(pwTypo);   }   &authenticateUser($FORM{'username'}, $FORM{'password'}, $pwPath);      # Common sense checks on new passwd   if (length( $FORM{'passwd_1'} ) < $MinPasswdLength) {	   &error(tooShort);   }      # Attempt to change user/password   open(PASSWD,">$pwPath") || &error(aclWrite);   $newPasswd = crypt($FORM{'passwd_1'}, substr($FORM{'passwd_1'}, 0, 2));   if ($FORM{'newUsername'}) {      $newUsername = $FORM{'newUsername'};   }   else {      $newUsername = $username;   }   print PASSWD "$newUsername:$newPasswd";   close(PASSWD);   &sendStatus(chgPasswd);}##################################################			 	Local Subroutines				##################################################sub parseQuery {   local( @arg ) = split(/&/, $ENV{'QUERY_STRING'});   foreach ( @arg ) {      # Un-Webify plus signs and %-encoding      tr/+/ /;      s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;   }   return( @arg );}sub urlEncode {	$_[0] =~ tr/ /+/;}sub showConsole {#-----------------------------------------# Build form-based control console#-----------------------------------------	&readRegDB( "$homepath/$regfile" );	&mkHead( "Admin4M Console", "$homeURL", STDOUT );	print "<body bgcolor=\"$CONSOLE_BGCOLOR\" text=\"$CONSOLE_TEXT\">\n";	print "<h1 align=\"center\">Admin4M Control Console</h1>\n";		print "<FORM METHOD=POST ACTION=\"$cgiURL\">\n";	print "<center><table width=\"80%\" cellpadding=6 border=1>\n";	print "<tr><td align=\"left\" width=\"40%\">\n";	print "<dl><dt>$verb Files<dd>\n";	print "<input type=\"radio\" name=\"command\" value=\"remove\"> by Thread<BR>\n";	print "<input type=\"radio\" name=\"command\" value=\"remByNum\"> by Message Number<BR>\n";	print "<input type=\"radio\" name=\"command\" value=\"remByDate\"> by Date<BR>\n";	print "<input type=\"radio\" name=\"command\" value=\"remByAuthor\"> by Author<BR>\n";	print "</dd><p>\n";	print "<dt>Browse<dd>\n";	print "<input type=\"radio\" name=\"command\" value=\"browse\"> Go to Forum\n";	print "</dd><p>\n";	print "<dt>Authentication<dd>\n";	print "<input type=\"radio\" name=\"command\" value=\"chgPasswd\"> Change Password\n";	print "</dd><p>\n";	print "</dl></td>\n";		# Compose list of forums available for update	# Identify by concatenating bb_dir::bb_name to 'bb_id'	print "<td align=\"center\">Pick a forum:<br>\n";	print "<select name=\"bb_id\" size=4>\n";	foreach (sort keys( %REGLIST )) {		print "<option value=\"$_$sep$REGLIST{ $_ }\"> $REGLIST{ $_ }\n";	}	print "</select></td>\n";	print "</tr><tr>\n";	print "<th COLSPAN=2><input type=submit value=\"Execute\"> <input type=reset value=\"Clear\"></th>\n";	print "</tr></table></center></FORM>\n";	print "<p align=\"center\">[ <a href=\"$homeURL\">Home</a> ]</p>\n";	print "</body></html>\n";}sub read4M { #-----------------------------------------# Slurps forum specifed by $bb_file into global array '@bbLines'#-----------------------------------------   local( $aref ) = $_[0];   open( BB,"$homepath/$bb_dir/$bb_file" ) || &error(bad4MRead);   @$aref = <BB>;   close( BB );}sub mkPageIntro {   local( $s ) = $_[0];	   print "<BODY>\n<h1 align=\"center\">$s</h1>\n";   print "<h3 align=\"center\"><I>Target: $bb_name</I></h3>\n";   print "<p align=\"center\"><IMG SRC=\"$divider\" ALT=\"separator\"></p>\n";}sub buttonBar {	# [ $verb | $verb by Date | ...by Author | ...by Num | Forum | Home ]	local( $urlEncodedID ) = &urlEncode($FORM{'bb_id'});	print "<p align=\"center\"><font size=-1>\n";	print "[ <a href=\"$cgiURL\?remove\&$urlEncodedID\">$verb</a> | \n";	print "<a href=\"$cgiURL\?remByDate\">$verb by date</a> | \n";	print "<a href=\"$cgiURL\?remByAuthor\">$verb by Author</a> | \n";	print "<a href=\"$cgiURL\?remByNum\">$verb by Number</a> | \n";	print "<a href=\"$homeURL/$bb_dir/$bb_file\">$bb_name</a> | <A HREF=\"$homeURL\">Home</A> ]\n";	print "</font></p>\n";}sub mkRemovalForm { #-----------------------------------------# Builds parts of query FORM common to remove # and remByNum commands#-----------------------------------------   local( $msgnum );   $command =~ s/^(rem[^\d]+)\d*/$1/;	# Strip any page numbers   									# to make generic 'type'   print "<form method=POST action=\"$cgiURL\">\n";   # Embed call to removal method in generated form   print "<input type=hidden name=\"action\" value=\"remove\">\n";   print "<input type=hidden name=\"type\" value=\"$command\">\n";   print "<input type=hidden name=\"bb_id\" value=\"$FORM{'bb_id'}\">\n";   foreach ( @bbLines ) {      next unless m#<!--top: (\d*)-->#;	  $msgnum = $1;      push( @ENTRIES,$msgnum );	  m#"$msgdir/$msgnum[^>]+">(.*)</a>[ -]+<b>(.*)</b>\s+<i>(.*)</i>#;      $SUBJECT{$msgnum} = $1;      $AUTHOR{$msgnum} = $2;      $DATE{$msgnum} = $3;   }   @SORTED_ENTRIES = (sort { $a <=> $b; } @ENTRIES);   $max = $SORTED_ENTRIES[$#ENTRIES];   $min = $SORTED_ENTRIES[0];   print "<input type=hidden name=\"min\" value=\"$min\">\n";   print "<input type=hidden name=\"max\" value=\"$max\">\n";   # ------------------   # Pagination routine   # ------------------   if ( @ENTRIES % $pgRows ) {	# Round up	   $numPages = int( @ENTRIES/$pgRows ) + 1;   }   else { $numPages = @ENTRIES/$pgRows; }### Debugprint "<p align=\"center\">\n";if (@ENTRIES > 0) {	my( $word ) = 'message';	$word .= 's' if (@ENTRIES > 1);	print "Found ", scalar(@ENTRIES), " $word spanning <br>\n";	# Strip times	($oiliest = $DATE{$min}) =~ s#([\d/]+)\s+([\d:]+)#$1#;	($latemost = $DATE{$max}) =~ s#([\d/]+)\s+([\d:]+)#$1#;	print "$oiliest -- $latemost<br>\n";	print "This is page $thisPage of $numPages ($pgRows lines ea.)";}else {	print "No records found; forum appears to be empty."}print "</p>\n";   # ------------------   # Calculate paginated lastRow   # ------------------   if ($thisPage == $numPages) {	# We're on last page	   $lastRow = $#ENTRIES;		# so last row is last entry   }   else {	   $lastRow = ($thisPage * $pgRows) - 1;   }}sub buildMsgTable { # Requires Perl 5#-----------------------------------------# Builds table for remove & [remByNum]# 'aref' is pointer to @ENTRIES or [@SORTED_ENTRIES]# 'i' counts table rows#-----------------------------------------	local( $aref ) = $_[0];	local( $i, $entry );    print "<center><table cellpadding=4 border=1>\n";# Top Row -- usrname + passwd text boxes    print "<tr>\n";    print "<th colspan=6>Username: <input type=text name=\"username\"> -- Password: <input type=password name=\"password\"></th>\n";# Row 2 -- column titles    print "</tr><tr>\n";    print "<th>Post # </th><th>Thread </th><th>Single </th><th>Subject </th><th> Author</th><th> Date</th></tr>\n";	for ($i=($thisPage - 1)*$pgRows; $i<=$lastRow; $i++) {	   $entry = $aref->[$i];	   print "<tr>\n";	   print "\t<th>$entry </th>\n";	   print "\t<td><input type=radio name=\"$entry\" value=\"all\"></td>\n";	   print "\t<td><input type=radio name=\"$entry\" value=\"single\"></td>\n";	   print "\t<td><a href=\"$homeURL/$bb_dir/$msgdir/$entry\.$ext\">$SUBJECT{$entry}</a></td>\n";	   print "\t<td>$AUTHOR{$entry}</td>\n";	   print "\t<td>$DATE{$entry}</td>\n";	   print "</tr>\n";   }# End table   print "<tr>\n";   print "<th align=\"center\" colspan=6><input type=submit value=\"$verb Messages\"> <input type=reset value=\"Clear\"></th>\n";   print "</tr>\n";   print "</table></center></form><p>\n";}sub mkPageFooter {#-----------------------------------------# Prints page number and ends HTML on remove forms#-----------------------------------------   local( $id ) = $FORM{'bb_id'};   &urlEncode( $id );   print "<table width=\"100%\" cellpadding=10 border=0>\n";   print "<tr><td align=\"left\">[ ";   if ($thisPage < $numPages) {	   $nextPage = $thisPage + 1;	   print "<a href=\"$cgiURL\?$command$nextPage\&$id\">Next</a> |\n";   }   elsif ($numPages > 1) {	   print " <a href=\"$cgiURL\?$command\&$id\">1</a> |\n";   }   print "<a href=\"$cgiURL\">Admin4M Console</a> ]</td>\n";   print "<td align=\"right\">$thisPage of $numPages</td></tr>\n";   print "</table>\n";   print "</body></html>";	}sub hash2Table { # requires Perl 5#-----------------------------------------# Routine common to remByDate and remByAuthor#-----------------------------------------    local( $hashref ) = $_[0];	local( $match, $key, $hitCount ); 	   undef(@keyList);   # Compare each date or author with     foreach $value (sort values(%$hashref)) {      $match = 0;      $hitCount = 0;      foreach $hit (@keyList) {         if ($value eq $hit) {            $match = 1;            last;         }      }      if ($match == 0) {         undef(@listOfKeyHREFs); undef(@listOfKeyNums);         foreach $key (keys %$hashref) {            if ($value eq $$hashref{$key}) {               $keyHREF = "<a href=\"$homeURL/$bb_dir/$msgdir/$key\.$ext\">$key</a>";               push(@listOfKeyHREFs,$keyHREF);			   push(@listOfKeyNums,$key);               $hitCount++;            }         }		 # Canonize date separators and spaces to underbars; names to lowercase         ($formValue = $value) =~ tr/\/ A-Z/__a-z/;		          print "<tr>\n<td><input type=checkbox name=\"$formValue\" value=\"@listOfKeyNums\"></td>\n";         print "<th>$value</th>\n<td>$hitCount </td>\n<td>@listOfKeyHREFs<br></td></tr>\n";         push(@keyList,$value);         push(@usedFormValues,$formValue);	  }   }   print "</table>\n";   print "<input type=hidden name=\"usedValues\" value=\"@usedFormValues\">\n";   print "<input type=submit value=\"$verb Messages\"> <input type=reset value=\"Clear\">\n";   print "</form></center>\n";}sub authenticateUser {   local( $user, $key, $acl ) = @_;   local( $pw ) = '';      open(PASSWD,"$acl") || &error(aclRead);   $_ = <PASSWD>;   close(PASSWD);   chop if /\n$/;   ($username,$passwd) = split(/:/);   $pw = crypt($key, substr($passwd, 0, 2));   if (($pw ne $passwd) || ($user ne $username)) {      &error(notAuth);   }}sub write4M {	local( $file ) = $_[0];		open(BB,">$file");	chmod 0664, $file;    print BB @bbLines;	close( BB );}sub modifyMsgs {#-----------------------------------------# Renames files to be deleted, a list of # which must be passed by reference.# Updates 3 global arrays to report status.#-----------------------------------------	local( $listref ) = $_[0];	local( $msg );		foreach $msg (@$listref) {	# mark files for deletion		$file2del = "$homepath/$bb_dir/$msgdir/$msg\.$ext";		if (-e $file2del) {			rename("$file2del","$file2del\.$delExt" ) || push(@NOT_REMOVED, $msg." ");		}		else {			push(@NO_FILE, $msg." ");		}		push(@ATTEMPTED, $msg." ");	}}sub update4M {   open(BB,">$homepath/$bb_dir/$bb_file") || &error(bad4MWrite);   print BB "@bbLines";   close(BB);   &sendStatus($FORM{'type'});}sub sendStatus {#-----------------------------------------# Report results of action taken#-----------------------------------------   local($type) = $_[0];   local($acktext) = "Results of Message Removal";   # Compose acknowledgement based on action taken   if ($type =~ /^rem/) {	   if ($type eq 'remByNum') {		   $acktext .= " by Number";	   }	   elsif ($type eq 'remByDate') {		   $acktext .= " by Date";       }	   elsif ($type eq 'remByAuthor') {		   $acktext .= " by Author";       }	  &mkHead( $acktext, $homeURL, STDOUT );	  &mkPageIntro( $acktext );      print "<p><font size=+2>B</font>elow is a short summary of messages removed from $bb_name and its \n";      print "$msgdir directory. Files the script attempted to remove were removed \n";      print "reliably unless otherwise noted.</p>\n";	  print "<hr size=4 width=75%><p>\n";      print "<blockquote>\n";	  print "<p><b>Messages removed from forum:</b> @ATTEMPTED <\p>\n";	  print "<p><font size=-1>(Message files renamed to \'<i>\*.$ext.$delExt</i>\' in dir \'<i>$bb_dir</i>\' for \n";	  print "eventual deletion.)</font></p>\n";      if (@NOT_REMOVED) {         print "<b>Some files could not be renamed:</b> @NOT_REMOVED<p>\n";      }      if (@NO_FILE) {         print "<b>Message files Not Found:</b> @NO_FILE<p>\n";      }#	  print "Lines deleted from forum:<p>\n";#	  print @arcLines;      print "</blockquote>\n";	  print "<hr size=4 width=75%><p>\n";   }   elsif ($type eq 'chgPasswd') {	  $banner = "Admin Password Changed";	  &mkPageIntro( $banner );      print "<p><font size=+2>T</font>he password for administering $bb_name has been changed!</p>\n";      print "<blockquote><p>Results are as follows:</p>\n";	  print "<ul type=\"square\">\n";	  print "<lh><hr align=\"left\" width=\"33%\"></lh>\n";      print "<li><b>New Username: $newUsername</b>\n";      print "<li><b>New Password: $FORM{'passwd_1'}</b>\n";	  print "</ul></blockquote>\n";	  print "<center><table cellpadding=8 border=4>\n";	  print "<tr><th>\n";      print "<I>Don\'t forget these, since they are now encoded in a file, and N<font size=-1>OT READABLE</font>!</I>\n";	  print "</th></tr></table></center>\n";   }   print "<p align=\"center\">[ $AdminLink | $ForumLink | $HomeLink ]</p>\n";   print "</body></html>\n";}sub printSig {#-----------------------------------------# Prints (hard-coded) signature#-----------------------------------------	  return if ($use_sig ne '1');      print "<H5 ALIGN=\"center\">Site design by<BR>\n";      print "<A HREF=\"$siglink\"><IMG BORDER=0 SRC=\"$sigimg\" ALT=\"$sigtext\"></A></H5>\n";}sub readRegDB { #-----------------------------------------# Reads regfile and loads bb_dir::bb_name# pairs into (global) hash %REGLIST#-----------------------------------------	local( $x, $y );		open( REGF, "$_[0]" ) || &error(bad_reg);	while (<REGF>) {		chop;		next if /^(\s*#|\s*$)/;	# skip blank & comment lines		s/^\s+(\S)/$1/;			# eat leading spaces		($x,$y) = split( /$sep/ );		$REGLIST{$x} = $y;	}	close( REGF );}sub error {#-----------------------------------------# Error handler. Arg is string specifying error type.#-----------------------------------------   $err = $_[0];   local( $msg, $detail );   if ($err eq 'notAuth') {	  $msg = "Bad Username - Password Combination";	  $detail = "You entered and invalid username password pair. Try again.";   }   elsif ($err eq 'aclRead') {	  $msg = "Couldn't Open Password File For Reading";	  $detail = "Problem reading $pwPath, $shiboleth: Fix permissions and try again.";   }   elsif ($err eq 'aclWrite') {	  $msg = "Couldn't Open Password File For Writing";	  $detail = "Problem writing $shiboleth: Password not changed.";   }   elsif ($err eq 'pwTypo') {	  $msg = "Incorrect Password Type-In";	  $detail = "The passwords you typed in for your new password were not the same.\nYou may have mistyped, please try again.";   }   elsif ($err eq 'bad4MRead') {	  $msg = "Couldn't read forum \'$bb_name\'";	  $detail = "$msg! System says: $!";   }   elsif ($err eq 'bad4MWrite') {	  $msg = "Couldn't write to forum \'$bb_name\'";	  $detail = "$msg! System says: $!";   }   elsif ($err eq 'badBackup') {	  $msg = "Couldn't back up forum \'$bb_name\'";	  $detail = "$rollbackExt $bb_file $homepath/$bb_dir/$bb_file $msgdir $msgfile $bb_file Copy to .$rollbackExt failed. System says: $!";   }   elsif ($err eq 'tooShort') {	  $msg = "New password too short";	  $detail = "Must be $MinPasswdLength characters or longer. Try again.";   }   elsif ($err eq 'bad_reg') {	  $msg = "Error: Problem Reading Registry";	  $detail = "Couldn't open the forum registry file, $regfile, for reading.";   }   print "<html><head><title>$msg</title></head>\n";   print "<body><h2 align=\"center\">$msg</h2>\n";   print "<p>$detail<\p>\n";   print "<pre>\n\n</pre>\n";   print "<hr size=4 width=75%>\n";   print "<p align=\"center\"><font size=-1>\n";   print "[ <a href=\"$cgiURL\">Admin4M Console</a> ] [ <a href=\"$homeURL\">Home</a> ]\n";   print "</font></p><hr size=4 width=75%>\n";   print "</body></html>\n";   exit(1);}sub Archiving { $mode == 'arc'; }