const http = require('http');

// Default values if no arguments are provided


// HOW TO MAKE CALLS WITH EXAMPLES FROM MOCK:

// node ball.js [FQR] [AttributeID] [StartTime] [EndTime]
// Default : ball.js
// Different Meter and Attribute: node ball.js "NAE-01/Building-Power" 123
// Completely Custom Time Window: node ball.js "Metasys15_NAE-47" 85 "2025-02-15T12:00:00Z" "2025-02-15T14:00:00Z"

const args = process.argv.slice(2);
const CONFIG = {
    host: 'localhost',
    port: 8000,
    fqr: args[0] || 'Metasys15_NAE-47_ModbusTCP',
    attributeId: args[1] || 85,
    startTime: args[2] || '2025-01-01T08:00:00Z',
    endTime: args[3] || '2025-01-01T10:00:00Z'
};

function getObjectId(fqr, callback) {
    const encodedFqr = encodeURIComponent(fqr);
    const url = `http://${CONFIG.host}:${CONFIG.port}/api/v3/objectIdentifiers?fqr=${encodedFqr}`;

    http.get(url, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
            try {
                const result = JSON.parse(data);
                if (result.id) callback(null, result.id);
                else callback(new Error("ID not found"));
            } catch (e) { callback(e); }
        });
    }).on('error', (err) => callback(err));
}

function generateFinalUri(objectId) {
    const query = new URLSearchParams({
        startTime: CONFIG.startTime,
        endTime: CONFIG.endTime,
        pageSize: 1000,
        sort: 'timestamp'
    }).toString();

    return `http://${CONFIG.host}:${CONFIG.port}/api/v3/objects/${objectId}/attributes/${CONFIG.attributeId}/samples?${query}`;
}

// Execution 
getObjectId(CONFIG.fqr, (err, id) => {
    if (err) {
        console.error('Error:', err.message);
        return;
    }
    console.log(generateFinalUri(id));
});