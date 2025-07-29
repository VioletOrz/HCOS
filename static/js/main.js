// 灵动岛提示控制
function showFlashMessage(message, type="success") {
    let flashDiv = document.createElement('div');
    flashDiv.className = `flash-message ${type}`;
    flashDiv.innerText = message;
    document.body.appendChild(flashDiv);

    // 4秒后自动消失
    setTimeout(() => {
        flashDiv.style.opacity = "0";
        flashDiv.style.transform = "translateY(-20px)";
        setTimeout(() => flashDiv.remove(), 600);
    }, 4000);
}

// 页面加载时执行：处理 Flask 的 flash 消息
window.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((msg, i) => {
        setTimeout(() => {
            msg.style.opacity = "1";
            msg.style.transform = "translateY(0)";
            setTimeout(() => {
                msg.style.opacity = "0";
                msg.style.transform = "translateY(-20px)";
                setTimeout(() => msg.remove(), 600);
            }, 4000);
        }, i * 200); // 多个消息依次显示
    });
});
