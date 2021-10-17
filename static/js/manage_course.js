document.querySelectorAll('.add_btn').forEach(element => {
    element.addEventListener('click', (event) => {
        event.preventDefault();
        if (loading()) return;
        const url = element.getAttribute('data-url')
        const action = element.getAttribute('data-action')
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value
        let course_id = Number(element.getAttribute('data-id'))
        loading(true);
        $.ajax({
            url: url,
            dataType: "json",
            headers: { "X-CSRFToken": csrfToken },
            type: "Post",
            async: true,
            data: { 'course_id': course_id, 'action': action },
            success: function (res) {
                console.log(res)
                if (res.status == 302){
                    popUp("You already have this Course")
                } else{
                    popUp("Course Added To The Cart")
                }
                loading(false);
            },
            error: function (err) {
                console.log(err)
                if (err.status == 202){
                    popUp("Course Added To The Cart")
                }
                else if (err.status == 302){
                    popUp("You already have this Course")
                }
                loading(false);
            }
        });

    })
});

document.querySelectorAll('.remove-course-btn').forEach(element => {
    element.addEventListener('click', (event) => {
        event.preventDefault();
        if (loading()) return;
        const url = element.getAttribute('data-url')
        const action = element.getAttribute('data-action')
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value
        let course_id = Number(element.getAttribute('data-id'))
        loading(true);
        $.ajax({
            url: url,
            dataType: "json",
            headers: { "X-CSRFToken": csrfToken },
            type: "Post",
            async: true,
            data: { 'course_id': course_id, 'action': action },
            success: function (res) {
                console.log(res)
                popUp("Course Removed From The Cart")
                loading(false);
                window.location.reload()
            },
            error: function (err) {
                console.log(err)
                if (err.status == 202){
                    window.location.reload();
                }
                loading(false);
            }
        });

    })
});


document.querySelectorAll('.approve-course-btn').forEach(element => {
    element.addEventListener('click', (event) => {
        event.preventDefault();
        if (loading()) return;
        const url = element.getAttribute('data-url')
        console.log(url)
        const action = element.getAttribute('data-action')
        const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value
        let course_id = Number(element.getAttribute('data-id'))
        loading(true);
        $.ajax({
            url: url,
            dataType: "json",
            headers: { "X-CSRFToken": csrfToken },
            type: "Post",
            async: true,
            data: { 'course_id': course_id, 'action': action },
            success: function (res) {
                console.log(res)
                popUp("Course Marked as Approved")
                loading(false);
                window.location.reload()
            },
            error: function (err) {
                console.log(err)
                if (err.status == 200){
                    popUp("Course Marked as Approved")
                    window.location.reload();
                }
                loading(false);
            }
        });

    })
});
