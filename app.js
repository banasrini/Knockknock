// need to subscribe and publish to the channels
// need to subscribe to the Pi channel that sends images and print them out
// publish a 'yes(1)' or a 'no(0)' depending on the image


(function(){

			var button = PUBNUB.$('button');
			var pubnub = PUBNUB.init({
			publish_key   : 'demo',
			subscribe_key : 'demo',
			uuid : 'Bana1110'
		})
		
  
// Sending messages to the Pi to open the door through pibellchannel

$("#open").click(function(){
	pubnub.publish({
		channel : 'pibellchannel',
		message : '1'
		});
});

// Sending messages to the Pi to open the door through pibellchannel

$("#close").click(function(){
	pubnub.publish({
		channel : 'pibellchannel',
		message : '0'
		});
});


// printing the server messages on its own page

			pubnub.subscribe({
			channel : 'knock',
			message : person_at_door
				
			});
			
			

// action when message received from the server
			function person_at_door(message)
			{
			// convert the base64 string back to image and print it
				document.getElementById("pic").src = 'data:image/png;base64,' + message + '";
			}


})();
  