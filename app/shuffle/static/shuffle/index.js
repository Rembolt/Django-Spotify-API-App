

window.addEventListener('DOMContentLoaded', ()=> {

    let authenticated = true;

    intro();
    queueScroll();
    descriptions();
})


function intro (){

    const intro = document.querySelector('.intro');
    const logo = document.querySelector('#logo-shuffle');
    const logoSpan = document.querySelectorAll('.logo');

    setTimeout(()=>{

        logoSpan.forEach((span, i)=>{
            setTimeout(()=>{
                span.classList.add('active');
            }, (i + 1) * 400)
        });
        
        setTimeout(()=>{
            logoSpan.forEach((span,i)=>{
                if(i !=0){ setTimeout(()=>{
                        span.classList.remove('active');
                        span.classList.add('fade');
                    }, (i + 1) * 50)}
            });
        },2000)

        setTimeout(()=>{
            intro.style.top = '-100vh';
        // logo.classList.add('to-bottom');
        }, 3000)

        setTimeout(()=>{
            intro.remove();
        // logo.classList.add('to-bottom');
        }, 5000)
    })
}

function queueScroll (){
    
    const queueWrapper = document.querySelector('.queue-wrapper');

    let pressedX = false;
    let startX = 0;

    queueWrapper.addEventListener('mousedown', (e)=> {
        pressedX = true;
        startX = e.clientX;
        queueWrapper.style.cursor = 'grabbing';
    })
    queueWrapper.addEventListener('mouseleave', function (e) {
        pressedX = false;
    })
    window.addEventListener('mouseup', (e)=> {
        pressedX = false;
        queueWrapper.style.cursor = 'grab';
    })
    queueWrapper.addEventListener('mousemove', function (e) {
        if(!pressedX) {
        return;
        }
    
        this.scrollLeft += (startX - e.clientX);
    })
}

function descriptions(){

    const buttons = document.querySelectorAll('.description');

    for (var i = 0; i < buttons.length; i++) {
        let button = buttons[i];
        let description = document.querySelector(`#${button.id}-description`);
        console.log(description.innerHTML)
        button.addEventListener('click', () =>{
            if(description.style.display != "none"){
                description.style.display = "none";
                button.classList.remove('clicked');
            }else{
                description.style.display = "block";
                button.classList.add('clicked');
                typeWriter(description, description.textContent);
            }
        }); 
    }
}

function typeWriter(element, text, i = 0){
    if(i === 0){
        element.textContent='';
    }else if(i === text.length-1){
        return;
    }
    element.textContent += text[i]
    setTimeout(()=> typeWriter(element,text, i+1), 20);
}    

    

    
    

    // const songsWrapper = document.querySelector('.songs-list');
    // let pressedY = false;
    // let startY = 0;
     // songsWrapper.addEventListener('mousedown', (e)=> {
    //     pressedY = true;
    //     startY = e.clientY;
    //     songsWrapper.style.cursor = 'grabbing';
    // })
    // songsWrapper.addEventListener('mousemove', function (e) {
    //     if(!pressedY) {
    //       return;
    //     }
      
    //     this.scrollUp += (startY - e.clientY);
    // })
    // songsWrapper.addEventListener('mouseleave', function (e) {
    //     pressedY = false;
    // })



    
