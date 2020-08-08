document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".like").forEach(link => {
        link.onclick = () => {
            var elem = link.parentElement.querySelector(".number-of-likes");
            elem.innerHTML = parseInt(elem.innerHTML) + 1;

            var pk = link.parentElement.parentElement.querySelector(".post-content").id;

            fetch(`like/${pk}`)
        };
    });
});