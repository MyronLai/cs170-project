/*
Run in JS console
Leaderboard JSON data will be copied to clipboard
Paste in leaderboard.json
*/

let messages = [];
let a = `{"t":"d","d":{"r":1,"a":"s","b":{"c":{"sdk.js.7-14-0":1}}}}`;
let b = `{"t":"d","d":{"r":2,"a":"q","b":{"p":"/leaderboard","h":""}}}`;
var ws = new WebSocket("wss://s-usc1c-nss-232.firebaseio.com/.ws?v=5&ns=cs-170-project-sp20");
let sent = false;
ws.onmessage = function(event) {
   messages.push(event.data);
   if(!sent) {
        ws.send(a);
        ws.send(b);
        sent = true;
   }
}

// After a couple seconds run
json = messages.slice(3,-1).join("")
copy(json)