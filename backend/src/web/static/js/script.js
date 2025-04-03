document.addEventListener('DOMContentLoaded', () => {
    const analyzeButton = document.getElementById('analyze');
    const clearHistoryButton = document.getElementById('clear-history');
    const downloadButton = document.getElementById('download');
    const situationInput = document.getElementById('situation');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    
    // Function to show loading state
    const showLoading = () => {
        loadingDiv.classList.remove('hidden');
        resultDiv.classList.add('hidden');
        analyzeButton.disabled = true;
        analyzeButton.classList.add('opacity-50');
    };
    
    // Function to hide loading state
    const hideLoading = () => {
        loadingDiv.classList.add('hidden');
        resultDiv.classList.remove('hidden');
        analyzeButton.disabled = false;
        analyzeButton.classList.remove('opacity-50');
    };
    
    // Function to display categories
    const displayCategories = (categories) => {
        const categoriesDiv = document.getElementById('categories');
        categoriesDiv.innerHTML = '';
        categories.forEach(category => {
            const span = document.createElement('span');
            span.className = 'px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm';
            span.textContent = category;
            categoriesDiv.appendChild(span);
        });
    };
    
    // Function to display laws
    const displayLaws = (laws) => {
        const lawsUl = document.getElementById('laws');
        lawsUl.innerHTML = '';
        laws.forEach(law => {
            const li = document.createElement('li');
            li.className = 'text-gray-600';
            li.textContent = law;
            lawsUl.appendChild(li);
        });
    };
    
    // Function to display advice
    const displayAdvice = (advice) => {
        const adviceDiv = document.getElementById('advice');
        adviceDiv.textContent = advice;
    };
    
    // Function to display references
    const displayReferences = (references) => {
        const referencesDiv = document.getElementById('references');
        referencesDiv.innerHTML = '';
        references.forEach(ref => {
            const div = document.createElement('div');
            div.className = 'p-4 bg-gray-50 rounded-lg';
            div.innerHTML = `
                <div class="font-semibold">${ref.name_of_law} (${ref.citation_title})</div>
                <div class="text-sm text-gray-600">
                    <div>BWB ID: ${ref.identification_number}</div>
                    <div>Domein: ${ref.legal_domain}</div>
                    <div>Inwerkingtreding: ${ref.date_of_entry_into_force}</div>
                    <div>Bevoegd gezag: ${ref.regulatory_authority}</div>
                </div>
            `;
            referencesDiv.appendChild(div);
        });
    };
    
    // Function to analyze the situation
    const analyzeSituation = async () => {
        const situation = situationInput.value.trim();
        if (!situation) {
            alert('Voer eerst uw juridische situatie in.');
            return;
        }
        
        showLoading();
        
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ situation }),
            });
            
            const result = await response.json();
            
            if (result.success) {
                displayCategories(result.data.categories);
                displayLaws(result.data.laws);
                displayAdvice(result.data.advice);
                displayReferences(result.data.references);
            } else {
                alert('Er is een fout opgetreden bij het analyseren van uw situatie.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Er is een fout opgetreden bij het verwerken van uw verzoek.');
        } finally {
            hideLoading();
        }
    };
    
    // Function to clear history
    const clearHistory = async () => {
        try {
            const response = await fetch('/api/clear-history', {
                method: 'POST',
            });
            
            const result = await response.json();
            
            if (result.success) {
                window.location.reload();
            } else {
                alert('Er is een fout opgetreden bij het wissen van de geschiedenis.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Er is een fout opgetreden bij het verwerken van uw verzoek.');
        }
    };
    
    // Function to download advice
    const downloadAdvice = async () => {
        const situation = situationInput.value.trim();
        if (!situation) {
            alert('Voer eerst uw juridische situatie in.');
            return;
        }
        
        try {
            const response = await fetch('/api/download-advice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ situation }),
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Create and download the file
                const blob = new Blob([result.content], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = result.filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                alert('Er is een fout opgetreden bij het downloaden van het advies.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Er is een fout opgetreden bij het verwerken van uw verzoek.');
        }
    };
    
    // Add event listeners
    analyzeButton.addEventListener('click', analyzeSituation);
    clearHistoryButton.addEventListener('click', clearHistory);
    downloadButton.addEventListener('click', downloadAdvice);
    
    // Add keyboard shortcut (Ctrl/Cmd + Enter) to analyze
    situationInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            analyzeSituation();
        }
    });
}); 