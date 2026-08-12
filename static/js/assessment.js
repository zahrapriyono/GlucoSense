console.log("assessment.js loaded");

let currentStep = 1;
const totalSteps = 3;

function showStep(step) {
    document.querySelectorAll('.step').forEach(el => el.classList.add('hidden'));
    document.getElementById(`step${step}`).classList.remove('hidden');

    const percent = (step / totalSteps) * 100;
    document.getElementById('progressFill').style.width = `${percent}%`;
    document.getElementById('stepPercent').textContent = `${Math.round(percent)}% Complete`;

    const labels = ['Personal Details', 'Medical History', 'Lifestyle'];
    document.getElementById('stepLabel').textContent = `Step ${step} of ${totalSteps}: ${labels[step - 1]}`;
}

function nextStep() {
    if (currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

async function submitAssessment(event) {
    console.log("submitAssessment() called");

    const btn = event.target;
    const originalText = btn.textContent;

    // Loading state
    btn.textContent = '⏳ Processing...';
    btn.disabled = true;

    try {
        const token = localStorage.getItem('token');

        if(!token) {
            throw new Error('Authentication token not found.')
        }
        const formData = collectFormData();

        console.log("Assessment form data:", formData);

        console.log("Sending assessment request...");
        
        const response = await fetch('/api/assessment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        console.log('Assessment status:', response.status);
        console.log('Assessment result:', result);

        if (!response.ok) {
            throw new Error(result.message || `Server responded ${response.status}`);
        }

        sessionStorage.setItem('assessmentResult', JSON.stringify(result));
        window.location.href = '/assessment/result/';

    } catch (err) {
        console.error('Assessment error:', err);
        // Reset button jika error
        btn.textContent = originalText;
        btn.disabled = false;
        alert(err.message || 'Something went wrong. Please try again.');
    }
}

function collectFormData() {
    return {
        // Step 1 - Personal Detail
        full_name: document.getElementById('full_name').value,
        age: document.getElementById('age').value,
        sex: document.querySelector('[name=sex]').value,
        weight: document.getElementById('weight').value,
        height: document.getElementById('height').value,
        activity_level: document.querySelector('.choice-card.selected[data-group="activity_level"]')?.dataset.value,

        // Step 2 - Medical History
        high_cholesterol: document.querySelector('input[name=high_cholesterol]:checked')?.value,
        cholesterol_check_5yr: document.querySelector('input[name=cholesterol_check_5yr]:checked')?.value,
        stroke: document.querySelector('input[name=stroke]:checked')?.value,
        heart_disease: document.querySelector('input[name=heart_disease]:checked')?.value,
        difficulty_walking: document.querySelector('input[name=difficulty_walking]:checked')?.value,

        // Step 3 - Lifestyle & Wellbeing
        bp_systolic: document.getElementById('bp_systolic').value,
        bp_diastolic: document.getElementById('bp_diastolic').value,
        smoking_status: document.getElementById('smoking_status').value,
        eat_fruits: document.querySelector('input[name=eat_fruits]:checked')?.value,
        eat_vegetables: document.querySelector('input[name=eat_vegetables]:checked')?.value,
        heavy_alcohol: document.querySelector('input[name=heavy_alcohol]:checked')?.value,
        general_health: document.querySelector('.choice-card.selected[data-group="general_health"]')?.dataset.value,
        poor_mental_health_days: document.getElementById('poor_mental_health_days').value,
        poor_physical_health_days: document.getElementById('poor_physical_health_days').value,
        health_insurance: document.querySelector('input[name=health_insurance]:checked')?.value,
        skipped_doctor_cost: document.querySelector('input[name=skipped_doctor_cost]:checked')?.value,
        education_level: document.getElementById('education_level').value,
        income_level: document.getElementById('income_level').value,
    };
}

// Handle choice card selection (activity level, general health)
function selectChoice(el) {
    const group = el.dataset.group;
    document.querySelectorAll(`.choice-card[data-group="${group}"]`)
        .forEach(card => card.classList.remove('selected'));
    el.classList.add('selected');
}