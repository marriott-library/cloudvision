<div class="main-search collapse" id="main-search">
  <div class="container">
    <div class="row">
      <div class="col-12">
        <div class="homesearch-container">
          <div class="searchbox">
            <form>
              <div class="form-row">
                <div class="col">
                  <label class="sr-only" for="marriottFederatedSearch">Search Marriott Library Resources</label>
                  <div class="input-group">
                    <div class="input-group-prepend">
                      <div class="input-group-text">Search</div>
                    </div>
                    <input id="marriottFederatedSearch" class="form-control form-control-lg" type="text" name="search" value="" />
                  </div>
                </div>
                <div class="col-auto search-options-container">
                  <select id="SearchOptions" class="form-control form-control-lg search-options">
                    <option value="all">Everything</option>
                    <option value="us">USearch Catalog</option>
                    <option value="w">Website</option>
                    <option value="cr">Course Reserves</option>
                    <option value="lg">Subject Guides</option>
                    <option value="dl">Digital Library</option>
                  </select>
                </div>
                <div class="col-auto"><button class="btn btn-search btn-lg" onclick="Teleport(); return false;"><em class="fas fa-search"><!--Search Icon --></em></button></div>
              </div>
            </form>
          </div>
          <div class="one-search-welcome">
            <a class="float-right advanced-search" href="https://utah-primoprod.hosted.exlibrisgroup.com/primo-explore/search?vid=UTAH&amp;mode=advanced">Advanced Catalog Search</a>
            <h2>All U Need</h2>
            <p>Your gateway to the
              <a href="https://utah-primoprod.hosted.exlibrisgroup.com/primo-explore/search?vid=UTAH">Library Catalog</a>,
              <a href="https://utah-primoprod.hosted.exlibrisgroup.com/primo-explore/search?tab=uuu_alma_cr_restricted&search_scope=UUU_ALMA_CR_RESTRICTED&vid=UTAH&lang=en_US&offset=0">Course Reserves</a>,
              <a href="https://collections.lib.utah.edu">Digital Items</a>,
              <a href="https://gcse.search.utah.edu/index.php?site=Look-only-in-marriott-library-main-website&amp;gcse_action=site_search">Library Website search results</a>,
              and more simultaneously!
            </p>
          </div>
          <div class="buttons-flex-links">
            <a class="button content-button" href="https://lib.utah.edu/collections/">Collections</a>
            <a class="button content-button" href="https://databases.tools.lib.utah.edu/">Databases</a>
            <a class="button content-button" href="https://utah-primoprod.hosted.exlibrisgroup.com/primo-explore/jsearch?vid=UTAH&amp;lang=en_US">Journals</a>
            <a class="button content-button" href="https://campusguides.lib.utah.edu/index.php?b=s">Research Guides</a>
          </div>
            <script type="text/javascript">// <![CDATA[
              //Takes you to the correct search depending on what area you select to search on the dropdown.
              function Teleport()
              {

              var searchArea = document.getElementById("SearchOptions").value;
              var searchString = document.getElementById("marriottFederatedSearch").value;
              var location = "";
              switch (searchArea)
              {

              case "all":
              location = "https://lib.utah.edu/discover/?search=" + searchString;
              break;
              case "us":
              location = "https://utah-primoprod.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains," + searchString + "&tab=everything&search_scope=EVERYTHING&vid=UTAH&offset=0";
              break;
              case "cr":
              location = "https://utah-primoprod.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains," + searchString + "&tab=uuu_alma_cr_restricted&search_scope=UUU_ALMA_CR_RESTRICTED&vid=UTAH&offset=0";
              break;
              case "lg":
              location = "https://campusguides.lib.utah.edu/srch.php?q=" + searchString;
              break;
              case "dl":
              location = "https://collections.lib.utah.edu/search?q=" + searchString;
              break;
              case "w":
              location = "https://gcse.search.utah.edu/index.php?q=" + searchString + "&site=Look-only-in-marriott-library-main-website&gcse_action=site_search";


              break;
              }
              window.location.href = location;
              }
              // ]]>
          </script>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- Start Main Content -->
