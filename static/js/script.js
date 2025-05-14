$(document).ready(function () {
    // Like Button Click
    $(".like-btn").click(function () {
        let postId = $(this).data("id");
        let likesCount = $("#likes-" + postId);
        $.post("/like/" + postId, function (data) {
            likesCount.text(data.likes);
        });
    });

    // Copy Link to Clipboard
    $(".copy-link").click(function () {
        let link = $(this).data("url");
        navigator.clipboard.writeText(link).then(() => {
            alert("Link copied! Share it on Instagram or anywhere.");
        });
    });

    // Apply Image Fitting Dynamically
    $(".post-img").each(function () {
        if (this.naturalWidth > this.naturalHeight) {
            $(this).addClass("landscape"); // Landscape images use cover
        } else {
            $(this).addClass("portrait"); // Portrait images use contain
        }
    });
});

// Preview Image Before Upload
document.getElementById("imageInput").addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById("imagePreview");
            preview.src = e.target.result;
            preview.classList.remove("d-none");
        };
        reader.readAsDataURL(file);
    }
});

//JavaScript to Toggle Comment Form -->
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".comment-btn").forEach(button => {
        button.addEventListener("click", function () {
            let postId = this.getAttribute("data-id");
            let commentForm = document.getElementById("comment-form-" + postId);
                if (commentForm.style.display === "none") {
                    commentForm.style.display = "block";
                } else {
                    commentForm.style.display = "none";
                }
        });
    });
});