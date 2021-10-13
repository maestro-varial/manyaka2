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

