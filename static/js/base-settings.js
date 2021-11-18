let main_cont = document.getElementById('main-settings');

document.querySelectorAll('.setting-tabs').forEach(tab => {
    tab.addEventListener('click', (event) => {
      event.preventDefault();
      const url = tab.getAttribute('data-url')
      loading(true);

      $.ajax({
        url: url,
        dataType: "json",
        type: "Get",
        async: true,
        data: {},
        success: function(data) {
          const res_data = JSON.parse(data);
          if (res_data){
            main_cont.innerHTML = res_data
          }
          loading(false);
        },
        error: function(err) {
          if (err.responseText){
            main_cont.innerHTML = err.responseText
          }
          console.log(err)
          loading(false);
        }
      });
  
    })
  });


document.querySelectorAll('.setting-tabs-with-id').forEach(tab => {
    tab.addEventListener('click', (event) => {
      event.preventDefault();
      const url = tab.getAttribute('data-url')
      const id = tab.getAttribute('data-id')
      loading(true);

      $.ajax({
        url: `${url}?id=${id}`,
        dataType: "json",
        type: "Get",
        async: true,
        data: {},
        success: function(data) {
          const res_data = data;
          if (res_data){
            main_cont.innerHTML = res_data
          }
          loading(false);
        },
        error: function(err) {
          if (err.responseText){
            main_cont.innerHTML = err.responseText
          }
          console.log(err)
          loading(false);
        }
      });
  
    })
  });



function vendorFormSubmit(){
  const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value
  const vendorForm = $('#vendor-form')
  const url = vendorForm[0].getAttribute('data-url')
  loading(true);

  $.ajax({
    url: `${url}`,
    dataType: "json",
    headers: {"X-CSRFToken": csrfToken},
    type: "Post",
    data: vendorForm.serialize(),
    processData: false,
    success: function(res) {
      console.log(res)
      if (res.status == 202) {
        window.location.reload()
      }
      loading(false);
    },
    error: function(res) {
      console.log(res)
      if (res.status == 202) {
        window.location.reload()
      }
      loading(false);
    }
  });
}