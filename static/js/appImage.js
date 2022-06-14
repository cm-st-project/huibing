HEIGHT = 50;
WIDTH= 300;
currIndex = 0;

image = document.getElementById('image');
image.src = 'static/pictures/picture-114.jpeg';
imagePathList = [image.src]
forward = false;
previous= false;

divs = document.getElementsByTagName("joint");

for (div of divs) div.onmousedown = onMouseDown;

joints = {"right_shoulder":{"x":700,"y":100},
"left_shoulder":{"x":850,"y":100},
"right_waist":{"x":725,"y":250},
"left_waist":{"x":825,"y":250},
"right_elbow":{"x":670,"y":200},
"left_elbow":{"x":880,"y":200},
"right_wrist":{"x":670,"y":300},
"left_wrist":{"x":880,"y":300},
"right_knee":{"x":725,"y":350},
"left_knee":{"x":825,"y":350},
"right_ankle":{"x":725,"y":500},
"left_ankle":{"x":825,"y":500}};

right_shoulder = document.getElementById("right_shoulder");
left_shoulder = document.getElementById("left_shoulder");
right_waist = document.getElementById("right_waist");
left_waist = document.getElementById("left_waist");
right_elbow = document.getElementById("right_elbow");
left_elbow = document.getElementById("left_elbow");
right_wrist = document.getElementById("right_wrist");
left_wrist = document.getElementById("left_wrist");
right_knee = document.getElementById("right_knee");
left_knee = document.getElementById("left_knee");
right_ankle = document.getElementById("right_ankle");
left_ankle = document.getElementById("left_ankle");

document.onmousemove = onMouseMove;
document.onmouseup   = onMouseUp;
var the_moving_div = '';
var the_last_mouse_position = { x:0, y:0 };

fetchPictures();
setVisibilityPrevious();
setVisibilityNext();
initJoints();
drawJoints();

function initJoints(){
    for (joint in joints){
       d = document.getElementById(joint);
       setJoint(d, joints[joint].x, joints[joint].y )
    }
}

function setJoint(joint, x, y){
    joint.style.left = WIDTH + x + "px";
    joint.style.top  = HEIGHT + y + "px";
}

function setJointsforServer(){
    for (joint in joints){
       joints[joint].x -= WIDTH;
       joints[joint].y -=HEIGHT;
    }
}

function onMouseDown(e) {
    e.preventDefault();
    the_moving_div            = e.target.id;      // remember which joint has been selected
    the_last_mouse_position.x = e.clientX;        // remember where the mouse was when it was clicked
    the_last_mouse_position.y = e.clientY;
    e.target.style.border = "2px solid blue";     // highlight the border of the joint

}

function onMouseMove(e) {
    e.preventDefault();
    if (the_moving_div == "") return;
    var d = document.getElementById(the_moving_div);
    d.style.left = d.offsetLeft + e.clientX - the_last_mouse_position.x + "px";     // move the div by however much the mouse moved
    d.style.top  = d.offsetTop  + e.clientY - the_last_mouse_position.y + "px";
    the_last_mouse_position.x = e.clientX;                                          // remember where the mouse is now
    the_last_mouse_position.y = e.clientY;

    //Update code. I have a mistake in this part when I set the coordinates of the joint(eg, right_wrist, left_wrist, right_shoulder...)
    joints[the_moving_div].x = d.offsetLeft + e.clientX - the_last_mouse_position.x - WIDTH
    joints[the_moving_div].y = d.offsetTop + e.clientY - the_last_mouse_position.y - HEIGHT
    d = document.getElementById(the_moving_div);
    setJoint(d, joints[the_moving_div].x , joints[the_moving_div].y)
    drawJoints();
    console.log(joints[the_moving_div])
}

function onMouseUp(e) {
    e.preventDefault();
    if (the_moving_div == "") return;
    document.getElementById(the_moving_div).style.border = "none";             // hide the border again
    the_moving_div = "";
}

function drawJoints() {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth/2;
    canvas.height = window.innerHeight;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.beginPath();
    ctx.strokeStyle="#15a5ed";
    ctx.lineWidth=3;
    drawConnector(ctx,canvas,left_shoulder, right_shoulder);
    drawConnector(ctx,canvas,left_shoulder, left_waist);
    drawConnector(ctx,canvas,left_waist, left_knee);
    drawConnector(ctx,canvas,left_knee, left_ankle);
    drawConnector(ctx,canvas,left_shoulder, left_elbow);
    drawConnector(ctx,canvas,left_elbow, left_wrist);
    drawConnector(ctx,canvas,left_waist, right_waist);
    drawConnector(ctx,canvas,right_shoulder, right_waist);
    drawConnector(ctx,canvas,right_waist, right_knee);
    drawConnector(ctx,canvas,right_knee, right_ankle);
    drawConnector(ctx,canvas,right_shoulder, right_elbow);
    drawConnector(ctx,canvas,right_elbow, right_wrist);
}

function drawConnector(ctx,canvas,joint1, joint2) {
    height = 55;
    ctx.moveTo(joint1.offsetLeft - window.innerWidth/2+ joint1.clientWidth/2, joint1.offsetTop-  height + joint1.clientHeight/2);
    ctx.bezierCurveTo(joint1.offsetLeft- window.innerWidth/2, joint1.offsetTop-  height,
                      joint2.offsetLeft- window.innerWidth/2, joint2.offsetTop-  height,
                      joint2.offsetLeft - window.innerWidth/2+ joint2.clientWidth/2, joint2.offsetTop-  height + joint2.clientHeight/2);
    ctx.stroke();
}

function search(){
    url = "/search"
//    setJointsforServer();
    $.ajax({
    type: "POST",
    url: url,
    data: JSON.stringify({joints: joints}),
    contentType: "application/json; charset=utf-8",
    success: function(response){
        console.log(response)

        currIndex = 0;
        image.src = imagePathList[currIndex] // String. You have to covert the result to JSON. You can use this picturesList = JSON.parse(response);
        forward = true;
        previous = false;
        setVisibilityNext();
        setVisibilityPrevious();
    }
    });
}

function fetchPictures(){
    url = "/pictures"
    $.ajax({
        type: "GET",
        url: url,
        success: function(response){
            picturesList = JSON.parse(response);
            for (i in picturesList){
//                console.log(picturesList[i].substring(16))
                var option = document.createElement("option")
                option.value = picturesList[i];
                option.append(picturesList[i].substring(16))

                 $('select').append(option);
            }

        }
    });

}

function setImage(){
    var selectBox = document.getElementById("selectedPicture");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    console.log(selectedValue);
    image.src = selectedValue;
    previous = false;
    forward = false;
    setVisibilityPrevious();
    setVisibilityNext();
}


function setVisibilityPrevious() {
  if (previous == false) {
    $("#previous").hide();
  } else {
    $("#previous").show();
  }
}


function setVisibilityNext() {
  if (forward == false) {
    $("#next").hide();
  } else {
    $("#next").show();
  }
}

function getNextImage(){
    currIndex += 1;
    image.src = imagePathList[currIndex];
    forward = currIndex != imagePathList.length-1;
    previous = true;
    setVisibilityPrevious();
    setVisibilityNext();
}

function getpreviousImage(){
    currIndex -= 1;
    image.src = imagePathList[currIndex];
    console.log(currIndex);
    previous = currIndex != 0;
    forward = true;
    setVisibilityPrevious();
    setVisibilityNext();
}