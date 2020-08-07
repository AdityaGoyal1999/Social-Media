document.addEventListener("DOMContentLoaded", () => {
    // window.alert("Works");
    document.querySelectorAll(".edit").forEach(link => {
        link.onclick = function() {
            var content = this.parentElement.parentElement.querySelector(".post-content").innerHTML;
            var elem = this.parentElement.parentElement.querySelector(".post-content");
            var pk = elem.id;
            elem.style.display = 'none';

            var form = document.createElement("form");

            var textArea = document.createElement("textarea");
            textArea.className = 'form-control';
            textArea.innerHTML = content;

            var button = document.createElement("button");
            button.className = 'btn btn-primary';
            button.innerHTML = "Edit post";
            button.type = "submit";

            form.appendChild(textArea);
            form.append(button);

            var exchangeDiv = elem.parentElement;
            exchangeDiv.appendChild(form)

            form.onsubmit = () => {
                var newText = textArea.value;

                // TODO: return value to server
                elem.innerHTML = newText;
                elem.style.display = 'block';

                fetch(`/edit/${pk}/${newText}`)

                form.style.display = 'none';

            };

        }
    });

    document.querySelectorAll(".like").forEach(link => {
        link.onclick = () => {
            // window.alert(link.parentElement.innerHTML) 
            var elem = link.parentElement.querySelector(".number-of-likes");
            elem.innerHTML = parseInt(elem.innerHTML) + 1;

            var pk = link.parentElement.parentElement.querySelector(".post-content").id;

            fetch(`like/${pk}`)
        };
    });
});