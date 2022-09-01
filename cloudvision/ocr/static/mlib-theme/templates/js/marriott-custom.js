$(document).ready(function() {
	$(".megamenu").on("click", function(e) {
		e.stopPropagation();
	});

	$('.flexslider').flexslider({
    animation: "slide",
    controlNav: "thumbnails",
  });
});

//load Hours into Nav Bar Dropdown
$(function () {

    var url = "https://forms.lib.utah.edu/includes/google_api/calendar/lib_hours.php";
    $.ajax({
        type: 'GET',
        dataType: 'jsonp',
        url: url,
        success: function (data)
        {

            /*
             Each Location has its calendar named as location name.
             Events named "hours" will be displayed in the dropdown
             All events will be pulled will be pulled into hours_info page. This required future implementation
             Calendar "Marriott Library" represents the library hour information
             //link to info page is defined in description body of hours event
             */

            data = JSON.stringify(data)
            //console.log(data);
            var calendars = JSON.parse(data);
            var marriot_hours = false;
            $('.dropdown-menu.hours-menu').html("");
            for (var calendar in calendars) {
                var calendar_name = calendars[calendar].name;
                var hours = calendars[calendar].hours;
                var link = calendars[calendar].link;

                var location_closed = false;
                if (hours.length == 0) {
                    location_closed = true;
                }
                var day_hours = [];
                var multi_sub_hours = false;
                for (var i = 0; i < hours.length; i++) {
                    if (hours[i].subject == "hours") {
                        day_hours.push(hours[i]);
                    }
                    if(multi_sub_hours == false && hours[i].location != null)
                      multi_sub_hours = true;
                }

                if (day_hours.length == 0) {
                    location_closed = true;
                }

                if (location_closed == true) {
                    var html_dom = '<a class="dropdown-item" href="' + link + '"><div class="hours-dept-title">' + calendar_name + '</div><div class="row"><div class="col "><span class="quick-time">CLOSED</span></div></div></a>';
                    //$('.dropdown-menu.hours-menu').prepend(html_dom);
                    $('.dropdown-menu.hours-menu').append(html_dom);
                    continue;
                }

                if (link == null)
                    link = "https://www.lib.utah.edu/info/hours.php";
							 var time_dom = "";
               //if(day_hours.length == 1)
               if(multi_sub_hours == true){
                    var hours_link = 'https://www.lib.utah.edu/info/hours.php?cal_name=';
                    switch(calendar_name){
                      case "Book Arts Studio": hours_link += "book_arts";break;
                      case "Knowledge Commons": hours_link += "knowledge_commons";break;
                      case "Marriott Library": hours_link += "marriott_library";break;
                      case "Mom's Cafe": hours_link += "mom%27s_cafe";break;
                      case "Mom's Pantry": hours_link += "mom%27s_pantry";break;
                      case "Special Collections": hours_link += "special_collections";break;
                    }

                    time_dom = '<div class="col "><span class="quick-time">' + 'Multiple Schedule - <a target="_blank" href="'+ hours_link + '">View Department Hours</a>' + '</span></div>';
               }
               else{
                 for(var j =0; j < day_hours.length; j++){

                  var d = new Date(day_hours[j].start);
                  var afterfix = "am";
                  var Hr = d.getHours();
                  if (Hr >= 12) {
                      afterfix = "pm";
                      if (Hr != 12)
                          Hr -= 12;
                  } else if (Hr == 0) {
                      Hr = 12;
                  }
                  var Min = d.getMinutes();
                  if (Min < 10 && Min > 0) {
                      Min = ":0" + Min;
                  } else if (Min == 0)
                      Min = "";
                  else {
                      Min = ":" + Min;
                  }

                  var start = Hr + Min + afterfix;
                  var d = new Date(day_hours[j].end);
                  var afterfix = "am";
                  var Hr = d.getHours();
                  if (Hr >= 12) {
                      afterfix = "pm";
                      if (Hr != 12)
                          Hr -= 12;
                  } else if (Hr == 0) {
                      Hr = 12;
                  }
                  var Min = d.getMinutes();
                  if (Min < 10 && Min > 0) {
                      Min = ":0" + Min;
                  } else if (Min == 0)
                      Min = "";
                  else {
                      Min = ":" + Min;
                  }

                 var end = Hr + Min + afterfix;

                 time_dom += '<div class="col "><span class="quick-time">' + start + ' - ' + end + '</span></div>';
                }
               }


                if (calendar_name == "Marriott Library") {
                    marriot_hours = true;
                    $('a.nav-link.dropdown-toggle').find('.quick-time').html(start + ' - ' + end);
                } else {
                    if(multi_sub_hours == true){
                      var html_dom = '<div><div class="hours-dept-title"><a class="dropdown-item" href="' + link + '" style="text-align: center;font-weight: bold;">' + calendar_name + '</a></div><div class="row">' + time_dom + '</div></div>';
                    }
                    else if(multi_sub_hours == false){
                      var html_dom = '<a class="dropdown-item" href="' + link + '"><div class="hours-dept-title">' + calendar_name + '</div><div class="row">' + time_dom + '</div></a>';

                    }
                      //$('.dropdown-menu.hours-menu').prepend(html_dom);
                    console.log(html_dom);
                    $('.dropdown-menu.hours-menu').append(html_dom);

                }


            }

            if (marriot_hours == false) {
                $('a.nav-link.dropdown-toggle').find('.quick-time').html("CLOSED");
            }
            $('.dropdown-menu.hours-menu').append('<div class="dropdown-divider"></div><a class="dropdown-item" href="https://www.lib.utah.edu/info/hours.php">View All Hours <em class="fas fa-angle-right"><!-- Arrow right icon --></em></a>');

        },
        error: function (err) {
            console.log("AJAX error in request: " + JSON.stringify(err, null, 2));
        }
    });
});
