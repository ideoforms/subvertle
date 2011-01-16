// ==UserScript==
// @name           IOLab Tag Bar
// @namespace      http://people.ischool.berkeley.edu/~npdoty
// @description    Show Delicious tags for the current page
// @include        http://*
// @include        https://*
// @require		   http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js
// @require		http://courses.ischool.berkeley.edu/i290-4/f09/resources/gm_jq_xhr.js
// @require		http://plugins.jquery.com/files/jquery.md5.js.txt
// ==/UserScript==

if (window.top != window.self)	//don't run on frames or iframes
	return;

var stylesheet = '					\
<style>								\
	div#bar {						\
		width: 100%; 				\
		height: 100px; 				\
		position: fixed; 			\
		bottom: 0; 					\
		left: 0; 					\
		padding: 10px; 				\
		background-color: #eee;		\
	}								\
									\
	div#bar ul li {					\
		display: inline;			\
		padding: 5px;				\
	}								\
</style>';

var bar = '\
<div id="bar">What are people saying about this website?\
	<ul></ul>\
</div>';

$('head').append(stylesheet);
$('body').append(bar);

var theUrl = $.md5(window.location.href);
console.log(theUrl);

$.get('http://feeds.delicious.com/v2/xml/url/' + theUrl, function(xml){
	console.log(xml);
	$(xml).find("category").each(function(index) {
		$("#bar ul").append('<li>' + $(this).text() + '</li>');
		//console.log($(this).text());
	});
});