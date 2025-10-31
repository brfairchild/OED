const http = require('http');

// mock server URL
const url = 'http://localhost:8000';

// TESTING 2 hour window
const startTime = new Date('2025-01-01T08:00:00Z'); // found the easiest time to start on sample data
const endTime = new Date(startTime.getTime() + 2 * 60 * 60 * 1000); // +2 hours

http.get(url, (res) => {
    let data = '';

    res.on('data', chunk => {
        data += chunk;
    });

    res.on('end', () => {
        try {
            const jsonData = JSON.parse(data);

            // Filter 2 hours worth of data
            const filtered = jsonData.filter(item => {
                const itemTime = new Date(item.timestamp);
                return itemTime >= startTime && itemTime < endTime;
            });

            console.log('Filtered Data:', filtered);

        } catch (err) {
            console.error('Error parsing data:', err);
        }
    });

}).on('error', err => {
    console.error('Error fetching mock data:', err);
});
