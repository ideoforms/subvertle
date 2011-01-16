$(function() {
        $('#subtitles_enable').bind('click', function() {
                $.getJSON('http://localhost:5000/_add_numbers', {
                        a: 4,
                        b: 3
                }, function(data) {
          // $.getJSON('http://localhost:5000/get', {
          // url: window.location.href
		  // url: "http://www.bbc.co.uk/iplayer/episode/b00rrd81/Human_Planet_Oceans_Into_the_Blue/"
          // }, function(data) {
			alert("hello");
            $("#subtitles_output").text(data.result);
          });
          return false;
        });

        $('a#calculate').bind('click', function() {
                $.getJSON('http://localhost:5000/_add_numbers', {
                        a: $('input[name="a"]').val(),
                        b: $('input[name="b"]').val()
                }, function(data) {
						alert(data);
                        $("#result").text(data.result);
                });
                return false;
        });

});
