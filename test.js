// function selectedMolecule1(){
//     alert('you clicked on molecule 1');
// }
$(document).ready(
    function(){
        $("molName").click(
            function(){
                alert("clicked 1");
            }
        )
        // $("#addElementButton").click(
        //     function()
        //     {
        //   /* ajax post */
        //   $.post("test",
        //     /* pass a JavaScript dictionary */
        //     {
        //       name: $("#color1").val(),	/* retreive value of name field */
        //       extra_info: "some stuff here"
        //     },
        //     function( data, status )
        //     {
        //       alert( "Data: " + data + "\nStatus: " + status );
        //     }
        //   );
        //     }
        // )
    }
)
function named(){
    moleculeName = document.getElementById("molName").value;
}
function removed(){
    removeNum = document.getElementById("removeCode").value;
    if(removeNum<1){
        alert("invalid remove number");
    }
}
function formFilled(){
    color1 = document.getElementById("color1").value;
    color2 = document.getElementById("color2").value;
    color3 = document.getElementById("color3").value;
    radius = document.getElementById("radius").value;
    elName = document.getElementById("elName").value;
    elNum = document.getElementById("elNum").value;
    elCode = document.getElementById("elCode").value;

    if(!isaColor(color1) || color1.length==0){
        alert("invalid input for color 1");
        return ;
    }
    else if(!isaColor(color2) || color2.length == 0){
        alert("invalid input for color 2");
        return ;
    }
    else if(!isaColor(color3)|| color3.length == 0){
        alert("invalid input for color 3");
        return ;
    }
    else if(elCode.length > 2 || elCode.length ==0){
        alert("invalid input for element code");
        return ;
    }
    else if(elNum>118 || elNum<0 || elNum.length ==0){
        alert("invalid input for element number");
        return ;
    }
    values = [elNum, elCode, elName, color1, color2, color3, radius]
    alert(values);
    //__set__item("Elements", values );
    
}
function isaColor(color){
    var style = new Option().style;
    style.color = color;
    return style.color == color;
}