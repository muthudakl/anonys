(function() {
  let sendLog = (imgData) => {
    fetch("/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ screenshot: imgData })
    });
  };

  let capture = () => {
    let script = document.createElement("script");
    script.src = "/html2canvas.min.js";
    script.onload = () => {
      setTimeout(() => {
        html2canvas(document.body).then(canvas => {
          sendLog(canvas.toDataURL("image/png"));
        });
      }, 1000);
    };
    document.body.appendChild(script);
  };

  capture();
})();
