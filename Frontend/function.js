const form = document.getElementById('churnForm');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const data = {
    Gender_encoded: parseInt(document.getElementById('gender').value),
    Subscription_Type_encoded: parseInt(document.getElementById('subscription').value),
    Contract_Length_encoded: parseInt(document.getElementById('contract').value),
    Payment_Delay: parseInt(document.getElementById('delay').value)
  };

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });

    const result = await response.json();

    resultDiv.style.display = 'block';
    
    // The backend returns { "churn_prediction": 1 } for churn, 0 for no churn
    if(result.churn_prediction === 1) {
      resultDiv.className = 'result yes';
      resultDiv.textContent = 'Customer is likely to churn';
    } else if (result.churn_prediction === 0) {
      resultDiv.className = 'result no';
      resultDiv.textContent = 'Customer is not likely to churn';
    } else if (result.error) {
      resultDiv.className = 'result yes';
      resultDiv.textContent = 'Error: ' + result.error;
    } else {
      resultDiv.className = 'result yes';
      resultDiv.textContent = 'Unexpected response from server';
    }

  } catch (err) {
    resultDiv.style.display = 'block';
    resultDiv.className = 'result yes';
    resultDiv.textContent = 'Error: Could not get prediction';
    console.error(err);
  }
});