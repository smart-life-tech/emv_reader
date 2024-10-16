const checkInterval = 5000; // Interval to check connectivity in milliseconds
const testUrl = 'https://www.google.com/'; // URL to test connectivity
let isChecking = false; // Flag to manage ongoing fetch requests
let timeoutHandle = null; // Handle for the timeout
let checkAttempts = 0; // Counter for the number of checks
const maxAttempts = 4; // Maximum number of attempts

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
        handleOffline();
        isChecking = false;
    }, 1000);

    // Perform the fetch request
    fetch(testUrl, { method: 'HEAD', mode: 'no-cors' })
        .then(response => {
            // If fetch completes within 2 seconds, clear timeout and update status to online
            clearTimeout(timeoutHandle);
            checkAttempts = 0; // Reset attempts on successful fetch
            fetchBatteryData(); // Fetch battery data on successful connectivity check
        })
        .catch(error => {
            // If fetch fails, clear timeout and handle offline status
            clearTimeout(timeoutHandle);
            checkAttempts++;
            if (checkAttempts >= maxAttempts) {
                callOfflineEndpoint();
            }
        })
        .finally(() => {
            isChecking = false; // Reset the flag once the fetch completes
        });
}

// Function to handle offline status
function handleOffline() {
    console.log('Offline');
    //const statusElement = document.getElementById('status');
    //statusElement.innerText = 'Offline';
    //statusElement.style.color = 'red';
}

// Function to call the offline endpoint
function callOfflineEndpoint() {
    handleOffline();
    window.location.href = 'http://localhost:5000/offline';
    fetch('http://localhost:5000/offline')
        .then(response => console.log('Offline endpoint called'))
        .catch(error => console.error('Error calling offline endpoint', error));
}

// Function to check network status
function checkNetworkStatus() {
    checkInternetConnectivity();
    fetchBatteryData(); // Fetch battery data on successful connectivity check
}

// Periodically check network status
setInterval(checkNetworkStatus, checkInterval);

// Initial check on page load
window.onload = checkNetworkStatus;

// Function to update battery status
function updateBatteryStatus(batteryLevel, chargingStatus) {
    const statusElement = document.getElementById('status');
    // Get the current time
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const currentTime = `${hours}:${minutes}`;
    statusElement.innerText = `Battery ${batteryLevel}%   Status ${chargingStatus} Time: ${currentTime}`;
    statusElement.style.position = 'absolute';
    statusElement.style.top = '20px';
    statusElement.style.right = '20px';
    statusElement.style.fontSize = '30px';
    statusElement.style.fontWeight = 'bold';
    statusElement.style.color = 'black';
    statusElement.style.whiteSpace = 'nowrap'; // This ensures the text stays on a single line

}

// Function to fetch battery data from the Flask server
function fetchBatteryData() {
    fetch('http://localhost:5000/battery')
        .then(response => response.json())
        .then(data => {
            updateBatteryStatus(data.Battery, data.Status);
            console.log(data.Battery, data.Status);
        })
        .catch(error => console.error('Error fetching battery status', error));
}