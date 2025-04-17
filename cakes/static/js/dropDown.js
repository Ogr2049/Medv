function toggleDropdownMenu() {
    var dropdown = document.getElementById("dropdownMenu");
    if (dropdown.style.display === "none") {
        dropdown.style.display = "flex"
        dropdown.style.flexDirection = "column"
        dropdown.style.alignItems = "flex-start"
        dropdown.style.justifyContent="center"
        dropdown.style.gap = "10px"
        dropdown.style.zIndex ="1"
    } else {
        dropdown.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var dropdown = document.querySelector('.navigationWrapperProfile');
    var dropdownContent = document.querySelector('.dropdownContent');

    dropdown.addEventListener('click', function (event) {
        toggleDropdownMenu();
        event.stopPropagation(); 
    });
    document.addEventListener('click', function(event) {
        var isClickInside = dropdown.contains(event.target);

        if (!isClickInside) {
            dropdownContent.style.display = '';
        }
    });

    dropdownContent.addEventListener('click', function(event) {
        event.stopPropagation();
    });
});
