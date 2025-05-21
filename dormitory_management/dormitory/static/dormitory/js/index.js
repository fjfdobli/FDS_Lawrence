function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function openTab(tabId) {
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => {
        pane.classList.remove('active');
    });
    
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });
    
    document.getElementById(tabId).classList.add('active');
    
    const activeButton = document.querySelector(`button[onclick="openTab('${tabId}')"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
    document.body.style.overflow = 'hidden'; 
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.body.style.overflow = 'auto'; 
}

window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}

function saveStudent() {
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const middleName = document.getElementById('middleName').value;
    const gender = document.getElementById('gender').value;
    const email = document.getElementById('email').value;
    const contactNumber = document.getElementById('contactNumber').value;
    const birthdate = document.getElementById('birthdate').value;
    
    if (!firstName || !lastName || !gender || !email || !contactNumber || !birthdate) {
        alert('Please fill all required fields.');
        return;
    }
    
    fetch('/api/students/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            firstName,
            lastName,
            middleName,
            gender,
            email,
            contactNumber,
            birthdate
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('addStudentForm').reset();
            closeModal('addStudentModal');
            
            alert('Student added successfully!');
            
            window.location.reload();
        } else {
            alert('Error adding student: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the student.');
    });
}

function assignRoom() {
    const studentId = document.getElementById('studentSelect').value;
    const buildingId = document.getElementById('buildingSelect').value;
    const roomId = document.getElementById('roomSelect').value;
    const assignmentDate = document.getElementById('assignmentDate').value;
    const paymentStatus = document.getElementById('paymentStatus').value;
    
    if (!studentId || !buildingId || !roomId || !assignmentDate || !paymentStatus) {
        alert('Please fill all required fields.');
        return;
    }
    
    fetch('/api/rooms/assign/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            studentId,
            buildingId,
            roomId,
            assignmentDate,
            paymentStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('assignRoomForm').reset();
            closeModal('assignRoomModal');
            
            alert('Room assigned successfully!');
            
            window.location.reload();
        } else {
            alert('Error assigning room: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while assigning the room.');
    });
}

document.getElementById('buildingSelect').addEventListener('change', function() {
    const buildingId = this.value;
    const roomSelect = document.getElementById('roomSelect');
    
    roomSelect.innerHTML = '<option value="">Choose a room</option>';
    
    if (!buildingId) return;
    
    fetch(`/api/rooms/available/?building_id=${buildingId.replace('B', '')}`)
    .then(response => response.json())
    .then(data => {
        if (data.rooms && data.rooms.length > 0) {
            data.rooms.forEach(room => {
                roomSelect.innerHTML += `
                    <option value="R${room.room_id}">${room.room_number} - ${room.room_type} Room (Available)</option>
                `;
            });
        } else {
            if (buildingId === 'B001') {
                roomSelect.innerHTML += `
                    <option value="R002">102 - Single Room (Available)</option>
                    <option value="R004">104 - Double Room (Available)</option>
                `;
            } else if (buildingId === 'B002') {
                roomSelect.innerHTML += `
                    <option value="R007">201 - Single Room (Available)</option>
                    <option value="R009">203 - Double Room (Available)</option>
                `;
            } else if (buildingId === 'B003') {
                roomSelect.innerHTML += `
                    <option value="R012">301 - Single Room (Available)</option>
                    <option value="R014">303 - Double Room (Available)</option>
                `;
            }
        }
    })
    .catch(error => {
        console.error('Error fetching rooms:', error);
        
        if (buildingId === 'B001') {
            roomSelect.innerHTML += `
                <option value="R002">102 - Single Room (Available)</option>
                <option value="R004">104 - Double Room (Available)</option>
            `;
        } else if (buildingId === 'B002') {
            roomSelect.innerHTML += `
                <option value="R007">201 - Single Room (Available)</option>
                <option value="R009">203 - Double Room (Available)</option>
            `;
        } else if (buildingId === 'B003') {
            roomSelect.innerHTML += `
                <option value="R012">301 - Single Room (Available)</option>
                <option value="R014">303 - Double Room (Available)</option>
            `;
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dormitory Management System initialized');
});