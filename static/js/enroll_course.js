let video_frame = document.getElementById('video-frame');
let mark_form = document.getElementById('mark-course');

document.querySelectorAll('.video-change').forEach(element => {
  element.addEventListener('click', (event) => {
    event.preventDefault();
    let video_id = Number(element.getAttribute('data-id'))
    const url = element.getAttribute('data-url')
    loading(true);
    $.ajax({
      url: url,
      dataType: "json",
      type: "Get",
      async: true,
      data: { 'video_id': video_id },
      success: function(data) {
        const res_data = JSON.parse(data);
        if (res_data){
          video_frame.innerHTML = res_data
        }
        loading(false);
      },
      error: function(err) {
        console.log(err)
        loading(false);
      }
    });

  })
});

// mark_form.addEventListener('submit', (event)=>{
//   event.preventDefault();
//   const url = mark_form.getAttribute('data-url');
//   const course_id = mark_form.querySelector('.checked').value
//   const isChecked = mark_form.querySelector('.checked').checked
//   const formData = new FormData(event.target);
//   formData.append('course_id',course_id)
//   formData.append('isChecked',isChecked)

//   $.ajax({
//     url: url,
//     dataType: "json",
//     type: "Post",
//     async: true,
//     data: formData,
//     processData: false,
//     contentType: false,
//     success: function(data) {

//       loading(false);
//       window.location.reload()
//     },
//     error: function(err) {

//       loading(false);
//       window.location.reload()
//     }
//   });
// })


