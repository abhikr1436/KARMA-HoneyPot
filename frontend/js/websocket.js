/*
 * WebSocket Real-Time Telemetry Listener for Aegis-SOC
 */

class TelemetryWebSocket {
    constructor(onEventCallback, onStatusCallback) {
        this.onEventCallback = onEventCallback;
        this.onStatusCallback = onStatusCallback;
        this.ws = null;
        this.connect();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/telemetry`;

        try {
            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => {
                console.log("[Aegis-SOC WS] Connected to live threat stream.");
                if (this.onStatusCallback) this.onStatusCallback(true);
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (this.onEventCallback) this.onEventCallback(data);
                } catch (err) {
                    console.error("[Aegis-SOC WS] Parse error:", err);
                }
            };

            this.ws.onclose = () => {
                console.warn("[Aegis-SOC WS] Disconnected. Reconnecting in 3s...");
                if (this.onStatusCallback) this.onStatusCallback(false);
                setTimeout(() => this.connect(), 3000);
            };

            this.ws.onerror = (err) => {
                console.error("[Aegis-SOC WS] Error:", err);
                this.ws.close();
            };
        } catch (e) {
            console.error("[Aegis-SOC WS] Connection exception:", e);
        }
    }
}
