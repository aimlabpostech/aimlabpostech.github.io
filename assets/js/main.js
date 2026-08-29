/* AIM Lab — shared behaviour: mobile nav, publication filters */
(function () {
  "use strict";

  /* ---- Mobile navigation ---- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---- Publication / project filters ---- */
  var filterBars = document.querySelectorAll("[data-filter-bar]");
  Array.prototype.forEach.call(filterBars, function (bar) {
    var targetSel = bar.getAttribute("data-filter-bar");
    var buttons = bar.querySelectorAll("button[data-filter]");

    function apply(value) {
      var items = document.querySelectorAll(targetSel + " [data-tags]");
      Array.prototype.forEach.call(items, function (el) {
        var tags = (el.getAttribute("data-tags") || "").split(/\s+/);
        el.hidden = value !== "all" && tags.indexOf(value) === -1;
      });
      // Hide year headings whose items are all hidden
      var groups = document.querySelectorAll(targetSel + " [data-group]");
      Array.prototype.forEach.call(groups, function (g) {
        var visible = g.querySelectorAll("[data-tags]:not([hidden])").length;
        g.hidden = visible === 0;
      });
      var counter = document.querySelector(targetSel + "-count");
      if (counter) {
        var n = document.querySelectorAll(targetSel + " [data-tags]:not([hidden])").length;
        counter.textContent = n;
      }
    }

    Array.prototype.forEach.call(buttons, function (btn) {
      btn.addEventListener("click", function () {
        Array.prototype.forEach.call(buttons, function (b) {
          b.setAttribute("aria-pressed", b === btn ? "true" : "false");
        });
        apply(btn.getAttribute("data-filter"));
      });
    });
  });

  /* ---- Current year in footer ---- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
