document.addEventListener('DOMContentLoaded', function() {
    const startCaptureButton = document.getElementById('startCapture');
    const packetList = document.getElementById('packetList');

    startCaptureButton.addEventListener('click', function() {
        fetch('/start_capture')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'capture started') {
                    console.log('Packet capture started');
                }
            });
    });

    function updatePacketList() {
        fetch('/get_packets')
            .then(response => response.json())
            .then(data => {
                packetList.innerHTML = '';
                data.forEach(packet => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${packet.protocol}</td>
                        <td>${packet.src_ip}</td>
                        <td>${packet.dst_ip}</td>
                        <td>${packet.src_port}</td>
                        <td>${packet.dst_port}</td>
                    `;
                    packetList.appendChild(row);
                });
            });
    }

    setInterval(updatePacketList, 1000);
});
