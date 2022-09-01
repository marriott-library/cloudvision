
<!DOCTYPE html>
<html lang="en">
   <head>
	   <meta charset="UTF-8"><title><?php if (!empty($metatitle)){echo "$metatitle - ";} ?>J. Willard Marriott Library</title>
	   <meta name="keywords"  content="marriott library, university of utah, library, usearch, catalog, research, hours"/>
	   <meta name="description" content="<?php if (!empty($metadescription)){echo $metadescription;} ?>" />
	   <meta name="robots" content="index, follow"/>
	   <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
		<link rel="shortcut icon" href="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>favicon.ico"/>
    <?php if(isset($google_tag_manager)) { echo $google_tag_manager; } ?>
		<link href="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>css/bootstrap.min.css" rel="stylesheet"/>
		<link rel="stylesheet" href="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>css/fontawesome-all.css"/>
		<link href="https://fonts.googleapis.com/css?family=Encode+Sans+Condensed:300,400,500,600,700,800,900" rel="stylesheet"/>
		<link href="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>css/flexslider.css" rel="stylesheet" media="screen"/>
		<link href="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>css/marriott.css" rel="stylesheet"/>
    <link href="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>css/alert.css" rel="stylesheet"/>
		<script src="https://code.jquery.com/jquery-3.4.1.min.js"> </script>
		<script src="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>js/bootstrap.bundle.min.js"> </script>
		<script src="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>js/jquery.flexslider.js"> </script>
    <?php
    if(!isset($css_links))
            $css_links = array();
    foreach ($css_links as $css)
    {
    ?>
    <link rel="stylesheet" href="<?php echo $css; ?>" type="text/css"/>
    <?php
    }
    ?>
    <?php if(isset($custom_leah_code)) { echo $custom_leah_code; } ?>
   </head>
   <body>
     <?php if(isset($google_tag_manager_noscript)){ echo $google_tag_manager_noscript; } ?>
     <header>
	  	<a id="skip" class="sr-only sr-only-focusable" href="#content">Skip to main content</a>
<!-- Alert Bar  -->
      <div id="library-covid-alert" style="  background-image: url('<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>images/alert-ribbon-bg.png');"><span class="u-alert-icon">
        <img src="<?php echo defined('TEMPLATES_URL')?TEMPLATES_URL: $_SERVER["REQUEST_SCHEME"].'://'.$_SERVER["HTTP_HOST"].'/templates/';?>images/alert-ribbon-icon.png" alt="alert icon" /></span> <a class="covid-hub" href="https://lib.utah.edu/covid-19.php">
        <h2 class="u-alert-text">Marriott Library Covid-19 Updates</h2></a>
      </div>
<!-- Start Topbar  -->

<div id="subhead">
  <div class="container-fluid">
    <div class="row">
      <div class="col-9">
        <ul class="nav">
          <li class="nav-item hours-dropdown">
            <a class="nav-link  dropdown-toggle" href="#" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
              <em class="far fa-clock"><!-- Clock Icon --></em> Today's Hours: <span class="quick-time"></span>
            </a>
            <div class="dropdown-menu hours-menu">
              <a class="dropdown-item" href="https://www.lib.utah.edu/collections/book-arts/">
                <div class="hours-dept-title">Book Arts Studio</div>
                <div class="row">
                    <div class="col "><span class="quick-time"></span></div>
                </div>
              </a>
              <a class="dropdown-item" href="https://www.lib.utah.edu/services/knowledge-commons/index.php">
                <div class="hours-dept-title">Knowledge Commons</div>
                <div class="row">
                  <div class="col "><span class="quick-time"></span></div>
                </div>
              </a>
              <a class="dropdown-item" href="https://www.lib.utah.edu/info/hours.php">
                <div class="hours-dept-title">Mom's Cafe</div>
                <div class="row">
                  <div class="col "><span class="quick-time"></span></div>
                </div>
              </a>
              <a class="dropdown-item" href="https://www.lib.utah.edu/info/hours.php">
                <div class="hours-dept-title">Mom's Pantry</div>
                <div class="row">
                  <div class="col "><span class="quick-time"></span></div>
                </div>
              </a>
              <a class="dropdown-item" href="https://www.lib.utah.edu/collections/special-collections">
                <div class="hours-dept-title">Special Collections</div>
                <div class="row">
                  <div class="col "><span class="quick-time"></span></div>
                </div>
              </a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="https://www.lib.utah.edu/info/hours.php">View All Hours <em class="fas fa-angle-right"><!-- Arrow right icon --></em></a></div>
          </li>
          <li class="nav-item ml-phone">
            <a class="nav-link" href="tel:801-581-8558"> 801-581-8558</a>
          </li>
        </ul>
      </div>
      <div class="col-3">
        <ul class="nav justify-content-end">
          <li class="nav-item">
            <a class="nav-link dropdown-toggle" href="#" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Log in </a>
            <div class="dropdown-menu dropdown-menu-right">
              <a class="dropdown-item" href="https://utah-primoprod.hosted.exlibrisgroup.com/primo-explore/account?vid=UTAH&amp;section=overview&amp;lang=en_US">Library Account</a>
              <a class="dropdown-item" href="https://lib.utah.edu/help/off-campus.php">Off Campus</a>
              <a class="dropdown-item" href="https://scheduling.tools.lib.utah.edu/">Library Scheduling</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="https://lib.utah.edu/info/policies.php">More on library access </a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>
<!-- End Topbar  -->
