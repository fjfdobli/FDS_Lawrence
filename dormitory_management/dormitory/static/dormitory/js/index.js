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
    tabPanes.forEach(pane => pane.classList.remove('active'));

    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => button.classList.remove('active'));

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
            // Update student count in UI
            const studentCountElement = document.querySelector('.stat-card.students h3');
            if (studentCountElement) {
                const currentCount = parseInt(studentCountElement.textContent);
                studentCountElement.textContent = currentCount + 1;
            }
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
    let studentId = document.getElementById('studentSelect').value;
    let buildingId = document.getElementById('buildingSelect').value;
    let roomId = document.getElementById('roomSelect').value;
    let assignmentDate = document.getElementById('assignmentDate').value;
    let paymentStatus = document.getElementById('paymentStatus').value;

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
            studentId: studentId,
            buildingId: buildingId,
            roomId: roomId,
            assignmentDate,
            paymentStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('assignRoomForm').reset();
            closeModal('assignRoomModal');
            
            // Update building count in UI if new building was created
            const buildingsCountElement = document.querySelector('.stat-card.buildings h3');
            if (buildingsCountElement) {
                // We'll just reload to ensure accuracy
                window.location.reload();
            } else {
                alert('Room assigned successfully!');
                window.location.reload();
            }
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
    
    // Clear existing options
    roomSelect.innerHTML = '<option value="">Choose a room</option>';
    
    // Return early if no building selected
    if (!buildingId || !buildingId.startsWith('B')) {
        return;
    }

    // Extract numeric part (e.g., 'B001' -> '001')
    const buildingNumericId = buildingId.substring(1);

    fetch(`/api/rooms/available/?building_id=${encodeURIComponent(buildingNumericId)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.rooms && data.rooms.length > 0) {
                data.rooms.forEach(room => {
                    roomSelect.innerHTML += `
                        <option value="R${room.room_id}">${room.room_number} - ${room.room_type} Room (Available)</option>
                    `;
                });
            } else {
                insertFallbackRooms(buildingId, roomSelect);
            }
        })
        .catch(error => {
            console.error('Error fetching rooms:', error);
            insertFallbackRooms(buildingId, roomSelect);
        });
});

function insertFallbackRooms(buildingId, roomSelect) {
    const fallbackOptions = {
        'B001': [
            { id: 'R1', label: '101 - Single Room (Available)' },
            { id: 'R2', label: '102 - Double Room (Available)' }
        ],
        'B002': [
            { id: 'R3', label: '201 - Single Room (Available)' },
            { id: 'R4', label: '202 - Double Room (Available)' }
        ],
        'B003': [
            { id: 'R5', label: '301 - Single Room (Available)' },
            { id: 'R6', label: '302 - Double Room (Available)' }
        ]
    };

    const rooms = fallbackOptions[buildingId] || [];
    rooms.forEach(room => {
        roomSelect.innerHTML += `<option value="${room.id}">${room.label}</option>`;
    });
}


function addFallbackRooms(buildingId, roomSelect) {
    const rooms = {
        B001: [
            { id: 'R1', label: '101 - Single Room (Available)' },
            { id: 'R2', label: '102 - Double Room (Available)' }
        ],
        B002: [
            { id: 'R3', label: '201 - Single Room (Available)' },
            { id: 'R4', label: '202 - Double Room (Available)' }
        ],
        B003: [
            { id: 'R5', label: '301 - Single Room (Available)' },
            { id: 'R6', label: '302 - Double Room (Available)' }
        ]
    };

    if (rooms[buildingId]) {
        rooms[buildingId].forEach(room => {
            roomSelect.innerHTML += `<option value="${room.id}">${room.label}</option>`;
        });
    }
}

function editStudent(studentId) {
    fetch(`/api/students/${studentId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('editStudentId').value = data.student.student_id;
                document.getElementById('editFirstName').value = data.student.f_name;
                document.getElementById('editLastName').value = data.student.l_name;
                document.getElementById('editMiddleName').value = data.student.m_name || '';
                document.getElementById('editGender').value = data.student.gender;
                document.getElementById('editEmail').value = data.student.email;
                document.getElementById('editContactNumber').value = data.student.contact_number;
                document.getElementById('editBirthdate').value = data.student.birthdate;
                
                openModal('editStudentModal');
            } else {
                alert('Error fetching student data: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching student data.');
        });
}

