<?php include 'header.php';?>
<?php include 'mainNav.php';?>
<?php include 'mainSearch.php';?>
<!-- Start Main Content -->
<style>
pre.code {
    padding: 6px 10px;
    background-color: #fafafa;
    border: 1px solid #ddd;
    overflow: auto;
}
@media (min-width: 768px) {
  .bd-sidebar {
      position: -webkit-sticky;
      position: sticky;
      top: 4rem;
      z-index: 1000;
      height: calc(100vh - 4rem);
  }
}
</style>
<div id="content">
  <div class="ml-breadcrumb">
    <div class="container">
      <ul class="breadcrumb">
         <li class="firstitem">
          <a href="https://lib.utah.edu/">
          Home
          </a>
         </li>
         <li class="icon-angle-double-right">
          <a href="/">Custom Themes</a>
         </li>
         <li class="icon-angle-double-right">Marriott Library Web Application</li>
      </ul>
    </div>
  </div>
  <div class="container">
    <!-- <div class="row">
      <div class="col-md-2 bd-sidebar d-none d-lg-block">
        <nav class="nav flex-column">
          <a class="nav-link active" href="#test">test</a>
          <a class="nav-link" href="#">Link</a>
          <a class="nav-link" href="#">Link</a>
          <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
        </nav>
      </div> -->
      <div class="main-content">
        <h1 class="mt-3">Marriott Library External Application Theme</h1>
        <p class="lead">The Marriott Library theme is built with <a href="https://getbootstrap.com/">Bootstrap 4</a>. Bootstrap utilizes <a href="https://jquery.com/">jQuery</a> and <a href="https://popper.js.org/">Popper.js</a></p>
        <p>The <code class="highlighter-rouge">bootstrap.bundle.min.js</code> includes <a href="https://popper.js.org/">Popper</a>.</p>

    <div class="row">
      <div class="col">
        <h2 class="short_headline">Setup</h2>
        <p>Get started with the <strong>Marriott Library External App Theme</strong></p>
        <h3>Converting an existing application to the new theme</h3>
        <div class="alert alert-warning" role="alert">
          The process converting a theme with the old theme to the new theme will not be seamless as mobileMainNav.php no longer exists
        </div>
        <p>If you are converting an application from the old template to the new, the first thing you'll need to do is remove the template symlink.</p>
        <p>Then get the submodule with the command:</p>
        <pre class="notranslate code">git submodule add git@gitlab.lib.utah.edu:user-experience/mlib-theme.git templates
        </pre>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <h2 class="short_headline">Config Example</h2>
        <p>More configuration may be added by placing a config file root folder of the site. </p>
        <h3>Sample config php</h3>
        <pre class="notranslate code">&lt;?php
$dev_flag = true;
if ($dev_flag) {
    $url = explode('/', (isset($_SERVER['HTTPS']) ? &quot;https&quot; : &quot;http&quot;) . &quot;://&quot; . $_SERVER[HTTP_HOST] . $_SERVER[REQUEST_URI]);
    array_pop($url);
    $url = implode('/', $url);
    $url .= '/';
} elseif (!$dev_flag) {
    $url = (isset($_SERVER['HTTPS']) ? &quot;https&quot; : &quot;http&quot;) . &quot;://&quot; . $_SERVER['HTTP_HOST'] . '/';
}

//Path to templates
define(&quot;TEMPLATES_PATH&quot;, realpath(__DIR__). &quot;/templates&quot;);

//URL to templates
define(&quot;TEMPLATES_URL&quot;, $url. &quot;templates/&quot;);
        </pre>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <h2 class="short_headline">Layout Templates</h2>
        <p>Components and options for laying out your Marriott App project. For more documentation and code examples, visit
          <a href="https://getbootstrap.com/docs/4.4/layout/overview/">Bootstrap 4 Layout Overview.</a></p>
        <div class="alert alert-primary" role="alert">
          <strong>Quick Note:</strong> When using this theme, please wrap your app content with a div id="content"  This is so the accessibility "Skip to Content" button works correctly.
        </div>
        <p>Be sure to have your application set up with the latest git theme files and development standards. If you can use php includes in your application, your layout template looks like this:</p>
        <h3>Basic template</h3>
      </div>
    </div>
    <div class="row">
      <div class="col-md">
        <pre class="notranslate code">  &lt;?php
  $css_links = ["css/appSpecificStyles.css"];
  ?&gt;
  &lt;?php include 'templates/header.php';?&gt;
  &lt;?php include 'templates/mainNav.php';?&gt;
  &lt;?php include 'templates/mainSearch.php';?&gt;
  &lt;!-- Start Main Content --&gt;
  &lt;div id="content"&gt;
    ..app content here
  &lt;/div&gt;
  &lt;!-- End Main Content --&gt;
  &lt;?php include 'templates/footer.php';?&gt;
        </pre>
      </div>
      <div class="col-md">
          <img src="/images/basicTemplate.jpg" alt="example of basic template">
      </div>
    </div>
    <div class="spacer-32">&nbsp;</div>
    <h3>Content Container</h3>
    <div class="row">
      <div class="col-md">
        <p>Restrict app width by wrapping content in class="container" which has a max-width of 1270px on large monitors with responsive breakpoints at 1400px, 1200px, 992px, 768px, and 576px.</p>
        <pre class="notranslate code">&lt;!-- Start Main Content --&gt;
&lt;div id="content"&gt;
  &lt;div class="container"&gt;
    &lt;div class="row"&gt;
      &lt;div class="col"&gt;
        &lt;p&gt;A contained width row&lt;/p&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/div&gt;
&lt;!-- End Main Content --&gt;
        </pre>
      </div>
      <div class="col-md">
        <img src="/images/containedWidth.jpg" alt="example of contained width container">
      </div>
    </div>
    <div class="spacer-32">&nbsp;</div>
    <h3>Full width and contained width content</h3>
    <div class="row">
      <div class="col-md">
        <p>If an application needs a combination of full width and contained with content, class="container" and class="container-fluid" can be used together in layouts.</p>
        <pre class="notranslate code">  &lt;!-- Start Main Content --&gt;
  &lt;div id="content"&gt;
    &lt;div class="container-fluid"&gt;
      &lt;div class="row"&gt;
        &lt;div class="col"&gt;
          &lt;p&gt;A full width row&lt;/p&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="container"&gt;
      &lt;div class="row"&gt;
        &lt;div class="col"&gt;
          &lt;p&gt;A contained width row&lt;/p&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
  &lt;!-- End Main Content --&gt;
        </pre>
      </div>
      <div class="col-md">
        <img src="/images/templateRows.png" alt="example of template containers">
      </div>
    </div>
  </div>
</div>
</div>
</div>
<!-- End Main Content -->
<?php include 'footer.php';?>
