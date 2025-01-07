// Handle image analysis
document.getElementById('imageForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);

  try {
      const response = await fetch('/analyze_image', {
          method: 'POST',
          body: formData,
      });
      const result = await response.json();
      console.log(result.annotated_image_url)

      if (response.ok) {
          document.getElementById('imageResult').innerHTML = `
              <p>${result.message}</p>
              <p>Counts:</p>
              <ul>
                  <li>dog: ${result.counts.dog}</li>
                  <li>cat: ${result.counts.cat}</li>
                  
              </ul>
              <img src="${result.annotated_image_url}" alt="Annotated Image" style="max-width: 100%;">
          `;
      } else {
          document.getElementById('imageResult').textContent = `Error: ${result.error}`;
      }
  } catch (err) {
      console.error(err);
      document.getElementById('imageResult').textContent = 'Something went wrong.';
  }
});