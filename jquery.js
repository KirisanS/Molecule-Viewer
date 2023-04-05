/* javascript to accompany jquery.html */

var id;
var currentNo;
var currentCode;
var currentName;
var colour1;
var colour2;
var colour3;
var radius;
var currentData;
let currentMoleculeName

function sleep(ms)
{
  return new Promise(resolve => setTimeOut(resolve, ms));
}

$(document).ready( 
  /* this defines a function that gets called after the document is in memory */
  
  function()
  {
    if(window.location.pathname == '/') {
      $.ajax(
        {
          type: "GET",
          url: "/currentElements",
          success: function()
          {
            $.getJSON("/currentElements", function(data) {
              let length = data.length;
              for(let i = 0; i < length; i++)
              {
                row = "<TR id=\"something\"><TD>" +  data[i][0] + "</TD>" +
                    "<TD>" + data[i][1]  + "</TD>" +
                    "<TD id=\"elementId\">" + data[i][2]  + "</TD>" +
                    "<TD>" + data[i][3] + "</TD>" +
                    "<TD>" + data[i][4] + "</TD>" +
                    "<TD>" + data[i][5] + "</TD>" +
                    "<TD>" + data[i][6] + "</TD>/TR>"

                $("#elementTable").append(row)
              }
            })
          }
        }
      )
    }

    else if (window.location.pathname == '/moleculePage') {
      $.ajax(
        {
          type: "GET",
          url: "/currentMolecules",
          success: function() 
          {
            $.getJSON("/currentMolecules", function(data) {
              let length = data.length;
              for(let i = 0; i < length; i++)
              {
                var item = "<div class=\"item\"> <p class=\"moleculeText\"> Molecule: " + data[i][0] + "<br><br>Atoms: " + data[i][1]
                + "<br>Bonds: " + data[i][2] + "</p><button id=\"" +data[i][0] + "\" class=\"view\">View</button> </div>"

                $("#moleculeWrapper").append(item)
              }
            })
          }
        } 
      );
    }
    ///moleculePage
    let pos = 'L';

    $("#homePage").click(
      function()
      {
        window.location = 'http://localhost:56029/'
      }
    )

    $("#elementPage").click(
      async function()
      {
        window.location = 'http://localhost:56029/elementPage'
      }
    )

    

    $("#moleculePage").click(
      function()
      {
        $.get("/moleculePage",
        {

        },
        function()
        {
          window.location.replace( "http://localhost:56029/moleculePage")
          //myFunction()
        },
        );
      }
    )


    $("#sdfPage").click(
      function()
      {
        $.get("/sdfPage",
        {

        },
        function()
        {
          window.location.replace("http://localhost:56029/sdfPage")
        }

        );
      }
    )



    $("#sdfSubmit").click(
      function()
      {
        //document.getElementById('elementNo').valu e,
        var fileName = $('input[type=file]').val().replace(/.*(\/|\\)/, '')
        var ending = fileName.split(".")



        if (ending[1] == "sdf") {
          $("#p2").text("File name: " + fileName)

        } else {
          $("#p2").text("Invalid type of file. Please upload a valid sdf file!")
        }
      }
    )

    //$("#elementTable").on('click', '#something',
    $("#moleculeWrapper").on('click', '.view',
    function(e)
    {
      //e.preventDefault();
      currentMoleculeName = this.id
      $.post("/sendId",
      {
        molName: this.id,
        success: function()
        {
          $.ajax(
            {
              type: "GET",
              url: "/viewMolecule",
              success: function()
              {
                $.getJSON("/viewMolecule", function(data)
                {
                  $("#svgT").remove()
                  $("#rotateButton").remove()
                  $("#moleculeViewBox").append(data)

                  button1 = "<button id=\"rotateButton\" class=\"rotationButton\">Rotate!</button>"

                  $("#moleculeViewBox").append(button1)
                })
              }
            }
          );
        }
      })
    }
    );
    /* Everything Under This Comment is for Elements */
    $("#moleculeViewBox").on('click', '#rotateButton',
      function()
      {
        $("#prompt").removeClass('visible')
      }
    )

    $("#addElement").click(
      function()
      {
        $("#d1").removeClass("visible")
        $("#elementTable").addClass("visible")
      } );

    $("#removeElement").click(
      function()
      {
        var length = $("#elementTable TR").length;
        document.getElementById("elementTable").deleteRow(length-1);

        $.post("/removeElement",
        {
           elementNo: currentNo,
           elementCode: currentCode,
           elementName: currentName,
           colour1: colour1,
           colour2: colour2,
           colour3: colour3,
           radius: radius,
           extra_info: "This is for removing an element"
        },
        );

      }
    );



    $("#elementTable").on('click', '#something',
      function()
      { 
        id = $(this).index();
        currentNo = $(this).find("td:eq(0)").html();
        currentCode = $(this).find("td:eq(1)").html();
        currentName = $(this).find("td:eq(2)").html();
        colour1 = $(this).find("td:eq(3)").html();
        colour2 = $(this).find("td:eq(4)").html();
        colour3 = $(this).find("td:eq(5)").html();
        radius =  $(this).find("td:eq(6)").html();

        $("#buttonDiv1").addClass("visible");
        $("#yes").removeClass("visible");
        $("#no").removeClass("visible"); 

        $("#p1").text("Would you like to remove element \n'" + currentName + "'?")

      }
    );

    $("#no").click(
      function()
      {
        $("#buttonDiv1").removeClass("visible");
        $("#yes").addClass("visible");
        $("#no").addClass("visible");

        $("#p1").text("Please click on which row you'd like to delete")
      } 
    )

    $("#yes").click(
      function()
      {
        document.getElementById("elementTable").deleteRow(id);
        $("#buttonDiv1").removeClass("visible");
        $("#yes").addClass("visible");
        $("#no").addClass("visible");
        
        $("#p1").text("Removed '" + currentName + "'")

        $.post("/removeElement",
        {
           elementNo: currentNo,
           elementCode: currentCode,
           elementName: currentName,
           colour1: colour1,
           colour2: colour2,
           colour3: colour3,
           radius: radius,
           extra_info: "This is for removing an element"
        },
        );
        

      }
    )

    $("#formUpload").submit(
      function(event)
      {
        event.preventDefault();
        $("#p2").text("Loading SDF File")
        var fd = new FormData(this)
        $.ajax(
        {
          type: 'POST',
          url: "/uploadSDF",
          processData: false,
          contentType: false,
          data: fd,
          error: function()
          {
            $.ajax(
              {
                type: 'GET',
                url: "/validateSDF",
                success: function()
                {
                  $.getJSON("/validateSDF", function(data) {
                    if(data == 1) 
                    {
                      $("#p2").text("Invalid SDF Detected!")
                    } else if (data == 2) {
                      $("#p2").text("That Molecule name has already been added!")
                    } else {
                      $("#p2").text("Molecule Added!")
                    }
                  })
                }
              }
            )
          }
        }

        );
      }
    )

    $("#rotationId").click(
      function(e) 
      {
        e.preventDefault()
        check = 0
        xR = document.getElementById('xR').value
        xY = document.getElementById('yR').value
        xZ = document.getElementById('yR').value
        if(xY.length === 0) {
          check = 1
        }
        if(xR.length === 0) {
          check = 1
        }
        if(xZ.length === 0) {
          check = 1
        }
        if(xR >= 0 && xY >= 0 && xZ >= 0 && check == 0)  {
          $.post("/rotation",
          {
            xR: document.getElementById('xR').value,
            xY: document.getElementById('yR').value,
            xZ: document.getElementById('yR').value,
            molName: currentMoleculeName,
            extra_info: "Rotation Values",
            success: function()
            {
              $.ajax(
                {
                  type: "GET",
                  url: "/loadCurrentSVG",
                  success: function()
                    {
                      $.getJSON("/loadCurrentSVG", function(data)
                       {
                        $("#prompt").addClass("visible")
                        $("#svgT").remove()
                        $("#rotateButton").remove()
                        $("#moleculeViewBox").append(data)
                        button1 = "<button id=\"rotateButton\" class=\"rotationButton\">Rotate!</button>"
                        $("#moleculeViewBox").append(button1)

                      })
                    }
                  }
                )
              }
            }
            
          )
        } else {
          $("#pheaderId2").text("You must enter a value for each rotation")
        }
        
        
      }
    )

    $("#i1").click(

      function()
      {

        /*var elementNo=  document.getElementById('elementNo').value
        var elementCode = document.getElementById('elementCode').value
        var elementName = document.getElementById('elementName').value
        var colour1 = document.getElementById('colour1').value
        var colour2 = document.getElementById('colour2').value
        var colour3 = document.getElementById('colour3').value
        var radius = document.getElementById('radius').value
        var check = 0
        errorString = ""
        if(elementNo > 118 || elementNo < 1 || typeof(elementNo) === null) 
        {
          errorString+= "Invalid ElementNo\n"
          $("#f1")[0].reset();
          check = 1;
        } else if (elementCode.length > 2 || typeof(elementCode) === null) {
          errorString+= "Invalid Element Code"
          check = 1;
        }*/

        $.post("/load",
        {
          elementNo: document.getElementById('elementNo').value,
          elementCode: document.getElementById('elementCode').value,
          elementName: document.getElementById('elementName').value,
          colour1: document.getElementById('colour1').value,
          colour2: document.getElementById('colour2').value,
          colour3: document.getElementById('colour3').value,
          radius:  document.getElementById('radius').value,
          extra_info: "hehehehaw",
          success: function()
          {
            $.ajax(
              {
                type: "GET",
                url:"/validateElement",
                success: function()
                {
                  $.getJSON("/validateElement", function(data) {
                    if(data == 1) {
                      $("#pheaderId").text("Invalid Input, Try Again")
                    } else if (data == 2) {
                      $("#pheaderId").text("That Element Exists Already!")
                    }
                    else {
                      $("#p1").text("Successfully Added Element")
                      var x = document.getElementById("elementTable").rows.length;
                      var table = document.getElementById("elementTable");
            
                      row = "<TR id=\"something\"><TD>" +  document.getElementById('elementNo').value + "</TD>" +
                               "<TD>" + document.getElementById('elementCode').value  + "</TD>" +
                               "<TD id=\"elementId\">" + document.getElementById('elementName').value  + "</TD>" +
                               "<TD>" + document.getElementById('colour1').value  + "</TD>" +
                               "<TD>" + document.getElementById('colour2').value  + "</TD>" +
                               "<TD>" + document.getElementById('colour3').value  + "</TD>" +
                               "<TD>" + document.getElementById('radius').value  + "</TD></TR>"
                       $("#elementTable").append(row)
                       $("#pheaderId").text("Enter Element: ")
                       $("#d1").addClass("visible")
                       $("#elementTable").removeClass("visible")

                    }

                  })
                }
              }
            )
          }
        }
        );
      }
    );


  } );

