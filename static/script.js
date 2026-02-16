// Smart Airport Pool - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rideForm');
    const responseDiv = document.getElementById('response');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);

        // Show loading
        const submitBtn = form.querySelector('.btn-primary');
        const originalText = submitBtn.textContent;
        submitBtn.innerHTML = '<span class="loading"></span> Processing...';
        submitBtn.disabled = true;

        try {
            // Geocode locations to coordinates
            console.log('Geocoding locations...');
            const pickupCoords = await getCoordinates(formData.get('pickupLocation'));
            const dropCoords = await getCoordinates(formData.get('dropLocation'));

            const data = {
                passenger_id: 1, // Default for demo
                pickup_lat: pickupCoords.lat,
                pickup_lng: pickupCoords.lng,
                drop_lat: dropCoords.lat,
                drop_lng: dropCoords.lng,
                detour_tolerance_percent: parseFloat(formData.get('detourTolerance'))
            };

            console.log('Sending ride request:', data);

            const response = await fetch('/ride/request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const responseText = await response.text();
            let result;
            try {
                result = JSON.parse(responseText);
            } catch (e) {
                throw new Error('Server error: ' + (responseText || response.statusText));
            }

            if (response.ok) {
                showResponse('Ride request submitted successfully! ' + result.message, 'success');
                form.reset();
            } else {
                let errorMsg = 'Something went wrong';
                if (result.detail) {
                    if (Array.isArray(result.detail)) {
                        errorMsg = result.detail.map(d => d.msg || d.message || (d.loc ? `${d.loc.join('.')}: ${d.type}` : 'Unknown error')).join(', ');
                    } else {
                        errorMsg = result.detail;
                    }
                }
                showResponse('Error: ' + errorMsg, 'error');
            }
        } catch (error) {
            showResponse('Network error: ' + error.message, 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });

    async function getCoordinates(address) {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`);
        const data = await response.json();
        
        if (data && data.length > 0) {
            return { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) };
        }
        throw new Error(`Location not found: ${address}`);
    }

    function showResponse(message, type) {
        responseDiv.textContent = message;
        responseDiv.className = 'response ' + type;
        responseDiv.style.display = 'block';

        // Auto-hide after 5 seconds
        setTimeout(() => {
            responseDiv.style.display = 'none';
        }, 5000);
    }

    // Add click handlers for feature cards
    const features = document.querySelectorAll('.feature');
    features.forEach(feature => {
        feature.style.cursor = 'pointer';
        feature.addEventListener('click', function() {
            const title = this.querySelector('h3').textContent;
            navigateToFeaturePage(title);
        });
    });

    function navigateToFeaturePage(title) {
        let url = '';
        switch(title) {
            case 'Smart Matching':
                url = '/smart-matching';
                break;
            case 'Real-time Updates':
                url = '/real-time-updates';
                break;
            case 'Safe & Reliable':
                url = '/safe-reliable';
                break;
        }
        if (url) {
            window.location.href = url;
        }
    }

    // Smooth scrolling for any anchor links (if added later)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add hover effects to form inputs
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });

        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
});