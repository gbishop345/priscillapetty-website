<?php
//=============================================================//
//
// ! YABDAB SMART STACK - FORMLOOM JR. v 1.0.0
// - edited: 09-15-10 05.35.30 AM
// - author: Mike Yrabedra
// - (c)2010 Yabdab Inc. All rights reserved.
//
//	Harvesting code from this script is prohibited.
//	If you are caught using any code found here, it will be made very public, and very ugly.
//	Don't steal code ( or ideas ), create your own.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
//  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
//  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
//  THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
//  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
//  OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
//  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR 
//  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
//  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//=============================================================//

//=============================================================//
// ! DEBUGGING
//=============================================================//

// If you are having problems, them uncomment the following 2 lines to see what is going wrong.
//error_reporting(E_ALL);
//ini_set('display_errors', 1);

function ydssStringCleaner($str) { 
	$str = preg_replace( '((?:\n|\r|\t|%0A|%0D|%08|%09)+)i' , '', $str );
	// Remove those slashes
	if(get_magic_quotes_gpc()){
		$str = stripslashes($str);
	}
	
	return $str;
} 


function YDSSValidateEmail($email) {
   //check for all the non-printable codes in the standard ASCII set,
   //including null bytes and newlines, and exit immediately if any are found.
   if (preg_match("/[\\000-\\037]/",$email)) {
      return false;
   }
   $pattern = "/^[-_a-z0-9\'+*$^&%=~!?{}]++(?:\.[-_a-z0-9\'+*$^&%=~!?{}]+)*+@(?:(?![-.])[-a-z0-9.]+(?<![-.])\.[a-z]{2,6}|\d{1,3}(?:\.\d{1,3}){3})(?::\d++)?$/iD";
   if(!preg_match($pattern, $email)){
      return false;
   }
   return true;
} 



function ydssSendEmail($stack, $p)
{

	//clean the input
	
	$YDSSfromemail = ydssStringCleaner($stack['fromemail']);
	$YDSSfromname = ydssStringCleaner($stack['fromname']);
	$YDSStoemail = ydssStringCleaner($stack['toemail']);
	$YDSStoname = ydssStringCleaner($stack['toname']);
	
	$YDSSto = $YDSStoname . ' <' . $YDSStoemail . '>';
	
	$YDSSemail = ydssStringCleaner($p['ydss_email']);
	$YDSSname = ydssStringCleaner($p['ydss_name']);
	$YDSSsubject = ydssStringCleaner($p['ydss_subject']);
	$YDSSmsg = ydssStringCleaner($p['ydss_msg']);
	
	// generate the payload
	
	$browser = $_SERVER['HTTP_USER_AGENT'];
	$ipaddress = $_SERVER['REMOTE_ADDR'];
	$date = date('r');
	
	$YDSSbody = '';
	$YDSSbody .= ' Browser: ' . $browser . PHP_EOL;
	$YDSSbody .= ' IP Address: ' . $ipaddress . PHP_EOL;
	$YDSSbody .= ' Date: ' . $date . PHP_EOL;
	$YDSSbody .= PHP_EOL . $stack['subjectlabel'] . ' : ' . $YDSSsubject . PHP_EOL;
	$YDSSbody .= $stack['namelabel'] . ' : ' . $YDSSname . PHP_EOL;
	$YDSSbody .= $stack['emaillabel'] . ' : ' . $YDSSemail . PHP_EOL;
	$YDSSbody .= PHP_EOL . $stack['msglabel'] . ' : ' . PHP_EOL;
	$YDSSbody .= PHP_EOL . $YDSSmsg . PHP_EOL;
	
	
	$YDSSheaders = '';
	$YDSSheaders .= 'From: ' . $YDSSfromname . ' <' . $YDSSfromemail . '>' . PHP_EOL;
	$YDSSheaders .= 'Reply-To: ' . $YDSSname . ' <' . $YDSSemail . '>' . PHP_EOL;
	$YDSSheaders .= 'Return-Path: ' . $YDSSfromname . ' <' . $YDSSfromemail . '>' . PHP_EOL;
	$YDSSheaders .= "Message-ID: <" . time() . $YDSStoemail . ">" . PHP_EOL;
	$YDSSheaders .= 'X-Sender-IP: ' . $_SERVER["REMOTE_ADDR"] . PHP_EOL;
	$YDSSheaders .= 'MIME-Version: 1.0' . PHP_EOL;
	$YDSSheaders .= 'Content-type: text/plain; charset="utf-8"' . PHP_EOL;
	$YDSSheaders .= 'Content-transfer-encoding: 8bit' . PHP_EOL;
	
	
	// send
	if( mail($YDSSto, $YDSSsubject, $YDSSbody, $YDSSheaders) ) { return 'good'; }else{  return 'fail'; }
	
	
}