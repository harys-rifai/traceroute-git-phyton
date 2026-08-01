(function () {
    var container = document.getElementById('dnsResolutionContainer');
    if (!container) return;

    var steps = container.querySelectorAll('.dns-step');
    var connectors = container.querySelectorAll('.dns-connector');
    var resultEl = document.getElementById('dnsResult');
    var restartBtn = document.getElementById('dnsRestartBtn');

    var resolutionData = [
        { label: 'Your Browser', icon: '\u{1F4BB}', detail: '192.168.1.100', location: 'New York, US', color: '#4DFF00' },
        { label: 'DNS Resolver', icon: '\u{1F310}', detail: '8.8.8.8', location: 'Google DNS, US', color: '#76B900' },
        { label: 'Root Server', icon: '\u{1F310}', detail: 'a.root-servers.net', location: 'Anycast, Global', color: '#FFA500' },
        { label: 'TLD Server', icon: '\u{1F310}', detail: 'a.gtld-servers.net', location: 'Verisign, US', color: '#FFA500' },
        { label: 'Authoritative', icon: '\u{1F310}', detail: 'ns1.example.com', location: 'Cloudflare, US', color: '#00BFFF' },
    ];

    var currentStep = -1;
    var intervalId = null;
    var packetElements = [];

    function reset() {
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
        }

        packetElements.forEach(function (pkt) {
            if (pkt.element && pkt.element.parentNode) {
                pkt.element.parentNode.removeChild(pkt.element);
            }
        });
        packetElements = [];

        currentStep = -1;

        for (var i = 0; i < steps.length; i++) {
            steps[i].classList.remove('active', 'completed');
        }

        for (var j = 0; j < connectors.length; j++) {
            connectors[j].classList.remove('active');
        }

        if (resultEl) {
            resultEl.textContent = 'Press Start to begin DNS resolution';
            resultEl.style.borderColor = 'rgba(118, 185, 0, 0.3)';
            resultEl.style.color = '#9ca3af';
        }
    }

    function createPacket(fromIdx, toIdx) {
        var fromStep = steps[fromIdx];
        var toStep = steps[toIdx];
        if (!fromStep || !toStep) return;

        var fromNode = fromStep.querySelector('.dns-node');
        var toNode = toStep.querySelector('.dns-node');
        if (!fromNode || !toNode) return;

        var fromRect = fromNode.getBoundingClientRect();
        var toRect = toNode.getBoundingClientRect();
        var containerRect = container.getBoundingClientRect();

        var x1 = fromRect.left + fromRect.width / 2 - containerRect.left;
        var y1 = fromRect.top + fromRect.height / 2 - containerRect.top;
        var x2 = toRect.left + toRect.width / 2 - containerRect.left;
        var y2 = toRect.top + toRect.height / 2 - containerRect.top;

        var svg = container.querySelector('svg');
        if (!svg) {
            svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '100%');
            svg.setAttribute('height', '100%');
            svg.style.position = 'absolute';
            svg.style.top = '0';
            svg.style.left = '0';
            svg.style.pointerEvents = 'none';
            container.style.position = 'relative';
            container.appendChild(svg);
        }

        var pkt = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        pkt.setAttribute('r', '6');
        pkt.setAttribute('fill', '#4DFF00');
        pkt.setAttribute('opacity', '1');
        svg.appendChild(pkt);

        var glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        glow.setAttribute('r', '12');
        glow.setAttribute('fill', 'rgba(77, 255, 0, 0.2)');
        svg.appendChild(glow);

        packetElements.push({
            element: pkt,
            glow: glow,
            fromX: x1,
            fromY: y1,
            toX: x2,
            toY: y2,
            progress: 0,
            speed: 0.03,
        });
    }

    function updatePackets() {
        packetElements = packetElements.filter(function (pkt) {
            pkt.progress += pkt.speed;
            if (pkt.progress >= 1) {
                if (pkt.element && pkt.element.parentNode) {
                    pkt.element.parentNode.removeChild(pkt.element);
                }
                if (pkt.glow && pkt.glow.parentNode) {
                    pkt.glow.parentNode.removeChild(pkt.glow);
                }
                return false;
            }

            var x = pkt.fromX + (pkt.toX - pkt.fromX) * pkt.progress;
            var y = pkt.fromY + (pkt.toY - pkt.fromY) * pkt.progress;

            pkt.element.setAttribute('cx', x);
            pkt.element.setAttribute('cy', y);
            pkt.glow.setAttribute('cx', x);
            pkt.glow.setAttribute('cy', y);

            if (pkt.progress > 0.7) {
                var fade = 1 - (pkt.progress - 0.7) / 0.3;
                pkt.element.setAttribute('opacity', fade);
                pkt.glow.setAttribute('opacity', fade * 0.5);
            } else {
                pkt.element.setAttribute('opacity', '1');
                pkt.glow.setAttribute('opacity', '0.5');
            }

            return true;
        });
    }

    function activateStep(index) {
        if (index < 0 || index >= steps.length) return;

        currentStep = index;

        for (var i = 0; i < steps.length; i++) {
            if (i < index) {
                steps[i].classList.remove('active');
                steps[i].classList.add('completed');
            } else if (i === index) {
                steps[i].classList.add('active');
                steps[i].classList.remove('completed');
            } else {
                steps[i].classList.remove('active', 'completed');
            }
        }

        for (var j = 0; j < connectors.length; j++) {
            if (j < index) {
                connectors[j].classList.add('active');
            } else {
                connectors[j].classList.remove('active');
            }
        }

        if (resultEl) {
            var step = resolutionData[index];
            resultEl.innerHTML = '<span style="color:#76B900">Step ' + (index + 1) + ':</span> Querying <code>' + step.detail + '</code> <span style="color:#9ca3af">(' + step.location + ')</span>';
        }
    }

    function startResolution() {
        reset();

        var stepIndex = 0;
        activateStep(stepIndex);

        intervalId = setInterval(function () {
            stepIndex++;
            if (stepIndex >= steps.length) {
                clearInterval(intervalId);
                intervalId = null;
                if (resultEl) {
                    resultEl.innerHTML = '<span style="color:#4DFF00">&#10003; Resolution complete</span> &rarr; IP: <code>93.184.216.34</code> (TTL: 300s)';
                    resultEl.style.borderColor = 'rgba(77, 255, 0, 0.5)';
                    resultEl.style.color = '#4DFF00';
                }
                for (var i = 0; i < steps.length; i++) {
                    steps[i].classList.add('completed');
                    steps[i].classList.remove('active');
                }
                for (var j = 0; j < connectors.length; j++) {
                    connectors[j].classList.add('active');
                }
                return;
            }
            activateStep(stepIndex);
        }, 1500);
    }

    function animateLoop() {
        updatePackets();
        requestAnimationFrame(animateLoop);
    }

    if (restartBtn) {
        restartBtn.addEventListener('click', startResolution);
    }

    animateLoop();
    reset();
})();