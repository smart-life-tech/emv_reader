const checkInterval = 5000; // Interval to check connectivity in milliseconds
const testUrl = 'https://www.google.com/'; // URL to test connectivity
let isChecking = false; // Flag to manage ongoing fetch requests
let timeoutHandle = null; // Handle for the timeout
let checkAttempts = 0; // Counter for the number of checks
const maxAttempts = 10; // Maximum number of attempts

// Function to perform a fetch request to test connectivity
function checkInternetConnectivity() {
    if (isChecking) return; // Exit if a check is already in progress
    isChecking = true;

    // Clear any previous timeout to ensure it's reset
    if (timeoutHandle) {
        clearTimeout(timeoutHandle);
    }

    // Create a new timeout for the 2-second delay
    timeoutHandle = setTimeout(() => {
        // Update status to offline if fetch is not completed in 2 seconds
        updateNetworkStatus(false);
        isChecking = false;
    }, 2000);

    // Perform the fetch request
    fetch(testUrl, { method: 'HEAD', mode: 'no-cors' })
        .then(response => {
            // If fetch completes within 2 seconds, clear timeout and update status to online
            clearTimeout(timeoutHandle);
            checkAttempts++;
            if (checkAttempts >= maxAttempts) {
                updateNetworkStatus(true);
            } else {
                setTimeout(checkInternetConnectivity, 1000); // Continue checking
            }
        })
        .catch(error => {
            // If fetch fails, clear timeout and update status to offline
            clearTimeout(timeoutHandle);
            updateNetworkStatus(false);
        })
        .finally(() => {
            isChecking = false; // Reset the flag once the fetch completes
        });
}

// Function to update the status on the webpage
function updateNetworkStatus(isOnline) {
    const statusElement = document.getElementById('status');
    if (isOnline) {
        statusElement.innerText = 'Online';
        statusElement.style.color = 'lightgreen';
        document.getElementById('loadingScreen').classList.add('hidden');
        document.getElementById('mainContent').classList.remove('hidden');
        document.getElementById('offlineMessage').classList.add('hidden');
    } else {
        statusElement.innerText = 'Offline';
        statusElement.style.color = 'lightcoral';
        document.getElementById('loadingScreen').classList.add('hidden');
        document.getElementById('offlineMessage').classList.remove('hidden');
        document.getElementById('mainContent').classList.add('hidden');
    }
}

// Function to check network status
function checkNetworkStatus() {
    checkAttempts = 0; // Reset the attempts counter
    checkInternetConnectivity();
}

// Listen for online/offline events
window.addEventListener('online', checkNetworkStatus);
window.addEventListener('offline', () => updateNetworkStatus(false));

// Periodically check network status
setInterval(checkNetworkStatus, checkInterval);

// Initial check on page load
window.onload = checkNetworkStatus;
