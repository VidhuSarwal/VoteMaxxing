const encryptedObject = "EncryptedVote123"; // Example encrypted object data

// Construct the data object
const data = new FormData();
data.append('encrypted_object', encryptedObject);

// Make a POST request to the /recieveVotes route
fetch('http://your-server-address/recieveVotes', {
  method: 'POST',
  body: data
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Vote received and added to the blockchain:', data);
})
.catch(error => {
  console.error('There was a problem with your fetch operation:', error);
});
