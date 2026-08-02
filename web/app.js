/* Royal Stables yard board.
 *
 * Four near-identical blocks. This is the "unfamiliar technologies" exercise:
 * have Claude explain it, identify what varies between the repetitions, then extract
 * the pattern into one reusable function WITHOUT changing behaviour.
 *
 * Note there are two small inconsistencies planted between the blocks. Extracting
 * the pattern naively will silently change behaviour. Find them first.
 */

const HORSES = {
  northgate:  ["Copperfield", "Bramble", "Hazelnut", "Barleycorn"],
  willowmere: ["Silvermane", "Dobbin", "Quickthorn", "Sorrel"],
  ashcombe:   ["Marigold", "Thistledown", "Mistletoe", "Willowherb"],
  fairwater:  ["Pennywhistle", "Greyling"]
};

// --- Northgate ---------------------------------------------------------------
var northgateList = document.getElementById("list-northgate");
var northgateBtn = document.getElementById("btn-northgate");
var northgateCount = document.getElementById("count-northgate");
northgateCount.textContent = HORSES.northgate.length;
northgateBtn.addEventListener("click", function () {
  if (northgateList.children.length > 0) {
    northgateList.innerHTML = "";
    northgateBtn.textContent = "Show horses";
    return;
  }
  for (var i = 0; i < HORSES.northgate.length; i++) {
    var li = document.createElement("li");
    li.textContent = HORSES.northgate[i];
    northgateList.appendChild(li);
  }
  northgateBtn.textContent = "Hide horses";
});

// --- Willowmere --------------------------------------------------------------
var willowmereList = document.getElementById("list-willowmere");
var willowmereBtn = document.getElementById("btn-willowmere");
var willowmereCount = document.getElementById("count-willowmere");
willowmereCount.textContent = HORSES.willowmere.length;
willowmereBtn.addEventListener("click", function () {
  if (willowmereList.children.length > 0) {
    willowmereList.innerHTML = "";
    willowmereBtn.textContent = "Show horses";
    return;
  }
  for (var i = 0; i < HORSES.willowmere.length; i++) {
    var li = document.createElement("li");
    li.textContent = HORSES.willowmere[i];
    willowmereList.appendChild(li);
  }
  willowmereBtn.textContent = "Hide horses";
});

// --- Ashcombe ---------------------------------------------------------------
var ashcombeList = document.getElementById("list-ashcombe");
var ashcombeBtn = document.getElementById("btn-ashcombe");
var ashcombeCount = document.getElementById("count-ashcombe");
ashcombeCount.textContent = HORSES.ashcombe.length;
ashcombeBtn.addEventListener("click", function () {
  if (ashcombeList.children.length > 0) {
    ashcombeList.innerHTML = "";
    ashcombeBtn.textContent = "Show horses";
    return;
  }
  // Sorted here, but not in the other three blocks.
  var sorted = HORSES.ashcombe.slice().sort();
  for (var i = 0; i < sorted.length; i++) {
    var li = document.createElement("li");
    li.textContent = sorted[i];
    ashcombeList.appendChild(li);
  }
  ashcombeBtn.textContent = "Hide horses";
});

// --- Fairwater --------------------------------------------------------------
var fairwaterList = document.getElementById("list-fairwater");
var fairwaterBtn = document.getElementById("btn-fairwater");
var fairwaterCount = document.getElementById("count-fairwater");
fairwaterCount.textContent = HORSES.fairwater.length;
fairwaterBtn.addEventListener("click", function () {
  if (fairwaterList.children.length > 0) {
    fairwaterList.innerHTML = "";
    fairwaterBtn.textContent = "Show horses";
    return;
  }
  for (var i = 0; i < HORSES.fairwater.length; i++) {
    var li = document.createElement("li");
    li.textContent = HORSES.fairwater[i].toUpperCase();  // uppercase only here
    fairwaterList.appendChild(li);
  }
  fairwaterBtn.textContent = "Hide list";   // different label only here
});
