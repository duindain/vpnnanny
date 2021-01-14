$(document).ready( function () {
  $.prototype.once = function() {
    var ret = this.not(function() {
        return this.once;
    });
    this.each(function(id, el) {
        el.once = true;
    });
    return ret;
  };
  $(".filter_button").click(function()
  {
    var filter = $(this).attr("data-filter");
    dTable.search(dTable.search() == filter ? "" : filter).draw();
  });
  dTable = $("#vpnTable").DataTable({
    "ajax": "/vpns",
    "deferRender": true,
    scrollY: "50vh",
    scrollCollapse: true,
    "lengthMenu": [
      [50, 250, 1000, -1],
      [50, 250, 1000, "All"]
    ],
    "columnDefs": [
    {
      "visible": false,
      "searchable": false,
      "targets": [0,2]
    },
    {"render": function ( data, type, row )
      {
        if(data <= -3)
          return "disabled";
        if(data <= 0)
        {
          var chances = parseInt(data) + 3;
          return chances + " more chance"+(chances > 1 ? "s" : "");
        }
        return data;
      },
      "targets": 3
    }],
  });

  dTable.on( 'draw', function ()
  {
    if ( typeof addTableClickEvents == 'function' )
    {
      addTableClickEvents();
    }
    calculateCounts();
  });
});

function calculateCounts()
{
  var queued = dTable.column(3).data().filter(function(value,index)
  {
      return value === "Queued" ? true : false;
  });
  updateOrHideBadge("Queued", queued.length);
  var encoding = dTable.column(3).data().filter(function(value,index)
  {
      return value === "Encoding" ? true : false;
  });
  updateOrHideBadge("Encoding", encoding.length);
  var evaluating = dTable.column(3).data().filter(function(value,index)
  {
      return value === "Evaluating" ? true : false;
  });

  $(".badges").show();
}

function updateOrHideBadge(filter, value)
{
  var badgeElement = $(".filter_button").filter("button[data-filter='"+filter+"']")
  if(badgeElement.length > 0)
  {
    if(value > 0)
    {
      badgeElement.children(":first").text(value);
      badgeElement.show();
    }
    else
    {
      badgeElement.hide();
    }
  }
}
