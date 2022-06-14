 const iTitle = document.querySelector('.aboutTitle')

 function myMove(){
   let id = null;
    var elem = document.querySelector(".aboutTitle")
    elem.style.left = "500px"
    var pos = 0;
    clearInterval(id)
    id = setInterval(frame,2)
    function frame(){
    if(pos ==500){
        clearInterval(id)
    }else{
    pos++
    elem.style.bottom = pos + 'px';
    }
    }
 }

 myMove();

 iTitle.addEventListener('click', () => {
       document.querySelector("#s1").style.display = 'block'
        document.querySelector("#s2").style.display = 'block'

          document.querySelector("#s3").style.display = 'block'
           document.querySelector("#s4").style.display = 'block'
            document.querySelector("#s5").style.display = 'block'


    })

