(function () {
    const script = document.currentScript;
    const apiKey = script.getAttribute("data-api-key");
    if (!apiKey) {
      console.error("ChatWidget: data-api-key is required.");
      return;
    }
  
    // Пробрасываем config в глобальный контекст
    window.chatbotConfig = { apiKey };
  
    // Создаем iframe
    const iframe = document.createElement("iframe");
    iframe.src = window.location.origin + "/widget.html";
    iframe.style.position = "fixed";
    iframe.style.bottom = "20px";
    iframe.style.right = "20px";
    iframe.style.width = "420px";
    iframe.style.height = "600px";
    iframe.style.border = "none";
    iframe.style.borderRadius = "16px";
    iframe.style.zIndex = "9999";
    iframe.allow = "clipboard-write";
  
    document.body.appendChild(iframe);
  })();
  