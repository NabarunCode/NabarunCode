/* =========================================
   TYPING EFFECT
========================================= */

const typed = document.getElementById("typed");

const commands = [
    "whoami",
    "python learn_ai.py",
    "docker ps",
    "building_the_future.sh"
];

let commandIndex = 0;
let charIndex = 0;


function typeCommand() {

    const command = commands[commandIndex];

    if (charIndex < command.length) {

        typed.textContent += command.charAt(charIndex);

        charIndex++;

        setTimeout(typeCommand, 70);

    } else {

        setTimeout(() => {

            typed.textContent = "";

            charIndex = 0;

            commandIndex =
                (commandIndex + 1) % commands.length;

            typeCommand();

        }, 1800);

    }

}


typeCommand();



/* =========================================
   PARTICLES
========================================= */

const particleContainer =
    document.getElementById("particles");


for (let i = 0; i < 45; i++) {

    const particle =
        document.createElement("div");

    particle.classList.add("particle");

    particle.style.left =
        Math.random() * 100 + "%";

    particle.style.top =
        Math.random() * 100 + "%";

    particle.style.animationDelay =
        Math.random() * 8 + "s";

    particle.style.animationDuration =
        5 + Math.random() * 8 + "s";

    particleContainer.appendChild(particle);

}



/* =========================================
   SCROLL REVEAL
========================================= */

const revealElements =
    document.querySelectorAll(
        ".timeline-item, .learning-card, .writing-card, .pipeline-node"
    );


const observer =
    new IntersectionObserver(

        entries => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.style.opacity = "1";

                    entry.target.style.transform =
                        "translateY(0)";

                }

            });

        },

        {
            threshold: 0.15
        }

    );


revealElements.forEach(element => {

    element.style.opacity = "0";

    element.style.transform =
        "translateY(25px)";

    element.style.transition =
        "opacity .7s ease, transform .7s ease";

    observer.observe(element);

});



/* =========================================
   MOUSE PARALLAX
========================================= */

document.addEventListener("mousemove", event => {

    const x =
        (event.clientX / window.innerWidth - .5);

    const y =
        (event.clientY / window.innerHeight - .5);


    const terminal =
        document.querySelector(".terminal");


    if (terminal) {

        terminal.style.transform =
            `rotate(3deg)
             translate(${x * 15}px, ${y * 15}px)`;

    }

});
