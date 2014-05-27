####### Pajilla v0.1 - xHamster Video Catcher #########
# Author: The X-C3LL
# http://0verl0ad.blogspot.com
# http://twitter.com/TheXC3LL
#######################################################

use LWP::UserAgent;
use WWW::Mechanize;
$url = $ARGV[0];
$file = $ARGV[1];
$del1 = ' <a href="';
$del2 = '" class="mp4Thumb"';

$ua= WWW::Mechanize->new( autocheck=>1 );
$response = $ua->get($url);
$html = $response->decoded_content; 
if ($html =~ m/$del1(.*)$del2/g) {
	$video = $1;
}

$ua->get($video,":content_file" => $file ) ;
