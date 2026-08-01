(function () {
    var canvas = document.getElementById('tracerouteCanvas');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');
    var width = 0;
    var height = 0;
    var animId = null;
    var running = true;

    var datacenters = [
        { name: 'AWS Tokyo', country: 'Japan', city: 'Tokyo', lat: 35.6762, lng: 139.6503, rtt: 1.2, asn: 'AS16509', color: '#4DFF00', x: 0, y: 0 },
        { name: 'Azure Singapore', country: 'Singapore', city: 'Singapore', lat: 1.3521, lng: 103.8198, rtt: 3.8, asn: 'AS8075', color: '#4DFF00', x: 0, y: 0 },
        { name: 'Google Frankfurt', country: 'Germany', city: 'Frankfurt', lat: 50.1109, lng: 8.6821, rtt: 5.2, asn: 'AS15169', color: '#4DFF00', x: 0, y: 0 },
        { name: 'AWS Jakarta', country: 'Indonesia', city: 'Jakarta', lat: -6.2088, lng: 106.8456, rtt: 12.4, asn: 'AS16509', color: '#FFA500', x: 0, y: 0 },
        { name: 'Azure Bali', country: 'Indonesia', city: 'Bali', lat: -8.3405, lng: 115.0920, rtt: 15.7, asn: 'AS8075', color: '#FFA500', x: 0, y: 0 },
        { name: 'Cloudflare Batam', country: 'Indonesia', city: 'Batam', lat: 1.0514, lng: 104.0300, rtt: 18.3, asn: 'AS13335', color: '#FFA500', x: 0, y: 0 },
        { name: 'Linode Newark', country: 'United States', city: 'Newark', lat: 40.7357, lng: -73.9911, rtt: 0.5, asn: 'AS63949', color: '#4DFF00', x: 0, y: 0 },
        { name: 'Google New York', country: 'United States', city: 'New York', lat: 40.7128, lng: -74.0060, rtt: 1.9, asn: 'AS15169', color: '#4DFF00', x: 0, y: 0 },
        { name: 'Google Washington', country: 'United States', city: 'Washington DC', lat: 38.9072, lng: -77.0369, rtt: 9.7, asn: 'AS15169', color: '#4DFF00', x: 0, y: 0 },
    ];

    var connections = [
        [0, 1], [0, 2], [1, 3], [1, 4], [3, 5], [2, 6], [6, 7], [7, 8], [0, 6], [1, 3], [2, 0], [6, 8], [7, 0], [8, 2]
    ];

    var packets = [];
    var packetSpeed = 0.003;
    var trailLength = 25;

    function resize() {
        var rect = canvas.parentElement.getBoundingClientRect();
        width = rect.width;
        height = Math.max(300, rect.width * 0.5);
        canvas.width = width * window.devicePixelRatio;
        canvas.height = height * window.devicePixelRatio;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        ctx.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);
        computePositions();
    }

    function computePositions() {
        var padding = 40;
        var w = width - padding * 2;
        var h = height - padding * 2;

        datacenters.forEach(function (dc) {
            var x = ((dc.lng + 180) / 360) * w + padding;
            var y = ((90 - dc.lat) / 180) * h + padding;
            dc.x = x;
            dc.y = y;
        });
    }

    function getPos(dc) {
        return { x: dc.x, y: dc.y };
    }

    function drawBackground() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.fillRect(0, 0, width, height);

        ctx.strokeStyle = 'rgba(118, 185, 0, 0.06)';
        ctx.lineWidth = 1;
        var gridSize = 40;
        for (var x = 0; x < width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        for (var y = 0; y < height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }

        ctx.strokeStyle = 'rgba(118, 185, 0, 0.08)';
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 8]);
        for (var i = 0; i < connections.length; i++) {
            var a = connections[i][0];
            var b = connections[i][1];
            var posA = getPos(datacenters[a]);
            var posB = getPos(datacenters[b]);
            ctx.beginPath();
            ctx.moveTo(posA.x, posA.y);
            ctx.lineTo(posB.x, posB.y);
            ctx.stroke();
        }
        ctx.setLineDash([]);
    }

    function drawHop(dc, index) {
        var pos = getPos(dc);
        var isDest = index === datacenters.length - 1;
        var radius = isDest ? 16 : 10;

        var gradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, radius * 3);
        if (isDest) {
            gradient.addColorStop(0, 'rgba(77, 255, 0, 0.3)');
        } else {
            gradient.addColorStop(0, 'rgba(118, 185, 0, 0.2)');
        }
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, radius * 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = dc.color;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#0B0B0B';
        ctx.font = 'bold ' + (isDest ? '10' : '8') + 'px Rajdhani, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(index + 1, pos.x, pos.y);

        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.font = '10px Rajdhani, sans-serif';
        ctx.fillText(dc.name, pos.x, pos.y + radius + 14);

        ctx.fillStyle = 'rgba(0, 191, 255, 0.8)';
        ctx.font = '8px monospace';
        ctx.fillText(dc.country, pos.x, pos.y + radius + 26);

        ctx.fillStyle = 'rgba(255, 165, 0, 0.9)';
        ctx.font = 'bold 9px Rajdhani, sans-serif';
        ctx.fillText(dc.rtt + 'ms', pos.x, pos.y - radius - 8);
    }

    function createPacket() {
        return { progress: 0, hopIndex: 0, trail: [] };
    }

    function drawPacket(packet) {
        if (packet.hopIndex >= connections.length) return;

        var conn = connections[packet.hopIndex];
        var from = getPos(datacenters[conn[0]]);
        var to = getPos(datacenters[conn[1]]);

        var t = packet.progress;
        var x = from.x + (to.x - from.x) * t;
        var y = from.y + (to.y - from.y) * t;

        packet.trail.push({ x: x, y: y, alpha: 1 });
        if (packet.trail.length > trailLength) {
            packet.trail.shift();
        }

        for (var i = 0; i < packet.trail.length; i++) {
            var p = packet.trail[i];
            var r = Math.max(0.5, 3 * p.alpha);
            ctx.fillStyle = 'rgba(77, 255, 0, ' + (p.alpha * 0.5).toFixed(3) + ')';
            ctx.beginPath();
            ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.fillStyle = '#4DFF00';
        ctx.shadowColor = '#4DFF00';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
    }

    function updatePackets() {
        if (packets.length === 0 || packets[packets.length - 1].progress > 0.2) {
            packets.push(createPacket());
        }

        for (var i = packets.length - 1; i >= 0; i--) {
            packets[i].progress += packetSpeed;

            if (packets[i].progress >= 1) {
                packets[i].progress = 0;
                packets[i].hopIndex++;
                packets[i].trail = [];

                if (packets[i].hopIndex >= connections.length) {
                    packets.splice(i, 1);
                }
            }
        }
    }

    function draw() {
        if (!running) return;

        ctx.clearRect(0, 0, width, height);
        drawBackground();

        for (var i = 0; i < datacenters.length; i++) {
            drawHop(datacenters[i], i);
        }

        for (var j = 0; j < packets.length; j++) {
            drawPacket(packets[j]);
        }

        updatePackets();
        animId = requestAnimationFrame(draw);
    }

    function start() {
        if (animId) cancelAnimationFrame(animId);
        running = true;
        draw();
    }

    function stop() {
        running = false;
        if (animId) {
            cancelAnimationFrame(animId);
            animId = null;
        }
    }

    resize();
    start();

    window.addEventListener('resize', function () {
        resize();
    });

    window.tracerouteAnimation = { start: start, stop: stop };
})();