    function updateFileName() {
        var input = document.getElementById('file-upload');
        var fileName = input.files.length > 0 ? input.files[0].name : 'No file chosen';
        document.getElementById('file-name').textContent = fileName;
    }