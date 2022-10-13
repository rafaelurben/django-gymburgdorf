// Masonry Layout

function masonry_resizeItem(item) {
    //console.log("Masonry: resize item ", item);

    grid = document.getElementsByClassName("panel-container")[0];
    rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
    rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));
    rowSpan = Math.ceil((item.getBoundingClientRect().height + rowGap) / (rowHeight + rowGap));
    item.style.gridRowEnd = "span " + rowSpan;
}

function masonry_resizeAllItems() {
    // console.log("Masonry: resize all");

    allitems = document.getElementsByClassName("panel");
    for (x = 0; x < allitems.length; x++) {
        masonry_resizeItem(allitems[x]);
    }
}

function masonry_resizeInstance(instance) {
    //console.log("Masonry: resize instance ", instance);

    item = instance.elements[0];
    masonry_resizeItem(item);
}

function masonry_imagesLoaded() {
    allitems = document.getElementsByClassName("panel");
    for (x = 0; x < allitems.length; x++) {
        imagesLoaded(allitems[x], masonry_resizeInstance);
    }
}

window.addEventListener("resize", masonry_resizeAllItems);

// onoffline/ononline Panels

function handleNetworkChange(event = null) {
    if (navigator.onLine) {
        document.body.classList.remove("offline");
        masonry_resizeAllItems();
    } else {
        document.body.classList.add("offline");
        masonry_resizeAllItems();
    }
}


window.addEventListener("online", handleNetworkChange);
window.addEventListener("offline", handleNetworkChange);

// Onload

window.addEventListener("load", function() {
    handleNetworkChange();
    masonry_resizeAllItems();
})