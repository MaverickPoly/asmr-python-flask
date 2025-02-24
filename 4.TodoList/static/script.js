function updateTodoStatus(todoId, completed) {
    fetch("/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: todoId,
            completed: completed
        })
    }).then(() =>
        location.reload(true));
}