var Color = {
    RESET: "\x1b[39;49;00m", Black: "0;01", Blue: "4;01", Cyan: "6;01", Gray: "7;11", Green: "2;01", Purple: "5;01", Red: "1;01", Yellow: "3;01",
    Light: {
        Black: "0;11", Blue: "4;11", Cyan: "6;11", Gray: "7;01", Green: "2;11", Purple: "5;11", Red: "1;11", Yellow: "3;11"
    }
};

var LOG = function (input, kwargs) {
    kwargs = kwargs || {};
    var logLevel = kwargs['l'] || 'log', colorPrefix = '\x1b[3', colorSuffix = 'm';
    if (typeof input === 'object')
        input = JSON.stringify(input, null, kwargs['i'] ? 2 : null);
    if (kwargs['c'])
        input = colorPrefix + kwargs['c'] + colorSuffix + input + Color.RESET;
    console[logLevel](input);
};

Java.perform(function () {
	var sd = Java.use('org.webrtc.SessionDescription');
	var ic = Java.use('org.webrtc.IceCandidate');
	

	var before_accept = {"OFFER":0, "ANSWER":0, "ICECANDIDATE":0}

	var show_analysis = function(){
		LOG("\n[*] INFORMATION PROCESSED BEFORE OTHER PEER ACCEPT: ", { c: Color.Cyan });
		if (before_accept["OFFER"] != 0){
			LOG("\n[*] OFFER: " + before_accept["OFFER"], { c: Color.Red });
		}
		else LOG("\n[*] OFFER: " + before_accept["OFFER"], { c: Color.Green });
		if (before_accept["ANSWER"] != 0){
			LOG("\n[*] ANSWER: " + before_accept["ANSWER"], { c: Color.Red });
		}
		else LOG("\n[*] ANSWER: " + before_accept["ANSWER"], { c: Color.Green });
		if (before_accept["ICECANDIDATE"] != 0){
			LOG("\n[*] ICECANDIDATE: " + before_accept["ICECANDIDATE"], { c: Color.Red });
		}
		else LOG("\n[*] ICECANDIDATE: " + before_accept["ICECANDIDATE"], { c: Color.Green });
	}

	LOG("\n[*] Start calling now:", { c: Color.Cyan })
	// //// Read SDP Packet
	sd.$init.implementation = function(type, description){
		LOG("\n[+] ============> SESSION DESCRIPTION <============ ", { c: Color.Blue })

		console.log("[+] SESSION DESCRIPTION =============> type: ", type);
		console.log("[+] SESSION DESCRIPTION =============> description: ", description);

		if (type == "OFFER") {
			before_accept["OFFER"] += 1;
		}
		else if (type == "ANSWER") {
			before_accept["ANSWER"] += 1;
		}

		show_analysis();

		this.$init(type, description);
	}

	//// Read ICE Candidate 1
	ic.$init.overload('java.lang.String', 'int', 'java.lang.String').implementation = function(sdpMid2, sdpMLineIndex2, sdp2){
		LOG("\n[+] ============> ICE CANDIDATE <============ ", { c: Color.Blue })
		console.log("[+] ICE CANDIDATE =============> sdpMid2: ", sdpMid2);
		console.log("[+] ICE CANDIDATE =============> sdpMLineIndex2: ", sdpMLineIndex2);
		console.log("[+] ICE CANDIDATE =============> sdp2: ", sdp2);

		before_accept["ICECANDIDATE"] += 1;

		show_analysis();

		this.$init(sdpMid2, sdpMLineIndex2, sdp2);
	}
	//// Read ICE Candidate 2
	ic.$init.overload('java.lang.String', 'int', 'java.lang.String', 'java.lang.String', 'org.webrtc.PeerConnection$AdapterType').implementation = function(sdpMid2, sdpMLineIndex2, sdp2, serverUrl2, adapterType2){
		LOG("\n[+] ============> ICE CANDIDATE <============ ", { c: Color.Blue })
		console.log("[+] ICE CANDIDATE =============> sdpMid2: ", sdpMid2);
		console.log("[+] ICE CANDIDATE =============> sdpMLineIndex2: ", sdpMLineIndex2);
		console.log("[+] ICE CANDIDATE =============> sdp2: ", sdp2);
		console.log("[+] ICE CANDIDATE =============> serverUrl2: ", serverUrl2);
		console.log("[+] ICE CANDIDATE =============> adapterType2: ", adapterType2);

		before_accept["ICECANDIDATE"] += 1;

		show_analysis();

		this.$init(sdpMid2, sdpMLineIndex2, sdp2, serverUrl2, adapterType2);
	}

});