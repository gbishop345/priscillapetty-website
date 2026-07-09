<?php session_start(); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type"
        content="text/html; charset=utf-8" />
  <meta name="robots"
        content="all" />
  <meta name="generator"
        content="RapidWeaver" />

  <title>Contact Priscilla Petty</title>
  <link rel="stylesheet"
        type="text/css"
        media="screen"
        href="../rw_common/themes/simplebusiness/styles.css" />
  <link rel="stylesheet"
        type="text/css"
        media="print"
        href="../rw_common/themes/simplebusiness/print.css" />
  <link rel="stylesheet"
        type="text/css"
        media="handheld"
        href="../rw_common/themes/simplebusiness/handheld.css" />
  <link rel="stylesheet"
        type="text/css"
        media="screen"
        href=
        "../rw_common/themes/simplebusiness/css/sidebar/sidebar_left.css" />

<script type="text/javascript"
      src="../rw_common/themes/simplebusiness/javascript.js">
</script>
</head>

<body>
  <div id="sidebarContainer">
    <!-- Start Sidebar wrapper -->

    <div id="navcontainer">
      <!-- Start Navigation -->

      <ul>
        <li><a href="../index.html"
           rel="self">HOME</a></li>

        <li><a href="page3.php"
           rel="self"
           id="current"
           name="current">Contact Priscilla Petty</a></li>

        <li><a href="../page8/page8.html"
           rel="self">W. Edwards Deming</a></li>

        <li><a href="../page7/page7.html"
           rel="self">The Deming of America</a></li>

        <li><a href="../page26/page26.php"
           rel="self">Buy Deming of America DVD</a></li>

        <li><a href="../page9/page9.html"
           rel="self">About Priscilla Petty</a></li>

        <li><a href="../page17/page17.html"
           rel="self">Priscilla's Columns</a></li>

        <li><a href="../page18/page18.html"
           rel="self">Allain Philosophy &amp; Quotes</a></li>

        <li><a href="../page24/page24.html"
           rel="self">Priscilla's Blog</a></li>

        <li><a href="../page19/page19.html"
           rel="self">Quotes: P&amp;G Leaders</a></li>

        <li><a href="../page21/page21.html"
           rel="self">Have Your Say</a></li>

        <li><a href="../page22/page22.html"
           rel="self">Special Reports</a></li>

        <li><a href="../page23/page23.html"
           rel="self">Links</a></li>

        <li><a href="../page16/page16.html"
           rel="self">Site Map</a></li>
      </ul>
    </div><!-- End navigation -->

    <div id="sidebar">
      <!-- Start sidebar content -->

      <h1 class="sideHeader"></h1><!-- Sidebar header -->

      <br />
      <!-- sidebar content you enter in the page inspector -->
       <!-- sidebar content such as the blog archive links -->
    </div><!-- End sidebar content -->
  </div><!-- End sidebar wrapper -->

  <div id="container">
    <!-- Start container -->

    <div id="pageHeader">
      <!-- Start page header -->

      <h1>PriscillaPetty.com</h1>
    </div><!-- End page header -->

    <div id="contentContainer">
      <!-- Start main content wrapper -->

      <div id="content">
        <!-- Start content -->
        <?php
        if(!array_key_exists('formMessage', $_SESSION))
        $_SESSION['formMessage'] = "";
        if(!array_key_exists('form_element0', $_SESSION))
        $_SESSION['form_element0'] = "";
        if(!array_key_exists('form_element1', $_SESSION))
        $_SESSION['form_element1'] = "";
        if(!array_key_exists('form_element2', $_SESSION))
        $_SESSION['form_element2'] = "";
        if(!array_key_exists('form_element3', $_SESSION))
        $_SESSION['form_element3'] = "";
        ?>

        <div class="message-text">
          <?php
          if (!$_SESSION['formMessage']) { 
          echo 'You can write to Priscilla Petty at:<br />    Petty Consulting Productions<br />    229 Oliver Road<br />    Cincinnati, Ohio 45215<br /><br />You can email Priscilla Petty at:  <strong>priscilla@priscillapetty.com</strong><br />Or, you can fill in the form below to send an email.';
          } else {
           echo $_SESSION['formMessage'];
           }
           ?>
        </div>
        <br />

        <form action="./files/mailer.php"
              method="post"
              enctype="multipart/form-data">
          <label>Your Name:</label> *
          <br />
          <input class="form-input-field"
                type="text"
                value="<?php echo $_SESSION['form_element0']; ?>"
                name="form_element0"
                size="40" />
          <br />
          <br />
          <label>Your Email:</label> *
          <br />
          <input class="form-input-field"
                type="text"
                value="<?php echo $_SESSION['form_element1']; ?>"
                name="form_element1"
                size="40" />
          <br />
          <br />
          <label>Subject:</label> *
          <br />
          <input class="form-input-field"
                type="text"
                value="<?php echo $_SESSION['form_element2']; ?>"
                name="form_element2"
                size="40" />
          <br />
          <br />
          <label>Message:</label> *
          <br />
          <textarea class="form-input-field"
                name="form_element3"
                rows="8"
                cols="38">
