const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8108/ws/chat/test_student');

ws.on('open', () => {
  console.log('✓ WebSocket connection established!');
  
  // Send a test message
  const testMessage = {
    content: 'What is a variable?',
    student_id: 'test_student'
  };
  
  ws.send(JSON.stringify(testMessage));
  console.log('✓ Test message sent');
});

ws.on('message', (data) => {
  console.log('✓ Received message:', data.toString());
  ws.close();
});

ws.on('error', (error) => {
  console.log('✗ WebSocket error:', error.message);
});

ws.on('close', () => {
  console.log('✓ WebSocket connection closed');
});

// Timeout after 5 seconds
setTimeout(() => {
  if (ws.readyState === WebSocket.CONNECTING) {
    console.log('✗ Connection timeout');
    ws.close();
  }
}, 5000);
