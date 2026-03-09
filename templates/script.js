function gradeQuiz(){

let correct = 0

let q1 = document.querySelector('input[name="q1"]:checked')

if(q1.value === "a"){
correct++
}

let score = correct * 100

if(score >= 80){

document.getElementById("result").innerHTML =
"✅ Passed! Lesson complete."

}

else{

document.getElementById("result").innerHTML =
"❌ Try again."

}

}
