let selectedParticles = [];
function selectParticle(particle) {
  const particleFields = document.getElementById("particle-fields");
  const particleNumber = selectedParticles.length + 1;

  if (
    (particle === "Particle 1" && !selectedParticles.includes("Particle 1")) ||
    (particle === "Particle 2" && !selectedParticles.includes("Particle 2")) ||
    (particle === "Particle 3" && !selectedParticles.includes("Particle 3"))
  ) {
    const particleField = document.createElement("div");
    particleField.classList.add("particle-field");

    const particleHeader = document.createElement("h3");
    particleHeader.textContent = `Particle ${particleNumber}`;

    const inputSection = document.createElement("div");
    inputSection.classList.add("input-section");

    const inputALabel = document.createElement("label");
    inputALabel.setAttribute("for", `inputA-${particleNumber}`);
    inputALabel.textContent = "A:";

    const inputA = document.createElement("input");
    inputA.setAttribute("type", "text");
    inputA.setAttribute("id", `inputA-${particleNumber}`);

    const inputZLabel = document.createElement("label");
    inputZLabel.setAttribute("for", `inputZ-${particleNumber}`);
    inputZLabel.textContent = "Z:";

    const inputZ = document.createElement("input");
    inputZ.setAttribute("type", "text");
    inputZ.setAttribute("id", `inputZ-${particleNumber}`);

    inputSection.appendChild(inputALabel);
    inputSection.appendChild(inputA);
    inputSection.appendChild(inputZLabel);
    inputSection.appendChild(inputZ);

    particleField.appendChild(particleHeader);
    particleField.appendChild(inputSection);

    particleFields.appendChild(particleField);

    selectedParticles.push(particle);
  }
}


const startButton = document.querySelector(".start-button");

startButton.addEventListener("click", () => {
  if (selectedParticles.length === 3) {
    const particleValues = selectedParticles.map((particle, index) => ({
      particle: particle,
      a: document.getElementById(`inputA-${index + 1}`).value,
      z: document.getElementById(`inputZ-${index + 1}`).value
    }));

    // Perform actions when Start button is clicked
    retrieveDataAndCalculateMassExcess(particleValues);
  } else {
    alert("Please select three particles.");
  }
});


function retrieveDataAndCalculateMassExcess(particleValues) {
  fetch("https://localhost:8080/retrive_data")
    .then(response => response.json())
    .then(data => {
      const df = JSON.parse(data);
      const massExcessValues = getMassExcessValues(df, particleValues);

      const popup = document.createElement("div");
      popup.classList.add("popup");

      const closeButton = document.createElement("span");
      closeButton.classList.add("close-button");
      closeButton.textContent = "x";
      closeButton.addEventListener("click", () => {
        document.body.removeChild(overlay);
        document.body.removeChild(popup);
      });

      const content = document.createElement("div");
      content.classList.add("popup-content");
      content.innerHTML = `
        <h2>Mass Excess Values</h2>
        <ul>
          ${massExcessValues
            .map(
              ({ particle, massExcess }) =>
                `<li>${particle}: ${massExcess}</li>`
            )
            .join("")}
        </ul>
      `;

      popup.appendChild(closeButton);
      popup.appendChild(content);

      const overlay = document.createElement("div");
      overlay.classList.add("overlay");

      document.body.appendChild(overlay);
      overlay.appendChild(popup);
    })
    .catch(error => {
      console.error("An error occurred:", error);
    });
}
