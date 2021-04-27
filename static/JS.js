var test =['85_hires.png', '70_hires.png', '53_hires.png', '86_hires.png', '7_hires.png', '2_hires.png']
let i = 0;

function updateBtn() {
  console.log(i)
  var a = test[i]
  imgbtn.src = "/static/pokemon/" + a + ";
  var i = i + 1;
  if (i == 8){
    i=0;}
}