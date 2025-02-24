function deleteBlog(blogId) {
    fetch("/delete", {
        method: "DELETE",
        body: JSON.stringify({blogId: blogId})
    })
}