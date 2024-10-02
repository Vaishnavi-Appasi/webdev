var output=document.getElementById("display");
function display(input){
    output.value+=input;
}
function cal(){
    output.value=eval(output.value);
}
function cle(){
    output.value="";
    }