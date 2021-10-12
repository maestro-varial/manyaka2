document.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', (event) => {
        event.preventDefault()
        const name = event.target.getAttribute('data-name');
        let container = event.target.parentElement
        let curriculam_form = container.querySelectorAll(".multiField")
        let addButton = event.target
        let totalForms = document.querySelector(`#id_${name}-TOTAL_FORMS`)
        let formNum = curriculam_form.length-1
        
        addForm()
        function addForm(){
            let newForm = curriculam_form[0].cloneNode(true)
            let formRegex = RegExp(`${name}-(\\d){1}-`,'g')
            
            formNum++
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
            container.insertBefore(newForm, addButton)
            
            totalForms.setAttribute('value', `${formNum+1}`)
        }
    })
});