<?php echo $_SESSION['form_element3']; ?>
</textarea>
          <br />
          <br />
          <input class="form-input-button"
                type="reset"
                name="resetButton"
                value="Reset" /> <input class="form-input-button"
                type="submit"
                name="submitButton"
                value="Submit" />
        </form><?php session_destroy(); ?><?php
        if (!$_SESSION['formMessage']) { 
        echo 'We look forward to hearing from you.<br />';
        } else {
         echo $_SESSION['formMessage'];
         }
         ?>
      </div><!-- End content -->
    </div><!-- End main content wrapper -->

    <div class="clearer"></div>

    <div id="breadcrumbcontainer">
      <!-- Start the breadcrumb wrapper -->

      <ul>
        <li><a href="../index.html">HOME</a>&nbsp;/&nbsp;</li>

        <li><a href="page3.php">Contact Priscilla
        Petty</a>&nbsp;/&nbsp;</li>
      </ul>
    </div><!-- End breadcrumb -->

    <div id="footer">
      <!-- Start Footer -->

      <p>© MMIX Priscilla Petty <a href="#"
         id="rw_email_contact"
         name="rw_email_contact">Contact Priscilla
         Petty</a><script type="text/javascript">
//<![CDATA[
var _rwObsfuscatedHref0 = "mai";var _rwObsfuscatedHref1 = "lto";var _rwObsfuscatedHref2 = ":pr";var _rwObsfuscatedHref3 = "isc";var _rwObsfuscatedHref4 = "ill";var _rwObsfuscatedHref5 = "a@p";var _rwObsfuscatedHref6 = "ris";var _rwObsfuscatedHref7 = "cil";var _rwObsfuscatedHref8 = "lap";var _rwObsfuscatedHref9 = "ett";var _rwObsfuscatedHref10 = "y.c";var _rwObsfuscatedHref11 = "om";var _rwObsfuscatedHref = _rwObsfuscatedHref0+_rwObsfuscatedHref1+_rwObsfuscatedHref2+_rwObsfuscatedHref3+_rwObsfuscatedHref4+_rwObsfuscatedHref5+_rwObsfuscatedHref6+_rwObsfuscatedHref7+_rwObsfuscatedHref8+_rwObsfuscatedHref9+_rwObsfuscatedHref10+_rwObsfuscatedHref11; document.getElementById('rw_email_contact').href = _rwObsfuscatedHref;
//]]>
</script></p>
    </div><!-- End Footer -->
  </div><!-- End container -->
  <!-- Start Google Analytics -->
  <script type="text/javascript">
//<![CDATA[
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
//]]>
</script><script type="text/javascript">
//<![CDATA[
try {
var pageTracker = _gat._getTracker("UA-7711826-2");
pageTracker._trackPageview();
} catch(err) {}
//]]>
</script><!-- End Google Analytics -->
</body>
</html>