function updateStudent() {
    const studentId = document.getElementById('editStudentId').value;
    const firstName = document.getElementById('editFirstName').value;
    const lastName = document.getElementById('editLastName').value;
    const middleName = document.getElementById('editMiddleName').value;
    const gender = document.getElementById('editGender').value;
    const email = document.getElementById('editEmail').value;
    const contactNumber = document.getElementById('editContactNumber').value;
    const birthdate = document.getElementById('editBirthdate').value;

    if (!firstName || !lastName || !gender || !email || !contactNumber || !birthdate) {
        alert('Please fill all required fields.');
        return;
    }

    fetch(`/api/students/${studentId}/update/`, {
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
            closeModal('editStudentModal');
            alert('Student updated successfully!');
            window.location.reload();
        } else {
            alert('Error updating student: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the student.');
    });
}

function deleteStudent(studentId) {
    if (confirm('Are you sure you want to delete this student? This action cannot be undone.')) {
        fetch(`/api/students/${studentId}/delete/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update student count in UI
                const studentCountElement = document.querySelector('.stat-card.students h3');
                if (studentCountElement) {
                    const currentCount = parseInt(studentCountElement.textContent);
                    if (currentCount > 0) {
                        studentCountElement.textContent = currentCount - 1;
                    }
                }
                
                // Room may have been set to Available, so refresh the page
                alert('Student deleted successfully!');
                window.location.reload();
            } else {
                alert('Error deleting student: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the student.');
        });
    }
}

function viewStudent(studentId) {
    fetch(`/api/students/${studentId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const student = data.student;
                let detailsHTML = `
                    <h4>Student Details</h4>
                    <p><strong>ID:</strong> ${studentId}</p>
                    <p><strong>Name:</strong> ${student.f_name} ${student.m_name ? student.m_name + ' ' : ''}${student.l_name}</p>
                    <p><strong>Gender:</strong> ${student.gender}</p>
                    <p><strong>Email:</strong> ${student.email}</p>
                    <p><strong>Contact:</strong> ${student.contact_number}</p>
                    <p><strong>Birthdate:</strong> ${student.birthdate}</p>
                `;
                document.getElementById('viewDetailsContent').innerHTML = detailsHTML;
                openModal('viewDetailsModal');
            } else {
                alert('Error fetching student data: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching student data.');
        });
}

function viewRoom(roomId) {
    fetch(`/api/rooms/${roomId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const room = data.room;
                let detailsHTML = `
                    <h4>Room Details</h4>
                    <p><strong>ID:</strong> ${roomId}</p>
                    <p><strong>Building:</strong> ${room.building_name}</p>
                    <p><strong>Room Number:</strong> ${room.room_number}</p>
                    <p><strong>Floor:</strong> ${room.floor}</p>
                    <p><strong>Type:</strong> ${room.room_type}</p>
                    <p><strong>Capacity:</strong> ${room.room_capacity}</p>
                    <p><strong>Status:</strong> ${room.room_status}</p>
                    <p><strong>Items:</strong> ${room.room_item || 'None'}</p>
                `;
                document.getElementById('viewDetailsContent').innerHTML = detailsHTML;
                openModal('viewDetailsModal');
            } else {
                alert('Error fetching room data: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching room data.');
        });
}

function editRoom(roomId) {
    fetch(`/api/rooms/${roomId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const room = data.room;
                document.getElementById('editRoomId').value = room.room_id;
                document.getElementById('editRoomNumber').value = room.room_number;
                document.getElementById('editRoomFloor').value = room.floor;
                document.getElementById('editRoomType').value = room.room_type;
                document.getElementById('editRoomCapacity').value = room.room_capacity;
                document.getElementById('editRoomStatus').value = room.room_status;
                document.getElementById('editRoomItems').value = room.room_item || '';
                
                openModal('editRoomModal');
            } else {
                alert('Error fetching room data: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching room data.');
        });
}

function updateRoom() {
    const roomId = document.getElementById('editRoomId').value;
    const roomNumber = document.getElementById('editRoomNumber').value;
    const floor = document.getElementById('editRoomFloor').value;
    const roomType = document.getElementById('editRoomType').value;
    const roomCapacity = document.getElementById('editRoomCapacity').value;
    const roomStatus = document.getElementById('editRoomStatus').value;
    const roomItems = document.getElementById('editRoomItems').value;

    if (!roomNumber || !floor || !roomType || !roomCapacity || !roomStatus) {
        alert('Please fill all required fields.');
        return;
    }

    fetch(`/api/rooms/${roomId}/update/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            roomNumber,
            floor,
            roomType,
            roomCapacity,
            roomStatus,
            roomItems
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeModal('editRoomModal');
            alert('Room updated successfully!');
            window.location.reload();
        } else {
            alert('Error updating room: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the room.');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dormitory Management System initialized');
});
