// ==UserScript==
// @name          iPlayer Subtitles
// @namespace     http://www.subvertle.com/
// @description   Display multilingual subtitles for BBC iPlayer
// @include       http://www.bbc.co.uk/iplayer/*
// @require       http://jqueryjs.googlecode.com/files/jquery-1.3.2.min.js
// @require       http://courses.ischool.berkeley.edu/i290-4/f09/resources/gm_jq_xhr.js
// ==/UserScript==


// Hostname and port to the subvertle server.
// This server must be running the subvertle-web.py web service.
//-----------------------------------------------------------------
var webHost = "http://localhost:5000";

// List of available language IDs
//-----------------------------------------------------------------
var languages = [ "Spanish", "French", "German", "Esperanto", "Expletive" ];


var t0 = 0.0;
var captions = [];
var iplayer = 0;
var emp = 0;
var timer = 0;
var startTime = 0.0;
var nextCaptionIndex = 0;


function addStyle(css)
{
	// Append some CSS styling to the current document.
	//------------------------------------------------------------
    var head, style;
    head = document.getElementsByTagName('head')[0];
    if (!head) { return; }
    style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = css;
    head.appendChild(style);
}

function addMarkup()
{
	// Append some CSS styling to the current document.
	//------------------------------------------------------------
    div = document.createElement('div');
    
    languageopts = "";
    for (var i = 0; i < languages.length; i++)
    {
        languageopts += '<option value="' + languages[i].toLowerCase() + '">' + languages[i] + '</option>';
    }
    
    html = '<div id="subtitles">' +
           '<span>Language:</span>' +
           '<select name="lang" id="subtitle_lang">' + languageopts +
           '</select>' +
           '<input type="button" id="subtitles_enable" value="Enable subtitles" />' +
           '<img src="' + webHost + '/static/spinner.gif" id="subtitles_spinner" alt="spinner" />' +
//           '<input type="button" id="subtitles_start" value="Start" />' +
           '</div>' +
           '<div id="caption"></div>' +
           '<script type="text/javascript" src="http://jqueryjs.googlecode.com/files/jquery-1.3.2.min.js"></script>';
    div.innerHTML = html;
    
    el = document.getElementById("emp-container");
    el.appendChild(div);
}

function setCaptionIndex(time)
{
	for (var i = 0; i < captions.length; i++)
	{
		if (captions[i].start > time)
		{
			nextCaptionIndex = i;
			// alert(captions[i].start + " > " + time + ", nextCaptionIndex: " + nextCaptionIndex);
			return;
		}
	}
}


function getCaptions()
{
	//---------------------------------------------------------------------
	// Begin the server-side caption generation, and display a spinny
	// wheel while we're waiting for processing to finish.
	//---------------------------------------------------------------------
	var dialect = $("#subtitle_lang :selected").val().toLowerCase();
	
	$("#subtitles_spinner").addClass("active");
	
	$.getJSON(webHost + '/get',
	{
		url: 		window.location.href,
		dialect: 	dialect
	},
	function(data)
	{
		$("#subtitles_spinner").removeClass("active");
		$("#subtitles_enable").addClass("ready");
		captions = data.result;
	});
	return false;
}

function hideCaptions()
{
	$("#caption").text("");
}

function startCaptions()
{
	//---------------------------------------------------------------------
	// Start our playback timer, and kick off server-side generation.
	//---------------------------------------------------------------------
	startTime = emp.getCurrentTimecode();
	setCaptionIndex(startTime);
	$.getJSON(webHost + '/start', { });
	
	t0 = (new Date).getTime();
	timer = setInterval(tick, 50);
}

function stopCaptions()
{
	//---------------------------------------------------------------------
	// Stop.
	//---------------------------------------------------------------------
	hideCaptions();
	clearInterval(timer);
}

function addCallbacks()
{   
	//---------------------------------------------------------------------
	// jQuery button bindings.
	//---------------------------------------------------------------------
	$('#subtitles_enable').bind('click', getCaptions);
	$('#subtitles_start').bind('click', startCaptions);
}

function addPlayerCallbacks()
{
	//---------------------------------------------------------------------
	// Register events with the iPlayer EMP device.
	//---------------------------------------------------------------------
	
	setTimeout(function () {
		emp._emp.onMediaPlaying = function () { startCaptions(); };
		emp._emp.onMediaPaused = function () { stopCaptions(); };
		emp._emp.onMediaSeeking = function () { hideCaptions(); };
		emp._emp.onMediaPlayerError = function () { };		
	}, 4000);
}

$(document).ready(function()
{
	var t = setInterval(function ()
	{
		//---------------------------------------------------------------------
		// Extracts the ID of the iPlayer EMP object, to detect and trigger
		// playback events.
		//---------------------------------------------------------------------
		emp = eval("window.content.wrappedJSObject.iplayer.models.Emp.getInstance()");
		
		if (emp != undefined)
		{
			iplayer = window.content.wrappedJSObject.iplayer;
			addPlayerCallbacks();
			clearInterval(t);
		};
	}, 100);
});

function tick()
{
	//---------------------------------------------------------------------
	// Called every few milliseconds, this function updates the captions
	// according to our current queue of caption events. Assumes that
	// the next event in the array is the next to be displayed.
	// For compatibility with random seeking through the video, will
	// ultimately need to be replaced with an alternative method that
	// can retrieve the appropriate caption for an arbitrary timepoint.
	//---------------------------------------------------------------------
	var dt = (new Date).getTime() - t0;
	dt = startTime + (dt / 1000.0) - 1;
    
	var nextTime = captions[nextCaptionIndex].start;
	document.title = "now: " + dt + ", next: " + nextTime;
	
	if (dt > nextTime)
	{
		var caption = captions[nextCaptionIndex];
		$("#caption").text(caption.text);
		nextCaptionIndex += 1;
		if (nextCaptionIndex >= captions.length)
		{
			stopCaptions();
		}
	}
	else if (nextCaptionIndex > 1)
	{
		var curFinishTime = captions[nextCaptionIndex - 1].end;
		if (dt > curFinishTime)
		{
			hideCaptions();
		}
	}
}

addMarkup();
addCallbacks();

addStyle(
    '.ready { background: #444 !important; }' +
    '#subtitles {'+
    '  font-size: 90%;' +
    '  color: #444;' +
    '  text-align: center; ' +
    '}'+
    '#subtitles * {' +
    '  vertical-align: middle; ' +
    '}' +
    '#subtitles input, #subtitles select {' +
    '  background: #222; ' +
    '  color: #ccc; ' +
    '  border: 1px solid #444; ' +
    '  border-radius: 2px; ' +
    '  -moz-border-radius: 3px; ' +
    '  margin: 4px; ' +
    '  padding: 3px; ' +
    '}' +
    '#caption {' +
    '  color: white; ' +
    '  position: absolute;' +
    '  left: 200px;' +
    '  top: 350px;' +
    '  font-size: 22px;' +
    '  font-family: helvetica;' +
    '  text-align: center;' +
    '  width: 500px; ' +
    '  line-height: 1.3em; ' +
    '  text-shadow: black 1px 1px 1px; ' +
    '}' +
    '#subtitles_spinner { visibility: hidden; }' +
    '#subtitles_spinner.active { visibility: visible; }'
);

